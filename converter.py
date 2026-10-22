from pathlib import Path
import io
from PIL import Image, ImageOps, ImageSequence

# Register AVIF support
try:
    import pillow_avif
except ImportError:
    pass

# Register HEIF / HEIC support
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

# Initialize all built-in Pillow plugin openers
try:
    Image.init()
except Exception:
    pass


# =========================================================================
# Categorized Supported Extensions
# =========================================================================

# Scalable Vector Graphics & Vector Formats
VECTOR_EXTENSIONS = {
    ".svg", ".svgz", ".emf", ".wmf", ".eps", ".ps", ".cgm", ".ai",
    ".sk", ".sk1", ".cdr", ".vsd", ".vsdx", ".pes", ".pdf"
}

# Modern & High-Efficiency Web / Mobile Formats
MODERN_EXTENSIONS = {
    ".webp", ".avif", ".avis", ".heic", ".heif", ".hif", ".heics", ".heifs"
}

# Standard Web & Raster Formats
STANDARD_EXTENSIONS = {
    ".png", ".apng",
    ".jpg", ".jpeg", ".jpe", ".jfif", ".jif", ".jfi",
    ".bmp", ".dib",
    ".gif",
    ".tiff", ".tif",
    ".ico", ".cur",
}

# Adobe Design & Texture Formats
DESIGN_EXTENSIONS = {
    ".psd", ".psb",
    ".tga", ".icb", ".vda", ".vst",
    ".dds", ".blp", ".qoi", ".odg",
}

# Professional Digital Camera RAW Formats
RAW_EXTENSIONS = {
    ".raw", ".raf", ".cr2", ".cr3", ".arw", ".crw", ".dcr", ".dng",
    ".mrw", ".nef", ".orf", ".pef", ".3fr", ".dcs", ".drf", ".erf",
    ".iiq", ".k25", ".kdc", ".mef", ".mos", ".nrw", ".ptx", ".rw2",
    ".sr2", ".srf", ".srw", ".x3f"
}

# Specialized, Scientific & Miscellaneous Image Formats
SPECIALIZED_EXTENSIONS = {
    ".jp2", ".j2k", ".jpf", ".jpx", ".jpc",
    ".ppm", ".pgm", ".pbm", ".pnm",
    ".pcx", ".dcx",
    ".icns",
    ".hdr", ".pic",
    ".sgi", ".rgb", ".rgba", ".bw",
    ".xbm", ".xpm",
    ".fits", ".fit", ".fts",
    ".im", ".msp", ".palm", ".pcd",
    ".fli", ".flc",
    ".dcm", ".dpx", ".exr", ".fax", ".hrz",
    ".mng", ".mtv", ".pfm", ".picon", ".pict", ".pix",
    ".pwp", ".rla", ".sct", ".sfw", ".sun", ".art", ".wpg",
}

# Master Comprehensive Supported Set (100+ formats)
SUPPORTED_EXTENSIONS = (
    VECTOR_EXTENSIONS
    | MODERN_EXTENSIONS
    | STANDARD_EXTENSIONS
    | DESIGN_EXTENSIONS
    | RAW_EXTENSIONS
    | SPECIALIZED_EXTENSIONS
)


# =========================================================================
# Image Loader Pipeline
# =========================================================================

