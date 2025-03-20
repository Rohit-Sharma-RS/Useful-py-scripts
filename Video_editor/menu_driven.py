import os
import sys
from moviepy.editor import *

def clear_screen():
    """Clear the console screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_video_path():
    """Get video path from user"""
    path = input("\nEnter the path to your video file: ")
    if not os.path.exists(path):
        print("File not found! Please check the path.")
        return None
    return path

def speed_change():
    """Change the speed of a video"""
    path = get_video_path()
    if not path: return
    
    try:
        factor = float(input("Enter speed factor (0.5 for half speed, 2 for double speed): "))
        output = input("Enter output filename (with extension): ")
        
        print("\nProcessing... This may take a while.")
        video = VideoFileClip(path)
        fast_video = video.fx(vfx.speedx, factor)
        fast_video.write_videofile(output)
        video.close()
        fast_video.close()
        print(f"\nDone! Video saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def trim_video():
    """Trim a video to specific start and end times"""
    path = get_video_path()
    if not path: return
    
    try:
        video = VideoFileClip(path)
        print(f"\nVideo duration: {video.duration} seconds")
        
        start = float(input("Enter start time in seconds: "))
        end = float(input("Enter end time in seconds: "))
        output = input("Enter output filename (with extension): ")
        
        print("\nProcessing... This may take a while.")
        trimmed = video.subclip(start, end)
        trimmed.write_videofile(output)
        video.close()
        trimmed.close()
        print(f"\nDone! Video saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def extract_audio():
    """Extract audio from a video"""
    path = get_video_path()
    if not path: return
    
    try:
        output = input("Enter output audio filename (with .mp3 extension): ")
        
        print("\nExtracting audio...")
        video = VideoFileClip(path)
        audio = video.audio
        audio.write_audiofile(output)
        video.close()
        audio.close()
        print(f"\nDone! Audio saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def add_text():
    """Add text overlay to a video"""
    path = get_video_path()
    if not path: return
    
    try:
        text = input("Enter text to overlay: ")
        fontsize = int(input("Enter font size (e.g., 70): "))
        color = input("Enter text color (e.g., 'white', 'yellow', 'red'): ")
        output = input("Enter output filename (with extension): ")
        
        print("\nProcessing... This may take a while.")
        video = VideoFileClip(path)
        
        # Generate a text clip
        txt_clip = TextClip(text, fontsize=fontsize, color=color)
        txt_clip = txt_clip.set_position('center').set_duration(video.duration)
        
        # Overlay the text clip on the video
        final = CompositeVideoClip([video, txt_clip])
        final.write_videofile(output)
        
        video.close()
        final.close()
        print(f"\nDone! Video saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def reverse_video():
    """Reverse a video"""
    path = get_video_path()
    if not path: return
    
    try:
        output = input("Enter output filename (with extension): ")
        
        print("\nProcessing... This may take a while.")
        video = VideoFileClip(path)
        reversed_clip = video.fx(vfx.time_mirror)
        reversed_clip.write_videofile(output)
        video.close()
        reversed_clip.close()
        print(f"\nDone! Video saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def merge_videos():
    """Merge multiple videos"""
    try:
        num_videos = int(input("How many videos do you want to merge? "))
        clips = []
        
        for i in range(num_videos):
            path = input(f"\nEnter path for video {i+1}: ")
            if not os.path.exists(path):
                print("File not found! Skipping this video.")
                continue
            clips.append(VideoFileClip(path))
        
        if not clips:
            print("No valid videos provided.")
            return
            
        output = input("\nEnter output filename (with extension): ")
        
        print("\nMerging videos... This may take a while.")
        final_clip = concatenate_videoclips(clips)
        final_clip.write_videofile(output)
        
        for clip in clips:
            clip.close()
        final_clip.close()
        print(f"\nDone! Merged video saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def rotate_video():
    """Rotate a video"""
    path = get_video_path()
    if not path: return
    
    try:
        print("\nRotation options:")
        print("1. 90 degrees clockwise")
        print("2. 90 degrees counterclockwise")
        print("3. 180 degrees")
        
        choice = int(input("Enter your choice (1-3): "))
        output = input("Enter output filename (with extension): ")
        
        print("\nProcessing... This may take a while.")
        video = VideoFileClip(path)
        
        if choice == 1:
            rotated = video.rotate(90)
        elif choice == 2:
            rotated = video.rotate(-90)
        elif choice == 3:
            rotated = video.rotate(180)
        else:
            print("Invalid choice!")
            return
            
        rotated.write_videofile(output)
        video.close()
        rotated.close()
        print(f"\nDone! Video saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def create_gif():
    """Convert video to GIF"""
    path = get_video_path()
    if not path: return
    
    try:
        start = float(input("Enter start time in seconds: "))
        duration = float(input("Enter duration in seconds: "))
        output = input("Enter output filename (with .gif extension): ")
        
        print("\nCreating GIF... This may take a while.")
        video = VideoFileClip(path).subclip(start, start+duration)
        video.write_gif(output, fps=10)
        video.close()
        print(f"\nDone! GIF saved as {output}")
    except Exception as e:
        print(f"Error: {e}")

def main_menu():
    """Display the main menu"""
    while True:
        clear_screen()
        print("\n==== MoviePy Demo Program ====")
        print("1. Change video speed")
        print("2. Trim video")
        print("3. Extract audio from video")
        print("4. Add text overlay")
        print("5. Reverse video")
        print("6. Merge multiple videos")
        print("7. Rotate video")
        print("8. Convert video to GIF")
        print("9. Exit")
        
        try:
            choice = int(input("\nEnter your choice (1-9): "))
            
            if choice == 1:
                speed_change()
            elif choice == 2:
                trim_video()
            elif choice == 3:
                extract_audio()
            elif choice == 4:
                add_text()
            elif choice == 5:
                reverse_video()
            elif choice == 6:
                merge_videos()
            elif choice == 7:
                rotate_video()
            elif choice == 8:
                create_gif()
            elif choice == 9:
                print("\nThank you for using MoviePy Demo Program!")
                sys.exit(0)
            else:
                print("Invalid choice! Please try again.")
                
            input("\nPress Enter to continue...")
        except ValueError:
            print("Please enter a number!")
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nExiting program.")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()