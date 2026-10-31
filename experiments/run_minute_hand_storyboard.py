
"""
Indie-Genius: The Minute Hand Storyboard Experiment (Step 6 & 7)
Human Software Engineer Style: Clean, crisp, single-responsibility execution.
"""

import json
import os
from capabilities.image_generation.contract import ImageGenerationRequest
from capabilities.image_generation.service import ImageGenerationCapability

MINUTE_HAND_PANELS = [
    {
        "panel_id": "panel_01_establishing",
        "beat": "Establish the shop, rain, and wall clock at 6:55",
        "request": ImageGenerationRequest(
            prompt="Comic-book illustration, interior of a small old watch repair shop on a rainy evening, warm desk lamp, wall clock reading 6:55, shelves of watch parts, inked graphic-novel linework, restrained palette, no text",
            negative_prompt="blurry, low quality, distorted, deformed, watermark, text",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=20260701,
            observation="Storyboard Panel 1: Establishing shop and clock."
        )
    },
    {
        "panel_id": "panel_02_action",
        "beat": "Dev working beneath desk lamp, screw slips",
        "request": ImageGenerationRequest(
            prompt="Comic-book illustration, 60-year-old Indian man working beneath a desk lamp in a crowded watch repair shop, magnifying eyepiece, vintage tools, inked graphic-novel linework, no text",
            negative_prompt="blurry, low quality, distorted, deformed, watermark, text",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=20260702,
            observation="Storyboard Panel 2: Character action and desk setup."
        )
    },
    {
        "panel_id": "panel_03_reveal",
        "beat": "Old wristwatch revealed between them on the desk",
        "request": ImageGenerationRequest(
            prompt="Comic-book illustration, close-up of an old vintage wristwatch resting on a wooden desk between two people, warm tungsten lighting, inked graphic-novel linework, no text",
            negative_prompt="blurry, low quality, distorted, deformed, watermark, text",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=20260703,
            observation="Storyboard Panel 3: Watch reveal and emotional pause."
        )
    }
]

def run_storyboard():
    print("=== Starting THE MINUTE HAND Storyboard Generation ===")
    capability = ImageGenerationCapability()
    capability.load_model()

    results_summary = []

    for idx, panel in enumerate(MINUTE_HAND_PANELS, start=1):
        print(f"\n[{idx}/{len(MINUTE_HAND_PANELS)}] Generating {panel['panel_id']}: {panel['beat']}...")
        response = capability.execute(panel["request"])
        
        print(f" -> Status: {response.status} | Time: {response.execution_time_seconds}s | Saved: {response.output_path}")
        results_summary.append({
            "panel_id": panel["panel_id"],
            "beat": panel["beat"],
            "run_id": response.run_id,
            "output_path": response.output_path,
            "execution_time_seconds": response.execution_time_seconds
        })

    # Save summary plan log
    plan_path = "experiments/minute_hand_storyboard_summary.json"
    os.makedirs("experiments", exist_ok=True)
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(results_summary, f, indent=2, ensure_ascii=False)

    print(f"\n=== Storyboard Complete! Summary saved to {plan_path} ===")

if __name__ == "__main__":
    run_storyboard()