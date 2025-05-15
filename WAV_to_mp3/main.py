import os
import sys
from pydub import AudioSegment

def convert_wav_to_mp3(wav_path, mp3_path=None, bitrate="192k"):
    """
    Converts a WAV file to an MP3 file.

    Args:
        wav_path (str): The path to the input WAV file.
        mp3_path (str, optional): The path to save the output MP3 file.
                                    Defaults to None, in which case the MP3 file
                                    is saved in the same directory as the WAV
                                    with an .mp3 extension.
        bitrate (str, optional): The bitrate for the MP3 file (e.g., "128k", "192k", "320k").
                                 Defaults to "192k".

    Returns:
        str: The path to the generated MP3 file, or None if conversion failed.
    """
    try:
        # Check if the WAV file exists
        if not os.path.exists(wav_path):
            print(f"Error: WAV file not found at '{wav_path}'")
            return None

        # Check if the input file is a WAV file (basic check)
        if not wav_path.lower().endswith(".wav"):
            print(f"Error: Input file '{wav_path}' does not appear to be a WAV file.")
            return None

        # Load the WAV file
        print(f"Loading WAV file: {wav_path}")
        audio = AudioSegment.from_wav(wav_path)
        print("WAV file loaded successfully.")

        # Determine the output MP3 path
        if mp3_path is None:
            base, ext = os.path.splitext(wav_path)
            mp3_path = base + ".mp3"
        elif not mp3_path.lower().endswith(".mp3"):
            # If user provides an output path without .mp3, append it.
            # Or you could raise an error/warning. For now, let's append.
            print(f"Warning: Output path '{mp3_path}' did not end with .mp3. Appending .mp3 extension.")
            mp3_path += ".mp3"


        # Ensure the output directory exists
        output_dir = os.path.dirname(mp3_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")

        # Export as MP3
        print(f"Exporting to MP3: {mp3_path} with bitrate: {bitrate}")
        audio.export(mp3_path, format="mp3", bitrate=bitrate)

        print(f"Successfully converted '{wav_path}' to '{mp3_path}'")
        return mp3_path

    except FileNotFoundError:
        print(f"Error: Could not find the WAV file at '{wav_path}'. Please check the path.")
        return None
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        print("Please ensure FFmpeg or Libav is installed and in your system's PATH.")
        print("You can install FFmpeg from https://ffmpeg.org/download.html")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wav_to_mp3_converter.py <input_wav_path> [output_mp3_path]")
        print("Example: python wav_to_mp3_converter.py my_audio.wav")
        print("Example: python wav_to_mp3_converter.py sounds/track1.wav converted/track1_converted.mp3")
        sys.exit(1)

    input_wav = sys.argv[1]
    output_mp3 = None

    if len(sys.argv) > 2:
        output_mp3 = sys.argv[2]    
    convert_wav_to_mp3(input_wav, output_mp3)
