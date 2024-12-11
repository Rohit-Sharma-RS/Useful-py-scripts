from PIL import Image
import os

def divide_image(image_path, output_folder):
    # Open the image
    img = Image.open(image_path)
    width, height = img.size
    
    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Calculate block dimensions
    block_width = width // 3
    block_height = height // 3
    
    # Crop the image into 9 parts (3x3 grid)
    for row in range(3):
        for col in range(3):
            left = col * block_width
            upper = row * block_height
            right = left + block_width
            lower = upper + block_height
            
            # Crop the image
            cropped_image = img.crop((left, upper, right, lower))
            
            # Save each part
            block_name = f"block_{row + 1}_{col + 1}.png"
            cropped_image.save(os.path.join(output_folder, block_name))
            print(f"Saved: {block_name}")

# Example usage
image_path = "your_image.jpg"  # Replace with the path to your image
output_folder = "output_blocks"  # Replace with your output directory
divide_image(image_path, output_folder)