def load_image(image_path):
    """
    Load an image from disk using the best specialized engine:
      - SVG / SVGZ via resvg-py (pure Rust SVG rasterizer)
      - Camera RAW via rawpy (LibRaw engine)
      - PSD / PSB via psd-tools
      - PDF / AI via pypdfium2 (PDFium engine)
      - Medical DICOM (.dcm) via pydicom
      - HEIC / HEIF / AVIF / WebP / Standard via Pillow + pillow-heif
      - ImageIO fallback for specialist scientific/graphics formats
    """
    path = Path(image_path)
    ext = path.suffix.lower()

    # 1. SVG & Compressed SVGZ (resvg-py)
    if ext in {".svg", ".svgz"}:
        try:
            import resvg_py
            png_bytes = resvg_py.svg_to_bytes(svg_path=str(path))
            return Image.open(io.BytesIO(png_bytes))
        except Exception as e:
            raise ValueError(f"SVG render error: {e}")

    # 2. Camera RAW formats (rawpy)
    if ext in RAW_EXTENSIONS:
        try:
            import rawpy
            with rawpy.imread(str(path)) as raw:
                rgb = raw.postprocess(use_camera_wb=True)
                return Image.fromarray(rgb)
        except Exception:
            # Fall back to Pillow if rawpy fails (e.g. DNG files)
            pass

    # 3. Adobe Photoshop (.psd, .psb) (psd-tools)
    if ext in {".psd", ".psb"}:
        try:
            from psd_tools import PSDImage
            psd = PSDImage.open(str(path))
            composite = psd.composite()
            if composite:
                return composite
        except Exception:
            pass

    # 4. PDF / AI Document rendering (first page) (pypdfium2)
    if ext in {".pdf", ".ai"}:
        try:
            import pypdfium2
            pdf = pypdfium2.PdfDocument(str(path))
            if len(pdf) > 0:
                # 2.0x scale provides crisp 144 DPI rasterization
                return pdf[0].render(scale=2.0).to_pil()
        except Exception:
            pass

    # 5. Medical DICOM (.dcm) (pydicom)
    if ext == ".dcm":
        try:
            import pydicom
            import numpy as np
            ds = pydicom.dcmread(str(path))
            arr = ds.pixel_array
            if arr.dtype != np.uint8:
                arr = (arr - arr.min()) / (arr.max() - arr.min() + 1e-8) * 255.0
                arr = arr.astype(np.uint8)
            return Image.fromarray(arr)
        except Exception:
            pass

    # 6. Standard Pillow opener (covers PNG, JPG, GIF, WebP, AVIF, HEIC, TIFF, BMP, ICO, TGA, DDS, WMF, EMF, etc.)
    try:
        img = Image.open(path)
        # Correct orientation based on EXIF camera metadata
        try:
            img = ImageOps.exif_transpose(img)
        except Exception:
            pass
        return img
    except Exception:
        pass

    # 7. ImageIO fallback (for EXR, DPX, HRZ, MTV, PIX, etc.)
    try:
        import imageio.v3 as iio
        arr = iio.imread(str(path))
        return Image.fromarray(arr)
    except Exception as e:
        raise ValueError(f"Cannot decode image '{path.name}': {e}")


# =========================================================================
# Image Conversion
# =========================================================================

def convert_image(image_path, output_folder=None, quality=80, lossless=False):
    """
    Convert a single image to WebP.

    Returns:
        (True, output_path) on success
        (False, error_message) on failure
    """
    try:
        image_path = Path(image_path)

        if not image_path.exists():
            return False, "File does not exist"

        img = load_image(image_path)

        if output_folder:
            output_folder = Path(output_folder)
            output_folder.mkdir(parents=True, exist_ok=True)
            output_file = output_folder / f"{image_path.stem}.webp"
        else:
            output_file = image_path.with_suffix(".webp")

        save_kwargs = {
            "quality": int(quality),
            "method": 6,
            "lossless": bool(lossless)
        }

        # Multi-frame animation support (GIF, APNG, animated WebP)
        is_animated = getattr(img, "is_animated", False) and getattr(img, "n_frames", 1) > 1

        if is_animated:
            extracted_frames = []
            durations = []
            for frame in ImageSequence.Iterator(img):
                f = frame.convert("RGBA")
                extracted_frames.append(f)
                durations.append(frame.info.get("duration", 100))

            extracted_frames[0].save(
                output_file,
                "WEBP",
                save_all=True,
                append_images=extracted_frames[1:],
                duration=durations,
                loop=img.info.get("loop", 0),
                **save_kwargs
            )
        else:
            # Preserve transparency where present, otherwise convert to RGB
            if img.mode not in ("RGB", "RGBA"):
                if (
                    img.mode in ("RGBA", "LA", "PA")
                    or "transparency" in img.info
                    or "A" in img.mode
                ):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")

            img.save(
                output_file,
                "WEBP",
                **save_kwargs
            )

        return True, output_file

    except Exception as e:
        return False, str(e)