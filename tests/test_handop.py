"""
tests/test_handop.py – Unit tests for Air Canvas helper functions.

Run with:
    pytest tests/
"""

import sys
import os

import numpy as np
import pytest

# Ensure the project root is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import CanvasConfig
from handop import (
    build_buttons,
    create_canvas,
    draw_toolbar,
    handle_button_click,
    is_pinching,
)


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture
def cfg():
    """Return a default CanvasConfig instance."""
    return CanvasConfig()


@pytest.fixture
def dummy_frame():
    """Return a small (100 x 200) blank BGR frame for testing."""
    return np.zeros((100, 200, 3), dtype=np.uint8)


# ── is_pinching ────────────────────────────────────────────────────────────────

class TestIsPinching:
    """Tests for the pinch-gesture detector."""

    def test_returns_true_when_tips_overlap(self):
        """Fingers at identical positions should register as a pinch."""
        assert is_pinching(50, 50, 50, 50, threshold=30) is True

    def test_returns_true_within_threshold(self):
        """Tips closer than the threshold should register as a pinch."""
        assert is_pinching(50, 50, 60, 60, threshold=30) is True

    def test_returns_false_beyond_threshold(self):
        """Tips further apart than the threshold must NOT register as a pinch."""
        assert is_pinching(0, 0, 100, 100, threshold=30) is False

    def test_threshold_boundary_exclusive(self):
        """A distance equal to the threshold is NOT a pinch (strict < comparison)."""
        # abs(0 - 30) == 30, which is not < 30
        assert is_pinching(0, 0, 30, 0, threshold=30) is False

    def test_threshold_boundary_inclusive(self):
        """A distance one below the threshold IS a pinch."""
        assert is_pinching(0, 0, 29, 0, threshold=30) is True

    def test_horizontal_separation_only(self):
        """Large horizontal gap beyond threshold -> not pinching."""
        assert is_pinching(0, 50, 50, 50, threshold=30) is False

    def test_vertical_separation_only(self):
        """Large vertical gap beyond threshold -> not pinching."""
        assert is_pinching(50, 0, 50, 50, threshold=30) is False


# ── create_canvas ──────────────────────────────────────────────────────────────

class TestCreateCanvas:
    """Tests for the blank canvas factory."""

    def test_returns_white_canvas(self, dummy_frame):
        """All pixels should be 255 (white)."""
        canvas = create_canvas(dummy_frame)
        assert np.all(canvas == 255)

    def test_canvas_matches_frame_shape(self, dummy_frame):
        """Canvas shape must match the reference frame."""
        canvas = create_canvas(dummy_frame)
        assert canvas.shape == dummy_frame.shape

    def test_canvas_dtype_uint8(self, dummy_frame):
        """Canvas dtype must be uint8 for OpenCV compatibility."""
        canvas = create_canvas(dummy_frame)
        assert canvas.dtype == np.uint8

    def test_canvas_is_independent_copy(self, dummy_frame):
        """Modifying the canvas must not affect the source frame."""
        canvas = create_canvas(dummy_frame)
        canvas[0, 0] = 0
        # dummy_frame was all zeros to begin with; still all zeros
        assert dummy_frame[0, 0, 0] == 0  # original frame unchanged by canvas write


# ── build_buttons ──────────────────────────────────────────────────────────────

class TestBuildButtons:
    """Tests for the toolbar button builder."""

    EXPECTED_BUTTONS = ["red", "green", "blue", "yellow", "purple", "orange", "eraser", "clear", "exit"]

    def test_returns_all_buttons(self, cfg):
        """All nine buttons must be present."""
        buttons = build_buttons(640, cfg)
        assert set(buttons.keys()) == set(self.EXPECTED_BUTTONS)

    def test_button_count(self, cfg):
        """Exactly nine buttons must be returned."""
        buttons = build_buttons(640, cfg)
        assert len(buttons) == 9

    def test_each_button_has_four_coordinates(self, cfg):
        """Each bounding box must be a 4-tuple of integers."""
        buttons = build_buttons(640, cfg)
        for name, box in buttons.items():
            assert len(box) == 4, f"Button '{name}' box has {len(box)} values, expected 4"

    def test_buttons_within_frame_width(self, cfg):
        """All button boxes must be inside the frame width."""
        frame_width = 640
        buttons = build_buttons(frame_width, cfg)
        for name, (x1, y1, x2, y2) in buttons.items():
            assert x2 <= frame_width, f"Button '{name}' exceeds frame width"

    def test_buttons_in_taskbar_area(self, cfg):
        """Button left edge must be inside the right taskbar strip."""
        frame_width = 640
        buttons = build_buttons(frame_width, cfg)
        for name, (x1, y1, x2, y2) in buttons.items():
            assert x1 >= frame_width - cfg.TASKBAR_WIDTH, (
                f"Button '{name}' left edge ({x1}) is outside the taskbar"
            )

    def test_vertical_ordering(self, cfg):
        """Buttons must appear top-to-bottom in the listed order."""
        buttons = build_buttons(640, cfg)
        tops = [buttons[name][1] for name in self.EXPECTED_BUTTONS]
        assert tops == sorted(tops), "Buttons are not in top-to-bottom order"

    def test_button_height_equals_button_size(self, cfg):
        """Each button's height must equal BUTTON_SIZE."""
        buttons = build_buttons(640, cfg)
        for name, (x1, y1, x2, y2) in buttons.items():
            assert (y2 - y1) == cfg.BUTTON_SIZE, (
                f"Button '{name}' height {y2 - y1} != BUTTON_SIZE {cfg.BUTTON_SIZE}"
            )


