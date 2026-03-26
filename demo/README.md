# Demo – Air Canvas

This folder contains example screenshots and usage documentation for
the Air Canvas application.

## Screenshots

Place your own screenshots under `screenshots/` after running the app.

Typical session flow:

1. Launch the app: `python handop.py`
2. Point your index finger at the camera.
3. Pinch your index finger and thumb together to start drawing.
4. Hover your finger over the right-hand toolbar to change colour,
   activate the eraser, clear the canvas, or quit.

## Features demonstrated

| Feature | Description |
|---------|-------------|
| Real-time detection | MediaPipe processes each frame in < 10 ms on modern hardware |
| Colour palette | 6 colours: red, green, blue, yellow, purple, orange |
| Eraser mode | Thick black stroke replaces ink on the white canvas |
| Clear canvas | Instantly resets the drawing surface |
| Pinch-to-draw | Natural gesture – no keyboard or mouse needed |

## Performance tips

- Good lighting improves detection accuracy.
- Keep your hand within 60 cm of the camera for best results.
- Adjust `MIN_DETECTION_CONFIDENCE` in `config.py` if detection is
  unreliable (lower value = more sensitive but noisier).
