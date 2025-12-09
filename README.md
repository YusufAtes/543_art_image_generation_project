# 543 Project: Art Generator

Bidirectional Vision-Language Networks for Cross-Modal Generation and Reconstruction

## Project Overview

This project investigates how neural networks can learn bidirectional mappings between visual data and natural-language descriptions. Using a paired image-caption dataset, the goal is to train two complementary neural models:

1. **Text-to-Image Decoder**: Generates images from long-form textual descriptions
2. **Image-to-Text Encoder**: Generates detailed natural-language descriptions from images

## Dataset

The dataset contains ~45,574 artwork images with metadata and generated long-form captions (100-200 words each).

### Dataset Creation

See `dataset/README.md` for instructions on creating the dataset from source files.

## Project Structure

```
.
├── dataset/           # Dataset creation scripts and structure
│   ├── scripts/      # Dataset creation pipeline
│   └── README.md     # Dataset creation instructions
├── archive/          # Original artwork images and metadata (not in repo)
└── requirements.txt  # Python dependencies
```

## Requirements

See `requirements.txt` for required Python packages.

## Dataset Creation Steps

1. Load and validate images
2. Process and merge metadata
3. Generate long-form captions (100-200 words)
4. Preprocess images (resize to 128×128, normalize)
5. Tokenize captions
6. Create train/val/test splits (80/10/10)

See `dataset/README.md` for detailed instructions.

## License

[Add your license here]

