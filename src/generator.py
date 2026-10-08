import os
import time
import uuid
import torch
from diffusers import StableDiffusionPipeline

# Direct Hugging Face URL to the 2.13GB FP16 safetensors file
DEFAULT_MODEL_URL = (
    "https://huggingface.co/cyberdelia/CyberRealistic/blob/main/"
    "CyberRealistic_V9_FP16.safetensors"
)

class ImageGeneratorService:
    """
    Reusable capability wrapper around a local Diffusers pipeline.
    Can be instantiated with CyberRealistic or swapped for another SD 1.5 checkpoint.
    """
    def __init__(self, model_url: str = DEFAULT_MODEL_URL, device: str = "cpu"):
        self.model_url = model_url
        self.device = device
        self.pipe = None

    def load_model(self) -> None:
        """Loads the single-file safetensors checkpoint into the Diffusers pipeline."""
        if self.pipe is not None:
            return

        print(f"[INFO] Loading model from: {self.model_url}")
        print(f"[INFO] Target execution device: {self.device}")

        # Using float32 on CPU to prevent Half-precision LayerNorm errors
        self.pipe = StableDiffusionPipeline.from_single_file(
            self.model_url,
            torch_dtype=torch.float32,
            use_safetensors=True
        )
        self.pipe.to(self.device)
        
        # Slices attention computation into smaller steps to prevent CPU RAM exhaustion
        self.pipe.enable_attention_slicing()
        print("[INFO] Model loaded successfully.")

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "blurry, low quality, distorted, deformed",
        num_inference_steps: int = 20,
        guidance_scale: float = 7.5,
        width: int = 512,
        height: int = 512,
        seed: int = 42,
        output_dir: str = "outputs"
    ) -> dict:
        """
        Runs a reproducible inference pass, saves the image to disk,
        and returns structured metadata about the run.
        """
        if self.pipe is None:
            self.load_model()

        os.makedirs(output_dir, exist_ok=True)

        # PyTorch Generator locks the random noise to a specific seed for reproducibility
        generator = torch.Generator(device=self.device).manual_seed(seed)

        start_time = time.perf_counter()

        # Execute the diffusion denoising loop
        result = self.pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            num_inference_steps=num_inference_steps,
            guidance_scale=guidance_scale,
            width=width,
            height=height,
            generator=generator
        )

        execution_time = round(time.perf_counter() - start_time, 2)

        # Extract the PIL Image object and save to disk
        image = result.images[0]
        run_id = str(uuid.uuid4())[:8]
        filename = f"cyberrealistic_seed{seed}_{run_id}.png"
        output_path = os.path.join(output_dir, filename)
        image.save(output_path)

        # Return structured run metadata as required by the Week 01 Mission
        return {
            "status": "success",
            "run_id": run_id,
            "model": "CyberRealistic_V9_FP16.safetensors",
            "device": self.device,
            "prompt": prompt,
            "negative_prompt": negative_prompt,
            "seed": seed,
            "steps": num_inference_steps,
            "guidance_scale": guidance_scale,
            "resolution": f"{width}x{height}",
            "execution_time_seconds": execution_time,
            "output_path": output_path
        }


if __name__ == "__main__":
    # Day 3 CLI smoke test (using 5 steps initially to verify the pipeline quickly on CPU)
    service = ImageGeneratorService()
    metadata = service.generate(
        prompt="Cinematic medium shot of a detective standing in a rainy neon alleyway at night, 35mm lens, film grain",
        num_inference_steps=5,
        seed=1001
    )
    print("\n--- Structured Run Metadata ---")
    for key, value in metadata.items():
        print(f"{key}: {value}")