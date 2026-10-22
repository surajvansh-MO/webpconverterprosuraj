import threading
import os
from pathlib import Path
from tkinter import filedialog

from converter import convert_image


class AppActions:

    # ==================================================
    # Common Add Files Method
    # ==================================================

    def add_files(self, files):

        if not hasattr(self, "file_statuses"):
            self.file_statuses = {}

        added = False

        for file in files:

            file = Path(file)

            if file.is_dir():

                for img in file.rglob("*"):

                    if (
                        img.is_file()
                        and img.suffix.lower() in self.supported_extensions
                        and img not in self.selected_files
                    ):
                        self.selected_files.append(img)
                        self.file_statuses[img] = "Waiting"
                        added = True

            elif file.is_file() and file not in self.selected_files:
                ext = file.suffix.lower()
                can_add = ext in self.supported_extensions
                if not can_add:
                    # Allow user to convert any custom/specialist image format if decodable
                    try:
                        from converter import load_image
                        test_img = load_image(file)
                        test_img.close()
                        can_add = True
                    except Exception:
                        can_add = False

                if can_add:
                    self.selected_files.append(file)
                    self.file_statuses[file] = "Waiting"
                    added = True

        if added:

            self.file_list.populate(self.selected_files, self.file_statuses, self.output_folder)

            self.file_list.set_status(
                f"{len(self.selected_files)} file(s) selected"
            )

            self.sidebar.convert_btn.configure(
                state="normal"
            )

    # ==================================================
    # Drag & Drop Event Handler
    # ==================================================

    def on_drop_files(self, event):
        if not event or not hasattr(event, "data") or not event.data:
            return

        try:
            files = self.tk.splitlist(event.data)
        except Exception:
            files = [event.data]

        if files:
            self.add_files(files)

    # ==================================================
    # Browse Images
    # ==================================================

    def browse_images(self):

        all_patterns = " ".join(f"*{ext}" for ext in sorted(self.supported_extensions))

        filetypes = [
            (
                "All Supported Formats",
                all_patterns
            ),
            (
                "Vector Graphics (*.svg, *.svgz, *.eps, *.pdf, *.ai)",
                "*.svg *.svgz *.eps *.ps *.pdf *.ai"
            ),
            (
                "Standard Web & Photo (*.png, *.jpg, *.jpeg, *.webp, *.gif, *.bmp, *.ico)",
                "*.png *.apng *.jpg *.jpeg *.jpe *.jfif *.webp *.gif *.bmp *.dib *.ico *.cur"
            ),
            (
                "High-Efficiency & Mobile (*.heic, *.heif, *.avif)",
                "*.heic *.heif *.hif *.heics *.heifs *.avif *.avis"
            ),
            (
                "Camera RAW Photos (*.raw, *.cr2, *.cr3, *.nef, *.arw, *.dng, ...)",
                "*.raw *.cr2 *.cr3 *.nef *.nrw *.arw *.srf *.sr2 *.dng *.orf *.rw2 *.pef *.raf *.x3f *.3fr *.mrw *.srw"
            ),
            (
                "Adobe & Design (*.psd, *.psb, *.tiff, *.tga, *.dds)",
                "*.psd *.psb *.tiff *.tif *.tga *.dds *.hdr"
            ),
            (
                "All Files (*.*)",
                "*.*"
            )
        ]

        files = filedialog.askopenfilenames(
            title="Select Images to Convert to WebP",
            filetypes=filetypes
        )

        if not files:
            return

        self.add_files(files)

    # ==================================================
    # Browse Folder
    # ==================================================

    def browse_folder(self):

        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if not folder:
            return

        self.add_files([folder])

    # ==================================================
    # Choose Output Folder
    # ==================================================

    def choose_output_folder(self):

        folder = filedialog.askdirectory(
            title="Select Output Folder"
        )

        if not folder:
            return

        self.output_folder = folder

        self.sidebar.set_output_folder(folder)

        self.file_list.update_output_paths(folder)

        self.file_list.set_status(
            "Output folder selected"
        )

    # ==================================================
    # Open Output Folder
    # ==================================================

    def open_output_folder(self):

        folder = None
        if self.output_folder:
            folder = Path(self.output_folder)
        elif self.selected_files:
            folder = Path(self.selected_files[0]).parent

        if folder:
            if not folder.exists():
                folder.mkdir(parents=True, exist_ok=True)
            os.startfile(folder)
        else:
            self.file_list.set_status("No output directory available")

    # ==================================================
    # Compression Settings Change Event
    # ==================================================

    def on_compression_settings_changed(self, immediate=False):
        if not self.selected_files:
            return

        auto_compress = (
            hasattr(self.sidebar, "auto_compress_switch")
            and self.sidebar.auto_compress_switch.get() == 1
        )

        quality = int(self.sidebar.quality_slider.get())
        lossless = bool(hasattr(self.sidebar, "lossless_switch") and self.sidebar.lossless_switch.get() == 1)
        q_desc = "Lossless" if lossless else f"{quality}% Quality"

        for idx, f in enumerate(self.selected_files):
            st = self.file_statuses.get(f, "")
            if "Processing" not in st:
                self.file_statuses[f] = "Ready"
                self.file_list.update_row(idx, "Ready")

        self.sidebar.convert_btn.configure(state="normal")

        if not auto_compress:
            self.file_list.set_status(f"Settings updated to {q_desc} • Click 'Start Conversion'")
            return

        if hasattr(self, "_auto_compress_job") and self._auto_compress_job:
            try:
                self.after_cancel(self._auto_compress_job)
            except Exception:
                pass

        delay = 0 if immediate else 450
        self._auto_compress_job = self.after(delay, self.start_conversion)

    # ==================================================
    # Convert Single File
    # ==================================================

    def convert_single_file(self, index):
        if not (0 <= index < len(self.selected_files)):
            return

        file_path = Path(self.selected_files[index])
        quality = int(self.sidebar.quality_slider.get())
        lossless = bool(hasattr(self.sidebar, "lossless_switch") and self.sidebar.lossless_switch.get() == 1)

        self.file_list.update_row(index, "Processing...")
        self.file_statuses[file_path] = "Processing..."

        def do_convert():
            orig_size = file_path.stat().st_size if file_path.exists() else 0

            result, message = convert_image(
                file_path,
                output_folder=self.output_folder,
                quality=quality,
                lossless=lossless
            )

            if result:
                out_path = Path(message)
                new_size = out_path.stat().st_size if out_path.exists() else 0
                if orig_size > 0 and new_size > 0 and new_size < orig_size:
                    reduction = (1 - new_size / orig_size) * 100
                    status_text = f"Compressed ✅ (-{int(reduction)}%)"
                else:
                    status_text = "Compressed ✅" if file_path.suffix.lower() == ".webp" else "Converted ✅"
            else:
                status_text = "Failed ❌"

            self.file_statuses[file_path] = status_text

            def update_ui():
                self.file_list.update_row(index, status_text)
                self.sidebar.open_output_btn.configure(state="normal")
                self.file_list.set_status(f"{file_path.name}: {status_text}")

            self.after(0, update_ui)

        threading.Thread(target=do_convert, daemon=True).start()

    # ==================================================
    # Start Conversion
    # ==================================================

    def start_conversion(self):

        if not self.selected_files:
            return

        self.sidebar.convert_btn.configure(
            state="disabled"
        )

        self.file_list.set_progress(0)

        thread = threading.Thread(
            target=self.convert_images,
            daemon=True
        )

        thread.start()

    # ==================================================
    # Convert Images
    # ==================================================

    def convert_images(self):

        total = len(self.selected_files)
        success = 0

        quality = int(self.sidebar.quality_slider.get())
        lossless = bool(hasattr(self.sidebar, "lossless_switch") and self.sidebar.lossless_switch.get() == 1)

        for index, file in enumerate(self.selected_files):

            file_path = Path(file)

            self.file_statuses[file_path] = "Processing..."
            curr_idx = index
            self.after(0, lambda idx=curr_idx: self.file_list.update_row(idx, "Processing..."))

            orig_size = file_path.stat().st_size if file_path.exists() else 0

            result, message = convert_image(
                file_path,
                output_folder=self.output_folder,
                quality=quality,
                lossless=lossless
            )

            if result:
                success += 1
                out_path = Path(message)
                new_size = out_path.stat().st_size if out_path.exists() else 0
                if orig_size > 0 and new_size > 0 and new_size < orig_size:
                    reduction = (1 - new_size / orig_size) * 100
                    status_text = f"Compressed ✅ (-{int(reduction)}%)"
                else:
                    status_text = "Compressed ✅" if file_path.suffix.lower() == ".webp" else "Converted ✅"
            else:
                status_text = "Failed ❌"

            self.file_statuses[file_path] = status_text
            prog = (index + 1) / total
            curr_success = success
            curr_status = status_text

            def update_step(idx=curr_idx, st=curr_status, p=prog, i=curr_idx + 1):
                self.file_list.update_row(idx, st)
                self.file_list.set_progress(p)
                self.file_list.set_status(f"Processed {i} of {total} ({st})")

            self.after(0, update_step)

        final_success = success

        def update_complete():
            self.file_list.set_progress(1)
            q_desc = "Lossless" if lossless else f"{quality}% Quality"
            self.file_list.set_status(f"Completed ({q_desc}) • {final_success}/{total} ready")
            self.sidebar.open_output_btn.configure(state="normal")
            self.sidebar.convert_btn.configure(state="normal")

        self.after(0, update_complete)

    # ==================================================
    # Clear All Files
    # ==================================================

    def clear_all_files(self):

        self.selected_files.clear()
        self.file_statuses.clear()

        self.output_folder = None

        self.file_list.clear()

        self.sidebar.clear_output_folder()

        self.sidebar.convert_btn.configure(
            state="disabled"
        )

        self.sidebar.open_output_btn.configure(
            state="disabled"
        )

        self.file_list.set_status(
            "Ready"
        )

    # ==================================================
    # Remove Single File
    # ==================================================

    def convert_single_file_by_path(self, path):
        file_path = Path(path)
        if file_path in self.selected_files:
            idx = self.selected_files.index(file_path)
            self.convert_single_file(idx)

    def remove_file_by_path(self, path):
        file_path = Path(path)
        if file_path in self.selected_files:
            idx = self.selected_files.index(file_path)
            self.remove_file(idx)

    def remove_file(self, index):

        if 0 <= index < len(self.selected_files):

            removed = self.selected_files.pop(index)
            self.file_statuses.pop(removed, None)

            if self.selected_files:

                self.file_list.remove_single_row(removed, self.selected_files)

                self.file_list.set_status(
                    f"{len(self.selected_files)} file(s) selected"
                )

            else:

                self.clear_all_files()