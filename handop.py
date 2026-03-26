"""
handop.py – Air Canvas: touchless drawing via hand gesture recognition.

Uses MediaPipe Hands to track the index-finger tip in real time.
Pinching the index finger and thumb together activates the pen; moving
them apart lifts the pen.  A toolbar on the right edge of the window
lets you pick colours, switch to the eraser, clear the canvas, or exit.

Usage
-----
    python handop.py

Controls
--------
    Pinch gesture  – draw / write on the canvas
    Open hand      – move cursor without drawing
    Toolbar hover  – select colour, eraser, clear, or exit
    Q key          – quit the application
"""

import sys

import cv2
import mediapipe as mp
import numpy as np

from config import CanvasConfig


# ── MediaPipe initialisation ───────────────────────────────────────────────────

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


# ── Helper functions ───────────────────────────────────────────────────────────

def build_buttons(frame_width, cfg):
    """Compute pixel bounding boxes for every toolbar button.

    The toolbar is a vertical strip on the *right* edge of the frame.
    Each entry maps a button name to ``(x1, y1, x2, y2)``.

    Parameters
    ----------
    frame_width : int
        Width of the video frame in pixels.
    cfg : CanvasConfig
        Application configuration instance.

    Returns
    -------
    dict
        Button name -> (left, top, right, bottom) bounding box.
    """
    tw = cfg.TASKBAR_WIDTH
    bs = cfg.BUTTON_SIZE
    sp = cfg.BUTTON_SPACING
    w = frame_width

    button_names = ["red", "green", "blue", "yellow", "purple", "orange", "eraser", "clear", "exit"]
    buttons = {}
    for i, name in enumerate(button_names):
        x1 = w - tw
        y1 = 10 + i * sp
        x2 = w - 10
        y2 = 10 + bs + i * sp
        buttons[name] = (x1, y1, x2, y2)
    return buttons


def create_canvas(frame):
    """Return a blank white canvas with the same shape as *frame*.

    Parameters
    ----------
    frame : numpy.ndarray
        Reference BGR video frame used to determine canvas dimensions.

    Returns
    -------
    numpy.ndarray
        White (255, 255, 255) canvas array matching *frame* shape.
    """
    return np.ones_like(frame, dtype=np.uint8) * 255


def is_pinching(x, y, thumb_x, thumb_y, threshold):
    """Determine whether the index finger and thumb form a pinch gesture.

    Parameters
    ----------
    x, y : int
        Pixel coordinates of the index-finger tip.
    thumb_x, thumb_y : int
        Pixel coordinates of the thumb tip.
    threshold : int
        Maximum pixel distance that counts as a pinch.

    Returns
    -------
    bool
        ``True`` when the two tips are within *threshold* pixels.
    """
    return abs(x - thumb_x) < threshold and abs(y - thumb_y) < threshold


