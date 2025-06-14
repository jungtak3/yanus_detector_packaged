# Yanus Detector

This project detects a specific image ("Yanus") on the screen and plays a sound when it is found.

## Project Structure

```
yanus_detector_packaged/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── window_capture.py
├── assets/
│   ├── images/
│   │   ├── yanus5_1080.jpg
│   │   └── yanus5_768.jpg
│   └── sounds/
│       └── 야누스_5초.mp3
├── .gitignore
├── README.md
└── requirements.txt
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd yanus_detector_packaged
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Place assets:**
    -   Place your image files (`yanus5_1080.jpg`, `yanus5_768.jpg`) into the `assets/images/` directory.
    -   Place your sound file (`야누스_5초.mp3`) into the `assets/sounds/` directory.

## Usage

You can run the application in two ways:

1.  **From the project's root directory (recommended):**
    ```bash
    python -m src.main
    ```

2.  **Directly from the `src` directory:**
    ```bash
    cd src
    python main.py
    ```

Press 'q' while the screen capture feed window is focused to exit the program.