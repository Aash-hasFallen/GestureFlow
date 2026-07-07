# ✋ GestureFlow

A real-time hand gesture recognition system built with **Python**, **OpenCV**, and **MediaPipe** that enables touch-free desktop interaction. Control applications with intuitive hand gestures or switch to a virtual drawing canvas—all through your webcam.

---

## 🚀 Features

- ✋ Real-time hand tracking and gesture recognition
- 🤖 Gesture-based desktop automation
- 🎨 Virtual drawing canvas with multiple brush colors
- 🔄 Gesture stabilization for improved accuracy
- 👍 Hold **Thumbs Up** to switch between Automation and Drawing modes
- 👌 Hold **OK Sign** to safely exit the application
- ⚡ Smooth real-time performance using MediaPipe

---

## ⚠️ Platform Note

The gesture recognition and drawing features work on any platform supported by the required Python libraries.

**Desktop automation is currently implemented for macOS only** using native commands (`open` and `pmset`). Windows and Linux users can easily replace these commands with their platform-specific equivalents.

# Note: This file contains macOS-specific commands for desktop automation.
# Replace them with platform-specific equivalents if using Windows or Linux.

---

## 🛠️ Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy

---

## 📁 Project Structure

```
GestureFlow/
│── main.py
│── requirements.txt
└── README.md
```

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/GestureFlow.git
cd GestureFlow
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Or install them manually:

```bash
pip install opencv-python mediapipe numpy
```

---

## ▶️ Running the Project

```bash
python main.py
```

Make sure your webcam is connected and accessible.

---

# 🎮 Gesture Controls

## Automation Mode

| Gesture | Action |
|---------|--------|
| ☝️ Index Finger | Open Spotify |
| ✌️ Peace Sign | Open YouTube |
| 🤟 Three Fingers | Open Google Chrome |
| ✊ Fist | Lock Display |

---

## Drawing Mode

| Gesture | Action |
|---------|--------|
| ☝️ Index Finger | Draw (Blue) |
| ✌️ Peace Sign | Draw (Green) |
| 🤟 Three Fingers | Draw (Red) |
| ✊ Fist | Clear Canvas |

---

## Global Controls

| Gesture | Function |
|---------|----------|
| 👍 Hold for 2 Seconds | Toggle between Automation & Drawing modes |
| 👌 Hold for 3 Seconds | Exit the application |

---

## ⚙️ How It Works

1. Captures live video using your webcam.
2. Detects hand landmarks with MediaPipe.
3. Recognizes predefined hand gestures based on finger positions.
4. Stabilizes predictions using a gesture buffer.
5. Executes desktop actions or enables virtual drawing based on the active mode.

---

## 📋 Requirements

- Python 3.10 or later
- Webcam
- OpenCV
- MediaPipe
- NumPy

---

## 💡 Future Improvements

- Windows & Linux automation support
- Custom gesture mapping
- Volume and media playback controls
- Mouse cursor control
- Air-writing recognition
- Save drawings as image files
- User-defined gesture training

---

## 📸 Demo

Add screenshots, GIFs, or a short demo video here.

---

## 🤝 Contributing

Contributions, suggestions, and improvements are always welcome.

If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 👨‍💻 Author

**Aashray Biswal**

Built with Python, OpenCV, and MediaPipe to explore real-time computer vision and gesture-based human-computer interaction.
