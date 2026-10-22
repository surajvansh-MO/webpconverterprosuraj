import customtkinter as ctk
from pathlib import Path
import theme
from ui.icons import get_icon


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            width=theme.SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=theme.BG_SIDEBAR,
            border_width=0
        )

        self.grid_propagate(False)
        self.pack_propagate(False)

        # Main vertical container with consistent 18px padding
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=theme.SIDEBAR_PAD, pady=(16, 12))

        # Bottom section pinned to the bottom
        self.bottom_box = ctk.CTkFrame(self.container, fg_color="transparent")
        self.bottom_box.pack(side="bottom", fill="x")

        # Top section expanding from the top
        self.top_box = ctk.CTkFrame(self.container, fg_color="transparent")
        self.top_box.pack(side="top", fill="both", expand=True)

        # 1. Brand Header
        self._build_brand_header(self.top_box)

        # 2. Card: ADD SOURCE IMAGES
        self._build_source_card(self.top_box)

        # 3. Card: QUALITY & SETTINGS
        self._build_quality_card(self.top_box)

        # 4. Card: DESTINATION FOLDER
        self._build_destination_card(self.top_box)

        # 5. Bottom Action Buttons (Start Conversion + Clear All)
        self._build_action_buttons(self.bottom_box)

        # 6. Footer (Avatar + Developed by + Email)
        self._build_footer(self.bottom_box)

    # ==================================================
    # 1. Brand Header
    # ==================================================
    def _build_brand_header(self, parent):
        brand_frame = ctk.CTkFrame(parent, fg_color="transparent")
        brand_frame.pack(fill="x", pady=(0, 12))

        # 38x38 rounded orange square with dark bolt icon
        badge = ctk.CTkFrame(
            brand_frame,
            width=38,
            height=38,
            corner_radius=10,
            fg_color=theme.ACCENT,
            border_width=0
        )
        badge.pack(side="left", padx=(0, 12))
        badge.pack_propagate(False)

        ctk.CTkLabel(
            badge,
            image=get_icon("bolt_dark", size=(18, 18)),
            text=""
        ).pack(expand=True)

        text_col = ctk.CTkFrame(brand_frame, fg_color="transparent")
        text_col.pack(side="left", fill="both", expand=True)

        ctk.CTkLabel(
            text_col,
            text="Conversion Panel",
            font=theme.FONT_APP_TITLE,
            text_color=theme.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            text_col,
            text="High-Performance Batch Engine",
            font=theme.FONT_APP_SUBTITLE,
            text_color=theme.TEXT_MUTED,
            anchor="w"
        ).pack(fill="x", pady=(1, 0))

    # ==================================================
    # 2. Card: ADD SOURCE IMAGES
    # ==================================================
    def _build_source_card(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color=theme.BG_SURFACE,
            border_width=1,
            border_color=theme.BORDER_LINE,
            corner_radius=theme.RADIUS_CARD
        )
        card.pack(fill="x", pady=(0, 8))

        # Header with icon
        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(8, 6))

        ctk.CTkLabel(
            hdr,
            image=get_icon("image_plus_dim", size=(14, 14)),
            text=""
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            hdr,
            text="ADD SOURCE IMAGES",
            font=theme.FONT_CARD_TITLE,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).pack(side="left")

        # Two equal buttons
        btns = ctk.CTkFrame(card, fg_color="transparent")
        btns.pack(fill="x", padx=12, pady=(0, 8))
        btns.grid_columnconfigure(0, weight=1)
        btns.grid_columnconfigure(1, weight=1)

        self.browse_images_btn = ctk.CTkButton(
            btns,
            text=" Files",
            image=get_icon("files_dark", size=(16, 16)),
            compound="left",
            height=34,
            corner_radius=theme.RADIUS_BUTTON,
            fg_color=theme.ACCENT,
            hover_color=theme.ACCENT_HOVER,
            text_color=theme.TEXT_ON_ACCENT,
            font=theme.FONT_BUTTON
        )
        self.browse_images_btn.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self.browse_folder_btn = ctk.CTkButton(
            btns,
            text=" Folder",
            image=get_icon("folder_primary", size=(16, 16)),
            compound="left",
            height=34,
            corner_radius=theme.RADIUS_BUTTON,
            fg_color=theme.BG_SURFACE,
            hover_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.BORDER_LINE_STRONG,
            text_color=theme.TEXT_PRIMARY,
            font=theme.FONT_BUTTON
        )
        self.browse_folder_btn.grid(row=0, column=1, padx=(4, 0), sticky="ew")

    # ==================================================
    # 3. Card: QUALITY & SETTINGS
    # ==================================================
    def _build_quality_card(self, parent):
        self.card_quality = ctk.CTkFrame(
            parent,
            fg_color=theme.BG_SURFACE,
            border_width=1,
            border_color=theme.BORDER_LINE,
            corner_radius=theme.RADIUS_CARD
        )
        self.card_quality.pack(fill="x", pady=(0, 10))

        # Header Row
        hdr = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(10, 8))

        ctk.CTkLabel(
            hdr,
            image=get_icon("sliders_dim", size=(14, 14)),
            text=""
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            hdr,
            text="QUALITY & SETTINGS",
            font=theme.FONT_CARD_TITLE,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).pack(side="left")

        # Pill badge on right ("80%")
        self.quality_badge_frame = ctk.CTkFrame(
            hdr,
            fg_color=theme.ACCENT_SOFT_FILL,
            border_width=1,
            border_color=theme.ACCENT_BORDER,
            corner_radius=theme.RADIUS_PILL
        )
        self.quality_badge_frame.pack(side="right")

        self.quality_label = ctk.CTkLabel(
            self.quality_badge_frame,
            text="80%",
            font=theme.FONT_VALUE_PILL,
            text_color=theme.ACCENT_TEXT
        )
        self.quality_label.pack(padx=10, pady=2)

        # Slider Row
        slider_frame = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        slider_frame.pack(fill="x", padx=12, pady=(0, 2))

        self.quality_slider = ctk.CTkSlider(
            slider_frame,
            from_=1,
            to=100,
            height=14,
            progress_color=theme.ACCENT,
            fg_color=theme.BORDER_LINE,
            button_color="#FFFFFF",
            button_hover_color="#FFFFFF",
            button_corner_radius=7,
            command=self.update_quality
        )
        self.quality_slider.set(80)
        self.quality_slider.pack(fill="x")

        # Sub labels under slider ("Smaller file", "Higher quality")
        sub_labels = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        sub_labels.pack(fill="x", padx=14, pady=(2, 6))

        ctk.CTkLabel(
            sub_labels,
            text="Smaller file",
            font=theme.FONT_DIM,
            text_color=theme.TEXT_DIM
        ).pack(side="left")

        ctk.CTkLabel(
            sub_labels,
            text="Higher quality",
            font=theme.FONT_DIM,
            text_color=theme.TEXT_DIM
        ).pack(side="right")

        # Preset Chips Row (3 equal chips: 40% Max, 75% Balance, 90% Sharp)
        presets_frame = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        presets_frame.pack(fill="x", padx=12, pady=(0, 10))
        presets_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.preset_chips = {}
        for idx, (q, label) in enumerate([(40, "Max"), (75, "Balance"), (90, "Sharp")]):
            btn = ctk.CTkButton(
                presets_frame,
                text=f"{q}%\n{label}",
                height=36,
                corner_radius=theme.RADIUS_CHIP,
                fg_color=theme.BG_SURFACE,
                hover_color=theme.BG_SURFACE_2,
                border_width=1,
                border_color=theme.BORDER_LINE,
                text_color=theme.TEXT_PRIMARY,
                font=theme.FONT_PRESET_LABEL,
                command=lambda val=q: self.set_preset(val)
            )
            btn.grid(row=0, column=idx, padx=3, sticky="ew")
            self.preset_chips[q] = btn

        # Divider line
        div1 = ctk.CTkFrame(self.card_quality, height=1, fg_color=theme.BORDER_LINE)
        div1.pack(fill="x", padx=14, pady=0)

        # Toggle Row 1: Lossless WebP Mode
        lossless_row = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        lossless_row.pack(fill="x", padx=14, pady=(8, 8))

        ctk.CTkLabel(
            lossless_row,
            text="Lossless WebP Mode",
            font=theme.FONT_TOGGLE_LABEL,
            text_color=theme.TEXT_PRIMARY
        ).pack(side="left")

        self.lossless_switch = ctk.CTkSwitch(
            lossless_row,
            text="",
            width=44,
            command=self.toggle_lossless,
            progress_color=theme.ACCENT,
            fg_color=theme.BG_SURFACE_2,
            button_color="#FFFFFF",
            button_hover_color="#FFFFFF"
        )
        self.lossless_switch.pack(side="right")

        # Divider line
        div2 = ctk.CTkFrame(self.card_quality, height=1, fg_color=theme.BORDER_LINE)
        div2.pack(fill="x", padx=14, pady=0)

        # Toggle Row 2: Auto-compress on change
        auto_row = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        auto_row.pack(fill="x", padx=14, pady=(8, 8))

        auto_texts = ctk.CTkFrame(auto_row, fg_color="transparent")
        auto_texts.pack(side="left")

        ctk.CTkLabel(
            auto_texts,
            text="Auto-compress on change",
            font=theme.FONT_TOGGLE_LABEL,
            text_color=theme.TEXT_PRIMARY,
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            auto_texts,
            text="Re-run when settings change",
            font=theme.FONT_TOGGLE_HELPER,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).pack(fill="x")

        self.auto_compress_switch = ctk.CTkSwitch(
            auto_row,
            text="",
            width=44,
            progress_color=theme.ACCENT,
            fg_color=theme.BG_SURFACE_2,
            button_color="#FFFFFF",
            button_hover_color="#FFFFFF"
        )
        self.auto_compress_switch.select()
        self.auto_compress_switch.pack(side="right")

    # ==================================================
    # 4. Card: DESTINATION FOLDER
    # ==================================================
    def _build_destination_card(self, parent):
        card = ctk.CTkFrame(
            parent,
            fg_color=theme.BG_SURFACE,
            border_width=1,
            border_color=theme.BORDER_LINE,
            corner_radius=theme.RADIUS_CARD
        )
        card.pack(fill="x", pady=(0, 8))

        hdr = ctk.CTkFrame(card, fg_color="transparent")
        hdr.pack(fill="x", padx=14, pady=(8, 6))

        ctk.CTkLabel(
            hdr,
            image=get_icon("folder_dim", size=(14, 14)),
            text=""
        ).pack(side="left", padx=(0, 8))

        ctk.CTkLabel(
            hdr,
            text="DESTINATION FOLDER",
            font=theme.FONT_CARD_TITLE,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).pack(side="left")

        self.output_entry = ctk.CTkEntry(
            card,
            placeholder_text="No folder selected",
            placeholder_text_color=theme.TEXT_DIM,
            state="readonly",
            height=30,
            corner_radius=theme.RADIUS_INPUT,
            font=theme.FONT_HELPER,
            fg_color=theme.BG_SURFACE,
            border_color=theme.BORDER_LINE,
            border_width=1,
            text_color=theme.TEXT_PRIMARY
        )
        self.output_entry.pack(fill="x", padx=12, pady=(0, 6))

        out_btns = ctk.CTkFrame(card, fg_color="transparent")
        out_btns.pack(fill="x", padx=12, pady=(0, 8))
        out_btns.grid_columnconfigure((0, 1), weight=1)

        self.output_button = ctk.CTkButton(
            out_btns,
            text="Choose",
            height=30,
            corner_radius=theme.RADIUS_BUTTON,
            fg_color=theme.BG_SURFACE,
            hover_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.BORDER_LINE,
            text_color=theme.TEXT_PRIMARY,
            font=theme.FONT_BUTTON
        )
        self.output_button.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self.open_output_btn = ctk.CTkButton(
            out_btns,
            text=" Open Folder",
            image=get_icon("folder_open_muted", size=(15, 15)),
            compound="left",
            height=30,
            corner_radius=theme.RADIUS_BUTTON,
            fg_color=theme.BG_SURFACE,
            hover_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.BORDER_LINE,
            text_color=theme.TEXT_MUTED,
            state="disabled",
            font=theme.FONT_BUTTON
        )
        self.open_output_btn.grid(row=0, column=1, padx=(4, 0), sticky="ew")

    # ==================================================
    # 5. Bottom Action Buttons (Start Conversion + Clear All)
    # ==================================================
    def _build_action_buttons(self, parent):
        actions_frame = ctk.CTkFrame(parent, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 8))

        # Start Conversion Button (46px tall, radius 12)
        self.convert_btn = ctk.CTkButton(
            actions_frame,
            text=" Start Conversion",
            image=get_icon("play_dim", size=(16, 16)),
            compound="left",
            height=44,
            corner_radius=theme.RADIUS_BUTTON_PRIMARY,
            state="disabled",
            fg_color=theme.BG_SURFACE,
            hover_color=theme.ACCENT_HOVER,
            border_width=1,
            border_color=theme.BORDER_LINE,
            text_color=theme.TEXT_DIM,
            font=theme.FONT_BUTTON_PRIMARY
        )
        self.convert_btn.pack(fill="x", pady=(0, 6))

        # Clear All Button directly BELOW Start (34px tall, radius 10)
        self.clear_btn = ctk.CTkButton(
            actions_frame,
            text=" Clear All",
            image=get_icon("trash_danger", size=(15, 15)),
            compound="left",
            height=32,
            corner_radius=theme.RADIUS_BUTTON,
            fg_color="transparent",
            hover_color=theme.DANGER_SOFT_FILL,
            border_width=1,
            border_color=theme.DANGER_BORDER,
            text_color=theme.DANGER_TEXT,
            font=theme.FONT_BUTTON_GHOST
        )
        self.clear_btn.pack(fill="x")

    # ==================================================
    # 6. Sidebar Footer
    # ==================================================
    def _build_footer(self, parent):
        div = ctk.CTkFrame(parent, height=1, fg_color=theme.BORDER_LINE)
        div.pack(fill="x", pady=(0, 8))

        footer_row = ctk.CTkFrame(parent, fg_color="transparent")
        footer_row.pack(fill="x", pady=(0, 2))

        # 30px Circular Avatar "SK"
        avatar = ctk.CTkFrame(
            footer_row,
            width=28,
            height=28,
            corner_radius=14,
            fg_color=theme.BG_SURFACE_2,
            border_width=1,
            border_color=theme.BORDER_LINE_STRONG
        )
        avatar.pack(side="left", padx=(0, 10))
        avatar.pack_propagate(False)

        ctk.CTkLabel(
            avatar,
            text="SK",
            font=theme.FONT_FOOTER_AVATAR,
            text_color=theme.TEXT_MUTED
        ).pack(expand=True)

        meta = ctk.CTkFrame(footer_row, fg_color="transparent")
        meta.pack(side="left", fill="both", expand=True)

        name_row = ctk.CTkFrame(meta, fg_color="transparent")
        name_row.pack(anchor="w")

        ctk.CTkLabel(
            name_row,
            text="Developed by ",
            font=theme.FONT_FOOTER_DEV,
            text_color=theme.TEXT_MUTED
        ).pack(side="left")

        ctk.CTkLabel(
            name_row,
            text="Suraj Kumar",
            font=theme.FONT_FOOTER_NAME,
            text_color=theme.ACCENT_TEXT
        ).pack(side="left")

        ctk.CTkLabel(
            meta,
            text="suraj.kumar@xecurify.com",
            font=theme.FONT_FOOTER_EMAIL,
            text_color=theme.TEXT_DIM,
            anchor="w"
        ).pack(fill="x")

    # ==================================================
    # State Helpers & Callbacks
    # ==================================================

    def set_convert_button_state(self, mode: str, text: str = None):
        """
        Updates Start Conversion button visual state:
          - 'disabled': surface fill, dim text, 1px line border, play_dim icon
          - 'enabled': solid orange fill, dark text, play_dark icon
          - 'converting': accent soft fill, accent border, accent text, loader icon
        """
        if mode == "disabled":
            self.convert_btn.configure(
                state="disabled",
                fg_color=theme.BG_SURFACE,
                border_width=1,
                border_color=theme.BORDER_LINE,
                text_color=theme.TEXT_DIM,
                image=get_icon("play_dim", size=(16, 16)),
                text=" Start Conversion"
            )
        elif mode == "enabled":
            self.convert_btn.configure(
                state="normal",
                fg_color=theme.ACCENT,
                hover_color=theme.ACCENT_HOVER,
                border_width=0,
                text_color=theme.TEXT_ON_ACCENT,
                image=get_icon("play_dark", size=(16, 16)),
                text=" Start Conversion"
            )
        elif mode == "converting":
            self.convert_btn.configure(
                state="disabled",
                fg_color=theme.ACCENT_SOFT_FILL,
                border_width=1,
                border_color=theme.ACCENT_BORDER,
                text_color=theme.ACCENT_TEXT,
                image=get_icon("loader_accent", size=(16, 16)),
                text=text or " Converting..."
            )

    def set_preset(self, q_value):
        if hasattr(self, "lossless_switch") and self.lossless_switch.get() == 1:
            self.lossless_switch.deselect()
            self.quality_slider.configure(state="normal")
        self.quality_slider.set(q_value)
        self.quality_label.configure(text=f"{int(q_value)}%", text_color=theme.ACCENT_TEXT)
        self._highlight_preset(q_value)
        if hasattr(self.master, "on_compression_settings_changed"):
            self.master.on_compression_settings_changed(immediate=True)

    def _highlight_preset(self, active_val):
        for q, btn in getattr(self, "preset_chips", {}).items():
            if q == active_val:
                btn.configure(
                    fg_color=theme.ACCENT_SOFT_FILL,
                    border_color=theme.ACCENT_BORDER,
                    text_color=theme.ACCENT_TEXT
                )
            else:
                btn.configure(
                    fg_color=theme.BG_SURFACE,
                    border_color=theme.BORDER_LINE,
                    text_color=theme.TEXT_PRIMARY
                )

    def update_quality(self, value):
        if hasattr(self, "lossless_switch") and self.lossless_switch.get() == 1:
            return
        val_int = int(value)
        self.quality_label.configure(text=f"{val_int}%", text_color=theme.ACCENT_TEXT)
        self._highlight_preset(val_int)
        if hasattr(self.master, "on_compression_settings_changed"):
            self.master.on_compression_settings_changed(immediate=False)

    def toggle_lossless(self):
        if self.lossless_switch.get() == 1:
            self.quality_slider.configure(state="disabled")
            self.quality_label.configure(text="Lossless", text_color=theme.TEXT_MUTED)
            self._highlight_preset(None)
        else:
            self.quality_slider.configure(state="normal")
            val_int = int(self.quality_slider.get())
            self.quality_label.configure(text=f"{val_int}%", text_color=theme.ACCENT_TEXT)
            self._highlight_preset(val_int)
        if hasattr(self.master, "on_compression_settings_changed"):
            self.master.on_compression_settings_changed(immediate=True)

    def set_output_folder(self, folder_path: str):
        self.output_entry.configure(state="normal")
        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, folder_path)
        self.output_entry.configure(state="readonly")
        self.open_output_btn.configure(
            state="normal",
            text_color=theme.TEXT_PRIMARY
        )

    def clear_output_folder(self):
        self.output_entry.configure(state="normal")
        self.output_entry.delete(0, "end")
        self.output_entry.configure(state="readonly")
        self.open_output_btn.configure(
            state="disabled",
            text_color=theme.TEXT_MUTED
        )