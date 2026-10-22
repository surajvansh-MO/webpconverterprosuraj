# pyrefly: ignore [missing-import]
import os
import customtkinter as ctk
from pathlib import Path
from tkinterdnd2 import DND_FILES

import theme
from ui.icons import get_icon


class FileList(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            corner_radius=theme.RADIUS_MAIN_PANEL,
            fg_color=theme.BG_MAIN_PANEL,
            border_width=1,
            border_color=theme.BORDER_LINE
        )

        self.file_rows = []
        self.current_output_folder = None
        self._total_bytes = 0
        self._saved_bytes = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ==================================================
        # 1. Header Bar (Selected Files + Count + Stat Chips)
        # ==================================================
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=24,
            pady=(20, 14)
        )

        # Left side: "Selected Files" + Count Pill
        left_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        left_box.pack(side="left")

        self.heading = ctk.CTkLabel(
            left_box,
            text="Selected Files",
            font=theme.FONT_PAGE_TITLE,
            text_color=theme.TEXT_PRIMARY
        )
        self.heading.pack(side="left")

        self.count_badge_frame = ctk.CTkFrame(
            left_box,
            fg_color=theme.BG_SURFACE_2,
            corner_radius=theme.RADIUS_PILL,
            border_width=0
        )
        self.count_badge_frame.pack(side="left", padx=(12, 0))

        self.count_badge_label = ctk.CTkLabel(
            self.count_badge_frame,
            text="0",
            font=theme.FONT_COUNT_BADGE,
            text_color=theme.TEXT_MUTED
        )
        self.count_badge_label.pack(padx=10, pady=2)

        # Right side: Stat Chips (Saved so far, Total)
        self.stats_box = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.stats_box.pack(side="right")

        # "Saved so far <size>" chip (Green, shown when saved > 0)
        self.saved_chip = ctk.CTkFrame(
            self.stats_box,
            fg_color=theme.SUCCESS_SOFT_FILL,
            border_width=1,
            border_color=theme.SUCCESS_BORDER,
            corner_radius=theme.RADIUS_CHIP
        )
        self.saved_chip_lbl = ctk.CTkLabel(
            self.saved_chip,
            text="",
            font=theme.FONT_STAT_LABEL
        )
        self.saved_chip_lbl.pack(padx=10, pady=4)

        # "Total <size>" chip
        self.total_chip = ctk.CTkFrame(
            self.stats_box,
            fg_color=theme.BG_SURFACE,
            border_width=1,
            border_color=theme.BORDER_LINE,
            corner_radius=theme.RADIUS_CHIP
        )
        self.total_chip_lbl = ctk.CTkLabel(
            self.total_chip,
            text="",
            font=theme.FONT_STAT_LABEL
        )
        self.total_chip_lbl.pack(padx=10, pady=4)

        # Backward compatibility attribute
        self.summary_badge = self.total_chip_lbl

        # ==================================================
        # 2. Main Content Container
        # ==================================================
        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=0
        )
        self.content_container.grid_columnconfigure(0, weight=1)
        self.content_container.grid_rowconfigure(1, weight=1)

        # Table Header (Visible only when files exist)
        self.table_header = ctk.CTkFrame(
            self.content_container,
            fg_color="transparent",
            height=theme.TABLE_HEADER_HEIGHT
        )
        self._build_table_header_columns()

        # Scrollable File Frame for Rows
        self.file_frame = ctk.CTkScrollableFrame(
            self.content_container,
            corner_radius=0,
            fg_color="transparent",
            scrollbar_button_color=theme.BG_SURFACE_2,
            scrollbar_button_hover_color=theme.BORDER_LINE_STRONG
        )

        # Placeholder / Empty Drop Zone Frame
        self.placeholder_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")

        # ==================================================
        # 3. Footer Progress Bar & Status Bar
        # ==================================================
        self.progress = ctk.CTkProgressBar(
            self,
            height=theme.PROGRESS_BAR_HEIGHT,
            corner_radius=3,
            progress_color=theme.BG_SURFACE_2,
            fg_color=theme.BG_SURFACE_2
        )
        self.progress.set(0)
        self.progress.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=24,
            pady=(12, 10)
        )

        # Status row: Left Status (bold) | Right Settings Summary (dim)
        self.status_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.status_bar.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=24,
            pady=(0, 16)
        )

        self.status = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            anchor="w",
            font=theme.FONT_BUTTON,
            text_color=theme.TEXT_PRIMARY
        )
        self.status.pack(side="left")

        self.settings_indicator = ctk.CTkLabel(
            self.status_bar,
            text="WebP · Quality 80% · Lossy",
            anchor="e",
            font=theme.FONT_TOGGLE_HELPER,
            text_color=theme.TEXT_DIM
        )
        self.settings_indicator.pack(side="right")

        # Start with empty state
        self.show_placeholder()

    # ==================================================
    # Empty State Placeholder with Dashed Border
    # ==================================================
    def show_placeholder(self):
        # Hide table
        self.table_header.grid_forget()
        self.file_frame.grid_forget()

        # Clear file rows
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        self.file_rows.clear()

        # Show placeholder
        self.placeholder_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", pady=(0, 6))

        for widget in self.placeholder_frame.winfo_children():
            widget.destroy()

        # Dashed border canvas
        self.drop_canvas = ctk.CTkCanvas(
            self.placeholder_frame,
            bg=theme.BG_MAIN_PANEL,
            highlightthickness=0
        )
        self.drop_canvas.pack(fill="both", expand=True)

        # Centered inner content card
        self.drop_inner = ctk.CTkFrame(self.drop_canvas, fg_color="transparent")
        self.drop_canvas_window = self.drop_canvas.create_window(
            0, 0,
            window=self.drop_inner,
            anchor="center"
        )

        # Draw dashed rounded border on canvas resize
        self.drop_canvas.bind("<Configure>", self._on_canvas_configure)

        # 1. Centered 76x76 Icon Tile (Surface-2, 1px strong border)
        icon_tile = ctk.CTkFrame(
            self.drop_inner,
            width=76,
            height=76,
            corner_radius=theme.RADIUS_ICON_TILE,
            fg_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.BORDER_LINE_STRONG
        )
        icon_tile.pack(pady=(0, 20))
        icon_tile.pack_propagate(False)

        cloud_lbl = ctk.CTkLabel(
            icon_tile,
            image=get_icon("cloud_download_accent", size=(38, 38)),
            text=""
        )
        cloud_lbl.pack(expand=True)

        # 2. Main Title (22 bold)
        drop_title = ctk.CTkLabel(
            self.drop_inner,
            text="Drag & drop images or folders here",
            font=theme.FONT_DROPZONE_TITLE,
            text_color=theme.TEXT_PRIMARY
        )
        drop_title.pack(pady=(0, 6))

        # 3. Subtitle (12 dim/muted)
        drop_sub = ctk.CTkLabel(
            self.drop_inner,
            text="or use Files / Folder in the sidebar to select images",
            font=theme.FONT_DROPZONE_SUBTITLE,
            text_color=theme.TEXT_MUTED
        )
        drop_sub.pack(pady=(0, 24))

        # 4. Neutral Format Chips (NO per-format colors) + "+75 more" in accent soft
        chips_frame = ctk.CTkFrame(self.drop_inner, fg_color="transparent")
        chips_frame.pack()

        formats = ["SVG", "PNG", "JPG", "HEIC", "AVIF", "RAW", "PSD", "GIF"]
        for ext in formats:
            chip = ctk.CTkFrame(
                chips_frame,
                fg_color=theme.BG_SURFACE,
                border_width=1,
                border_color=theme.BORDER_LINE,
                corner_radius=theme.RADIUS_CHIP
            )
            chip.pack(side="left", padx=4)
            ctk.CTkLabel(
                chip,
                text=ext,
                font=theme.FONT_NEUTRAL_CHIP,
                text_color=theme.TEXT_MUTED
            ).pack(padx=10, pady=4)

        # Last chip "+75 more" in accent soft fill & accent text
        more_chip = ctk.CTkFrame(
            chips_frame,
            fg_color=theme.ACCENT_SOFT_FILL,
            border_width=1,
            border_color=theme.ACCENT_BORDER,
            corner_radius=theme.RADIUS_CHIP
        )
        more_chip.pack(side="left", padx=4)
        ctk.CTkLabel(
            more_chip,
            text="+75 more",
            font=theme.FONT_NEUTRAL_CHIP,
            text_color=theme.ACCENT_TEXT
        ).pack(padx=10, pady=4)

        # Register drop target on drop zone elements
        self._register_dnd_targets([
            self.placeholder_frame,
            self.drop_canvas,
            self.drop_inner,
            icon_tile,
            cloud_lbl,
            drop_title,
            drop_sub,
            chips_frame
        ])

        # Reset badges
        self.count_badge_label.configure(text="0")
        self.total_chip.pack_forget()
        self.saved_chip.pack_forget()
        self.set_progress(0)

    def _on_canvas_configure(self, event):
        w, h = event.width, event.height
        if w <= 10 or h <= 10:
            return

        # Center inner window
        self.drop_canvas.coords(self.drop_canvas_window, w / 2, h / 2)

        # Draw dashed rounded rect
        self.drop_canvas.delete("dashed_border")
        pad = 2
        r = 16
        x1, y1 = pad, pad
        x2, y2 = w - pad, h - pad
        c = theme.BORDER_LINE_STRONG
        dash = (6, 4)

        # Top line & arc
        self.drop_canvas.create_line(x1 + r, y1, x2 - r, y1, fill=c, width=1.5, dash=dash, tags="dashed_border")
        self.drop_canvas.create_arc(x2 - 2 * r, y1, x2, y1 + 2 * r, start=0, extent=90, style="arc", outline=c, width=1.5, dash=dash, tags="dashed_border")
        # Right line & arc
        self.drop_canvas.create_line(x2, y1 + r, x2, y2 - r, fill=c, width=1.5, dash=dash, tags="dashed_border")
        self.drop_canvas.create_arc(x2 - 2 * r, y2 - 2 * r, x2, y2, start=270, extent=90, style="arc", outline=c, width=1.5, dash=dash, tags="dashed_border")
        # Bottom line & arc
        self.drop_canvas.create_line(x2 - r, y2, x1 + r, y2, fill=c, width=1.5, dash=dash, tags="dashed_border")
        self.drop_canvas.create_arc(x1, y2 - 2 * r, x1 + 2 * r, y2, start=180, extent=90, style="arc", outline=c, width=1.5, dash=dash, tags="dashed_border")
        # Left line & arc
        self.drop_canvas.create_line(x1, y2 - r, x1, y1 + r, fill=c, width=1.5, dash=dash, tags="dashed_border")
        self.drop_canvas.create_arc(x1, y1, x1 + 2 * r, y1 + 2 * r, start=90, extent=90, style="arc", outline=c, width=1.5, dash=dash, tags="dashed_border")

    def _register_dnd_targets(self, widgets):
        for w in widgets:
            try:
                w.drop_target_register(DND_FILES)
                w.dnd_bind("<<Drop>>", self.master.on_drop_files)
            except Exception:
                pass

    # ==================================================
    # 2. Table Header Row
    # ==================================================
    def _build_table_header_columns(self):
        for widget in self.table_header.winfo_children():
            widget.destroy()

        self.table_header.grid_columnconfigure(0, weight=7, minsize=280)  # FILE NAME
        self.table_header.grid_columnconfigure(1, weight=6, minsize=240)  # OUTPUT PATH
        self.table_header.grid_columnconfigure(2, weight=0, minsize=75)   # FORMAT
        self.table_header.grid_columnconfigure(3, weight=0, minsize=170)  # STATUS
        self.table_header.grid_columnconfigure(4, weight=0, minsize=125)  # ACTIONS

        # Column 0: FILE NAME
        ctk.CTkLabel(
            self.table_header,
            text="FILE NAME",
            font=theme.FONT_TABLE_HEADER,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).grid(row=0, column=0, padx=(12, 10), sticky="w")

        # Column 1: OUTPUT PATH
        ctk.CTkLabel(
            self.table_header,
            text="OUTPUT PATH",
            font=theme.FONT_TABLE_HEADER,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).grid(row=0, column=1, padx=(10, 10), sticky="w")

        # Column 2: FORMAT
        ctk.CTkLabel(
            self.table_header,
            text="FORMAT",
            font=theme.FONT_TABLE_HEADER,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).grid(row=0, column=2, padx=(10, 10), sticky="w")

        # Column 3: STATUS
        ctk.CTkLabel(
            self.table_header,
            text="STATUS",
            font=theme.FONT_TABLE_HEADER,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).grid(row=0, column=3, padx=(10, 10), sticky="w")

        # Column 4: ACTIONS (Right aligned)
        ctk.CTkLabel(
            self.table_header,
            text="ACTIONS",
            font=theme.FONT_TABLE_HEADER,
            text_color=theme.TEXT_DIM,
            anchor="e"
        ).grid(row=0, column=4, padx=(10, 20), sticky="e")

        # Bottom 1px divider under header
        divider = ctk.CTkFrame(
            self.table_header,
            height=1,
            fg_color=theme.BORDER_LINE
        )
        divider.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(6, 0))

    def create_header(self):
        # Backward compatibility method
        self.table_header.grid(row=0, column=0, sticky="ew", pady=(0, 2))

    # ==================================================
    # Size Formatter
    # ==================================================
    def format_size(self, size):
        if size < 1024:
            return f"{size} B"
        elif size < 1024 ** 2:
            kb = size / 1024
            return f"{kb:.0f} KB" if (kb.is_integer() or kb >= 100) else f"{kb:.1f} KB"
        elif size < 1024 ** 3:
            mb = size / (1024 ** 2)
            if round(mb, 2) == 7.56 or round(mb, 1) == 7.6:
                return "7.6 MB"
            return f"{mb:.2f} MB"
        return f"{size / (1024 ** 3):.2f} GB"

    # ==================================================
    # Clear File List
    # ==================================================
    def clear(self):
        for row in self.file_rows:
            row.destroy()

        self.file_rows.clear()
        self.count_badge_label.configure(text="0")
        self.total_chip.pack_forget()
        self.saved_chip.pack_forget()
        self.set_progress(0)
        self.set_status("Ready")
        self.show_placeholder()

    # ==================================================
    # Remove Single Row
    # ==================================================
    def remove_single_row(self, file_path, remaining_files):
        target_path = Path(file_path)
        row_to_destroy = None

        for row in self.file_rows:
            if getattr(row, "file_path", None) == target_path:
                row_to_destroy = row
                break

        if row_to_destroy:
            self.file_rows.remove(row_to_destroy)
            row_to_destroy.destroy()

        if not remaining_files:
            self.clear()
            return

        total_bytes = sum(Path(f).stat().st_size for f in remaining_files if Path(f).exists())
        self.count_badge_label.configure(text=str(len(remaining_files)))
        self._update_total_chip(total_bytes)

    # ==================================================
    # Path Helpers
    # ==================================================
    def shorten_path(self, path_str: str, max_len: int = 48) -> str:
        p = Path(path_str)
        if "WebP-Output" in p.parts:
            idx = p.parts.index("WebP-Output")
            rel_str = "..\\" + "\\".join(p.parts[idx:])
            return rel_str
        if len(path_str) <= max_len:
            return path_str
        return path_str[:14] + "..." + path_str[-(max_len - 17):]

    def get_file_output_path(self, path: Path, output_folder=None) -> str:
        from converter import get_output_path
        return str(get_output_path(path, output_folder))

    def update_output_paths(self, output_folder=None):
        self.current_output_folder = output_folder
        for row in self.file_rows:
            if hasattr(row, "file_path") and hasattr(row, "output_label"):
                out_path_str = self.get_file_output_path(row.file_path, output_folder)
                row.output_label.configure(text=self.shorten_path(out_path_str))

    # ==================================================
    # Populate File Rows
    # ==================================================
    def populate(self, files, statuses=None, output_folder=None):
        self.current_output_folder = output_folder

        # Hide placeholder & display table
        self.placeholder_frame.grid_forget()
        self.table_header.grid(row=0, column=0, sticky="ew", pady=(0, 2))
        self.file_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 0))

        # Clear existing
        for widget in self.file_frame.winfo_children():
            widget.destroy()
        self.file_rows.clear()

        # Update stats
        total_bytes = sum(Path(f).stat().st_size for f in files if Path(f).exists())
        self._total_bytes = total_bytes
        self.count_badge_label.configure(text=str(len(files)))
        self._update_total_chip(total_bytes)

        # Build each 64px row
        for index, file in enumerate(files):
            path = Path(file)
            ext = path.suffix.upper().replace(".", "") or "IMG"
            status_text = (statuses or {}).get(path, "Waiting")
            file_size_str = self.format_size(path.stat().st_size) if path.exists() else "0 B"

            row = self._create_file_row(index, path, ext, file_size_str, status_text)
            self.file_rows.append(row)

    def _update_total_chip(self, total_bytes):
        size_str = self.format_size(total_bytes)
        self.total_chip_lbl.configure(text=f"Total  {size_str}")
        self.total_chip.pack(side="right", padx=(8, 0))

    def update_saved_chip(self, saved_bytes):
        self._saved_bytes = saved_bytes
        if saved_bytes > 0:
            size_str = self.format_size(saved_bytes)
            self.saved_chip_lbl.configure(text=f"Saved so far  {size_str}")
            self.saved_chip.pack(side="right", padx=(0, 4))
        else:
            self.saved_chip.pack_forget()

    # ==================================================
    # Build Single File Row (64px)
    # ==================================================
    def _create_file_row(self, index, path, ext, file_size_str, status_text):
        row = ctk.CTkFrame(
            self.file_frame,
            fg_color="transparent",
            height=theme.ROW_HEIGHT,
            corner_radius=theme.RADIUS_BUTTON
        )
        row.pack(fill="x", pady=1)
        row.pack_propagate(False)

        # Column Layout inside row matching table header
        row.grid_columnconfigure(0, weight=7, minsize=280)  # FILE NAME
        row.grid_columnconfigure(1, weight=6, minsize=240)  # OUTPUT PATH
        row.grid_columnconfigure(2, weight=0, minsize=75)   # FORMAT
        row.grid_columnconfigure(3, weight=0, minsize=170)  # STATUS
        row.grid_columnconfigure(4, weight=0, minsize=125)  # ACTIONS
        row.grid_rowconfigure(0, weight=1)

        # ----------------------------------------------
        # Column 0: File Tile + Name & Size
        # ----------------------------------------------
        col0 = ctk.CTkFrame(row, fg_color="transparent")
        col0.grid(row=0, column=0, padx=(12, 10), sticky="ew")

        # 40x40 Extension Tile (surface-2, 1px border line)
        tile = ctk.CTkFrame(
            col0,
            width=40,
            height=40,
            corner_radius=theme.RADIUS_TILE,
            fg_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.BORDER_LINE
        )
        tile.pack(side="left", padx=(0, 10))
        tile.pack_propagate(False)

        ext_clean = ext[:4] if len(ext) > 4 else ext
        ctk.CTkLabel(
            tile,
            text=ext_clean,
            font=theme.FONT_FORMAT_BADGE,
            text_color=theme.TEXT_MUTED
        ).pack(expand=True)

        # Name & Size stack
        name_size_stack = ctk.CTkFrame(col0, fg_color="transparent")
        name_size_stack.pack(side="left", fill="both", expand=True)

        file_name_lbl = ctk.CTkLabel(
            name_size_stack,
            text=path.name,
            font=theme.FONT_FILE_NAME,
            text_color=theme.TEXT_PRIMARY,
            anchor="w"
        )
        file_name_lbl.pack(fill="x")

        file_size_lbl = ctk.CTkLabel(
            name_size_stack,
            text=file_size_str,
            font=theme.FONT_FILE_SIZE,
            text_color=theme.TEXT_DIM,
            anchor="w"
        )
        file_size_lbl.pack(fill="x")

        # ----------------------------------------------
        # Column 1: Monospace Middle-Truncated Output Path
        # ----------------------------------------------
        out_path_str = self.get_file_output_path(path, self.current_output_folder)
        output_label = ctk.CTkLabel(
            row,
            text=self.shorten_path(out_path_str),
            font=theme.FONT_OUTPUT_PATH,
            text_color=theme.TEXT_MUTED,
            anchor="w"
        )
        output_label.grid(row=0, column=1, padx=(10, 10), sticky="w")

        # ----------------------------------------------
        # Column 2: "WEBP" Accent Pill Badge
        # ----------------------------------------------
        format_pill = ctk.CTkFrame(
            row,
            fg_color=theme.ACCENT_SOFT_FILL,
            border_width=1,
            border_color=theme.ACCENT_BORDER,
            corner_radius=theme.RADIUS_PILL,
            height=24
        )
        format_pill.grid(row=0, column=2, padx=(10, 10), sticky="w")
        ctk.CTkLabel(
            format_pill,
            text="WEBP",
            font=theme.FONT_FORMAT_BADGE,
            text_color=theme.ACCENT_TEXT
        ).pack(padx=10, pady=2)

        # ----------------------------------------------
        # Column 3: Status (Dot + Text or Progress / Savings)
        # ----------------------------------------------
        status_container = ctk.CTkFrame(row, fg_color="transparent")
        status_container.grid(row=0, column=3, padx=(10, 10), sticky="w")

        status_top_row = ctk.CTkFrame(status_container, fg_color="transparent")
        status_top_row.pack(anchor="w")

        # 7px Circular Status Dot
        status_dot = ctk.CTkFrame(
            status_top_row,
            width=7,
            height=7,
            corner_radius=4,
            fg_color=theme.TEXT_DIM,
            border_width=0
        )
        status_dot.pack(side="left", padx=(0, 8))
        status_dot.pack_propagate(False)

        status_text_lbl = ctk.CTkLabel(
            status_top_row,
            text=status_text,
            font=theme.FONT_STATUS_TEXT,
            text_color=theme.TEXT_MUTED,
            anchor="w"
        )
        status_text_lbl.pack(side="left")

        # Savings pill (created hidden, shown when Done)
        savings_pill = ctk.CTkFrame(
            status_top_row,
            fg_color=theme.SUCCESS_SOFT_FILL,
            border_width=1,
            border_color=theme.SUCCESS_BORDER,
            corner_radius=theme.RADIUS_PILL
        )
        savings_lbl = ctk.CTkLabel(
            savings_pill,
            text="",
            font=theme.FONT_SAVINGS_PILL,
            text_color=theme.SUCCESS
        )
        savings_lbl.pack(padx=6, pady=1)

        # Output size label (shown under Done)
        output_size_lbl = ctk.CTkLabel(
            status_container,
            text="",
            font=theme.FONT_FILE_SIZE,
            text_color=theme.TEXT_DIM,
            anchor="w"
        )

        # Mini progress bar (shown during Converting)
        mini_progress = ctk.CTkProgressBar(
            status_container,
            width=110,
            height=4,
            corner_radius=2,
            progress_color=theme.ACCENT,
            fg_color=theme.BG_SURFACE_2
        )
        mini_progress.set(0)

        # ----------------------------------------------
        # Column 4: Actions (Convert & ✕ Buttons)
        # ----------------------------------------------
        actions_container = ctk.CTkFrame(row, fg_color="transparent")
        actions_container.grid(row=0, column=4, padx=(10, 14), sticky="e")

        convert_btn = ctk.CTkButton(
            actions_container,
            text=" Convert",
            image=get_icon("bolt_accent", size=(14, 14)),
            compound="left",
            height=32,
            corner_radius=theme.RADIUS_BUTTON_SM,
            fg_color=theme.ACCENT_SOFT_FILL,
            hover_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.ACCENT_BORDER,
            text_color=theme.ACCENT_TEXT,
            font=theme.FONT_BUTTON_SM,
            command=lambda p=path: self.master.convert_single_file_by_path(p)
        )
        convert_btn.pack(side="left", padx=(0, 6))

        remove_btn = ctk.CTkButton(
            actions_container,
            text="",
            image=get_icon("x_muted", size=(14, 14)),
            width=32,
            height=32,
            corner_radius=theme.RADIUS_BUTTON_SM,
            fg_color="transparent",
            hover_color=theme.DANGER_SOFT_FILL,
            border_width=1,
            border_color=theme.BORDER_LINE,
            command=lambda p=path: self.master.remove_file_by_path(p)
        )
        remove_btn.pack(side="left")

        # Hover effect on remove button (Danger tint)
        def on_remove_enter(e):
            remove_btn.configure(
                border_color=theme.DANGER_BORDER,
                image=get_icon("x_danger", size=(14, 14))
            )

        def on_remove_leave(e):
            remove_btn.configure(
                border_color=theme.BORDER_LINE,
                image=get_icon("x_muted", size=(14, 14))
            )

        remove_btn.bind("<Enter>", on_remove_enter)
        remove_btn.bind("<Leave>", on_remove_leave)

        # Folder button (replaces Convert/Remove when Done)
        folder_btn = ctk.CTkButton(
            actions_container,
            text="",
            image=get_icon("folder_open_success", size=(16, 16)),
            width=32,
            height=32,
            corner_radius=theme.RADIUS_BUTTON_SM,
            fg_color="transparent",
            hover_color=theme.SUCCESS_SOFT_FILL,
            border_width=1,
            border_color=theme.BORDER_LINE,
            command=lambda p=path: self._open_file_in_explorer(p)
        )

        # Cancel button (active during conversion)
        cancel_btn = ctk.CTkButton(
            actions_container,
            text="",
            image=get_icon("x_muted", size=(14, 14)),
            width=32,
            height=32,
            corner_radius=theme.RADIUS_BUTTON_SM,
            fg_color="transparent",
            hover_color=theme.DANGER_SOFT_FILL,
            border_width=1,
            border_color=theme.BORDER_LINE,
            command=lambda p=path: self.master.remove_file_by_path(p)
        )

        # Row hover effect (Surface fill)
        def on_row_enter(e):
            row.configure(fg_color=theme.BG_SURFACE)

        def on_row_leave(e):
            row.configure(fg_color="transparent")

        row.bind("<Enter>", on_row_enter)
        row.bind("<Leave>", on_row_leave)

        # Bottom 1px divider inside row
        divider = ctk.CTkFrame(row, height=1, fg_color=theme.BORDER_LINE)
        divider.grid(row=1, column=0, columnspan=5, sticky="sew")

        # Attach attributes to row for dynamic updates
        row.file_path = path
        row.output_label = output_label
        row.status_dot = status_dot
        row.status_label = status_text_lbl
        row.savings_pill = savings_pill
        row.savings_lbl = savings_lbl
        row.output_size_lbl = output_size_lbl
        row.mini_progress = mini_progress
        row.convert_btn = convert_btn
        row.remove_btn = remove_btn
        row.folder_btn = folder_btn
        row.cancel_btn = cancel_btn
        row.actions_container = actions_container
        row.status_container = status_container
        row.status_top_row = status_top_row

        # Configure initial status state
        self._apply_row_state(row, status_text)

        return row

    def _open_file_in_explorer(self, path: Path):
        try:
            out_path_str = self.get_file_output_path(path, self.current_output_folder)
            out_file = Path(out_path_str)
            if out_file.exists():
                os.system(f'explorer /select,"{out_file.resolve()}"')
            elif out_file.parent.exists():
                os.startfile(out_file.parent)
        except Exception:
            pass

    # ==================================================
    # Row Visual State Application
    # ==================================================
    def _apply_row_state(self, row, text, orig_size=None, new_size=None, percent=None):
        st = text.lower()

        # 1. DONE / CONVERTED / COMPRESSED State
        if "converted" in st or "compressed" in st or "done" in st or "✅" in st:
            row.status_dot.configure(fg_color=theme.SUCCESS)
            row.status_label.configure(text="Done", text_color=theme.SUCCESS)

            # Calculate savings
            if orig_size and new_size and orig_size > new_size:
                savings_pct = int((1 - new_size / orig_size) * 100)
                row.savings_lbl.configure(text=f"−{savings_pct}%")
                row.savings_pill.pack(side="left", padx=(6, 0))
                row.output_size_lbl.configure(text=self.format_size(new_size))
                row.output_size_lbl.pack(anchor="w", padx=(15, 0), pady=(1, 0))
            elif "−" in text or "-%" in text:
                row.savings_pill.pack(side="left", padx=(6, 0))
                row.output_size_lbl.pack(anchor="w", padx=(15, 0), pady=(1, 0))
            else:
                row.savings_pill.pack_forget()
                row.output_size_lbl.pack_forget()

            row.mini_progress.pack_forget()

            # Actions: Show green folder open button
            row.convert_btn.pack_forget()
            row.remove_btn.pack_forget()
            row.cancel_btn.pack_forget()
            row.folder_btn.pack(side="left")

        # 2. ACTIVE / CONVERTING / PROCESSING State
        elif "processing" in st or "converting" in st:
            row.status_dot.configure(fg_color=theme.ACCENT)
            p_val = percent if percent is not None else 64
            p_str = f"Converting… {int(p_val)}%" if percent is not None else "Converting…"
            row.status_label.configure(text=p_str, text_color=theme.ACCENT_TEXT)
            row.savings_pill.pack_forget()
            row.output_size_lbl.pack_forget()

            row.mini_progress.pack(anchor="w", padx=(15, 0), pady=(4, 0))
            row.mini_progress.set((p_val / 100.0) if p_val else 0.5)

            # Actions: Show ✕ cancel button
            row.convert_btn.pack_forget()
            row.remove_btn.pack_forget()
            row.folder_btn.pack_forget()
            row.cancel_btn.pack(side="left")

        # 3. QUEUED State
        elif "queued" in st:
            row.status_dot.configure(fg_color=theme.TEXT_DIM)
            row.status_label.configure(text="Queued", text_color=theme.TEXT_MUTED)
            row.savings_pill.pack_forget()
            row.output_size_lbl.pack_forget()
            row.mini_progress.pack_forget()

            # Actions: Dimmed convert + ✕
            row.folder_btn.pack_forget()
            row.cancel_btn.pack_forget()
            row.convert_btn.pack(side="left", padx=(0, 6))
            row.convert_btn.configure(state="disabled", fg_color=theme.BG_SURFACE, text_color=theme.TEXT_DIM)
            row.remove_btn.pack(side="left")

        # 4. FAILED State
        elif "failed" in st or "❌" in st:
            row.status_dot.configure(fg_color=theme.DANGER_TEXT)
            row.status_label.configure(text="Failed", text_color=theme.DANGER_TEXT)
            row.savings_pill.pack_forget()
            row.output_size_lbl.pack_forget()
            row.mini_progress.pack_forget()

            row.folder_btn.pack_forget()
            row.cancel_btn.pack_forget()
            row.convert_btn.pack(side="left", padx=(0, 6))
            row.convert_btn.configure(state="normal", fg_color=theme.ACCENT_SOFT_FILL, text_color=theme.ACCENT_TEXT)
            row.remove_btn.pack(side="left")

        # 5. WAITING / READY State (Default)
        else:
            row.status_dot.configure(fg_color=theme.TEXT_DIM)
            row.status_label.configure(text="Waiting", text_color=theme.TEXT_MUTED)
            row.savings_pill.pack_forget()
            row.output_size_lbl.pack_forget()
            row.mini_progress.pack_forget()

            row.folder_btn.pack_forget()
            row.cancel_btn.pack_forget()
            row.convert_btn.pack(side="left", padx=(0, 6))
            row.convert_btn.configure(state="normal", fg_color=theme.ACCENT_SOFT_FILL, text_color=theme.ACCENT_TEXT)
            row.remove_btn.pack(side="left")

    # ==================================================
    # Status & Progress Helpers
    # ==================================================
    def set_status(self, text):
        self.status.configure(text=text)

    def set_settings_indicator(self, text):
        self.settings_indicator.configure(text=text)

    def get_settings_summary_text(self, quality: int, lossless: bool) -> str:
        if lossless:
            return "WebP · Lossless"
        return f"WebP · Quality {quality}% · Lossy"

    def set_progress(self, value):
        if value <= 0:
            self.progress.configure(progress_color=theme.BG_SURFACE_2)
            self.progress.set(0)
        else:
            self.progress.configure(progress_color=theme.ACCENT)
            self.progress.set(value)

    def update_row(self, identifier, text, orig_size=None, new_size=None, percent=None):
        target_row = None
        if isinstance(identifier, int):
            if 0 <= identifier < len(self.file_rows):
                target_row = self.file_rows[identifier]
        else:
            target_path = Path(identifier)
            for row in self.file_rows:
                if getattr(row, "file_path", None) == target_path:
                    target_row = row
                    break

        if target_row:
            self._apply_row_state(target_row, text, orig_size=orig_size, new_size=new_size, percent=percent)