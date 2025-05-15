# Video to Audio Converter - Easy Peasy!

Hey there! This nifty Python script is all about grabbing the sound from your video files and saving it as a separate audio file(MP4 to MP3). It does this cool trick using a helper called the `moviepy` library.

## What's Awesome About It?

-   Turns all sorts of videos (like MP4s, AVIs, MKVs, you name it!) into just audio.
-   You get to pick the name and even the type for your new audio file (fancy an MP3, WAV, or OGG?).
-   If you don't tell it where to save the audio, no worries! It'll just pop it in the same spot as your video, give it the same name, but with an `.mp3` at the end. Super simple!

## What You'll Need (The Techy Bits, But Not Scary!)

-   **Python 3.x**: This is the programming language the script uses. If you don't have it, you can grab it from [python.org](https://www.python.org/downloads/).
-   **pip**: Think of this as Python's little helper for installing extra tools. It usually tags along when you install Python.
-   **MoviePy**: This is the main tool the script uses to mess with video and audio.
-   **FFmpeg**: MoviePy needs this behind-the-scenes worker to actually read and write video/audio files.
    -   Good news! MoviePy often tries to download FFmpeg for you the first time you use it.
    -   But, if you want to be sure, or if that doesn't work, here's how to get it yourself:
        -   **Windows**: Head over to [ffmpeg.org](https://ffmpeg.org/download.html) to download it. Then, you'll need to tell your computer where to find it by adding it to something called the system's PATH.
        -   **macOS (if you use Homebrew)**: Just type `brew install ffmpeg` in your Terminal.
        -   **Linux (if you use apt)**: Pop open your terminal and type `sudo apt update && sudo apt install ffmpeg`.

