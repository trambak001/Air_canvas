# Air Canvas 🖐️🎨

> Touchless drawing powered by computer vision — draw in the air using only hand gestures and a webcam.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)](https://opencv.org)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)](https://mediapipe.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Project Overview

**Air Canvas** transforms your webcam and hand gestures into an interactive virtual whiteboard.
Pinch your index finger and thumb together to start drawing; release to lift the pen.
A toolbar on the right side of the window lets you pick colours, erase, clear the canvas, or quit — all without touching a keyboard or mouse.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Pinch-to-draw** | Natural gesture — pinch to draw, release to stop |
| **Real-time tracking** | MediaPipe detects hand landmarks at 30+ FPS |
| **6 colour palette** | Red, green, blue, yellow, purple, orange |
| **Eraser mode** | Wide eraser stroke for quick corrections |
| **Clear canvas** | One-gesture full reset |
| **Configurable** | All parameters in a single `config.py` |

---

## 🏗️ Project Architecture

```
Air_canvas/
├── handop.py          # Main application entry point
├── config.py          # CanvasConfig – all tuneable parameters
├── requirements.txt   # Pinned dependencies
├── setup.py           # Package distribution config
├── tests/
│   ├── __init__.py
│   └── test_handop.py # Unit tests (pytest)
└── demo/
    ├── README.md       # Usage documentation
    └── screenshots/    # Place your own snapshots here
```

### Key modules

| File | Responsibility |
|------|----------------|
| `handop.py` | Webcam loop, landmark processing, canvas rendering |
| `config.py` | `CanvasConfig` dataclass — one place to tweak everything |
| `tests/test_handop.py` | Unit tests for pure-Python helper functions |

### Data flow

```
Webcam frame
    │
    ▼
cv2.flip()          ← mirror for selfie view
    │
    ▼
MediaPipe Hands     ← landmark detection (RGB frame)
    │
    ▼
process_landmarks() ← pinch detection, stroke drawing, toolbar handling
    │
    ▼
cv2.addWeighted()   ← blend camera feed + drawing canvas
    │
    ▼
draw_toolbar()      ← overlay colour buttons
    │
    ▼
cv2.imshow()        ← display result
```

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Webcam (built-in or USB)
- pip package manager

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/trambak001/Air_canvas.git
cd Air_canvas

# 2. (Recommended) create a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

```bash
python handop.py
```

### Controls

| Action | How |
|--------|-----|
| **Draw** | Pinch index finger and thumb together |
| **Lift pen** | Open your hand (spread fingers) |
| **Change colour** | Hover index finger over a colour button in the right toolbar |
| **Erase** | Hover over the black square (eraser) button |
| **Clear canvas** | Hover over the **C** button |
| **Quit** | Press **Q** on the keyboard, or hover over **X** button |

---

## ⚙️ Configuration

All tuneable parameters live in `config.py`:

```python
class CanvasConfig:
    MIN_DETECTION_CONFIDENCE = 0.7   # raise for less false positives
    PINCH_THRESHOLD = 30             # pixels; lower = tighter pinch needed
    DEFAULT_THICKNESS = 5            # pen stroke width
    ERASER_THICKNESS = 50            # eraser width
    CANVAS_BLEND_ALPHA = 0.5         # 0=canvas only, 1=camera only
    # … see config.py for the full list
```

No code changes needed — edit `config.py` and restart.

---

## 📊 Performance

| Metric | Typical value |
|--------|--------------|
| Frame rate | 25–35 FPS (720p, modern laptop) |
| Detection latency | < 10 ms per frame |
| CPU usage | ~30 % single core |
| Memory | ~200 MB resident |

*Results vary by hardware and lighting conditions.*

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

Tests cover gesture detection, canvas creation, toolbar layout, button
click handling, and configuration validation — no webcam required.

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| *"Could not open webcam"* | Check another app isn't using the camera; try `cv2.VideoCapture(1)` |
| Hand not detected | Improve lighting; lower `MIN_DETECTION_CONFIDENCE` in `config.py` |
| Jittery lines | Raise `PINCH_THRESHOLD` slightly so small movements are ignored |
| Slow frame rate | Close other GPU-intensive apps; reduce window resolution |
| Eraser too small | Increase `ERASER_THICKNESS` in `config.py` |

---

## 🔧 Dependencies

| Library | Version | Purpose |
|---------|---------|---------|
| **opencv-python** | >=4.8.0 | Frame capture, drawing, display |
| **mediapipe** | >=0.10.9,<0.11 | Hand landmark detection |
| **numpy** | >=1.24.0 | Canvas array operations |

---

## 📈 Advanced Usage

### Change the default pen colour

```python
# config.py
DEFAULT_COLOR = (255, 0, 0)   # BGR blue
```

### Add a new toolbar colour

```python
# config.py  – add to the COLORS dict
COLORS = {
    ...,
    "cyan": (255, 255, 0),
}
```

The new button appears automatically; no other changes needed.

### Run as an installed command

```bash
pip install -e .
air-canvas        # launches handop.main()
```

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.  In short:

1. Fork → branch → code → test → PR.
2. Follow PEP 8 and add docstrings to every new function.
3. All `pytest tests/` tests must pass.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 📧 Contact

**Developer**: [@trambak001](https://github.com/trambak001)  
**Repository**: [Air_canvas](https://github.com/trambak001/Air_canvas)  
**Issues**: [Report a bug or request a feature](https://github.com/trambak001/Air_canvas/issues)

---

## 🌟 Acknowledgments

- **OpenCV** community for comprehensive computer vision tools
- **MediaPipe** team at Google for accessible hand-tracking solutions
- All contributors and users of this project

---

### ⭐ Star this repo if you found it helpful!
