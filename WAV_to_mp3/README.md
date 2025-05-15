# WAV to MP3 Conversion Utility

This document provides an overview and operational instructions for a Python script designed to convert WAV (Waveform Audio File Format) files to MP3 (MPEG-1 Audio Layer III) format. The script leverages the `pydub` library for audio processing.

## Core Functionality

-   Facilitates the conversion of `.wav` audio files to the `.mp3` format, which typically offers a more compressed file size.
-   Allows users to specify the output path and filename for the converted MP3 file.
-   If an output path is not designated, the script will automatically save the MP3 file in the same directory as the source WAV file, using the original filename with an `.mp3` extension.
-   Provides an option to define the bitrate for the output MP3 file, enabling a balance between audio quality and file size.

## System Prerequisites

To ensure successful execution of the script, the following components are required:

-   **Python 3.x**: The script is developed for Python version 3 or later. The latest version can be obtained from [python.org](https://www.python.org/downloads/).
-   **pip**: The Python package installer, which is generally included with Python distributions.
-   **pydub**: The primary audio manipulation library utilized by this script.
-   **FFmpeg or Libav**: The `pydub` library requires either FFmpeg or Libav for encoding and decoding audio formats, including MP3 export. These are external multimedia frameworks.
    -   It is imperative that one of these dependencies is installed and accessible via the system's PATH environment variable.
    -   **FFmpeg Installation (Recommended):**
        -   **Windows**: Download the FFmpeg binaries from [ffmpeg.org](https://ffmpeg.org/download.html). Subsequently, add the path to the `bin` directory (containing `ffmpeg.exe`) to your system's PATH environment variable.
        -   **macOS (via Homebrew)**: Execute the command `brew install ffmpeg` in the Terminal.
        -   **Linux (Debian/Ubuntu-based systems via apt)**: Execute the command `sudo apt update && sudo apt install ffmpeg` in the terminal.
    -   Verification of the FFmpeg installation and PATH configuration can be performed by executing `ffmpeg -version` in a terminal or command prompt.

## Setup and Installation

1.  **Script Acquisition:**
    Download or copy the `wav_to_mp3_converter.py` script to a local directory on your system.

2.  **pydub Library Installation:**
    Open a terminal or command prompt interface and execute the following command to install the `pydub` library:
    ```bash
    pip install pydub
    ```

## Operational Instructions

The script is executed via the command line interface. The standard command syntax is as follows:

```bash
python wav_to_mp3_converter.py <input_wav_path> [output_mp3_path]
