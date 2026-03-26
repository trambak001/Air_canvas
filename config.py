"""
config.py – Central configuration for the Air Canvas application.

Modify the values in :class:`CanvasConfig` to customise colours,
detection thresholds, line widths and window dimensions without
touching the main application logic.
"""


class CanvasConfig:
    """All tuneable parameters for Air Canvas.

    Attributes
    ----------
    WINDOW_TITLE : str
        Title shown in the OpenCV window.
    WINDOW_WIDTH : int
        Initial window width in pixels.
    WINDOW_HEIGHT : int
        Initial window height in pixels.
    MAX_NUM_HANDS : int
        Maximum number of hands to detect simultaneously.
    MIN_DETECTION_CONFIDENCE : float
        Minimum confidence score (0–1) for hand detection.
    MIN_TRACKING_CONFIDENCE : float
        Minimum confidence score (0–1) for hand tracking.
    PINCH_THRESHOLD : int
        Pixel distance between index-finger tip and thumb tip that
        activates the drawing gesture.
    DEFAULT_COLOR : tuple[int, int, int]
        Default BGR pen colour (green).
    DEFAULT_THICKNESS : int
        Default pen stroke width in pixels.
    ERASER_THICKNESS : int
        Eraser stroke width in pixels.
    COLORS : dict[str, tuple[int, int, int]]
        Named BGR colour palette used for the toolbar buttons.
    TASKBAR_WIDTH : int
        Width of the right-hand toolbar strip in pixels.
    BUTTON_SIZE : int
        Height/width of each toolbar button in pixels.
    BUTTON_SPACING : int
        Vertical gap between successive toolbar buttons in pixels.
    POINTER_RADIUS : int
        Radius of the finger-tip pointer circle drawn on the live feed.
    CANVAS_BLEND_ALPHA : float
        Opacity of the webcam frame when blended with the drawing canvas
        (0 = canvas only, 1 = camera only).
    """

    # ── Window ────────────────────────────────────────────────────────────
    WINDOW_TITLE: str = "Air Canvas"
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720

    # ── Hand detection ─────────────────────────────────────────────────────
    MAX_NUM_HANDS: int = 1
    MIN_DETECTION_CONFIDENCE: float = 0.7
    MIN_TRACKING_CONFIDENCE: float = 0.5

    # ── Drawing gesture ────────────────────────────────────────────────────
    PINCH_THRESHOLD: int = 30  # pixels

    # ── Pen & eraser ──────────────────────────────────────────────────────
    DEFAULT_COLOR: tuple = (0, 255, 0)  # BGR green
    DEFAULT_THICKNESS: int = 5
    ERASER_THICKNESS: int = 50

    # ── Colour palette (BGR) ──────────────────────────────────────────────
    COLORS: dict = {
        "red":    (0,   0,   255),
        "green":  (0,   255, 0),
        "blue":   (255, 0,   0),
        "yellow": (0,   255, 255),
        "purple": (128, 0,   128),
        "orange": (0,   165, 255),
    }

    # ── Toolbar layout ─────────────────────────────────────────────────────
    TASKBAR_WIDTH: int = 50
    BUTTON_SIZE: int = 50
    BUTTON_SPACING: int = 60

    # ── Display ────────────────────────────────────────────────────────────
    POINTER_RADIUS: int = 10
    CANVAS_BLEND_ALPHA: float = 0.5
