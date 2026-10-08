from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from capabilities.image_generation.contract import (
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from capabilities.image_generation.service import ImageGenerationCapability

app = FastAPI(
    title="Indie-Genius Capability Runner API",
    description="Week 01 Local AI Capability Interface exposing image_generation.",
    version="0.1.0",
)

# Single instance holds the pipeline in memory across requests once loaded
capability_runner = ImageGenerationCapability()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    """
    Handles Missing prompt, Invalid dimensions, and Invalid numeric settings (Step 7)
    by returning a structured, human-readable HTTP 422 error payload.
    """
    errors = []
    for err in exc.errors():
        field_path = " -> ".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "field": field_path,
            "issue": err.get("msg"),
            "type": err.get("type"),
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "validation_error",
            "capability": "image_generation",
            "message": "Invalid input parameters provided to capability contract.",
            "details": errors,
        },
    )


@app.get("/health")
def health_check():
    """
    Lightweight readiness check verifying service status and whether the model
    is currently loaded into memory.
    """
    return {
        "status": "ok",
        "service": "indie-genius-capability-runner",
        "capability": "image_generation",
        "model": capability_runner.config.MODEL_NAME,
        "model_loaded_in_memory": capability_runner.pipe is not None,
    }


@app.post(
    "/capabilities/image/generate",
    response_model=ImageGenerationResponse,
    summary="Execute the image_generation capability",
)
def generate_image(request: ImageGenerationRequest):
    """
    Step 6 & Step 7 Capability Endpoint:
    Validates input contract, runs local Diffusers inference, saves the image,
    logs the experiment to JSON, and returns structured run metadata.
    """
    response = capability_runner.execute(request)

    if response.status == "error":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=response.model_dump(),
        )

    return response