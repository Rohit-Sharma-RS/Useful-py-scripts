import os
import requests
from PIL import Image
import io
import base64
from dotenv import load_dotenv


load_dotenv("secret.env")
# Set your Imgur API client ID here
CLIENT_ID = os.getenv("IMGUR_CLIENT_ID")

def upload_to_imgur(image_data):
    headers = {"Authorization": f"Client-ID {CLIENT_ID}"}
    response = requests.post("https://api.imgur.com/3/image", headers=headers, data={"image": image_data})
    return response.json()

def upload_image(file_path):
    try:
        # Open the image from the provided file path
        with Image.open(file_path) as image:
            with io.BytesIO() as output:
                image.save(output, format='PNG')
                image_data = base64.b64encode(output.getvalue()).decode()  # Convert to base64

        # Upload the image to Imgur
        response = upload_to_imgur(image_data)

        if response.get("success"):
            print("Image uploaded successfully:", response["data"]["link"])
        else:
            print("Failed to upload image:", response)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = input("Enter the full path of the image file you want to upload: ")
upload_image(file_path)
