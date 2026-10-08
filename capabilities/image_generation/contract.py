import json
import os
from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field


class ImageGenerationRequest(BaseModel):
    """
    Generic Input Contract for the Indie-Genius `image_generation` capability.
    Matches Step 6 & Step 7 validation requirements.
    """
    prompt: str = Field(
        ...,
        min_length=3,
        description="Cinematic description of the image to generate."
    )
    negative_prompt: str = Field(
        default="blurry, low quality, distorted, deformed, watermark, text",
        description="Elements to exclude from the generated image."
    )
    width: int = Field(
        default=512,
        ge=256,
        le=1024,
        multiple_of=64,
        description="Image width in pixels (must be a multiple of 64)."
    )
    height: int = Field(
        default=512,
        ge=256,
        le=1024,
        multiple_of=64,
        description="Image height in pixels (must be a multiple of 64)."
    )
    steps: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Number of denoising steps."
    )
    guidance_scale: float = Field(
        default=7.5,
        ge=1.0,
        le=20.0,
        description="Classifier-Free Guidance (CFG) scale."
    )
    seed: int = Field(
        default=12345,
        ge=0,
        description="Deterministic seed for reproducibility."
    )
    observation: Optional[str] = Field(
        default="Programmatic capability run.",
        description="Optional human/system observation for the experiment log."
    )


class ImageGenerationResponse(BaseModel):
    """
    Generic Output Contract for the Indie-Genius `image_generation` capability.
    Matches Step 6 & Step 8 metadata requirements for Film Brain.
    """
    status: str
    run_id: str
    timestamp: str
    capability: str = "image_generation"
    engine: str
    model: str
    model_version: str
    prompt: str
    negative_prompt: str
    seed: int
    width: int
    height: int
    steps: int
    guidance_scale: float
    hardware: str
    execution_time_seconds: float
    output_path: Optional[str] = None
    licence_reference: str
    observation: Optional[str] = None
    error_message: Optional[str] = None


def log_experiment_run(
    response_data: dict,
    log_file: str = "experiments/experiment_log.json"
) -> None:
    """
    Appends every capability run (success or failure) to a structured JSON array
    as required by Step 8 of the CTO Build Blueprint.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    records = []
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    records = json.loads(content)
        except json.JSONDecodeError:
            records = []

    records.append(response_data)

    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)