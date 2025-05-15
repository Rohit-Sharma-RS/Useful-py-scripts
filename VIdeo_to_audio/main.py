import moviepy.editor as mp
import os
import sys

def convert_video_to_audio(video_path, audio_path=None):
    """
    Converts a video file to an audio file.

    Args:
        video_path (str): The path to the input video file.
        audio_path (str, optional): The path to save the output audio file.
                                    Defaults to None, in which case the audio file
                                    is saved in the same directory as the video
                                    with an .mp3 extension.

    Returns:
        str: The path to the generated audio file, or None if conversion failed.
    """
    try:
        # Check if the video file exists
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at '{video_path}'")
            return None

        # Load the video file
        print(f"Loading video: {video_path}")
        video_clip = mp.VideoFileClip(video_path)

        # Extract the audio
        audio_clip = video_clip.audio
        print("Audio extracted successfully.")

        # Determine the output audio path
        if audio_path is None:
            base, ext = os.path.splitext(video_path)
            audio_path = base + ".mp3"
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(audio_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")


        # Write the audio file
        # You can specify codec and bitrate if needed, e.g., codec="libmp3lame", bitrate="192k"
        print(f"Writing audio to: {audio_path}")
        audio_clip.write_audiofile(audio_path)

        # Close the clips to free up resources
        audio_clip.close()
        video_clip.close()

        print(f"Successfully converted '{video_path}' to '{audio_path}'")
        return audio_path

    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        # Attempt to close clips if they were opened
        if 'video_clip' in locals() and video_clip:
            video_clip.close()
        if 'audio_clip' in locals() and audio_clip:
            audio_clip.close()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python video_to_audio_converter.py <input_video_path> [output_audio_path]")
        print("Example: python video_to_audio_converter.py my_video.mp4")
        print("Example: python video_to_audio_converter.py my_video.mp4 custom_audio_name.wav")
        sys.exit(1)

    input_video = sys.argv[1]
    output_audio = None

    if len(sys.argv) > 2:
        output_audio = sys.argv[2]

    convert_video_to_audio(input_video, output_audio)
