# Week 02 — Step 5: Model Candidate Shortlist (`docs/model_candidates.md`)

**Repository:** `https://github.com/PritamDevs/Indie_Genius.git`  
**Branch:** `week-02-storyboard-experiments`  
**Baseline Commit:** `af47a91`  

---

## Candidate 1: CyberRealistic V9 FP16 (Baseline Photorealistic Checkpoint)
- **Model Page URL:** [Hugging Face - CyberRealistic](https://huggingface.co/cyberdelia/CyberRealistic)
- **Creator:** Cyberdelia
- **Exact File Name & Version:** `CyberRealistic_V9_FP16.safetensors` (Stable Diffusion 1.5)
- **File Size:** ~2.13 GB
- **Base Architecture:** Stable Diffusion 1.5 (Full Checkpoint)
- **Licence & Usage Restrictions:** Governed by the **CreativeML Open RAIL-M** licence. Free for commercial and non-commercial use with safety moderation requirements.
- **Dependencies & Backend Compatibility:** Fully compatible with our existing `StableDiffusionPipeline.from_single_file()` loader and `EulerDiscreteScheduler` execution path on CPU.
- **Observed Performance & Limitations:** Generates high-fidelity photographic textures but tends to bias toward photographic lighting and skin textures rather than stylized comic-book ink lines when prompted for graphic-novel aesthetics.

---

## Candidate 2: Comic-Diffusion (Dedicated Graphic-Novel Checkpoint)
- **Model Page URL:** [Hugging Face - ogkalu/Comic-Diffusion](https://huggingface.co/ogkalu/Comic-Diffusion)
- **Creator:** ogkalu
- **Exact File Name & Version:** `comicDiffusion_v1.safetensors` (or standard hub variant) / Stable Diffusion 1.5
- **File Size:** ~2.0 GB
- **Base Architecture:** Stable Diffusion 1.5 (Full Checkpoint fine-tuned on comic illustration datasets)
- **Licence & Usage Restrictions:** CreativeML Open RAIL-M / Open Source community model terms.
- **Dependencies & Backend Compatibility:** Compatible with SD 1.5 single-file loading (`from_single_file`) and our CPU `torch.float32` pipeline.
- **Reason for Selection:** Designed specifically for comic book linework, dramatic graphic-novel shading, and panel readability, directly aligning with the visual target of *THE MINUTE HAND* storyboard.