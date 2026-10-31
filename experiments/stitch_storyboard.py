"""
Indie-Genius: Professional Storyboard Sheet Generator
Creates a publication-ready comic layout with white background, black borders, 
and text caption blocks underneath each panel.
"""

import os
from PIL import Image, ImageDraw, ImageFont

def stitch_professional_storyboard():
    panel_bases = [
        ("cyberrealistic_seed20260701_ae801592", "SHOT 1.1: INT. WATCH REPAIR SHOP - EVENING\nRain ticks against the window. Wall clock reads 6:55."),
        ("cyberrealistic_seed20260702_4fe0a94d", "SHOT 1.2: CLOSE UP - DEV AT DESK\nDev works beneath a desk lamp, tightening a tiny screw."),
        ("cyberrealistic_seed20260703_079a4ee5", "SHOT 1.3: INSERT - THE WRISTWATCH\nAn old wristwatch wrapped in faded cloth rests between them.")
    ]

    images = []
    for base_name, caption in panel_bases:
        path = None
        for ext in [(".png", ".jpg", ".jpeg")]:
            # Check all supported extensions
            for e in [".png", ".jpg", ".jpeg"]:
                candidate = os.path.join("outputs", base_name + e)
                if os.path.exists(candidate):
                    path = candidate
                    break
            if path:
                break
        
        if path:
            img = Image.open(path).convert("RGB")
            images.append((img, caption))
        else:
            print(f"[WARNING] Panel image not found for base: {base_name}")

    if not images:
        print("[ERROR] No panel images found to stitch.")
        return

    # Layout dimensions
    panel_size = (512, 512)
    cols = len(images)
    padding = 30
    header_height = 100
    caption_box_height = 90

    grid_width = cols * panel_size[0] + (cols + 1) * padding
    grid_height = header_height + panel_size[1] + caption_box_height + (2 * padding)

    # Create professional white canvas
    canvas = Image.new("RGB", (grid_width, grid_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # Load font or fallback to default
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_caption = ImageFont.truetype("arial.ttf", 13)
    except Exception:
        font_title = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    # Draw Header Title & Subtitle
    draw.text((padding, 30), "THE MINUTE HAND — VISUAL STORYBOARD (COMIC STYLE)", fill=(20, 20, 20), font=font_title)
    draw.text((padding, 60), "Project: Indie-Genius | Engine: Local PyTorch Diffusers (CPU Pipeline)", fill=(100, 100, 100), font=font_caption)

    # Draw horizontal divider line
    draw.line([(padding, header_height - 10), (grid_width - padding, header_height - 10)], fill=(200, 200, 200), width=2)

    # Paste panels with comic borders
    for idx, (img, caption) in enumerate(images):
        img_resized = img.resize(panel_size)
        x = padding + idx * (panel_size[0] + padding)
        y = header_height + padding
        
        # Draw comic panel border (black outer box)
        border_width = 4
        draw.rectangle(
            [x - border_width, y - border_width, x + panel_size[0] + border_width, y + panel_size[1] + border_width],
            outline=(0, 0, 0), width=border_width
        )

        # Paste image
        canvas.paste(img_resized, (x, y))
        
        # Draw caption text box underneath
        text_y = y + panel_size[1] + 15
        draw.text((x, text_y), caption, fill=(40, 40, 40), font=font_caption)

    os.makedirs("outputs", exist_ok=True)
    output_sheet = "outputs/minute_hand_professional_storyboard.png"
    canvas.save(output_sheet)
    print(f"[SUCCESS] Professional storyboard sheet saved to {output_sheet}")

if __name__ == "__main__":
    stitch_professional_storyboard()