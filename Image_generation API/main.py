import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
import os
from cloudinary import CloudinaryImage

def load_env_file(file_path):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

load_env_file(r"D:\github py_scripts\Useful-py-scripts\Image_generation API\secret.env")
api_secret = os.getenv("api_secret")
if api_secret is None:
    print("API secret not loaded. Check the .env file and path.")
else:
    print(f"API secret loaded: {api_secret}")
# Configuration       
cloudinary.config( 
    cloud_name = "dm3golsxs", 
    api_key = "579876256279641", 
    api_secret = os.getenv("api_secret"), 
)

# Upload an image
upload_result = cloudinary.uploader.upload("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
                                           public_id="shoes")
print(upload_result["secure_url"])

# Optimize delivery by resizing and applying auto-format and auto-quality
optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
print(optimize_url)

# Transform the image: auto-crop to square aspect_ratio
auto_crop_url, _ = cloudinary_url("shoes", width=500, height=500, crop="auto", gravity="auto")
print(auto_crop_url)

x = CloudinaryImage("https://platform.polygon.com/wp-content/uploads/sites/2/chorus/uploads/chorus_asset/file/25242262/26355890.jpeg?quality=90&strip=all&crop=7.8125,0,84.375,100").image(aspect_ratio="1:1", gravity="center", background="gen_fill", crop="pad")
print(x)

# Generate a 300x300 face-detection based thumbnail of an uploaded image
face_thumbnail_url, _ = cloudinary_url("shoes", width=300, height=300, gravity="auto", crop="thumb")
print(face_thumbnail_url)

# Generate a 300x300 circular crop thumbnail of an uploaded image
circle_thumbnail_url, _ = cloudinary_url("shoes", width=300, height=300, radius="max", crop="thumb")
print(circle_thumbnail_url)

blur = CloudinaryImage("https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg").image(effect="blur:300")
print(blur)

# And so on 
# checkout https://console.cloudinary.com/pm/c-a64bfdf647eb43c8f24a7105bf4387/transformations/center
