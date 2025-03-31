# Hand Gesture Controlled Presentation

A computer vision application that allows you to control presentation slides using hand gestures.

## Features

- Navigate slides with hand gestures (forward and backward)
- Point to content on slides
- Draw annotations on slides
- Delete annotations
- Webcam view embedded in slides

## Requirements

- Python 3.6+
- OpenCV
- cvzone
- NumPy
- PyAutoGUI
- MediaPipe (dependency of cvzone)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hand-gesture-presentation.git
   cd hand-gesture-presentation
   ```

2. Install dependencies:
   ```
   pip install opencv-python cvzone numpy pyautogui mediapipe
   ```

3. Place your presentation images in the `presentation` folder (PNG format recommended)

## Usage

Run the main script:
```
python main.py
```

### Gesture Controls

- **Thumb up (only)** [1,0,0,0,0]: Previous slide
- **Pinky up (only)** [0,0,0,0,1]: Next slide
- **Index and middle finger up** [0,1,1,0,0]: Pointer mode
- **Index finger up (only)** [0,1,0,0,0]: Draw annotations
- **Index, middle, and ring fingers up** [0,1,1,1,0]: Delete annotations

## Configuration

You can adjust various parameters in the `main.py` file:
- Camera resolution
- Gesture threshold
- Annotation color and thickness
- Delay between gestures

## Exit

Press 'q' to exit the application. 
