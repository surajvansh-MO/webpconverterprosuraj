import customtkinter as ctk
from PIL import Image


class SplashScreen(ctk.CTkToplevel):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # -----------------------------
        # Window Configuration
        # -----------------------------
        self.overrideredirect(True)

        width = 660
        height = 420

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.configure(fg_color="#030712")

        try:
            self.iconbitmap("assets/icon.ico")
        except Exception:
            pass

        # -----------------------------
        # Outer Card Container
        # -----------------------------
        container = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color="#0b0f19",
            border_width=1,
            border_color="#1e293b"
        )
        container.pack(expand=True, fill="both", padx=4, pady=4)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)

        # -----------------------------
        # Floating Format Badges
        # -----------------------------
        badges_data = [
            ("SVG", "#f97316", "#c2410c", 0.11, 0.20),
            ("PNG", "#38bdf8", "#0369a1", 0.15, 0.42),
            ("HEIC", "#ec4899", "#be185d", 0.10, 0.65),
            ("RAW", "#ef4444", "#b91c1c", 0.14, 0.84),
            ("JPG", "#34d399", "#047857", 0.88, 0.24),
            ("PSD", "#60a5fa", "#1d4ed8", 0.85, 0.54),
        ]

        for ext, text_col, border_col, rx, ry in badges_data:
            badge = ctk.CTkFrame(
                container,
                fg_color="#0f172a",
                border_width=1,
                border_color=border_col,
                corner_radius=6,
                width=54,
                height=26
            )
            badge.place(relx=rx, rely=ry, anchor="center")
            badge.pack_propagate(False)

            ctk.CTkLabel(
                badge,
                text=ext,
                font=("Segoe UI", 10, "bold"),
                text_color=text_col
            ).pack(expand=True)

        # -----------------------------
        # Central Content Container
        # -----------------------------
        content_frame = ctk.CTkFrame(container, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="nsew", pady=16)

        # App Logo Container
        try:
            icon_img = Image.open("assets/icon.ico")
            self.logo = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(68, 68))
            logo_widget = ctk.CTkLabel(content_frame, image=self.logo, text="")
        except Exception:
            logo_widget = ctk.CTkLabel(content_frame, text="🖼️", font=("Segoe UI", 48))

        logo_widget.pack(pady=(8, 6))

        # Title: WebP Converter Pro
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.pack()

        ctk.CTkLabel(
            title_frame,
            text="WebP ",
            font=("Segoe UI", 26, "bold"),
            text_color="#0080ff"
        ).pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="Converter Pro",
            font=("Segoe UI", 26, "bold"),
            text_color="#ffffff"
        ).pack(side="left")

        # Subtitle
        ctk.CTkLabel(
            content_frame,
            text="──  Fast  •  Modern  •  Batch Converter  ──",
            font=("Segoe UI", 11),
            text_color="#94a3b8"
        ).pack(pady=(2, 8))

        # Version Pill Badge
        version_pill = ctk.CTkFrame(
            content_frame,
            fg_color="#0f172a",
            border_width=1,
            border_color="#1d4ed8",
            corner_radius=12
        )
        version_pill.pack(pady=(0, 12))

        ctk.CTkLabel(
            version_pill,
            text="  Version 1.0.0  ",
            font=("Segoe UI", 10, "bold"),
            text_color="#38bdf8"
        ).pack(padx=8, pady=2)

        # -----------------------------
        # Two-Column Footer Cards (Developed by & Powered by)
        # -----------------------------
        footer_grid = ctk.CTkFrame(content_frame, fg_color="transparent")
        footer_grid.pack(fill="x", padx=90, pady=(0, 10))

        footer_grid.grid_columnconfigure(0, weight=1)
        footer_grid.grid_columnconfigure(1, weight=0)
        footer_grid.grid_columnconfigure(2, weight=1)

        # Left Column: Developed by Suraj Kumar
        left_col = ctk.CTkFrame(footer_grid, fg_color="transparent")
        left_col.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            left_col,
            text="👤",
            font=("Segoe UI", 14)
        ).pack()

        ctk.CTkLabel(
            left_col,
            text="Developed by",
            font=("Segoe UI", 10),
            text_color="#94a3b8"
        ).pack()

        ctk.CTkLabel(
            left_col,
            text="Suraj Kumar",
            font=("Segoe UI", 12, "bold"),
            text_color="#38bdf8"
        ).pack()

        ctk.CTkLabel(
            left_col,
            text="suraj.kumar@xecurify.com",
            font=("Segoe UI", 9),
            text_color="#64748b"
        ).pack()

        # Center Divider Line
        divider = ctk.CTkFrame(footer_grid, width=1, height=45, fg_color="#334155")
        divider.grid(row=0, column=1, sticky="ns", padx=12)

        # Right Column: Powered by miniOrange
        right_col = ctk.CTkFrame(footer_grid, fg_color="transparent")
        right_col.grid(row=0, column=2, sticky="nsew")

        ctk.CTkLabel(
            right_col,
            text="⚡",
            font=("Segoe UI", 14)
        ).pack()

        ctk.CTkLabel(
            right_col,
            text="Powered by",
            font=("Segoe UI", 10),
            text_color="#94a3b8"
        ).pack()

        ctk.CTkLabel(
            right_col,
            text="miniOrange",
            font=("Segoe UI", 12, "bold"),
            text_color="#f97316"
        ).pack()

        # -----------------------------
        # Progress Bar & Loading Text
        # -----------------------------
        self.loading_label = ctk.CTkLabel(
            content_frame,
            text="Loading...",
            font=("Segoe UI", 11),
            text_color="#cbd5e1"
        )
        self.loading_label.pack(pady=(4, 4))

        self.progress = ctk.CTkProgressBar(
            content_frame,
            width=360,
            height=10,
            corner_radius=6,
            progress_color="#2563eb",
            fg_color="#1e293b"
        )
        self.progress.pack()
        self.progress.set(0)

        # Start animation callback
        self.after(50, self.animate)

    # ==================================================
    # Animation Callback
    # ==================================================

    def animate(self):
        value = self.progress.get()

        if value < 1.0:
            value += 0.03
            self.progress.set(value)
            self.after(30, self.animate)
        else:
            self.destroy()
            self.parent.deiconify()