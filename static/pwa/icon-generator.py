#!/usr/bin/env python3
"""
Simple icon generator for PWA icons
Creates placeholder icons in different sizes
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, filename):
    """Create a simple icon with the OrganyxHub logo concept"""
    # Create image with green background
    img = Image.new('RGB', (size, size), '#3bb77e')
    draw = ImageDraw.Draw(img)
    
    # Draw a simple leaf/plant icon
    center = size // 2
    
    # Draw leaf shape
    leaf_size = size // 3
    leaf_points = [
        (center - leaf_size//2, center + leaf_size//2),
        (center - leaf_size//4, center - leaf_size//2),
        (center + leaf_size//4, center - leaf_size//2),
        (center + leaf_size//2, center + leaf_size//2)
    ]
    draw.polygon(leaf_points, fill='#ffffff')
    
    # Draw stem
    stem_width = max(2, size // 20)
    draw.rectangle([
        center - stem_width//2, 
        center + leaf_size//2, 
        center + stem_width//2, 
        center + leaf_size
    ], fill='#ffffff')
    
    # Add text for larger icons
    if size >= 128:
        try:
            font_size = max(12, size // 10)
            font = ImageFont.load_default()
            text = "OH"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = (size - text_width) // 2
            text_y = center + leaf_size + 10
            if text_y + text_height < size - 10:
                draw.text((text_x, text_y), text, fill='#ffffff', font=font)
        except:
            pass
    
    img.save(filename, 'PNG')
    print(f"Created {filename} ({size}x{size})")

def main():
    # Icon sizes for PWA
    sizes = [72, 96, 128, 144, 152, 192, 384, 512]
    
    # Create icons directory if it doesn't exist
    os.makedirs('/home/danmarques/Documentos/Workplace/organixhub-main/static/pwa', exist_ok=True)
    
    for size in sizes:
        filename = f'/home/danmarques/Documentos/Workplace/organixhub-main/static/pwa/icon-{size}x{size}.png'
        create_icon(size, filename)
    
    print("All PWA icons created successfully!")

if __name__ == "__main__":
    main()
