from flask import Flask, render_template, request, send_file
import cloudinary
import cloudinary.uploader
import os
from cloudinary import CloudinaryImage
import requests
from PIL import Image
from io import BytesIO
import dotenv

dotenv.load_dotenv("secret.env")

app = Flask(__name__)
app.secret_key = os.urandom(24).hex() 

    
cloudinary.config( 
    cloud_name = "dm3golsxs", 
    api_key = "447258379524869", 
    api_secret = '9aOg2R1NpIxXLre4Ag_r78pROjw', 
)

@app.route("/download", methods=["GET"])
def download_image():
    # Get the image URL from the request query parameters
    url = request.args.get('url')
    if not url:
        return "No URL provided.", 400

    # Fetch the image from the provided URL
    response = requests.get(url)
    if response.status_code != 200:
        return "Error fetching image.", 500

    try:
        # Open the image as a webp file and convert it to RGB (JPG format)
        webp_image = Image.open(BytesIO(response.content))
        jpg_image = webp_image.convert("RGB")
        
        # Save the converted image to a BytesIO buffer (in memory)
        buffer = BytesIO()
        jpg_image.save(buffer, "JPEG")
        buffer.seek(0)  # Reset the buffer position to the beginning
        
        # Send the file to the user with a download prompt
        return send_file(
            buffer,
            as_attachment=True,  # Forces the file to be downloaded
            download_name="converted_image.jpg",  # The filename the user will see
            mimetype='image/jpeg'  # Correct mimetype for JPG files
        )
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

uploads_dir = "uploads"
if not os.path.exists(uploads_dir):
    os.makedirs(uploads_dir)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        file = request.files.get("image")

        if file:
            file_path = os.path.join(uploads_dir, file.filename)
            file.save(file_path)
    
            upload_result = cloudinary.uploader.upload(file_path)
            public_id = upload_result['public_id']

            changed_image_url = CloudinaryImage(public_id).image(effect=f"gen_background_replace:prompt_{prompt}", fetch_format="auto", quality="auto")

            image_url = changed_image_url.split('"')[1]  # Extract URL from <img> tag
            
            print(f"Uploaded Image Public ID: {public_id}")
            print(f"Changed Image URL: {image_url}")  # Log the URL
            
            return render_template("index.html", changed_image_url=image_url)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