def draw_toolbar(frame, buttons, selected_button, cfg):
    """Render colour swatches and action buttons onto *frame* in-place.

    Parameters
    ----------
    frame : numpy.ndarray
        BGR image to draw on (modified in-place).
    buttons : dict
        Button bounding boxes returned by :func:`build_buttons`.
    selected_button : str or None
        Name of the currently active button (receives a white highlight).
    cfg : CanvasConfig
        Application configuration instance (used for colour values).
    """
    for button, (x1, y1, x2, y2) in buttons.items():
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        # Highlight the active button with a white border
        if button == selected_button:
            cv2.rectangle(frame, (x1 - 5, y1 - 5), (x2 + 5, y2 + 5), (255, 255, 255), 3)

        if button in cfg.COLORS:
            # Draw a filled circle in the button's colour
            cv2.circle(frame, (cx, cy), 20, cfg.COLORS[button], -1)
        elif button == "eraser":
            cv2.rectangle(frame, (x1 + 10, y1 + 10), (x2 - 10, y2 - 10), (0, 0, 0), -1)
        elif button == "clear":
            cv2.putText(frame, "C", (cx - 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        elif button == "exit":
            cv2.putText(frame, "X", (cx - 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


def handle_button_click(button, canvas, frame, cfg):
    """Apply the side-effect of clicking a toolbar *button*.

    Parameters
    ----------
    button : str
        Name of the button that was activated.
    canvas : numpy.ndarray
        Current drawing canvas (may be replaced on "clear").
    frame : numpy.ndarray
        Current video frame (used to size a fresh canvas).
    cfg : CanvasConfig
        Application configuration instance.

    Returns
    -------
    tuple
        Updated ``(drawing_color, thickness, canvas)`` triple.
        If *button* is "exit" the process is terminated.
    """
    drawing_color = cfg.DEFAULT_COLOR
    thickness = cfg.DEFAULT_THICKNESS

    if button in cfg.COLORS:
        drawing_color = cfg.COLORS[button]
        thickness = cfg.DEFAULT_THICKNESS
    elif button == "eraser":
        drawing_color = (0, 0, 0)  # Black erases on a white canvas
        thickness = cfg.ERASER_THICKNESS
    elif button == "clear":
        canvas = create_canvas(frame)
    elif button == "exit":
        sys.exit(0)

    return drawing_color, thickness, canvas


def process_landmarks(
    hand_landmarks,
    frame_width,
    frame_height,
    canvas,
    prev_x,
    prev_y,
    drawing,
    drawing_color,
    thickness,
    selected_button,
    buttons,
    cfg,
    frame,
):
    """Extract finger positions, detect gestures, and update canvas/state.

    Parameters
    ----------
    hand_landmarks : mediapipe landmark list
        Detected hand landmarks from MediaPipe.
    frame_width, frame_height : int
        Dimensions of the current video frame in pixels.
    canvas : numpy.ndarray
        Current drawing canvas (may be mutated by draw strokes or clear).
    prev_x, prev_y : int or None
        Previous index-finger tip position for continuous line drawing.
    drawing : bool
        Whether the pen was active in the previous frame.
    drawing_color : tuple
        Current BGR pen colour.
    thickness : int
        Current pen/eraser stroke width.
    selected_button : str or None
        Currently selected toolbar button name.
    buttons : dict
        Toolbar button bounding boxes.
    cfg : CanvasConfig
        Application configuration instance.
    frame : numpy.ndarray
        Current video frame (used when a "clear" resets the canvas).

    Returns
    -------
    tuple
        ``(prev_x, prev_y, drawing, drawing_color, thickness,
           selected_button, canvas)``
    """
    # Resolve index-finger tip and thumb tip to pixel coordinates
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

    x = int(index_tip.x * frame_width)
    y = int(index_tip.y * frame_height)
    thumb_x = int(thumb_tip.x * frame_width)
    thumb_y = int(thumb_tip.y * frame_height)

    # Detect pinch gesture -> pen active
    drawing = is_pinching(x, y, thumb_x, thumb_y, cfg.PINCH_THRESHOLD)

    # Draw a continuous stroke on the canvas when the pen is active
    if prev_x is not None and prev_y is not None and drawing:
        cv2.line(canvas, (prev_x, prev_y), (x, y), drawing_color, thickness)

    # Check whether the finger is hovering over the toolbar
    if x > frame_width - cfg.TASKBAR_WIDTH:
        for button, (x1, y1, x2, y2) in buttons.items():
            if x1 < x < x2 and y1 < y < y2:
                selected_button = button
                drawing_color, thickness, canvas = handle_button_click(
                    button, canvas, frame, cfg
                )
                prev_x, prev_y = None, None  # Lift pen when entering toolbar
    else:
        # Only update previous position when outside the toolbar
        prev_x, prev_y = x, y

    return prev_x, prev_y, drawing, drawing_color, thickness, selected_button, canvas


# ── Main application loop ──────────────────────────────────────────────────────

def main():
    """Entry point: open webcam, run detection loop, clean up on exit.

    The function initialises the webcam, the MediaPipe Hands detector,
    and an OpenCV window, then processes frames until the user presses
    **Q** or activates the exit button in the toolbar.

    Raises
    ------
    RuntimeError
        If the webcam cannot be opened.
    """
    cfg = CanvasConfig()

    # Initialise MediaPipe Hands detector
    hands = mp_hands.Hands(
        max_num_hands=cfg.MAX_NUM_HANDS,
        min_detection_confidence=cfg.MIN_DETECTION_CONFIDENCE,
        min_tracking_confidence=cfg.MIN_TRACKING_CONFIDENCE,
    )

    # Open the default webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError(
            "Could not open webcam. Make sure a camera is connected and not "
            "in use by another application."
        )

    # Set up the display window
    cv2.namedWindow(cfg.WINDOW_TITLE, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(cfg.WINDOW_TITLE, cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT)

    # State variables
    canvas = None
    buttons = {}
    prev_x = None
    prev_y = None
    drawing = False
    drawing_color = cfg.DEFAULT_COLOR
    thickness = cfg.DEFAULT_THICKNESS
    selected_button = None

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Warning: failed to read frame from webcam.")
                break

            # Mirror the frame for a natural selfie-view experience
            frame = cv2.flip(frame, 1)

            # Initialise canvas and button layout on the first valid frame
            h, w, _ = frame.shape
            if canvas is None:
                canvas = create_canvas(frame)
            if not buttons:
                buttons = build_buttons(w, cfg)

            # Run hand landmark detection (MediaPipe expects RGB input)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    (
                        prev_x, prev_y,
                        drawing,
                        drawing_color,
                        thickness,
                        selected_button,
                        canvas,
                    ) = process_landmarks(
                        hand_landmarks,
                        w, h,
                        canvas,
                        prev_x, prev_y,
                        drawing,
                        drawing_color,
                        thickness,
                        selected_button,
                        buttons,
                        cfg,
                        frame,
                    )

                    # Draw a pointer circle at the index-finger tip location
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    px = int(index_tip.x * w)
                    py = int(index_tip.y * h)
                    cv2.circle(frame, (px, py), cfg.POINTER_RADIUS, (255, 0, 0), -1)
            else:
                # No hand detected - lift the pen to avoid ghost strokes
                drawing = False

            # Blend the live camera feed with the drawing canvas
            frame = cv2.addWeighted(frame, cfg.CANVAS_BLEND_ALPHA, canvas, cfg.CANVAS_BLEND_ALPHA, 0)

            # Render toolbar on top of the blended frame
            draw_toolbar(frame, buttons, selected_button, cfg)

            cv2.imshow(cfg.WINDOW_TITLE, frame)

            # Allow the user to quit with the Q key
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        # Graceful exit on Ctrl-C
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        hands.close()


if __name__ == "__main__":
    main()
