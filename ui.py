import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path
from converter import convert_image, SUPPORTED_EXTENSIONS
import threading


class WebPConverterApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # ----------------------------
        # Window Settings
        # ----------------------------
        self.title("WebP Converter Pro")
        self.geometry("1100x700")
        self.minsize(950, 650)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ----------------------------
        # Build UI
        # ----------------------------
        self.create_widgets()
        self.selected_files = []
        self.supported_extensions = SUPPORTED_EXTENSIONS
        self.file_rows = []

    def create_widgets(self):

        # =====================================
        # Main Window Layout
        # =====================================

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =====================================
        # LEFT SIDEBAR
        # =====================================

        self.sidebar = ctk.CTkFrame(
            self,
            width=260,
            corner_radius=0
        )

        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        # Logo / Title

        self.title_label = ctk.CTkLabel(
            self.sidebar,
            text="🖼 WebP Converter Pro",
            font=("Segoe UI", 22, "bold")
        )

        self.title_label.pack(pady=(25, 5))

        self.subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Batch Image Converter",
            font=("Segoe UI", 13)
        )

        self.subtitle.pack(pady=(0, 30))

        # Browse Buttons

        self.browse_images_btn = ctk.CTkButton(
            self.sidebar,
            text="📂 Browse Images",
            width=200,
            command=self.browse_images
        )

        self.browse_images_btn.pack(pady=8)

        self.browse_folder_btn = ctk.CTkButton(
            self.sidebar,
            text="📁 Browse Folder",
            width=200,
            command=self.browse_folder
        )

        self.browse_folder_btn.pack(pady=8)

        # Quality

        quality_title = ctk.CTkLabel(
            self.sidebar,
            text="WebP Quality",
            font=("Segoe UI", 16, "bold")
        )

        quality_title.pack(pady=(35, 5))

        self.quality_slider = ctk.CTkSlider(
            self.sidebar,
            from_=1,
            to=100
        )

        self.quality_slider.set(80)

        self.quality_slider.pack(
            padx=20,
            fill="x"
        )

        self.quality_label = ctk.CTkLabel(
            self.sidebar,
            text="80%"
        )

        self.quality_label.pack(pady=5)

        # Output Folder

        output_title = ctk.CTkLabel(
            self.sidebar,
            text="Output Folder",
            font=("Segoe UI", 16, "bold")
        )

        output_title.pack(pady=(30, 5))

        self.output_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Same as source"
        )

        self.output_entry.pack(
            padx=20,
            fill="x"
        )

        self.output_button = ctk.CTkButton(
            self.sidebar,
            text="Choose Folder"
        )

        self.output_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # Convert Button

        self.convert_btn = ctk.CTkButton(
            self.sidebar,
            text="🚀 Convert",
            height=42,
            font=("Segoe UI", 15, "bold"),
            state="disabled",
            command=self.start_conversion
        )

        self.convert_btn.pack(
            side="bottom",
            padx=20,
            pady=20,
            fill="x"
        )

        # =====================================
        # RIGHT PANEL
        # =====================================

        self.content = ctk.CTkFrame(
            self,
            corner_radius=0
        )

        self.content.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=15,
            pady=15
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # Heading

        heading = ctk.CTkLabel(
            self.content,
            text="Selected Files",
            font=("Segoe UI", 24, "bold")
        )

        heading.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        header = ctk.CTkFrame(self.file_frame, fg_color="transparent")
        header.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header,
            text="File",
            width=250,
            anchor="w",
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Type",
            width=70,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Size",
            width=90,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header,
            text="Status",
            width=120,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")
        # File List

        self.file_frame = ctk.CTkScrollableFrame(
            self.content,
            corner_radius=8
        )

        self.file_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        # Progress

        self.progress = ctk.CTkProgressBar(
            self.content
        )

        self.progress.set(0)

        self.progress.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(5, 5)
        )

        # Status

        self.status = ctk.CTkLabel(
            self.content,
            text="Status : Ready",
            anchor="w"
        )

        self.status.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 15)
        )


    def browse_images(self):

        all_patterns = " ".join(f"*{ext}" for ext in sorted(self.supported_extensions))
        filetypes = [
            ("All Supported Formats", all_patterns),
            ("Vector Graphics (*.svg, *.svgz, *.eps, *.pdf, *.ai)", "*.svg *.svgz *.eps *.ps *.pdf *.ai"),
            ("Standard Web & Photo (*.png, *.jpg, *.jpeg, *.webp, *.gif, *.bmp)", "*.png *.apng *.jpg *.jpeg *.jpe *.jfif *.webp *.gif *.bmp *.dib *.ico"),
            ("High-Efficiency & Mobile (*.heic, *.heif, *.avif)", "*.heic *.heif *.hif *.heics *.heifs *.avif *.avis"),
            ("Camera RAW Photos (*.raw, *.cr2, *.cr3, *.nef, *.arw, *.dng, ...)", "*.raw *.cr2 *.cr3 *.nef *.nrw *.arw *.srf *.sr2 *.dng *.orf *.rw2 *.pef *.raf *.x3f *.3fr *.mrw *.srw"),
            ("Adobe & Design (*.psd, *.psb, *.tiff, *.tga, *.dds)", "*.psd *.psb *.tiff *.tif *.tga *.dds *.hdr"),
            ("All Files (*.*)", "*.*")
        ]

        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=filetypes
        )

        if not files:
            return

        self.selected_files = list(files)

        self.populate_file_list()

        for file in self.selected_files:

            path = Path(file)

            size = path.stat().st_size / 1024

            self.filebox.insert(
                "end",
                f"📄 {path.name}    ({size:.1f} KB)\n"
            )

        self.status.configure(
            text=f"Status : {len(self.selected_files)} file(s) selected"
        )

        self.convert_btn.configure(state="normal")

    def browse_folder(self):
        folder = filedialog.askdirectory(
            title="Select Folder"
        )

        if not folder:
            return

        folder = Path(folder)

        self.selected_files = []

        for file in folder.rglob("*"):

            if (
                file.is_file()
                and file.suffix.lower() in self.supported_extensions
            ):
                self.selected_files.append(file)

        self.populate_file_list()

        if not self.selected_files:

            self.filebox.insert(
                "1.0",
                "No supported images found."
            )

            self.status.configure(
                text="Status : No supported images found"
            )

            self.convert_btn.configure(state="disabled")

            return

        for file in self.selected_files:

            size = file.stat().st_size / 1024

            self.filebox.insert(
                "end",
                f"📄 {file.name}    ({size:.1f} KB)\n"
            )

        self.status.configure(
            text=f"Status : {len(self.selected_files)} image(s) found"
        )

        self.convert_btn.configure(
            state="normal"
        )

    def start_conversion(self):

        self.convert_btn.configure(state="disabled")

        thread = threading.Thread(
            target=self.convert_images,
            daemon=True
        )

        thread.start()

    def convert_images(self):

        total = len(self.selected_files)

        if total == 0:
            return

        self.progress.set(0)

        self.filebox.delete("1.0", "end")

        success = 0

        for index, file in enumerate(self.selected_files):

            result, message = convert_image(
                file,
                quality=self.quality_slider.get()
            )

            if result:

                success += 1

                self.filebox.insert(
                    "end",
                    f"✅ {Path(message).name}\n"
                )

            else:

                self.filebox.insert(
                    "end",
                    f"❌ {Path(file).name} : {message}\n"
                )

            self.progress.set((index + 1) / total)

            self.status.configure(
                text=f"Converting {index+1}/{total}"
            )

            self.update()

        self.status.configure(
            text=f"Completed • {success}/{total} converted"
        )

        self.convert_btn.configure(
        state="normal"
            )
        
    def populate_file_list(self):

        # Remove old rows
        for row in self.file_rows:
            row.destroy()

        self.file_rows.clear()

        for file in self.selected_files:

            row = ctk.CTkFrame(
                self.file_frame,
                fg_color="transparent"
            )

            row.pack(fill="x", pady=2)

            size = file.stat().st_size / (1024 * 1024)

            ctk.CTkLabel(
                row,
                text=file.name,
                width=250,
                anchor="w"
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=file.suffix.upper().replace(".", ""),
                width=70
            ).pack(side="left")

            ctk.CTkLabel(
                row,
                text=f"{size:.2f} MB",
                width=90
            ).pack(side="left")

            status = ctk.CTkLabel(
                row,
                text="Waiting",
                width=120
            )

            status.pack(side="left")

            row.status_label = status

            self.file_rows.append(row)