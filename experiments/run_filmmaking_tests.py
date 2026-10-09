from capabilities.image_generation.contract import ImageGenerationRequest
from capabilities.image_generation.service import ImageGenerationCapability

# Step 9 Filmmaking Use Cases (Use Case #2 - Interior Concept was already completed in Runs 1 & 2)
FILMMAKING_TEST_CASES = [
    {
        "category": "1. Screenplay / Location Reference",
        "request": ImageGenerationRequest(
            prompt="Cinematic wide shot of a narrow North Kolkata alleyway at dawn, wet cobblestones after rain, morning mist, colonial shutters, 24mm lens, natural diffused light",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=202601,
            observation="[Location Reference] Useful for a director and location scout to align on atmospheric mood, lens perspective, and morning lighting contrast before physical scouting."
        ),
    },
    {
        "category": "3. Character / Wardrobe Reference",
        "request": ImageGenerationRequest(
            prompt="Medium close-up portrait of a tired 40-year-old Indian investigative journalist wearing a faded olive cotton jacket and rain-stained collared shirt, 50mm anamorphic lens, shallow depth of field",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=202603,
            observation="[Character/Wardrobe Reference] Highly useful for costume design and casting lookbooks; CyberRealistic excels at fabric texture, skin tones, and shallow depth-of-field portraits."
        ),
    },
    {
        "category": "4. Production-Design / Prop Concept",
        "request": ImageGenerationRequest(
            prompt="Macro product shot of a weathered 1970s brass rotary telephone beside a coffee-stained leather notebook and fountain pen on a dark teak desk, warm desk lamp key light",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=202604,
            observation="[Prop Concept] Useful for the art department and prop master to visualize hero prop aging, patina, and color palette integration under tungsten lighting."
        ),
    },
    {
        "category": "5. Background / Set-Extension Plate",
        "request": ImageGenerationRequest(
            prompt="Locked-off wide shot of an overcast industrial city skyline seen from a rooftop edge at dusk, distant sodium vapor streetlamps, clean horizon line, matte painting plate style, no people",
            width=512,
            height=512,
            steps=8,
            guidance_scale=7.5,
            seed=202605,
            observation="[Set-Extension Plate] Useful as a concept plate or blurred background outside a window on set, though 512x512 base resolution requires an upscaling workflow (e.g., ComfyUI) for final VFX compositing."
        ),
    },
    {
        "category": "6. Difficult / Imperfect Prompt Control (Failure Mode Analysis)",
        "request": ImageGenerationRequest(
            prompt="Two actors shaking hands across a glass table while holding a wooden film clapperboard with clear readable text saying SCENE 42 TAKE 3, ten fingers visible",
            width=512,
            height=512,
            steps=8,
            guidance_scale=8.5,
            seed=202606,
            observation="[Imperfect Control Case] Limited direct usefulness without inpainting; exposes SD 1.5 architectural failure modes on multi-hand interactions (deformed/merged fingers) and garbled text rendering on the clapperboard."
        ),
    },
]

def run_suite():
    print("=== Starting Indie-Genius Week 01 Filmmaking Test Suite ===")
    capability = ImageGenerationCapability()
    capability.load_model()

    for idx, item in enumerate(FILMMAKING_TEST_CASES, start=1):
        print(f"\n[{idx}/{len(FILMMAKING_TEST_CASES)}] Running: {item['category']}...")
        response = capability.execute(item["request"])
        print(
            f" -> Status: {response.status} | "
            f"Time: {response.execution_time_seconds}s | "
            f"Saved: {response.output_path}"
        )

    print("\n=== All Filmmaking Tests Complete! Logged to experiments/experiment_log.json ===")

if __name__ == "__main__":
    run_suite()