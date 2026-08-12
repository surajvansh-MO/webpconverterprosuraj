# pyrefly: ignore [missing-import]
import customtkinter as ctk
from PIL import Image


class Sidebar(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(
            master,
            width=280,
            corner_radius=0,
            fg_color="#18181b"  # Deep modern slate background
        )

        self.grid_propagate(False)
        self.pack_propagate(False)

        # ==================================================
        # Header Bar (Clean Section Title)
        # ==================================================

        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=14, pady=(16, 6))

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="⚡ Conversion Panel",
            font=("Segoe UI", 14, "bold"),
            text_color="#f4f4f5",
            anchor="w"
        )
        self.title_label.pack(fill="x")

        self.subtitle = ctk.CTkLabel(
            self.header_frame,
            text="High-Performance Batch Engine",
            font=("Segoe UI", 11),
            text_color="#a1a1aa",
            anchor="w"
        )
        self.subtitle.pack(fill="x", pady=(1, 0))

        # Divider Line
        self.divider = ctk.CTkFrame(self, height=1, fg_color="#27272a")
        self.divider.pack(fill="x", padx=14, pady=(6, 8))

        # ==================================================
        # Single-Sight Main Content Container (No Scrollbar)
        # ==================================================

        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.pack(fill="both", expand=True, padx=12, pady=0)

        # --------------------------------------------------
        # Card 1: Add Source Images
        # --------------------------------------------------

        self.card_source = ctk.CTkFrame(
            self.content_container,
            fg_color="#202023",
            border_width=1,
            border_color="#2c2c30",
            corner_radius=10
        )
        self.card_source.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            self.card_source,
            text="📥 Add Source Images",
            font=("Segoe UI", 12, "bold"),
            text_color="#f4f4f5"
        ).pack(anchor="w", padx=12, pady=(8, 6))

        btns_frame = ctk.CTkFrame(self.card_source, fg_color="transparent")
        btns_frame.pack(fill="x", padx=10, pady=(0, 10))
        btns_frame.grid_columnconfigure(0, weight=1)
        btns_frame.grid_columnconfigure(1, weight=1)

        self.browse_images_btn = ctk.CTkButton(
            btns_frame,
            text="📂 Files",
            height=34,
            corner_radius=6,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=("Segoe UI", 12, "bold")
        )
        self.browse_images_btn.grid(row=0, column=0, padx=(0, 4), sticky="ew")

        self.browse_folder_btn = ctk.CTkButton(
            btns_frame,
            text="📁 Folder",
            height=34,
            corner_radius=6,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            font=("Segoe UI", 12, "bold")
        )
        self.browse_folder_btn.grid(row=0, column=1, padx=(4, 0), sticky="ew")

        # --------------------------------------------------
        # Card 2: Quality & Compression Settings
        # --------------------------------------------------

        self.card_quality = ctk.CTkFrame(
            self.content_container,
            fg_color="#202023",
            border_width=1,
            border_color="#2c2c30",
            corner_radius=10
        )
        self.card_quality.pack(fill="x", pady=(0, 8))

        q_header = ctk.CTkFrame(self.card_quality, fg_color="transparent")
        q_header.pack(fill="x", padx=12, pady=(8, 4))

        ctk.CTkLabel(
            q_header,
            text="⚙️ Quality & Settings",
            font=("Segoe UI", 12, "bold"),
            text_color="#f4f4f5"
        ).pack(side="left")

        self.quality_label = ctk.CTkLabel(
            q_header,
            text="80%",
            font=("Segoe UI", 12, "bold"),
            text_color="#60a5fa"
        )
        self.quality_label.pack(side="right")

        self.quality_slider = ctk.CTkSlider(
            self.card_quality,
            from_=1,
            to=100,
            button_color="#3b82f6",
            button_hover_color="#60a5fa",
            progress_color="#2563eb",
            command=self.update_quality
        )
        self.quality_slider.set(80)
        self.quality_slider.pack(fill="x", padx=12, pady=2)

        self.lossless_switch = ctk.CTkSwitch(
            self.card_quality,
            text="Lossless WebP Mode",
            command=self.toggle_lossless,
            font=("Segoe UI", 11),
            text_color="#d4d4d8",
            progress_color="#2563eb"
        )
        self.lossless_switch.pack(anchor="w", padx=12, pady=(6, 10))

        # --------------------------------------------------
        # Card 3: Destination Folder
        # --------------------------------------------------

        self.card_output = ctk.CTkFrame(
            self.content_container,
            fg_color="#202023",
            border_width=1,
            border_color="#2c2c30",
            corner_radius=10
        )
        self.card_output.pack(fill="x", pady=(0, 8))

        ctk.CTkLabel(
            self.card_output,
            text="📁 Destination Folder",
            font=("Segoe UI", 12, "bold"),
            text_color="#f4f4f5"
        ).pack(anchor="w", padx=12, pady=(8, 4))

        self.output_entry = ctk.CTkEntry(
            self.card_output,
            placeholder_text="Same folder as source",
            state="readonly",
            height=30,
            corner_radius=6,
            font=("Segoe UI", 11),
            fg_color="#18181b",
            border_color="#3f3f46"
        )
        self.output_entry.pack(fill="x", padx=12, pady=(0, 6))

        out_btns = ctk.CTkFrame(self.card_output, fg_color="transparent")
        out_btns.pack(fill="x", padx=10, pady=(0, 8))
        out_btns.grid_columnconfigure(0, weight=1)
        out_btns.grid_columnconfigure(1, weight=1)

        self.output_button = ctk.CTkButton(
            out_btns,
            text="Choose",
            height=30,
            corner_radius=6,
            fg_color="#3f3f46",
            hover_color="#52525b",
            font=("Segoe UI", 11)
        )
        self.output_button.grid(row=0, column=0, padx=(0, 3), sticky="ew")

        self.open_output_btn = ctk.CTkButton(
            out_btns,
            text="Open Folder",
            height=30,
            corner_radius=6,
            fg_color="#27272a",
            hover_color="#3f3f46",
            text_color="#a1a1aa",
            state="disabled",
            font=("Segoe UI", 11)
        )
        self.open_output_btn.grid(row=0, column=1, padx=(3, 0), sticky="ew")

        # ==================================================
        # Footer Action Area (Fixed at bottom)
        # ==================================================

        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="x", padx=12, pady=(6, 12), side="bottom")

        self.clear_btn = ctk.CTkButton(
            self.footer_frame,
            text="🗑️ Clear All",
            height=32,
            corner_radius=6,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=("Segoe UI", 11, "bold")
        )
        self.clear_btn.pack(fill="x", pady=(0, 6))

        self.convert_btn = ctk.CTkButton(
            self.footer_frame,
            text="🚀 Start Conversion",
            height=42,
            corner_radius=8,
            state="disabled",
            fg_color="#059669",
            hover_color="#047857",
            font=("Segoe UI", 14, "bold")
        )
        self.convert_btn.pack(fill="x")

        # Developer Branding Footer Card
        self.brand_footer = ctk.CTkFrame(
            self.footer_frame,
            fg_color="#1e1e24",
            corner_radius=8,
            border_width=1,
            border_color="#2d2d35"
        )
        self.brand_footer.pack(fill="x", pady=(8, 0))

        # 1. Developed by Suraj Kumar
        dev_frame = ctk.CTkFrame(self.brand_footer, fg_color="transparent")
        dev_frame.pack(pady=(12, 4))

        ctk.CTkLabel(
            dev_frame,
            text="👤 Developed by ",
            font=("Segoe UI", 13.5),
            text_color="#e4e4e7"
        ).pack(side="left")

        ctk.CTkLabel(
            dev_frame,
            text="Suraj Kumar",
            font=("Segoe UI", 13.5, "bold"),
            text_color="#60a5fa"
        ).pack(side="left")

        # 2. Email Address
        ctk.CTkLabel(
            self.brand_footer,
            text="suraj.kumar@xecurify.com",
            font=("Segoe UI", 11),
            text_color="#a1a1aa"
        ).pack(pady=(0, 12))

    # ==================================================
    # Event Callbacks & Helpers
    # ==================================================

    def update_quality(self, value):
        if hasattr(self, "lossless_switch") and self.lossless_switch.get() == 1:
            return
        self.quality_label.configure(text=f"{int(value)}%")

    def toggle_lossless(self):
        if self.lossless_switch.get() == 1:
            self.quality_slider.configure(state="disabled")
            self.quality_label.configure(text="Lossless", text_color="#a1a1aa")
        else:
            self.quality_slider.configure(state="normal")
            self.quality_label.configure(
                text=f"{int(self.quality_slider.get())}%",
                text_color="#60a5fa"
            )

    def set_output_folder(self, folder_path: str):
        self.output_entry.configure(state="normal")
        self.output_entry.delete(0, "end")
        self.output_entry.insert(0, folder_path)
        self.output_entry.configure(state="readonly")
        self.open_output_btn.configure(
            state="normal",
            fg_color="#3f3f46",
            text_color="#ffffff"
        )

    def clear_output_folder(self):
        self.output_entry.configure(state="normal")
        self.output_entry.delete(0, "end")
        self.output_entry.configure(state="readonly")
        self.open_output_btn.configure(
            state="disabled",
            fg_color="#27272a",
            text_color="#a1a1aa"
        )