# pyrefly: ignore [missing-import]
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES

from ui.sidebar import Sidebar
from ui.file_list import FileList
from ui.actions import AppActions
from converter import SUPPORTED_EXTENSIONS


class WebPConverterApp(ctk.CTk, TkinterDnD.DnDWrapper, AppActions):

    def __init__(self):
        super().__init__()

        # Initialize TkDND Tcl Extension
        try:
            self.TkdndVersion = TkinterDnD._require(self)
        except Exception:
            pass

        # ==================================================
        # Window Settings
        # ==================================================

        self.title("WebP Converter Pro")
        self.geometry("1020x650")
        self.minsize(700, 480)

        # Set Window Titlebar & Taskbar Icon
        try:
            self.iconbitmap("assets/icon.ico")
        except Exception:
            pass

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ==================================================
        # Application Data
        # ==================================================

        # Selected input images
        self.selected_files = []

        # Map Path -> Status string ("Waiting", "Converted ✅", "Failed ❌")
        self.file_statuses = {}

        # None = Save beside original image
        self.output_folder = None

        # Supported image formats (85+ formats: SVG, RAW, HEIC, PSD, PDF, and all standard formats)
        self.supported_extensions = SUPPORTED_EXTENSIONS

        # ==================================================
        # Window Layout
        # ==================================================

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================================================
        # Sidebar
        # ==================================================

        self.sidebar = Sidebar(self)

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        # ----------------------------
        # Button Events
        # ----------------------------

        self.sidebar.browse_images_btn.configure(
            command=self.browse_images
        )

        self.sidebar.browse_folder_btn.configure(
            command=self.browse_folder
        )

        self.sidebar.output_button.configure(
            command=self.choose_output_folder
        )

        self.sidebar.open_output_btn.configure(
            command=self.open_output_folder
        )

        self.sidebar.convert_btn.configure(
            command=self.start_conversion
        )
        self.sidebar.clear_btn.configure(
            command=self.clear_all_files
        )

        # ==================================================
        # File List
        # ==================================================

        self.file_list = FileList(self)

        self.file_list.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=15,
            pady=15
        )

        # ==================================================
        # Register Drag & Drop Drop Targets
        # ==================================================
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self.on_drop_files)

            self.file_list.drop_target_register(DND_FILES)
            self.file_list.dnd_bind("<<Drop>>", self.on_drop_files)

            self.file_list.file_frame.drop_target_register(DND_FILES)
            self.file_list.file_frame.dnd_bind("<<Drop>>", self.on_drop_files)
        except Exception as e:
            print("Drag and drop registration notice:", e)