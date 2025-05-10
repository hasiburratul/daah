import os
import re
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
from pathlib import Path

def get_celebrity_pairs_from_file(file_path):
    """Extract pairs of AI image filename and celebrity name from the results file"""
    pairs = []
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Use regex to find all matches
    pattern = r'## (person_\d+_\d+\.jpg)\nThe celebrity that this person most resembles is ([^\.]+)'
    matches = re.findall(pattern, content)
    
    for ai_filename, celebrity_name in matches:
        # Clean up the celebrity name (remove asterisks, etc.)
        clean_name = celebrity_name.strip().replace('*', '').replace(' ', '_')
        pairs.append((ai_filename, clean_name))
    
    return pairs

def get_wikipedia_image_url(celebrity_name):
    """Get the URL of the first image from a celebrity's Wikipedia page"""
    # Replace spaces with underscores and format for Wikipedia URL
    wiki_name = celebrity_name.replace('_', ' ')
    search_url = f"https://en.wikipedia.org/wiki/{urllib.parse.quote(wiki_name)}"
    
    try:
        response = requests.get(search_url)
        if response.status_code != 200:
            print(f"Failed to access Wikipedia page for {celebrity_name}. Trying search...")
            # If direct page fails, try Wikipedia search
            search_url = f"https://en.wikipedia.org/w/index.php?search={urllib.parse.quote(wiki_name)}"
            response = requests.get(search_url)
            if response.status_code != 200:
                return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for the infobox image first (main profile picture on Wikipedia)
        infobox = soup.find('table', class_='infobox')
        if infobox:
            image_tag = infobox.find('img')
            if image_tag and 'src' in image_tag.attrs:
                # Complete the URL if it's relative
                img_src = image_tag['src']
                if img_src.startswith('//'):
                    img_src = 'https:' + img_src
                return img_src
        
        # If no infobox image, look for any image in the article
        image_tag = soup.find('img')
        if image_tag and 'src' in image_tag.attrs:
            img_src = image_tag['src']
            if img_src.startswith('//'):
                img_src = 'https:' + img_src
            return img_src
        
        return None
    
    except Exception as e:
        print(f"Error fetching Wikipedia image for {celebrity_name}: {e}")
        return None

def download_image(url, save_path):
    """Download an image from URL and save it to the given path"""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return True
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def main():
    # Find the most recent celebrity lookalike results file
    result_files = [f for f in os.listdir() if f.startswith('celebrity_lookalikes_') and f.endswith('.txt')]
    
    if not result_files:
        print("No celebrity lookalike results file found!")
        return
    
    # Get the most recent file
    latest_file = max(result_files)
    print(f"Using results from: {latest_file}")
    
    # Create the images/real directory if it doesn't exist
    real_images_dir = "images/real"
    os.makedirs(real_images_dir, exist_ok=True)
    
    # Get the celebrity pairs from the file
    celebrity_pairs = get_celebrity_pairs_from_file(latest_file)
    
    print(f"Found {len(celebrity_pairs)} celebrity matches.")
    
    # Process each celebrity
    for ai_filename, celebrity_name in celebrity_pairs:
        print(f"Processing: {ai_filename} → {celebrity_name}")
        
        # Get the Wikipedia image URL
        image_url = get_wikipedia_image_url(celebrity_name)
        
        if not image_url:
            print(f"Could not find Wikipedia image for {celebrity_name}")
            continue
        
        # Create the output filename
        output_filename = f"{ai_filename.split('.')[0]}+{celebrity_name}.jpg"
        output_path = os.path.join(real_images_dir, output_filename)
        
        # Check if file already exists
        if os.path.exists(output_path):
            print(f"Image already exists: {output_filename}")
            continue
        
        # Download the image
        print(f"Downloading {image_url}")
        if download_image(image_url, output_path):
            print(f"Saved as: {output_filename}")
        
        # Add a small delay to avoid overwhelming Wikipedia's servers
        time.sleep(1)

if __name__ == "__main__":
    main() 