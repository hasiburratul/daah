import requests
import os
from datetime import datetime
from PIL import Image

def download_image():
    # URL of the website
    url = "https://thispersondoesnotexist.com/"
    
    # Send a GET request to the website
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Create images and images/fake directories if they don't exist
        if not os.path.exists("images"):
            os.makedirs("images")
        if not os.path.exists("images/fake"):
            os.makedirs("images/fake")
        
        # Generate a unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_filename = f"images/temp_{timestamp}.jpg"
        filename = f"images/fake/person_{timestamp}.jpg"
        
        # Save the original image temporarily
        with open(temp_filename, "wb") as f:
            f.write(response.content)
        
        # Open the image with Pillow
        img = Image.open(temp_filename)
        
        # Get image dimensions
        width, height = img.size
        
        # Calculate 1 cm in pixels (assuming 96 DPI, 1 cm ≈ 38 pixels)
        cm_in_pixels = 38
        
        # Crop the image (removing 1 cm from bottom)
        cropped_img = img.crop((0, 0, width, height - cm_in_pixels))
        
        # Remove metadata by creating a new image with just the pixel data
        img_without_metadata = Image.new(cropped_img.mode, cropped_img.size)
        img_without_metadata.putdata(list(cropped_img.getdata()))
        
        # Save the cropped image without metadata
        img_without_metadata.save(filename)
        
        # Remove the temporary file
        os.remove(temp_filename)
        
        print(f"Image successfully downloaded, cropped, metadata removed, and saved as {filename}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

if __name__ == "__main__":
    for i in range(50):
        download_image()