# ── handle_button_click ────────────────────────────────────────────────────────

class TestHandleButtonClick:
    """Tests for toolbar button click handler."""

    def test_colour_buttons_return_correct_bgr(self, cfg, dummy_frame):
        """Each colour button should return the matching BGR tuple."""
        canvas = create_canvas(dummy_frame)
        for color_name, expected_bgr in cfg.COLORS.items():
            color, thickness, new_canvas = handle_button_click(color_name, canvas, dummy_frame, cfg)
            assert color == expected_bgr, f"Color '{color_name}': got {color}, expected {expected_bgr}"

    def test_colour_buttons_return_default_thickness(self, cfg, dummy_frame):
        """Colour buttons must not change the stroke thickness."""
        canvas = create_canvas(dummy_frame)
        for color_name in cfg.COLORS:
            _, thickness, _ = handle_button_click(color_name, canvas, dummy_frame, cfg)
            assert thickness == cfg.DEFAULT_THICKNESS

    def test_eraser_returns_black(self, cfg, dummy_frame):
        """Eraser mode must set the drawing colour to black (0, 0, 0)."""
        canvas = create_canvas(dummy_frame)
        color, _, _ = handle_button_click("eraser", canvas, dummy_frame, cfg)
        assert color == (0, 0, 0)

    def test_eraser_returns_eraser_thickness(self, cfg, dummy_frame):
        """Eraser mode must set thickness to ERASER_THICKNESS."""
        canvas = create_canvas(dummy_frame)
        _, thickness, _ = handle_button_click("eraser", canvas, dummy_frame, cfg)
        assert thickness == cfg.ERASER_THICKNESS

    def test_clear_resets_canvas_to_white(self, cfg, dummy_frame):
        """The 'clear' button must return a fresh all-white canvas."""
        canvas = create_canvas(dummy_frame)
        # Draw something on the canvas first
        canvas[10, 10] = [0, 0, 0]
        _, _, new_canvas = handle_button_click("clear", canvas, dummy_frame, cfg)
        assert np.all(new_canvas == 255), "Canvas was not fully cleared to white"

    def test_clear_returns_canvas_with_correct_shape(self, cfg, dummy_frame):
        """The cleared canvas must match the frame dimensions."""
        canvas = create_canvas(dummy_frame)
        _, _, new_canvas = handle_button_click("clear", canvas, dummy_frame, cfg)
        assert new_canvas.shape == dummy_frame.shape

    def test_exit_raises_system_exit(self, cfg, dummy_frame):
        """The 'exit' button must call sys.exit()."""
        canvas = create_canvas(dummy_frame)
        with pytest.raises(SystemExit):
            handle_button_click("exit", canvas, dummy_frame, cfg)


# ── draw_toolbar ───────────────────────────────────────────────────────────────

class TestDrawToolbar:
    """Tests for the toolbar rendering function."""

    def test_does_not_raise(self, cfg):
        """draw_toolbar must complete without raising on a valid frame."""
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        buttons = build_buttons(1280, cfg)
        draw_toolbar(frame, buttons, None, cfg)  # Should not raise

    def test_selected_button_modifies_frame(self, cfg):
        """A selected button should produce a different frame than no selection."""
        frame_none = np.zeros((720, 1280, 3), dtype=np.uint8)
        frame_sel = np.zeros((720, 1280, 3), dtype=np.uint8)
        buttons = build_buttons(1280, cfg)

        draw_toolbar(frame_none, buttons, None, cfg)
        draw_toolbar(frame_sel, buttons, "red", cfg)

        # The frames must differ because the highlight border is drawn
        assert not np.array_equal(frame_none, frame_sel)

    def test_frame_modified_in_place(self, cfg):
        """draw_toolbar must modify the frame in-place (no copy returned)."""
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        original_id = id(frame)
        buttons = build_buttons(1280, cfg)
        draw_toolbar(frame, buttons, None, cfg)
        # Frame identity unchanged; pixels should differ from all-zero
        assert id(frame) == original_id
        assert np.any(frame != 0)


# ── CanvasConfig ───────────────────────────────────────────────────────────────

class TestCanvasConfig:
    """Sanity-check the default configuration values."""

    def test_default_color_is_tuple_of_three(self, cfg):
        assert len(cfg.DEFAULT_COLOR) == 3

    def test_default_thickness_positive(self, cfg):
        assert cfg.DEFAULT_THICKNESS > 0

    def test_eraser_thickness_greater_than_default(self, cfg):
        assert cfg.ERASER_THICKNESS > cfg.DEFAULT_THICKNESS

    def test_pinch_threshold_positive(self, cfg):
        assert cfg.PINCH_THRESHOLD > 0

    def test_colors_dict_not_empty(self, cfg):
        assert len(cfg.COLORS) > 0

    def test_all_colors_are_bgr_tuples(self, cfg):
        for name, color in cfg.COLORS.items():
            assert len(color) == 3, f"Color '{name}' must be a 3-tuple"
            assert all(0 <= c <= 255 for c in color), f"Color '{name}' values out of [0, 255]"

    def test_detection_confidence_in_range(self, cfg):
        assert 0.0 < cfg.MIN_DETECTION_CONFIDENCE <= 1.0

    def test_tracking_confidence_in_range(self, cfg):
        assert 0.0 < cfg.MIN_TRACKING_CONFIDENCE <= 1.0

    def test_canvas_blend_alpha_in_range(self, cfg):
        assert 0.0 <= cfg.CANVAS_BLEND_ALPHA <= 1.0
