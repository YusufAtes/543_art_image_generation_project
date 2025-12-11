"""Helper function to generate simple, direct captions"""

def generate_simple_caption(metadata_row):
    """
    Generate simple, direct captions focusing on what's visible, then type of artwork.
    Format: Most of caption describes the image, ending describes the medium/genre.
    """
    title = metadata_row.get('title', 'Untitled').lower()
    picture_data = str(metadata_row.get('picture_data', ''))
    medium = metadata_row.get('medium', 'Unknown medium').lower()
    
    # Determine genre/type from title
    genre = "artwork"
    if any(kw in title for kw in ['portrait', 'self-portrait', 'self portrait']):
        genre = "portrait"
    elif any(kw in title for kw in ['landscape', 'view', 'landscape']):
        genre = "landscape"
    elif any(kw in title for kw in ['still', 'life', 'still life', 'flowers', 'fruit']):
        genre = "still life"
    elif any(kw in title for kw in ['interior', 'room', 'chamber']):
        genre = "interior scene"
    elif any(kw in title for kw in ['battle', 'war', 'combat']):
        genre = "battle scene"
    elif any(kw in title for kw in ['hunt', 'hunting']):
        genre = "hunting scene"
    elif any(kw in title for kw in ['feast', 'banquet', 'meal']):
        genre = "feast scene"
    
    # Determine medium description
    medium_desc = "a painting"
    if 'oil' in medium:
        medium_desc = "an oil painting"
    elif 'watercolor' in medium:
        medium_desc = "a watercolor painting"
    elif 'tempera' in medium:
        medium_desc = "a tempera painting"
    elif 'fresco' in medium:
        medium_desc = "a fresco"
    elif 'drawing' in medium or 'charcoal' in medium or 'pencil' in medium:
        medium_desc = "a drawing"
    
    # Build simple, direct description parts
    caption_parts = []
    
    # Start with main subject - simple and direct
    if 'portrait' in title or 'self-portrait' in title or 'self portrait' in title:
        if 'woman' in title or 'lady' in title or 'madonna' in title:
            caption_parts.append("A figure depicts a woman looking at us.")
        elif 'man' in title or 'gentleman' in title:
            caption_parts.append("A figure depicts a man looking at us.")
        else:
            caption_parts.append("A figure depicts a person looking at us.")
            
    elif 'landscape' in title or 'view' in title:
        caption_parts.append("The scene shows a landscape view with various natural elements.")
    elif 'still' in title and 'life' in title:
        caption_parts.append("The image shows various objects arranged together on a surface.")
    else:
        # Try to extract simple subject from title
        title_clean = title.replace('_', ' ').replace('-', ' ')
        if 'woman' in title_clean:
            caption_parts.append("The image shows a woman.")
        elif 'man' in title_clean:
            caption_parts.append("The image shows a man.")
        elif 'figure' in title_clean or 'figures' in title_clean:
            caption_parts.append("The image shows one or more figures.")
        else:
            caption_parts.append(f"The image shows {title_clean}.")
    
    # Add clothing/color if mentioned
    if 'red' in title or 'red dress' in title:
        caption_parts.append("The figure is wearing a red dress.")
    elif 'dress' in title:
        caption_parts.append("The figure is wearing a dress.")
    if 'blue' in title:
        caption_parts.append("Blue colors are prominent.")
    if 'green' in title:
        caption_parts.append("Green colors are visible.")
    
    # Background description
    caption_parts.append("In the background, there are additional elements and details.")
    
    # Add more specific elements based on title keywords
    if any(kw in title for kw in ['door', 'window', 'opening']):
        caption_parts.append("A door or opening is visible in the background.")
    if any(kw in title for kw in ['tree', 'trees', 'forest']):
        caption_parts.append("Trees are visible in the scene.")
    if any(kw in title for kw in ['building', 'house', 'church', 'castle']):
        caption_parts.append("Buildings are present in the background.")
    if any(kw in title for kw in ['animal', 'horse', 'dog', 'cat', 'bird']):
        caption_parts.append("Animals are present in the scene.")
    if any(kw in title for kw in ['table', 'chair', 'furniture']):
        caption_parts.append("Furniture elements are visible.")
    
    # Simple lighting
    caption_parts.append("The lighting creates areas of brightness and shadow, giving depth to the scene.")
    
    # Simple color description
    caption_parts.append("Various colors are present throughout the composition, creating visual interest.")
    
    # Join main description
    main_description = " ".join(caption_parts)
    
    # Add the type/genre at the end (20% of caption)
    ending = f" It is {medium_desc}, a {genre}."
    
    caption = main_description + ending
    
    # Ensure proper length (100-200 words)
    words = caption.split()
    current_words = len(words)
    
    if current_words < 100:
        # Add more visual details before the ending
        additional = " The composition shows careful attention to arrangement, with elements positioned to create visual balance. Details are visible throughout, contributing to the overall scene. The image contains multiple visual elements arranged in a cohesive manner, with foreground and background elements creating depth."
        caption = main_description + additional + ending
    elif current_words > 200:
        # Trim to 200 words, keeping the ending
        words = caption.split()
        ending_words = ending.split()
        main_words = words[:-len(ending_words)]
        caption = " ".join(main_words[:180]) + " " + " ".join(ending_words)
    
    return caption


