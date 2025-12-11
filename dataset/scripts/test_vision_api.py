"""Test vision API with a single image"""
import sys
from pathlib import Path
from importlib import import_module
import pandas as pd

# Import the caption generation module
mod = import_module('3_generate_captions')

# Test with first image - use absolute path from project root
project_root = Path(__file__).parent.parent.parent
image_path = project_root / 'archive' / 'artwork' / '0.jpg'
print(f"Testing with image: {image_path}")
print(f"Image exists: {image_path.exists()}")

# Create test metadata
test_metadata = pd.Series({
    'title': 'venus and adonis',
    'medium': 'oil on canvas',
    'period': 'Mannerism',
    'artist': 'test',
    'year': '1574',
    'nationality': 'German'
})

print("\nCalling vision API...")
try:
    caption = mod.generate_caption_with_vision_api(
        image_path, 
        test_metadata.to_dict()
    )
    print(f"\nGenerated caption ({len(caption.split())} words):")
    print("-" * 60)
    print(caption)
    print("-" * 60)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

