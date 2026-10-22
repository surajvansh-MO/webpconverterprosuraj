# theme.py
# WebP Converter Pro Design System Tokens

# =============================================================================
# Backgrounds
# =============================================================================
BG_WINDOW = "#090B0F"
BG_SIDEBAR = "#0E1117"
BG_MAIN_PANEL = "#11141B"
BG_SURFACE = "#161A23"        # Cards, inputs, chips, table row hover
BG_SURFACE_2 = "#1B202B"      # Extension tiles, count badges, icon tile bg
BG_TABLE_ROW_ALT = "#131720"  # Subtle alternating table row

# =============================================================================
# Borders & Dividers
# =============================================================================
BORDER_LINE = "#212736"
BORDER_LINE_STRONG = "#2B3345"

# =============================================================================
# Typography Colors
# =============================================================================
TEXT_PRIMARY = "#E9ECF3"
TEXT_MUTED = "#8C95A8"
TEXT_DIM = "#5B6478"

# =============================================================================
# Accent Palette (Vibrant Orange)
# =============================================================================
ACCENT = "#FF7A1A"
ACCENT_HOVER = "#E6680A"
ACCENT_TEXT = "#FF9040"
TEXT_ON_ACCENT = "#1A0F05"     # Dark, NOT white!
ACCENT_SOFT_FILL = "#30211B"
ACCENT_BORDER = "#703D1B"

# =============================================================================
# Semantic Colors
# =============================================================================
SUCCESS = "#34D399"
SUCCESS_SOFT_FILL = "#152B2A"
SUCCESS_BORDER = "#1F423C"

DANGER_TEXT = "#F2A0B0"
DANGER_BORDER = "#4A1D2E"
DANGER_SOFT_FILL = "#251219"
DANGER_HOVER_BORDER = "#F2A0B0"

# =============================================================================
# Radii
# =============================================================================
RADIUS_WINDOW = 0
RADIUS_MAIN_PANEL = 18
RADIUS_CARD = 14
RADIUS_BUTTON_PRIMARY = 12     # Primary Start Conversion button (48px)
RADIUS_BUTTON = 10             # Action buttons (Files, Folder, Clear All, etc.)
RADIUS_BUTTON_SM = 8           # Row actions (Convert, Remove)
RADIUS_PILL = 999              # Status pills, count badges, format chips
RADIUS_CHIP = 8                # Format pills, preset boxes
RADIUS_TILE = 10               # 40x40 extension tile
RADIUS_ICON_TILE = 18          # 76x76 dropzone icon tile
RADIUS_INPUT = 8               # Output directory entry

# =============================================================================
# Font Families & Definitions
# =============================================================================
FONT_FAMILY = "Segoe UI"
FONT_MONO = "Consolas"

# Typography Tuples: (family, size, weight)
FONT_APP_TITLE = (FONT_FAMILY, 16, "bold")
FONT_APP_SUBTITLE = (FONT_FAMILY, 11)
FONT_CARD_TITLE = (FONT_FAMILY, 11, "bold")      # Uppercase section label
FONT_VALUE_PILL = (FONT_FAMILY, 11, "bold")

FONT_PAGE_TITLE = (FONT_FAMILY, 22, "bold")
FONT_COUNT_BADGE = (FONT_FAMILY, 12, "bold")
FONT_STAT_LABEL = (FONT_FAMILY, 12)
FONT_STAT_VALUE = (FONT_FAMILY, 12, "bold")

FONT_DROPZONE_TITLE = (FONT_FAMILY, 22, "bold")
FONT_DROPZONE_SUBTITLE = (FONT_FAMILY, 13)
FONT_NEUTRAL_CHIP = (FONT_FAMILY, 11, "bold")

FONT_TABLE_HEADER = (FONT_FAMILY, 11, "bold")    # Dim uppercase
FONT_FILE_NAME = (FONT_FAMILY, 13, "bold")
FONT_FILE_SIZE = (FONT_FAMILY, 11)
FONT_OUTPUT_PATH = (FONT_MONO, 11)
FONT_FORMAT_BADGE = (FONT_FAMILY, 10, "bold")
FONT_STATUS_TEXT = (FONT_FAMILY, 12)
FONT_SAVINGS_PILL = (FONT_FAMILY, 10, "bold")

FONT_BUTTON_PRIMARY = (FONT_FAMILY, 14, "bold")
FONT_BUTTON = (FONT_FAMILY, 12, "bold")
FONT_BUTTON_SM = (FONT_FAMILY, 11, "bold")
FONT_BUTTON_GHOST = (FONT_FAMILY, 11, "bold")

FONT_PRESET_NUM = (FONT_FAMILY, 14, "bold")
FONT_PRESET_SUB = (FONT_FAMILY, 10)
FONT_PRESET_LABEL = (FONT_FAMILY, 11, "bold")
FONT_DIM = (FONT_FAMILY, 11)
FONT_HELPER = (FONT_FAMILY, 11)
FONT_TOGGLE_LABEL = (FONT_FAMILY, 12)
FONT_TOGGLE_HELPER = (FONT_FAMILY, 11)
FONT_FOOTER_NAME = (FONT_FAMILY, 12, "bold")
FONT_FOOTER_DEV = (FONT_FAMILY, 11)
FONT_FOOTER_EMAIL = (FONT_FAMILY, 11)
FONT_FOOTER_AVATAR = (FONT_FAMILY, 11, "bold")

# =============================================================================
# Layout Metrics
# =============================================================================
SIDEBAR_WIDTH = 350
SIDEBAR_PAD = 18
CARD_GAP = 14
ROW_HEIGHT = 64
TABLE_HEADER_HEIGHT = 34
PROGRESS_BAR_HEIGHT = 6
MIN_WINDOW_WIDTH = 980
MIN_WINDOW_HEIGHT = 640
INITIAL_WINDOW_WIDTH = 1200
INITIAL_WINDOW_HEIGHT = 800
