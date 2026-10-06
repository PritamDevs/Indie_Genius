# CyberRealistic Model Provenance Note

## 1. Source and Identity
- **Model Name:** CyberRealistic
- **Creator:** Cyberdelia
- **Base Architecture:** Stable Diffusion 1.5
- **Format:** .safetensors (V9 FP16)
- **Source URL:** https://huggingface.co/cyberdelia/CyberRealistic

## 2. Intended Use
Designed to produce highly photorealistic, cinematic-quality image outputs. It is optimized for portraits and editorial-style scenes.

## 3. Licence Considerations
- **Licence:** CreativeML Open RAIL-M.
- **Commercial Use:** Permitted, provided users adhere to the use-case restrictions.
- **Restrictions:** Strict prohibitions against generating illegal, harmful, or malicious content.

## 4. Hardware Suitability (Local)
Because the target machine lacks an NVIDIA GPU and has only 512MB of integrated VRAM, the SD 1.5 FP16 version (2.13GB) of this model must be used for CPU-bound inference. Using the SDXL variant will result in out-of-memory (OOM) failures.
