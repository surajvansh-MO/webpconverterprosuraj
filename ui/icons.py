from pathlib import Path
from PIL import Image
import customtkinter as ctk

import sys

_ICON_CACHE = {}
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    _ICONS_DIR = Path(sys._MEIPASS) / "assets" / "icons"
else:
    _ICONS_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons"


def get_icon(name: str, size: tuple[int, int] = (16, 16)) -> ctk.CTkImage:
    """
    Load a cached 2x CTkImage from the assets/icons folder.
    """
    key = (name, size)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]

    path = _ICONS_DIR / f"{name}.png"
    if not path.exists():
        # Fallback or transparent blank
        img = Image.new("RGBA", (size[0] * 2, size[1] * 2), (0, 0, 0, 0))
    else:
        img = Image.open(path)

    ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=size)
    _ICON_CACHE[key] = ctk_img
    return ctk_img
