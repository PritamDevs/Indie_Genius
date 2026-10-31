"""
Indie-Genius: Dynamic Professional Storyboard Grid Stitcher
Dynamically builds a multi-row comic layout matching the exact number of panels provided,
with zero duplication.
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

def stitch_dynamic_grid():
    # Define ONLY the actual unique shots you want to display
    storyboard_shots = [
        ("cyberrealistic_seed20260701_ae801592", "SHOT 1.1: INT. REPAIR SHOP — EVENING\nEstablishing the antique shop and rain on windows."),
        ("cyberrealistic_seed20260702_4fe0a94d", "SHOT 1.2: CLOSE UP — DEV AT DESK\nDev works beneath a tungsten lamp with repair tools."),
        ("cyberrealistic_seed20260703_079a4ee5", "SHOT 1.3: INSERT — THE WRISTWATCH\nAn old wristwatch resting on wood between them."),
        ("cyberrealistic_seed20260702_3ab13630", "SHOT 1.4: REVISION TEST — WIDE WORKBENCH\nModified prompt adding wall framing above the workbench (demonstrating global drift).")
    ]

    loaded_panels = []
    for base_prefix, caption in storyboard_shots:
        path = None
        for filename in os.listdir("outputs"):
            if filename.startswith(base_prefix) and filename.endswith((".png", ".jpg", ".jpeg")):
                path = os.path.join("outputs", filename)
                break
        
        if path and os.path.exists(path):
            img = Image.open(path).convert("RGB")
            loaded_panels.append((img, caption))
        else:
            print(f"[WARNING] Asset not found for: {base_prefix}")

    if not loaded_panels:
        print("[ERROR] No panels available to stitch.")
        return

    # Dynamic layout calculation based on actual panel count
    total_panels = len(loaded_panels)
    cols = 3 if total_panels >= 3 else total_panels
    rows = math.ceil(total_panels / cols)
    
    panel_width = 380
    panel_height = 380
    padding = 35
    header_height = 110
    caption_height = 80

    grid_width = cols * panel_width + (cols + 1) * padding
    grid_height = header_height + rows * (panel_height + caption_height) + (rows + 1) * padding

    # Create crisp white canvas
    canvas = Image.new("RGB", (grid_width, grid_height), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype("arial.ttf", 24)
        font_subtitle = ImageFont.truetype("arial.ttf", 14)
        font_caption = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_caption = ImageFont.load_default()

    # Draw Header Metadata
    draw.text((padding, 30), "THE MINUTE HAND — A 3-4 MINUTE SHORT FILM", fill=(20, 20, 20), font=font_title)
    draw.text((padding, 65), f"VISUAL STORYBOARD SHEET ({total_panels}-PANEL SEQUENCE)", fill=(100, 100, 100), font=font_subtitle)
    draw.line([(padding, header_height - 15), (grid_width - padding, header_height - 15)], fill=(180, 180, 180), width=2)

    # Render panels dynamically
    for idx, (img, caption) in enumerate(loaded_panels):
        row = idx // cols
        col = idx % cols

        x = padding + col * (panel_width + padding)
        y = header_height + padding + row * (panel_height + caption_height + padding)

        img_resized = img.resize((panel_width, panel_height))

        # Draw bold black comic border
        border_width = 4
        draw.rectangle(
            [x - border_width, y - border_width, x + panel_width + border_width, y + panel_height + border_width],
            outline=(0, 0, 0), width=border_width
        )

        # Paste panel image
        canvas.paste(img_resized, (x, y))

        # Draw caption block underneath
        text_y = y + panel_height + 12
        draw.text((x, text_y), caption, fill=(30, 30, 30), font=font_caption)

    os.makedirs("outputs", exist_ok=True)
    output_path = "outputs/minute_hand_dynamic_storyboard.png"
    canvas.save(output_path)
    print(f"[SUCCESS] Dynamic storyboard sheet saved to {output_path}")

if __name__ == "__main__":
    stitch_dynamic_grid()