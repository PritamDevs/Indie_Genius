# Experiment Log

## Baseline Experiment (Day 2)
**Goal:** Run CyberRealistic manually in DiffusionBee to establish baseline metrics (time, VRAM usage, output quality).
**Result:** FAILED (Environment Constraint)
**Reason:** The official DiffusionBee application is exclusive to macOS (.dmg distributable). Our local development environment is Windows.
**Next Steps:** Baseline metrics will instead be established programmatically on Day 3 using the Hugging Face Diffusers library configured for CPU execution.

## Experiment 01: Day 3 Programmatic CPU Smoke Test
- **Model:** CyberRealistic_V9_FP16.safetensors (loaded in float32)
- **Device:** CPU (AMD Radeon Integrated Host)
- **Prompt:** Cinematic medium shot of a detective standing in a rainy neon alleyway at night, 35mm lens, film grain
- **Seed:** 1001
- **Steps:** 5
- **Guidance Scale:** 7.5
- **Resolution:** 512x512
- **Execution Time:** <YOUR_TIME> seconds
- **Result:** SUCCESS. Model unpacked via from_single_file() and saved PNG artifact to outputs/ directory.
