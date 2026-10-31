"""
Indie-Genius: Step 9 Targeted Revision Experiment
Tests object addition (round wall clock) and measures unintended visual drift.
"""

import os
from capabilities.image_generation.contract import ImageGenerationRequest
from capabilities.image_generation.service import ImageGenerationCapability

def run_revision():
    print("=== Starting Step 9 Targeted Revision Experiment ===")
    capability = ImageGenerationCapability()
    capability.load_model()

    # Original prompt (Panel 2 baseline)
    original_prompt = (
        "Comic-book illustration, 60-year-old Indian man working beneath a desk lamp "
        "in a crowded watch repair shop, magnifying eyepiece, vintage tools, "
        "inked graphic-novel linework, no text"
    )

    # Revision prompt (Adding a wall clock above workbench while keeping characters/lamp)
    revision_prompt = (
        "Comic-book illustration, 60-year-old Indian man working beneath a desk lamp "
        "in a crowded watch repair shop, with a clearly visible round analog wall clock "
        "mounted on the wooden wall directly above the workbench, magnifying eyepiece, "
        "vintage tools, inked graphic-novel linework, no text"
    )

    seed = 20260702  # Same seed as Panel 2 to measure drift

    print("\n[1/2] Generating Baseline Reference...")
    req_orig = ImageGenerationRequest(
        prompt=original_prompt,
        negative_prompt="blurry, low quality, distorted, deformed, watermark, text",
        width=512, height=512, steps=8, guidance_scale=7.5, seed=seed,
        observation="Revision Baseline: Original Panel 2 prompt."
    )
    res_orig = capability.execute(req_orig)
    print(f" -> Baseline saved to: {res_orig.output_path}")

    print("\n[2/2] Generating Revision Artifact (Adding Wall Clock)...")
    req_rev = ImageGenerationRequest(
        prompt=revision_prompt,
        negative_prompt="blurry, low quality, distorted, deformed, watermark, text",
        width=512, height=512, steps=8, guidance_scale=7.5, seed=seed,
        observation="Revision Test: Added round wall clock above workbench."
    )
    res_rev = capability.execute(req_rev)
    print(f" -> Revision saved to: {res_rev.output_path}")

    print("\n=== Revision Experiment Complete! Compare both outputs in outputs/ ===")

if __name__ == "__main__":
    run_revision()