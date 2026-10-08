import os
import time
import uuid
from datetime import datetime, timezone
import torch
from diffusers import StableDiffusionPipeline

from capabilities.image_generation.contract import (
    ImageGenerationRequest,
    ImageGenerationResponse,
    log_experiment_run,
)


class CyberRealisticConfig:
    """
    Model-specific configuration isolated from the capability execution logic.
    If CyberRealistic is replaced next month, only this configuration/adapter changes.
    """
    MODEL_NAME = "cyberrealistic"
    MODEL_VERSION = "V9_FP16 (SD 1.5)"
    MODEL_URL = (
        "https://huggingface.co/cyberdelia/CyberRealistic/blob/main/"
        "CyberRealistic_V9_FP16.safetensors"
    )
    LICENCE_REF = "CreativeML Open RAIL-M (docs/model_card_cyberrealistic.md)"


class ImageGenerationCapability:
    """
    Executes the `image_generation` capability using Hugging Face Diffusers
    and returns a structured `ImageGenerationResponse` while recording every run.
    """
    def __init__(self, config=CyberRealisticConfig, device: str = "cpu"):
        self.config = config
        self.device = device
        self.hardware_desc = "Windows CPU (AMD Radeon Integrated Host, 512MB VRAM)"
        self.pipe = None

    def load_model(self) -> None:
        """Loads the model into memory if not already loaded."""
        if self.pipe is not None:
            return

        print(f"[INFO] Loading {self.config.MODEL_NAME} ({self.config.MODEL_VERSION})...")
        self.pipe = StableDiffusionPipeline.from_single_file(
            self.config.MODEL_URL,
            torch_dtype=torch.float32,
            use_safetensors=True
        )
        self.pipe.to(self.device)
        self.pipe.enable_attention_slicing()
        print("[INFO] Model loaded and ready.")

    def execute(
        self,
        request: ImageGenerationRequest,
        output_dir: str = "outputs"
    ) -> ImageGenerationResponse:
        """
        Runs the capability, handles errors gracefully, saves the image,
        and logs the structured experiment record to JSON.
        """
        run_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now(timezone.utc).isoformat()
        start_time = time.perf_counter()

        try:
            if self.pipe is None:
                self.load_model()

            os.makedirs(output_dir, exist_ok=True)
            generator = torch.Generator(device=self.device).manual_seed(request.seed)

            result = self.pipe(
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                num_inference_steps=request.steps,
                guidance_scale=request.guidance_scale,
                width=request.width,
                height=request.height,
                generator=generator,
            )

            execution_time = round(time.perf_counter() - start_time, 2)

            image = result.images[0]
            filename = f"{self.config.MODEL_NAME}_seed{request.seed}_{run_id}.png"
            output_path = os.path.join(output_dir, filename).replace("\\", "/")
            image.save(output_path)

            response = ImageGenerationResponse(
                status="success",
                run_id=run_id,
                timestamp=timestamp,
                capability="image_generation",
                engine="diffusers",
                model=self.config.MODEL_NAME,
                model_version=self.config.MODEL_VERSION,
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                seed=request.seed,
                width=request.width,
                height=request.height,
                steps=request.steps,
                guidance_scale=request.guidance_scale,
                hardware=self.hardware_desc,
                execution_time_seconds=execution_time,
                output_path=output_path,
                licence_reference=self.config.LICENCE_REF,
                observation=request.observation,
            )

        except Exception as exc:
            execution_time = round(time.perf_counter() - start_time, 2)
            response = ImageGenerationResponse(
                status="error",
                run_id=run_id,
                timestamp=timestamp,
                capability="image_generation",
                engine="diffusers",
                model=self.config.MODEL_NAME,
                model_version=self.config.MODEL_VERSION,
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                seed=request.seed,
                width=request.width,
                height=request.height,
                steps=request.steps,
                guidance_scale=request.guidance_scale,
                hardware=self.hardware_desc,
                execution_time_seconds=execution_time,
                output_path=None,
                licence_reference=self.config.LICENCE_REF,
                observation=request.observation,
                error_message=f"{type(exc).__name__}: {str(exc)}",
            )

        # Record every experiment to experiments/experiment_log.json (Step 8)
        log_experiment_run(response.model_dump())
        return response


if __name__ == "__main__":
    # Verify the new capability contract and automated JSON logger
    capability = ImageGenerationCapability()
    test_req = ImageGenerationRequest(
        prompt="cinematic interior of a small Kolkata apartment at night, warm tungsten practical lamp, monsoon rain on window, 35mm film grain",
        width=512,
        height=512,
        steps=5,
        seed=12345,
        observation="Baseline programmatic test of the Indie-Genius capability contract."
    )
    res = capability.execute(test_req)
    print(res.model_dump_json(indent=2))