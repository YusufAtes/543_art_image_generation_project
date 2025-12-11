import pandas as pd
import sys
sys.path.insert(0, '.')
from importlib import import_module

# Import the function
gen_module = import_module('3_generate_captions')
generate_template_caption = gen_module.generate_template_caption

# Load a sample row
df = pd.read_csv('../../dataset/metadata.csv')
row = df.iloc[0].to_dict()

print("Sample Caption (Visual Elements Only):")
print("="*70)
caption = generate_template_caption(row)
print(caption)
print("="*70)
print(f"\nWord count: {len(caption.split())} words")

