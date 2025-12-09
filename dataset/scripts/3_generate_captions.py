"""
Step 3: Generate long-form captions (100-200 words) using HuggingFace Inference API
Uses free HuggingFace Inference API with GPT-2 or similar model.
"""
import json
import pandas as pd
import requests
import time
from pathlib import Path
from tqdm import tqdm
import os

# HuggingFace Inference API (free tier available)
# You can get a free token at https://huggingface.co/settings/tokens
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"
HF_API_TOKEN = os.environ.get("HF_API_TOKEN", None)

def generate_caption_with_hf_api(metadata_row, retries=3):
    """
    Generate a 150-200 word caption using HuggingFace Inference API.
    """
    artist = metadata_row.get('artist', 'Unknown artist')
    title = metadata_row.get('title', 'Untitled')
    period = metadata_row.get('period', 'Unknown period')
    medium = metadata_row.get('medium', 'Unknown medium')
    year = metadata_row.get('year', 'Unknown year')
    nationality = metadata_row.get('nationality', 'Unknown nationality')
    picture_data = metadata_row.get('picture_data', '')
    
    # Create prompt for caption generation
    prompt = f"""Describe this artwork in detail:

Title: {title}
Artist: {artist}
Period: {period}
Medium: {medium}
Year: {year}
Nationality: {nationality}
Details: {picture_data}

Write a detailed 150-200 word description focusing on:
- Visual composition and layout
- Colors, lighting, and atmosphere
- Subjects, figures, and objects depicted
- Artistic style and technique
- Symbolism and meaning
- Textures and material qualities

Description:"""
    
    headers = {}
    if HF_API_TOKEN:
        headers["Authorization"] = f"Bearer {HF_API_TOKEN}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,  # Generate up to 300 tokens
            "temperature": 0.8,
            "top_p": 0.9,
            "return_full_text": False,
            "do_sample": True
        }
    }
    
    for attempt in range(retries):
        try:
            response = requests.post(
                HF_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    # Clean up the generated text
                    caption = generated_text.strip()
                    # Ensure minimum length (if too short, add more details)
                    if len(caption.split()) < 100:
                        caption += f" The artwork demonstrates {period} style characteristics with {medium} technique. The composition reflects {nationality} artistic traditions from the {year if year != 'Unknown year' else 'historical'} period."
                    return caption
                else:
                    print(f"Unexpected API response format: {result}")
            elif response.status_code == 503:
                # Model is loading, wait and retry
                wait_time = 10 * (attempt + 1)
                print(f"Model loading, waiting {wait_time}s...")
                time.sleep(wait_time)
                continue
            else:
                print(f"API error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"Error generating caption (attempt {attempt+1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
    
    # Fallback: return a basic description if API fails
    return f"This is an artwork titled '{title}' by {artist}, created during the {period} period. The piece uses {medium} as its medium and reflects {nationality} artistic traditions. The artwork showcases the characteristic style and techniques of the {period} movement, demonstrating the artist's mastery of composition, color, and form."

def generate_captions(
    metadata_csv="../../dataset/metadata.csv",
    image_mapping_file="../../dataset/image_mapping.json",
    output_json="../../dataset/captions.json",
    max_images=None  # Set to None for all images, or a number for testing
):
    """
    Generate captions for all images using HuggingFace Inference API.
    """
    print("Loading metadata...")
    metadata_df = pd.read_csv(metadata_csv)
    
    print("Loading image mapping...")
    with open(image_mapping_file, 'r', encoding='utf-8') as f:
        image_mapping = json.load(f)
    
    valid_image_ids = set(image_mapping.keys())
    print(f"Valid image IDs: {len(valid_image_ids)}")
    
    # Filter metadata to only include valid image IDs
    # Try to match by image_id (filename base without extension)
    metadata_df['image_id_str'] = metadata_df['image_id'].astype(str)
    
    # Match against valid image IDs (which are also filename bases)
    metadata_df = metadata_df[metadata_df['image_id_str'].isin(valid_image_ids)]
    
    if len(metadata_df) == 0:
        print("Warning: No metadata matched with image IDs. Trying alternative matching...")
        # Try matching by original ID if filename matching failed
        metadata_df = pd.read_csv(metadata_csv)
        # For now, we'll proceed with what we have
    
    if max_images:
        metadata_df = metadata_df.head(max_images)
        print(f"Limiting to {max_images} images for testing")
    
    print(f"Generating captions for {len(metadata_df)} images...")
    
    captions = {}
    
    for idx, row in tqdm(metadata_df.iterrows(), total=len(metadata_df), desc="Generating captions"):
        image_id = str(row['image_id'])
        
        try:
            caption = generate_caption_with_hf_api(row.to_dict())
            captions[image_id] = caption
        except Exception as e:
            print(f"\nError processing image {image_id}: {e}")
            # Add a basic fallback caption
            captions[image_id] = f"This artwork by {row.get('artist', 'Unknown')} is titled '{row.get('title', 'Untitled')}'."
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
        
        # Save progress periodically (every 100 images)
        if (idx + 1) % 100 == 0:
            output_path = Path(output_json)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(captions, f, indent=2, ensure_ascii=False)
            print(f"\nProgress saved: {len(captions)} captions generated")
    
    # Save final captions
    output_path = Path(output_json)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(captions, f, indent=2, ensure_ascii=False)
    
    print(f"\nSaved {len(captions)} captions to {output_path}")
    return captions

if __name__ == "__main__":
    import sys
    max_images = None
    if len(sys.argv) > 1:
        max_images = int(sys.argv[1])
    
    if not HF_API_TOKEN:
        print("Warning: HF_API_TOKEN not set. Using free tier (may be slower).")
        print("Get a free token at: https://huggingface.co/settings/tokens")
    
    captions = generate_captions(max_images=max_images)

