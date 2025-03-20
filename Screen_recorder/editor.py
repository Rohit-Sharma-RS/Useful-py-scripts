from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.speedx import speedx 

video = VideoFileClip(r"D:\Useful-py-scripts\screen_record.avi")

# This is where magic happends fx is just function to reduce speedx to 0.5
part1 = video.subclip(0, 16)    
part2 = video.subclip(16, 42).fx(speedx, 0.5)  
part3 = video.subclip(42, video.duration)      

# Combine all parts smoothly hence "compose"
final_clip = concatenate_videoclips([part1, part2, part3], method="compose")

final_clip.write_videofile("output_video.mp4", codec="libx264", fps=25)