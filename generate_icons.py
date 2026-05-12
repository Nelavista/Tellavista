#!/usr/bin/env python3
"""
generate_icons.py
Generate all required PWA icons for Nelavista.
Run: python generate_icons.py
"""

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("❌ Pillow not installed. Installing...")
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image, ImageDraw, ImageFont

def create_icon(size, filename, is_favicon=False):
    """Create a single PWA icon."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for i in range(size):
        color = (
            int(56 + (i / size) * 20),    # R
            int(189 - (i / size) * 40),   # G
            int(248 - (i / size) * 50),   # B
            255
        )
        draw.rectangle([0, i, size, i + 1], fill=color)
    
    # Draw rounded rectangle background
    margin = size // 8
    radius = max(size // 6, 4)
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        fill=(5, 8, 16, 230)
    )
    
    # Draw 'N' text
    try:
        # Try multiple font paths
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
            "C:\\Windows\\Fonts\\Arial.ttf",
        ]
        
        font = None
        font_size = max(size // 2, 10)
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, font_size)
                    break
                except:
                    continue
        
        if font is None:
            font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    
    # Center the 'N'
    text = 'N'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(56, 189, 248, 255), font=font)
    
    # Add border
    draw.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=radius,
        outline=(56, 189, 248, 80),
        width=max(1, size // 50)
    )
    
    # Add shine for larger icons
    if size >= 72:
        shine_margin = size // 3
        draw.ellipse(
            [shine_margin, shine_margin,
             size - shine_margin, size - shine_margin],
            outline=(255, 255, 255, 40),
            width=max(1, size // 80)
        )
    
    # Save
    if is_favicon:
        img.save(filename, 'ICO', sizes=[(size, size)])
    else:
        img.save(filename, 'PNG')
    
    return True

def create_maskable_icon(size, filename):
    """Create maskable icon with safe zone padding."""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Safe zone (80% of icon for maskable)
    safe_margin = int(size * 0.1)
    icon_size = size - (2 * safe_margin)
    
    # Draw gradient in safe zone
    for i in range(icon_size):
        color = (
            int(56 + (i / icon_size) * 20),
            int(189 - (i / icon_size) * 40),
            int(248 - (i / icon_size) * 50),
            255
        )
        draw.rectangle(
            [safe_margin, safe_margin + i,
             size - safe_margin, safe_margin + i + 1],
            fill=color
        )
    
    # Draw 'N'
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            icon_size // 2
        )
    except:
        font = ImageFont.load_default()
    
    text = 'N'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, fill=(56, 189, 248, 255), font=font)
    
    img.save(filename, 'PNG')
    return True

def generate_all_icons():
    """Generate all required PWA icons."""
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(script_dir, 'static', 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    print("🎨 Nelavista PWA Icon Generator")
    print("=" * 50)
    
    # Standard icon sizes
    sizes = {
        16: 'favicon',
        32: 'favicon',
        72: 'icon',
        96: 'icon',
        120: 'apple',
        128: 'icon',
        144: 'icon',
        152: 'apple',
        167: 'apple',
        180: 'apple',
        192: 'icon',
        384: 'icon',
        512: 'icon'
    }
    
    generated = 0
    skipped = 0
    
    for size, icon_type in sizes.items():
        if icon_type == 'favicon':
            filename = os.path.join(icons_dir, f'favicon.ico')
            if not os.path.exists(filename):
                if create_icon(size, filename, is_favicon=True):
                    print(f'✅ Created favicon ({size}x{size})')
                    generated += 1
                else:
                    print(f'❌ Failed to create favicon')
        
        filename = os.path.join(icons_dir, f'nelavista-{size}x{size}.png')
        
        if os.path.exists(filename):
            print(f'⏭️  Skipped {size}x{size} (already exists)')
            skipped += 1
            continue
        
        if create_icon(size, filename):
            print(f'✅ Created {size}x{size} icon')
            generated += 1
        else:
            print(f'❌ Failed to create {size}x{size} icon')
    
    # Create maskable icons
    for maskable_size in [192, 384, 512]:
        maskable_filename = os.path.join(
            icons_dir, 
            f'nelavista-maskable-{maskable_size}x{maskable_size}.png'
        )
        
        if os.path.exists(maskable_filename):
            print(f'⏭️  Skipped maskable {maskable_size}x{maskable_size} (already exists)')
            skipped += 1
            continue
        
        if create_maskable_icon(maskable_size, maskable_filename):
            print(f'✅ Created maskable {maskable_size}x{maskable_size} icon')
            generated += 1
    
    print("=" * 50)
    print(f'🎉 Done! Generated: {generated}, Skipped: {skipped}')
    print(f'📁 Icons location: {icons_dir}')
    print("\n📋 Next steps:")
    print("   1. Verify icons in static/icons/")
    print("   2. Test PWA at http://localhost:5000")
    print("   3. Run Lighthouse PWA audit in Chrome DevTools")

if __name__ == '__main__':
    generate_all_icons()
