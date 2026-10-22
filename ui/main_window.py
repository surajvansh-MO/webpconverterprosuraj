# pyrefly: ignore [missing-import]
import customtkinter as ctk
from tkinterdnd2 import TkinterDnD, DND_FILES
import ctypes

import theme
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
        self.geometry(f"{theme.INITIAL_WINDOW_WIDTH}x{theme.INITIAL_WINDOW_HEIGHT}")
        self.minsize(theme.MIN_WINDOW_WIDTH, theme.MIN_WINDOW_HEIGHT)
        self.configure(fg_color=theme.BG_WINDOW)

        # Set Window Titlebar & Taskbar Icon
        try:
            self.iconbitmap("assets/icon.ico")
        except Exception:
            pass

        ctk.set_appearance_mode("dark")

        # Set Windows 10/11 Dark Titlebar & Color
        self._setup_dark_titlebar()

        # ==================================================
        # Application Data
        # ==================================================

        # Selected input images
        self.selected_files = []

        # Map Path -> Status string ("Waiting", "Converted ✅", "Failed ❌")
        self.file_statuses = {}

        # None = Save beside original image
        self.output_folder = None

        # Running total of bytes saved
        self.total_saved_bytes = 0

        # Supported image formats (85+ formats)
        self.supported_extensions = SUPPORTED_EXTENSIONS

        # ==================================================
        # Window Layout (Sidebar + Main Panel)
        # ==================================================

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==================================================
        # Sidebar (350px fixed width)
        # ==================================================

        self.sidebar = Sidebar(self)
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        # ----------------------------
        # Sidebar Button Events
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
        # Main Panel (FileList)
        # ==================================================

        self.file_list = FileList(self)
        self.file_list.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(0, 18),
            pady=18
        )

        # Initial status settings display
        self.update_settings_indicator()

        # ==================================================
        # Register Drag & Drop Drop Targets
        # ==================================================
        try:
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self.on_drop_files)

            self.file_list.drop_target_register(DND_FILES)
            self.file_list.dnd_bind("<<Drop>>", self.on_drop_files)

            if hasattr(self.file_list, "file_frame"):
                self.file_list.file_frame.drop_target_register(DND_FILES)
                self.file_list.file_frame.dnd_bind("<<Drop>>", self.on_drop_files)
        except Exception as e:
            print("Drag and drop registration notice:", e)

    def _setup_dark_titlebar(self):
        try:
            self.update_idletasks()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            # DWMWA_USE_IMMERSIVE_DARK_MODE (20 on Win 10 18985+ & Win 11, 19 on older Win 10)
            value = ctypes.c_int(2)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 20, ctypes.byref(value), 4)

            # DWMWA_CAPTION_COLOR (35 on Windows 11) - COLORREF 0x00BBGGRR (0x0F0B09 for #090B0F)
            caption_color = ctypes.c_int(0x000F0B09)
            ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption_color), 4)
        except Exception:
            pass

    def update_settings_indicator(self):
        """Update right-side indicator text: WebP · Quality X% · Lossy / Lossless"""
        try:
            quality = int(self.sidebar.quality_slider.get())
            lossless = bool(hasattr(self.sidebar, "lossless_switch") and self.sidebar.lossless_switch.get() == 1)
            summary = self.file_list.get_settings_summary_text(quality, lossless)
            self.file_list.set_settings_indicator(summary)
        except Exception:
            pass