# Subtitle Timestamp Shifter

This Python script allows you to adjust (shift) subtitle timestamps in `.srt` files. It helps you synchronize subtitles that appear too early or too late by applying an offset to all timestamps.

## Features
- **Batch Processing**: Shift timestamps for multiple subtitle files at once.
- **Offset Control**: Allows you to specify a positive or negative offset in seconds to delay or advance subtitles.
- **In-place File Modification**: The original `.srt` file is replaced with the adjusted file after applying the timestamp shifts.
- **Supports Multiple Input Formats**: Accepts file paths with backslashes, forward slashes, or quotes, and automatically normalizes them.
  
## Requirements

1. Python 3.x
2. The `chardet` library for character encoding detection:
   - Install it via `pip install chardet`

## Usage

1. **Clone or Download the Script**:
   - Save the Python script to a local directory.

2. **Run the Script**:
   - Open your terminal or command prompt.
   - Navigate to the folder where the script is located.
   - Run the script with:

   ```bash
   python subtitle_timestamp_shifter.py
