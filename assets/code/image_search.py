import os
import base64
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")

def encode_image(image_path):
    """Encode image to base64 string"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def get_celebrity_lookalike(image_path):
    """
    Send image to ChatGPT and ask for celebrity lookalike
    """
    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4.1-nano-2025-04-14", 
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a celebrity lookalike expert. You will be given an image of a person and you will need to identify the celebrity that this person most resembles. Please name just 1 celebrity that this person most resembles. Your answer should be in the following format: 'The celebrity that this person most resembles is [celebrity name].'"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    # Create a .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=your_api_key_here\n")
        print("Created .env file. Please add your OpenAI API key to it.")
        return
    
    # Get all images in the images/fake directory
    images_dir = "images/fake"
    if not os.path.exists(images_dir):
        print(f"Directory '{images_dir}' not found. Please run image.py first to download images.")
        return
    
    image_files = [f for f in os.listdir(images_dir) if f.startswith("person_") and f.endswith(".jpg")]
    
    if not image_files:
        print("No images found. Please run image.py first to download images.")
        return
    
    # Create a timestamp for the output file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"celebrity_lookalikes_{timestamp}.txt"
    
    # Open file for writing
    with open(output_file, "w") as f:
        # Write header
        f.write("# Celebrity Lookalike Results\n")
        f.write(f"# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Process each image
        for image_file in image_files:
            image_path = os.path.join(images_dir, image_file)
            print(f"Processing {image_file}...")
            
            # Get celebrity lookalike
            result = get_celebrity_lookalike(image_path)
            
            # Write to file
            f.write(f"## {image_file}\n")
            f.write(f"{result}\n\n")
            
            # Print result
            print(f"Celebrity lookalike for {image_file}:")
            print(result)
            print("-" * 50)
    
    print(f"\nResults saved to {output_file}")

if __name__ == "__main__":
    main()
