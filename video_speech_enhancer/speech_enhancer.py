import os
import numpy as np
import noisereduce as nr
import soundfile as sf
from moviepy.editor import VideoFileClip, AudioFileClip

# Paths to your input and output files
input_video_path = r"C:\Users\vampi\Videos\Captures\IPL Predictor - Forecast Match Results with AI - Personal - Microsoft​ Edge 2025-04-04 13-39-33.mp4"
temp_audio_path = "temp_audio.wav"
enhanced_audio_path = "enhanced_audio.wav"
output_video_path = "enhanced_video.mp4"

# Chunk parameters
chunk_duration = 10  # seconds per chunk

def process_audio_in_chunks(audio_data, sample_rate, n_fft=2048):
    """
    Process audio data in chunks to avoid memory issues.
    If stereo (2D array), process each channel separately.
    """
    num_samples = audio_data.shape[0]
    chunk_size = int(chunk_duration * sample_rate)
    num_chunks = int(np.ceil(num_samples / chunk_size))
    
    # Prepare an array for the enhanced audio
    enhanced_audio = np.empty_like(audio_data)

    if audio_data.ndim == 1:  # Mono audio
        for i in range(num_chunks):
            start = i * chunk_size
            end = min((i + 1) * chunk_size, num_samples)
            print(f"Processing mono chunk {i+1}/{num_chunks} (samples {start} to {end})...")
            enhanced_audio[start:end] = nr.reduce_noise(
                y=audio_data[start:end],
                sr=sample_rate,
                n_fft=n_fft
            )
    elif audio_data.ndim == 2:  # Stereo or multi-channel
        # Process each channel separately
        for ch in range(audio_data.shape[1]):
            for i in range(num_chunks):
                start = i * chunk_size
                end = min((i + 1) * chunk_size, num_samples)
                print(f"Processing channel {ch+1}, chunk {i+1}/{num_chunks} (samples {start} to {end})...")
                enhanced_audio[start:end, ch] = nr.reduce_noise(
                    y=audio_data[start:end, ch],
                    sr=sample_rate,
                    n_fft=n_fft
                )
    else:
        raise ValueError("Audio data has an unsupported number of dimensions.")
        
    return enhanced_audio

def main():
    # Step 1: Extract audio from video using moviepy
    print("Extracting audio from video...")
    video_clip = VideoFileClip(input_video_path)
    video_clip.audio.write_audiofile(temp_audio_path)
    
    # Step 2: Read the audio file
    print("Loading audio file...")
    audio_data, sample_rate = sf.read(temp_audio_path)
    print("Audio data shape:", audio_data.shape)
    
    # (Optional) Convert stereo to mono if desired:
    # Uncomment the following lines to convert to mono:
    # if audio_data.ndim > 1:
    #     print("Converting stereo audio to mono...")
    #     audio_data = np.mean(audio_data, axis=1)
    #     print("New audio shape (mono):", audio_data.shape)
    
    # Step 3: Process audio in chunks to apply noise reduction
    print("Applying noise reduction in chunks...")
    enhanced_audio = process_audio_in_chunks(audio_data, sample_rate, n_fft=2048)
    
    # Write the enhanced audio to a new file
    sf.write(enhanced_audio_path, enhanced_audio, sample_rate)
    print("Enhanced audio saved.")
    
    # Step 4: Replace the original video's audio with the enhanced audio
    print("Replacing audio in video...")
    new_audio = AudioFileClip(enhanced_audio_path)
    final_video = video_clip.set_audio(new_audio)
    
    # Write the final video file with the enhanced voice
    final_video.write_videofile(output_video_path, codec="libx264")
    print("Enhanced video saved as", output_video_path)
    
    # Clean up temporary files if desired
    os.remove(temp_audio_path)
    os.remove(enhanced_audio_path)

if __name__ == "__main__":
    main()
