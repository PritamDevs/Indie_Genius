import os
import time
import uuid
from datetime import datetime, timezone
import torch
from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler

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

        self.pipe.scheduler = EulerDiscreteScheduler.from_config(self.pipe.scheduler.config)
        
        self.pipe.to(self.device)
        self.pipe.enable_attention_slicing()
        print("[INFO] Model loaded and ready.")

    def execute(
        self,
        request: ImageGenerationRequest,
        output_dir: str = "outputs"
    ) -> ImageGenerationResponse:
        """
        Runs the capability, classifies failure modes explicitly (Step 7),
        saves the image, and logs the structured experiment record to JSON.
        """
        run_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now(timezone.utc).isoformat()
        start_time = time.perf_counter()
        error_category = None

        try:
            # 1. Model availability & loading check
            try:
                if self.pipe is None:
                    self.load_model()
            except Exception as load_exc:
                error_category = "MODEL_NOT_AVAILABLE"
                raise RuntimeError(f"Failed to load model: {load_exc}") from load_exc

            # 2. Inference execution check
            try:
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
            except Exception as inf_exc:
                error_category = "INFERENCE_FAILURE"
                raise RuntimeError(f"Model inference failed: {inf_exc}") from inf_exc

            execution_time = round(time.perf_counter() - start_time, 2)

            # 3. Output-writing check
            try:
                os.makedirs(output_dir, exist_ok=True)
                image = result.images[0]
                filename = f"{self.config.MODEL_NAME}_seed{request.seed}_{run_id}.png"
                output_path = os.path.join(output_dir, filename).replace("\\", "/")
                image.save(output_path)
            except Exception as io_exc:
                error_category = "OUTPUT_WRITING_FAILURE"
                raise OSError(f"Failed to write image to disk: {io_exc}") from io_exc

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
            category = error_category or "UNEXPECTED_EXCEPTION"
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
                error_message=f"[{category}] {type(exc).__name__}: {str(exc)}",
            )

        # Record every experiment to experiments/experiment_log.json (Step 8)
        log_experiment_run(response.model_dump())
        return response


if __name__ == "__main__":
    capability = ImageGenerationCapability()
    test_req = ImageGenerationRequest(
        prompt="cinematic interior of a small Kolkata apartment at night, warm tungsten practical lamp, monsoon rain on window, 35mm film grain",
        width=512,
        height=512,
        steps=8,
        seed=12345,
        observation="Baseline programmatic test of the Indie-Genius capability contract."
    )
    res = capability.execute(test_req)
    print(res.model_dump_json(indent=2))