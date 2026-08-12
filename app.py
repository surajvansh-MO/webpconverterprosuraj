import sys
import os
import ctypes
import subprocess
from pathlib import Path
from ui.main_window import WebPConverterApp
from windows.splash import SplashScreen


def ensure_shortcuts():
    """Automatically create Desktop and Start Menu shortcuts on Windows."""
    if sys.platform != "win32":
        return

    try:
        if getattr(sys, "frozen", False):
            exe_path = Path(sys.executable).resolve()
        else:
            exe_path = Path(sys.argv[0]).resolve()

        # Desktop folder
        desktop_dir = Path(os.path.expanduser("~/Desktop"))
        if not desktop_dir.exists():
            desktop_dir = Path(os.environ.get("USERPROFILE", "")) / "Desktop"

        # Start Menu folder
        start_menu_dir = Path(os.environ.get("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs"

        shortcuts_to_create = []

        if desktop_dir.exists():
            desktop_shortcut = desktop_dir / "WebP Converter Pro.lnk"
            if not desktop_shortcut.exists():
                shortcuts_to_create.append(desktop_shortcut)

        if start_menu_dir.exists():
            start_shortcut = start_menu_dir / "WebP Converter Pro.lnk"
            if not start_shortcut.exists():
                shortcuts_to_create.append(start_shortcut)

        if not shortcuts_to_create:
            return

        vbs_lines = ['Set WshShell = CreateObject("WScript.Shell")']
        for sc in shortcuts_to_create:
            vbs_lines.append(f'Set sc = WshShell.CreateShortcut("{sc}")')
            vbs_lines.append(f'sc.TargetPath = "{exe_path}"')
            vbs_lines.append(f'sc.WorkingDirectory = "{exe_path.parent}"')
            vbs_lines.append(f'sc.IconLocation = "{exe_path}, 0"')
            vbs_lines.append(f'sc.Description = "WebP Converter Pro"')
            vbs_lines.append('sc.Save')

        temp_dir = Path(os.environ.get("TEMP", "."))
        vbs_file = temp_dir / "create_webp_shortcuts.vbs"
        vbs_file.write_text("\n".join(vbs_lines), encoding="utf-8")

        subprocess.run(["cscript", "//Nologo", str(vbs_file)], shell=True, capture_output=True)

        if vbs_file.exists():
            vbs_file.unlink()

    except Exception:
        pass


if __name__ == "__main__":

    # Set explicit AppUserModelID so Windows taskbar uses custom app icon
    if sys.platform == "win32":
        try:
            myappid = "surajkumar.webpconverterpro.app.1.0"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        # Auto-create Desktop & Start Menu shortcuts
        ensure_shortcuts()

    app = WebPConverterApp()

    # Hide main window
    app.withdraw()

    # Show Splash Screen
    SplashScreen(app)

    # Start Application
    app.mainloop()