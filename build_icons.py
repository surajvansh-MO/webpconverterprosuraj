import resvg_py
from pathlib import Path

icons_dir = Path("assets/icons")
icons_dir.mkdir(parents=True, exist_ok=True)

ICONS = {
    "bolt": '''<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>''',
    "files": '''<rect x="3" y="3" width="18" height="18" rx="2" ry="2" fill="none" stroke="{color}" stroke-width="2"/><circle cx="8.5" cy="8.5" r="1.5" fill="{color}"/><polyline points="21 15 16 10 5 21" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>''',
    "folder": '''<path d="M4 20h16a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.93a2 2 0 0 1-1.66-.9l-.82-1.2A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13c0 1.1.9 2 2 2Z" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>''',
    "folder_open": '''<path d="m6 14 1.45-2.9A2 2 0 0 1 9.24 10H20a2 2 0 0 1 1.94 2.5l-1.55 6a2 2 0 0 1-1.94 1.5H4a2 2 0 0 1-2-2V5c0-1.1.9-2 2-2h3.93a2 2 0 0 1 1.66.9l.82 1.2a2 2 0 0 0 1.66.9H18a2 2 0 0 1 2 2v2" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>''',
    "sliders": '''<line x1="21" x2="14" y1="4" y2="4" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="10" x2="3" y1="4" y2="4" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="21" x2="12" y1="12" y2="12" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="8" x2="3" y1="12" y2="12" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="21" x2="16" y1="20" y2="20" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="12" x2="3" y1="20" y2="20" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="14" x2="14" y1="2" y2="6" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="8" x2="8" y1="10" y2="14" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="16" x2="16" y1="18" y2="22" stroke="{color}" stroke-width="2" stroke-linecap="round"/>''',
    "trash": '''<path d="M3 6h18" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="10" x2="10" y1="11" y2="17" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="14" x2="14" y1="11" y2="17" stroke="{color}" stroke-width="2" stroke-linecap="round"/>''',
    "play": '''<polygon points="6 3 20 12 6 21 6 3" fill="{color}" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>''',
    "x": '''<path d="M18 6 6 18" stroke="{color}" stroke-width="2" stroke-linecap="round"/><path d="m6 6 12 12" stroke="{color}" stroke-width="2" stroke-linecap="round"/>''',
    "cloud_download": '''<path d="M12 13v8l-4-4" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="m12 21 4-4" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M4.393 15.269A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>''',
    "loader": '''<path d="M21 12a9 9 0 1 1-6.219-8.56" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>''',
    "image_plus": '''<path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h7" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="16" x2="22" y1="5" y2="5" stroke="{color}" stroke-width="2" stroke-linecap="round"/><line x1="19" x2="19" y1="2" y2="8" stroke="{color}" stroke-width="2" stroke-linecap="round"/><circle cx="9" cy="9" r="2" fill="none" stroke="{color}" stroke-width="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'''
}

CONFIGS = [
    ("bolt_dark", "bolt", "#1A0F05", 48, 48),
    ("bolt_accent", "bolt", "#FF9040", 32, 32),
    ("bolt_muted", "bolt", "#8C95A8", 32, 32),
    ("files_dark", "files", "#1A0F05", 36, 36),
    ("folder_primary", "folder", "#E9ECF3", 36, 36),
    ("folder_dim", "folder", "#5B6478", 28, 28),
    ("folder_open_muted", "folder_open", "#8C95A8", 32, 32),
    ("folder_open_success", "folder_open", "#34D399", 32, 32),
    ("sliders_dim", "sliders", "#5B6478", 28, 28),
    ("image_plus_dim", "image_plus", "#5B6478", 28, 28),
    ("trash_danger", "trash", "#F2A0B0", 32, 32),
    ("play_dark", "play", "#1A0F05", 36, 36),
    ("play_dim", "play", "#5B6478", 36, 36),
    ("x_muted", "x", "#8C95A8", 32, 32),
    ("x_danger", "x", "#F2A0B0", 32, 32),
    ("cloud_download_accent", "cloud_download", "#FF9040", 80, 80),
    ("loader_accent", "loader", "#FF9040", 36, 36),
]

for filename, icon_key, color, w, h in CONFIGS:
    body = ICONS[icon_key].format(color=color)
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 24 24">{body}</svg>'
    png_bytes = resvg_py.svg_to_bytes(svg_string=svg)
    out_file = icons_dir / f"{filename}.png"
    out_file.write_bytes(png_bytes)
    print(f"Generated: {out_file.name}")

print("All icons successfully generated!")
