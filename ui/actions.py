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

            elif (
                file.is_file()
                and file.suffix.lower() in self.supported_extensions
                and file not in self.selected_files
            ):

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

        filetypes = [
            (
                "Supported Images",
                "*.png *.jpg *.jpeg *.bmp *.tiff *.tif *.gif *.avif *.ico"
            )
        ]

        files = filedialog.askopenfilenames(
            title="Select Images",
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
            result, message = convert_image(
                file_path,
                output_folder=self.output_folder,
                quality=quality,
                lossless=lossless
            )

            status_text = "Converted ✅" if result else "Failed ❌"
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

            # Skip if this file is already converted successfully
            if self.file_statuses.get(file_path) == "Converted ✅":
                success += 1
                prog = (index + 1) / total
                self.after(0, lambda p=prog: self.file_list.set_progress(p))
                continue

            self.file_statuses[file_path] = "Processing..."
            curr_idx = index
            self.after(0, lambda idx=curr_idx: self.file_list.update_row(idx, "Processing..."))

            result, message = convert_image(
                file_path,
                output_folder=self.output_folder,
                quality=quality,
                lossless=lossless
            )

            if result:
                success += 1
                status_text = "Converted ✅"
            else:
                status_text = "Failed ❌"

            self.file_statuses[file_path] = status_text
            prog = (index + 1) / total
            curr_success = success
            curr_status = status_text

            def update_step(idx=curr_idx, st=curr_status, p=prog, i=curr_idx + 1):
                self.file_list.update_row(idx, st)
                self.file_list.set_progress(p)
                self.file_list.set_status(f"Converting {i} of {total}")

            self.after(0, update_step)

        final_success = success

        def update_complete():
            self.file_list.set_progress(1)
            self.file_list.set_status(f"Completed • {final_success}/{total} converted")
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