import os
import base64
import requests
import csv
import json
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
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        raise

def get_image_analysis(fake_image_path, real_image_path):
    """
    Send both AI-generated image and celebrity image to ChatGPT for analysis
    """
    print(f"Preparing to analyze: {os.path.basename(fake_image_path)} and {os.path.basename(real_image_path)}")
    
    # Verify images exist
    if not os.path.exists(fake_image_path):
        raise FileNotFoundError(f"Image not found: {fake_image_path}")
    if not os.path.exists(real_image_path):
        raise FileNotFoundError(f"Image not found: {real_image_path}")
    
    # Get file sizes to verify images are valid
    fake_size = os.path.getsize(fake_image_path)
    real_size = os.path.getsize(real_image_path)
    print(f"Image sizes - Fake: {fake_size/1024:.1f} KB, Real: {real_size/1024:.1f} KB")
    
    fake_base64 = encode_image(fake_image_path)
    real_base64 = encode_image(real_image_path)
    
    print(f"Successfully encoded both images to base64")
    
    fake_filename = os.path.basename(fake_image_path)
    real_filename = os.path.basename(real_image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        # "model": "gpt-4.1-nano-2025-04-14",
        "model" : "gpt-4.1-2025-04-14",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an expert in analyzing images of faces. I'm showing you two images of faces. Please analyze them and provide your answers in the EXACT format specified below:\n\n```\nSimilarity: [rate from 1-10 how similar the two faces look]\nAI-Generated: [specify 'Image 1' or 'Image 2' - which one do you think is AI-generated?]\nExplanation: [explain how you identified the AI-generated image and what characteristics gave it away]\n```\n\nPlease stick EXACTLY to this format. It's important for my data processing.\n\nImage 1 (left):"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{fake_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Image 2 (right):"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{real_base64}"
                        }
                    }
                ]
            }
        ],
        "max_completion_tokens": 500
    }
    
    print("Sending request to ChatGPT API with both images...")
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Successfully received response from ChatGPT")
        return {
            "fake_image": fake_filename,
            "real_image": real_filename,
            "analysis": response.json()["choices"][0]["message"]["content"]
        }
    else:
        error_msg = f"Error: {response.status_code}, {response.text}"
        print(f"API request failed: {error_msg}")
        return {
            "fake_image": fake_filename,
            "real_image": real_filename,
            "analysis": error_msg
        }

def extract_analysis_data(analysis_text):
    """
    Extract structured data from the analysis text using the standardized format
    """
    data = {
        "similarity_score": None,
        "ai_generated_identification": None,
        "explanation": "",
        "full_analysis": analysis_text
    }
    
    # Extract each field using regular expressions
    import re
    
    # Extract similarity score
    similarity_match = re.search(r'Similarity:\s*(\d+)', analysis_text)
    if similarity_match:
        data["similarity_score"] = similarity_match.group(1)
    
    # Extract AI-generated image identification
    ai_match = re.search(r'AI-Generated:\s*(Image \d)', analysis_text)
    if ai_match:
        data["ai_generated_identification"] = ai_match.group(1)
    
    # Extract explanation
    explanation_match = re.search(r'Explanation:\s*(.+?)(?:\n|$)', analysis_text, re.DOTALL)
    if explanation_match:
        data["explanation"] = explanation_match.group(1).strip()
    
    return data

def main():
    # Create a .env file if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("OPENAI_API_KEY=your_api_key_here\n")
        print("Created .env file. Please add your OpenAI API key to it.")
        return
    
    # Check directories
    fake_dir = "images/fake"
    real_dir = "images/real"
    
    if not os.path.exists(fake_dir):
        print(f"Directory '{fake_dir}' not found. Please run image.py first to download AI-generated images.")
        return
    
    if not os.path.exists(real_dir):
        print(f"Directory '{real_dir}' not found. Please run celebrity_wiki_images.py first to download celebrity images.")
        return
    
    # Get all AI-generated images
    fake_images = [f for f in os.listdir(fake_dir) if f.startswith("person_") and f.endswith(".jpg")]
    
    if not fake_images:
        print("No AI-generated images found. Please run image.py first to download images.")
        return
    
    # Get all celebrity images
    real_images = [f for f in os.listdir(real_dir) if "+" in f and f.endswith(".jpg")]
    
    if not real_images:
        print("No celebrity images found. Please run celebrity_wiki_images.py first to download images.")
        return
    
    print(f"Found {len(fake_images)} AI-generated images and {len(real_images)} celebrity images")
    
    # Create a dictionary to quickly look up celebrity images by AI image filename
    real_image_lookup = {}
    for real_image in real_images:
        # The real image filename format is: person_DATE_TIME+Celebrity_Name.jpg
        # We need to extract the person_DATE_TIME part
        ai_image_part = real_image.split("+")[0]
        ai_image_filename = f"{ai_image_part}.jpg"
        real_image_lookup[ai_image_filename] = real_image
    
    # Create timestamp for the CSV file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"comparison_results_{timestamp}.csv"
    
    # Prepare CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['fake_image', 'real_image', 'similarity_score', 'ai_generated_correctly_identified', 'explanation', 'full_analysis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Process each AI-generated image
        for idx, fake_image in enumerate(fake_images):
            print(f"\n[{idx+1}/{len(fake_images)}] Processing {fake_image}...")
            
            # Find corresponding celebrity image
            if fake_image not in real_image_lookup:
                print(f"No matching celebrity image found for {fake_image}")
                continue
            
            real_image = real_image_lookup[fake_image]
            fake_image_path = os.path.join(fake_dir, fake_image)
            real_image_path = os.path.join(real_dir, real_image)
            
            print(f"Comparing {fake_image} with {real_image}")
            
            try:
                # Get analysis from ChatGPT
                result = get_image_analysis(fake_image_path, real_image_path)
                
                # Extract structured data from the analysis
                analysis_data = extract_analysis_data(result["analysis"])
                
                # Check if AI-generated image was correctly identified
                ai_correctly_identified = "Yes" if analysis_data["ai_generated_identification"] == "Image 1" else "No"
                
                # Write to CSV
                writer.writerow({
                    'fake_image': fake_image,
                    'real_image': real_image,
                    'similarity_score': analysis_data["similarity_score"],
                    'ai_generated_correctly_identified': ai_correctly_identified,
                    'explanation': analysis_data["explanation"],
                    'full_analysis': analysis_data["full_analysis"]
                })
                
                # Print result
                print(f"Results:")
                print(f"  Similarity Score: {analysis_data['similarity_score']}/10")
                print(f"  AI Generated Image Correctly Identified: {ai_correctly_identified}")
                print(f"  Explanation: {analysis_data['explanation'][:100]}...")
            except Exception as e:
                print(f"Error processing image pair: {e}")
            
            print("-" * 50)
    
    print(f"\nResults saved to {csv_filename}")

if __name__ == "__main__":
    main() 