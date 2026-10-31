"""
Indie-Genius: Universal Config-Driven Storyboard Engine
Generates any N-panel storyboard from a simple dictionary/JSON spec and 
automatically stitches a publication-ready multi-row comic sheet.
"""

import json
import math
import os
import sys
import textwrap
from PIL import Image, ImageDraw, ImageFont

from capabilities.image_generation.contract import ImageGenerationRequest
from capabilities.image_generation.service import ImageGenerationCapability


def stitch_sheet(
    title: str,
    subtitle: str,
    panel_records: list[dict],
    output_sheet_path: str,
    max_cols: int = 3,
) -> str:
    """Dynamically stitches 1 to N panels into a multi-row white storyboard sheet."""
    loaded_panels = []
    for rec in panel_records:
        img_path = rec.get("output_path")
        if img_path and os.path.exists(img_path):
            img = Image.open(img_path).convert("RGB")
            loaded_panels.append((img, rec["shot_title"], rec["caption"]))
        else:
            print(f"[WARNING] Missing image file: {img_path}")

    if not loaded_panels:
        raise RuntimeError("No valid panel images found to stitch.")

    total = len(loaded_panels)
    cols = min(total, max_cols)
    rows = math.ceil(total / cols)

    panel_w, panel_h = 380, 380
    padding = 35
    header_h = 110
    caption_h = 100

    grid_w = cols * panel_w + (cols + 1) * padding
    grid_h = header_h + rows * (panel_h + caption_h) + (rows + 1) * padding

    canvas = Image.new("RGB", (grid_w, grid_h), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_sub = ImageFont.truetype("arial.ttf", 13)
        font_shot = ImageFont.truetype("arialbd.ttf", 12)
        font_cap = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font_title = font_sub = font_shot = font_cap = ImageFont.load_default()

    # Header block
    draw.text((padding, 28), title.upper(), fill=(15, 15, 15), font=font_title)
    draw.text(
        (padding, 62),
        f"{subtitle}  |  {total} Panels ({rows}x{cols} Auto-Grid)",
        fill=(100, 100, 100),
        font=font_sub,
    )
    draw.line(
        [(padding, header_h - 15), (grid_w - padding, header_h - 15)],
        fill=(180, 180, 180),
        width=2,
    )

    # Render each panel + border + wrapped caption
    for idx, (img, shot_title, caption) in enumerate(loaded_panels):
        row = idx // cols
        col = idx % cols

        x = padding + col * (panel_w + padding)
        y = header_h + padding + row * (panel_h + caption_h + padding)

        border = 4
        draw.rectangle(
            [x - border, y - border, x + panel_w + border, y + panel_h + border],
            outline=(0, 0, 0),
            width=border,
        )
        canvas.paste(img.resize((panel_w, panel_h)), (x, y))

        # Shot heading + wrapped caption text
        text_y = y + panel_h + 10
        draw.text((x, text_y), shot_title, fill=(15, 15, 15), font=font_shot)
        wrapped_caption = textwrap.fill(caption, width=52)
        draw.text((x, text_y + 18), wrapped_caption, fill=(45, 45, 45), font=font_cap)

    os.makedirs(os.path.dirname(output_sheet_path) or "outputs", exist_ok=True)
    canvas.save(output_sheet_path)
    return output_sheet_path


def run_storyboard_spec(spec: dict) -> None:
    """Runs generation for all panels in a storyboard spec and stitches the final sheet."""
    title = spec["title"]
    subtitle = spec.get("subtitle", "VISUAL STORYBOARD (COMIC STYLE)")
    slug = spec["slug"]
    panels = spec["panels"]

    print(f"=== Building Storyboard: {title} ({len(panels)} panels) ===")
    capability = ImageGenerationCapability()
    capability.load_model()

    records = []
    for idx, panel in enumerate(panels, start=1):
        print(f"\n[{idx}/{len(panels)}] Generating {panel['shot_title']}...")
        req = ImageGenerationRequest(
            prompt=panel["prompt"],
            negative_prompt=panel.get(
                "negative_prompt",
                "blurry, low quality, distorted, deformed, extra fingers, mutated hands, watermark, text",
            ),
            width=panel.get("width", 512),
            height=panel.get("height", 512),
            steps=panel.get("steps", 8),
            guidance_scale=panel.get("guidance_scale", 7.5),
            seed=panel.get("seed", 20260800 + idx),
            observation=f"[{slug}] {panel['shot_title']}: {panel['caption']}",
        )
        res = capability.execute(req)
        print(f" -> Saved: {res.output_path} ({res.execution_time_seconds}s)")

        records.append({
            "panel_index": idx,
            "shot_title": panel["shot_title"],
            "caption": panel["caption"],
            "prompt": panel["prompt"],
            "seed": req.seed,
            "run_id": res.run_id,
            "output_path": res.output_path,
            "execution_time_seconds": res.execution_time_seconds,
        })

    # 1. Save JSON manifest of the storyboard
    manifest_path = f"experiments/{slug}_summary.json"
    os.makedirs("experiments", exist_ok=True)
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({"title": title, "slug": slug, "panels": records}, f, indent=2)

    # 2. Automatically stitch the professional sheet
    sheet_path = f"outputs/{slug}_storyboard_sheet.png"
    stitch_sheet(title, subtitle, records, sheet_path, max_cols=spec.get("max_cols", 3))
    print(f"\n[SUCCESS] Summary JSON: {manifest_path}")
    print(f"[SUCCESS] Final Storyboard Sheet: {sheet_path}")


# =====================================================================
# STORYBOARD PRESETS (Edit this or pass a custom .json file via CLI!)
# =====================================================================
PRESET_STORYBOARDS = {
    "compilation_run": {
        "title": "THE COMPILATION RUN — A LATE-NIGHT DEBUGGING SHORT",
        "subtitle": "INT. DEVELOPER BEDROOM — 3:00 AM (COMIC STORYBOARD)",
        "slug": "compilation_run",
        "max_cols": 3,
        "panels": [
            {
                "shot_title": "1.1 ESTABLISHING SHOT — INT. BEDROOM — 3:00 AM",
                "caption": "Dark room lit by a glowing ultrawide monitor showing terminal logs. A coffee mug sits beside the keyboard.",
                "prompt": "Comic-book illustration, wide shot of a dark bedroom desk at night illuminated by a glowing computer monitor and warm desk lamp, coffee mug on wooden desk, clean inked graphic-novel linework, dramatic lighting, no text",
                "seed": 20260801,
                "steps": 8,
            },
            {
                "shot_title": "1.2 MEDIUM SHOT — THE DEVELOPER",
                "caption": "A tired young software engineer leans forward in glasses, inspecting a broken service trace on screen.",
                "prompt": "Comic-book illustration, medium portrait of a focused young Indian software engineer wearing glasses looking at a glowing computer screen at night, warm tungsten key light, cool blue monitor rim light, graphic-novel inked style, no text",
                "seed": 20260802,
                "steps": 8,
            },
            {
                "shot_title": "1.3 CLOSE UP — SUNRISE & CLEAN BUILD",
                "caption": "Dawn light enters the window behind the desk. A fresh steaming cup of black coffee rests beside the quiet laptop.",
                "prompt": "Comic-book illustration, close-up of a steaming black coffee mug next to a sleek laptop on a wooden desk by a window at golden dawn sunrise, peaceful atmosphere, crisp inked graphic-novel style, no text",
                "seed": 20260803,
                "steps": 8,
            },
        ],
    }
}


if __name__ == "__main__":
    # Usage 1: python -m experiments.storyboard_engine
    # Usage 2: python -m experiments.storyboard_engine experiments/custom_storyboard.json
    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            custom_spec = json.load(f)
        run_storyboard_spec(custom_spec)
    else:
        preset_name = sys.argv[1] if len(sys.argv) > 1 else "compilation_run"
        run_storyboard_spec(PRESET_STORYBOARDS[preset_name])