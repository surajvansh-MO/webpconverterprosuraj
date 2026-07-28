from pathlib import Path
from PIL import Image, ImageFile

# Register AVIF support
import pillow_avif

# Handle truncated images safely
ImageFile.LOAD_TRUNCATED_IMAGES = True


SUPPORTED_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
    ".tif",
    ".gif",
    ".avif",
    ".ico",
}


def convert_image(image_path, output_folder=None, quality=80, lossless=False):
    """
    Convert a single image to WebP with security checks and memory safety.

    Returns:
        (True, output_path) on success
        (False, error_message) on failure
    """

    try:

        image_path = Path(image_path).resolve()

        if not image_path.is_file():
            return False, "File does not exist or is unreadable"

        if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            return False, "Unsupported file type"

        if output_folder:

            output_folder = Path(output_folder).resolve()
            output_folder.mkdir(parents=True, exist_ok=True)

            output_file = output_folder / f"{image_path.stem}.webp"

        else:

            output_file = image_path.with_suffix(".webp")

        save_kwargs = {
            "quality": int(quality),
            "method": 6,
            "lossless": bool(lossless)
        }

        # Memory safe opening with context manager to prevent file locks & leaks
        with Image.open(image_path) as img:

            if getattr(img, "is_animated", False):
                save_kwargs["save_all"] = True

            # Preserve transparency where possible
            if img.mode not in ("RGB", "RGBA"):
                converted_img = img.convert("RGBA")
                converted_img.save(
                    output_file,
                    "WEBP",
                    **save_kwargs
                )
                converted_img.close()
            else:
                img.save(
                    output_file,
                    "WEBP",
                    **save_kwargs
                )

        return True, output_file

    except Image.DecompressionBombError:

        return False, "Image resolution exceeds safety limits (decompression bomb protection)"

    except Exception as e:

        return False, str(e)