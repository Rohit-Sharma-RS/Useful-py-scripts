# Smart Educational Text Reader for Notes 📚🔊

Hey there! Welcome to Smart Educational Text Reader, your friendly text-to-speech tool designed to make reading educational content more accessible and enjoyable. LISTEN TO NOTES ON THE GO!

## What's This Thing Do? 🤔

Smart Educational Text Reader takes your PDFs and text files and turns them into speech with some clever features:

- 🧠 **Smart Reading**: Detects headings, emphasized text, and natural breaks in content
- 🔊 **Natural Speech**: Adds appropriate pauses and emphasis for a more human-like reading experience
- 💾 **Save As Audio**: Convert your documents to WAV or MP3 files to listen on the go
- 🖥️ **Easy UI**: Simple, intuitive interface with text highlighting as it reads
- 🏃‍♂️ **Adjustable Speed**: Slow, normal, or fast reading speeds to match your preference

## Getting Started 🚀

### Requirements

Before jumping in, make sure you have:

- Python 3.6 or higher
- The required Python packages (see below)
- FFmpeg installed for MP3 conversion

### Installation

1. Clone this repo or download the files
2. Install the required packages:

```bash
pip install pyttsx3 nltk PyPDF2 pydub
```

3. For MP3 support, install FFmpeg:
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
   - **Mac**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` or equivalent for your distro

### Running the Program

Just run the main script:

```bash
python smart_reader.py
```

Want to use command line instead of the GUI? No problem:

```bash
python smart_reader.py --cli
```

## Features Breakdown 🔍

### Document Support
- PDF files (.pdf)
- Text files (.txt)
- Markdown files (.md)

### Reading Enhancements
- Automatically emphasizes important text (like **bold** or UPPERCASE words)
- Adds natural pauses at periods, commas, and paragraph breaks
- Highlights text as it's being read

### Voice Options
- Choose from all voices installed on your system
- Adjust reading speed to your preference

### Audio Export
- Save as WAV or MP3 files
- Perfect for creating audiobooks or study materials

## How to Use the GUI 🖱️

1. **Open a file**: Click "File" → "Open PDF/Text" and choose your document
2. **Choose voice**: Select your preferred voice from the dropdown or Voice menu
3. **Set speed**: Choose slow, normal, or fast from the Speed menu
4. **Control playback**: Use Play/Pause, Previous, Next, and Stop buttons
5. **Save audio**: Click "Save Audio" button or "File" → "Save Audio As..."

## Command Line Usage 💻

If you prefer the command line:

1. Launch with the `--cli` flag
2. Follow the prompts to select voice and speed
3. Enter the path to your document
4. Choose whether to read immediately or save as audio

## Tips & Tricks 💡

- For best results with PDFs, use files with clear text (not scanned images)
- The reader works best with well-structured documents
- Try different voices to find the one you like best
- MP3 files are smaller than WAV, but require FFmpeg to be installed

## Troubleshooting 🔧

**"No text loaded to save as audio"**
- Make sure you've opened a document first before trying to save audio

**Error converting to MP3**
- Check that FFmpeg is properly installed and in your PATH
- The program will fall back to WAV if MP3 conversion fails

**Reading sounds robotic**
- This is a limitation of text-to-speech engines. The program tries to add natural pauses and emphasis to help with this.

## Contributing 🤝

Got ideas to make this better? Awesome! Feel free to:
- Fork the repo
- Add your cool features
- Submit a pull request

---

Built with ❤️ for making learning more accessible.

Happy listening! 🎧