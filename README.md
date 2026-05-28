# Lyrics-Window

A dynamic, multi-window lyric synchronization application built with Python, Tkinter, Pygame, and Pillow. The application plays an audio file (e.g., Taylor Swift's *"betty"*) and spawns pixelated, retro-styled Tkinter windows that render the lyrics word-by-word in real-time, synchronized with the music.

## Features

- **Cascading Floating Windows**: Spawns a new window for each lyric block, positioning them dynamically across the screen while avoiding excessive overlaps with existing windows.
- **Word-by-Word Syncing**: Renders lyrics progressively to match the exact timing of the audio playback.
- **Retro Pixelated Aesthetic**: Renders text at a low resolution and upscales it using nearest-neighbor interpolation (`Image.NEAREST`) to achieve a pixelated look.
- **Dynamic Text Fitting**: Uses binary search to automatically calculate the maximum font size that fits each lyric block perfectly within the window bounds.
- **Multi-Window Lifetime**: Windows lift and focus automatically as their corresponding lyrics play, closing all together when the app is exited.

## Project Structure

- **[betty.py](file:///e:/CODES/python/betty.py)**: Main application source code containing GUI window spawning, layout calculations, text wrapping, and drawing logic.
- **`betty.mp3`**: The audio track for the synchronized lyrics (expected in the root directory).
- **[run.bat](file:///e:/CODES/python/run.bat)**: A Windows batch script to launch the application cleanly without displaying a command prompt, using the pythonw executable in `.venv`.

## Getting Started

### Prerequisites

- Python 3.8+
- Active internet connection to install dependencies (or pre-installed modules).

### Setup and Installation

1. **Clone/extract the project** to your local machine.
2. **Create a virtual environment** in the project root:
   ```powershell
   python -m venv .venv
   ```
3. **Activate the virtual environment**:
   - **Windows PowerShell**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Command Prompt**:
     ```cmd
     .venv\Scripts\activate.bat
     ```
4. **Install dependencies**:
   ```powershell
   pip install pygame Pillow
   ```
5. Ensure your audio track `betty.mp3` is placed in the project directory.

## How to Run

### Windows (Quick Launch)
Double-click the **[run.bat](file:///e:/CODES/python/run.bat)** script or run it from the command line:
```powershell
.\run.bat
```

### Standard Run
Activate your virtual environment and run the python file directly:
```powershell
python betty.py
```

## Customization

You can adapt the lyrics, timing, and audio to fit another track by editing the parameters in **[betty.py](file:///e:/CODES/python/betty.py)**:

1. Update the `self.lyrics` dictionary array with your custom lyric words and timestamps (in seconds):
   ```python
   self.lyrics = [
       {
           "words": [
               {"time": 0.0, "text": "Hello"},
               {"time": 0.5, "text": "world"},
           ]
       },
   ]
   ```
2. Point `self.audio_path` to your new `.mp3` file:
   ```python
   self.audio_path = "your-audio.mp3"
   ```
