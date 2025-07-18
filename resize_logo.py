#!/usr/bin/env python3
"""Resize logo for web use."""

try:
    from PIL import Image
    import os
    
    # Open the original logo
    logo_path = "static/TravelAigent_logo.png"
    if not os.path.exists(logo_path):
        print("❌ Logo file not found!")
        exit(1)
    
    # Open and resize
    img = Image.open(logo_path)
    print(f"Original size: {img.size}")
    
    # Create a smaller version for header use (height 72px for retina displays)
    header_size = (72, 72)
    img_header = img.resize(header_size, Image.Resampling.LANCZOS)
    img_header.save("static/TravelAigent_logo_header.png", optimize=True)
    print(f"✅ Created header logo: {header_size}")
    
    # Get file sizes
    original_size = os.path.getsize(logo_path) / 1024 / 1024
    header_size = os.path.getsize("static/TravelAigent_logo_header.png") / 1024
    
    print(f"\n📊 File sizes:")
    print(f"  Original: {original_size:.2f} MB")
    print(f"  Header: {header_size:.2f} KB")
    
except ImportError:
    print("❌ PIL/Pillow not installed. Install with: pip install Pillow")
    print("For now, you can manually resize the logo to 72x72 pixels")
except Exception as e:
    print(f"❌ Error: {e}")