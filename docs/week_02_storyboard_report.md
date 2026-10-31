# Indie-Genius: Week 02 Storyboard & Capability Engineering Report

**Project:** Indie-Genius Capability & Execution Layer  
**Assignment:** Verified Windows baseline, model evaluation, comic-storyboard experiments, and dynamic layout architecture (V2)  
**Repository:** `https://github.com/PritamDevs/Indie_Genius.git`  
**Branch:** `week-02-storyboard-experiments`  
**Baseline Commit:** `af47a91`  
**Execution Environment:** Windows 11 Home, AMD Ryzen 5 7520U (CPU-only execution), 15.6 GB System RAM, 512 MB Integrated Radeon UMA VRAM, PyTorch + CPU Diffusers pipeline.

---

## 1. Executive Summary
During Week 02, we verified our Windows CPU baseline environment, validated model licensing (`CreativeML Open RAIL-M`), and extended the local `ImageGenerationCapability` workflow to produce multi-panel visual storyboards. We executed two full 3-panel storyboard sequences—**The Minute Hand** (`INT. WATCH REPAIR SHOP — EVENING`) and **The Compilation Run** (`INT. DEVELOPER BEDROOM — 3:00 AM`)—performed a controlled before/after targeted revision experiment (Step 9), and engineered a universal, config-driven Python layout engine (`experiments/storyboard_engine.py`) capable of generating and stitching $1 \dots N$ panels into publication-ready storyboard sheets from JSON specifications.

Rather than masking model and hardware limitations, this report transparently documents all positive capabilities, negative failure modes, hardware restrictions, and software engineering fixes encountered during execution.

---

## 2. Hardware & Runtime Restrictions Faced
1. **512 MB Integrated VRAM Ceiling (No CUDA Acceleration):**
   - **Restriction:** The host machine operates on an AMD Ryzen 5 7520U with 512 MB integrated Radeon UMA memory. Standard GPU-accelerated Stable Diffusion pipelines (`torch.float16` on CUDA) and heavy auxiliary conditioning networks (SDXL, ControlNet, IP-Adapter, or multi-LoRA stacks) cannot fit in memory without triggering immediate Out-Of-Memory (OOM) crashes.
   - **Engineering Mitigation:** We restricted execution strictly to CPU (`torch.float32`) using `EulerDiscreteScheduler` and memory attention slicing within the 15.6 GB system RAM envelope.
2. **CPU Inference Latency Bottleneck:**
   - **Restriction:** Generating a single `512x512` panel at `8 steps` requires **~150 to 230 seconds (~2.5 to 3.8 minutes)** on CPU. Re-rolling panels to fix AI anatomical errors or scaling up to a 12-panel full storyboard sheet takes 30–60+ minutes of compute time.
   - **Mitigation:** Established a two-tier workflow: `256x256` at `4 steps` (~28 seconds/panel) for rapid draft verification and live demonstrations, and `512x512` at `8 steps` for final storyboard sheets.

---

## 3. Experimental Findings: Positives vs. Negatives

### 3.1 Positive Outcomes (What Worked Well)
- **Atmospheric Lighting & Composition:** Across both *The Minute Hand* and *The Compilation Run*, `CyberRealistic` (SD 1.5) excelled at rendering dramatic lighting setups—specifically warm tungsten desk lamps (`seed=20260702`), moody dark room interiors (`seed=20260801`), and backlit morning window steam (`seed=20260803`).
- **Prompt Framing to Bypass Anatomical Failure Modes:** After observing deformed hand geometry in *The Minute Hand* Panel 3 (`seed=20260703`), we deliberately engineered *The Compilation Run* Panel 1.3 (`seed=20260803`) to focus on environmental objects (steaming coffee mug and laptop edge at sunrise), resulting in a clean, artifact-free close-up.
- **Modular Config-Driven Architecture:** We replaced single-use hardcoded scripts with `experiments/storyboard_engine.py`, allowing any new stakeholder storyboard request to be generated and stitched via a standalone `.json` specification file without modifying Python code.

### 3.2 Negative Outcomes & Model Limitations (What Failed or Drifted)
1. **Photorealistic Style Leakage vs. True Comic Linework:**
   - **Issue:** Because `CyberRealistic` weights are heavily fine-tuned on photographic portraits and lens physics, prompting for `"Comic-book illustration, inked graphic-novel linework"` produced inconsistent style adherence.
   - **Evidence:** In *The Minute Hand*, all three panels retained glossy photographic lighting rather than 2D ink lines. In *The Compilation Run*, Panel 1.2 (`seed=20260802`) successfully rendered a stylized blue comic illustration of the developer, whereas Panels 1.1 and 1.3 rendered as photorealistic 3D rooms—creating a visual style mismatch across the same 3-panel strip.
2. **Fine Anatomy & Micro-Object Distortion (Hands & Clocks):**
   - **Issue:** Standard SD 1.5 at 8 steps struggles with fine articulated geometry and text/numerals.
   - **Evidence:** In *The Minute Hand* Panel 3 (`seed=20260703`), the subject's hand resting near the wristwatch exhibited an uneven, elongated forefinger and distorted watch-face internals. Similarly, in *The Compilation Run* Panel 1.2 (`seed=20260802`), the developer's fingers resting on the miniature keyboard were blurred/merged, and in Panel 1.1 (`seed=20260801`), the monitor remained black instead of displaying the requested red error logs.
3. **Cross-Panel Character & Environment Discontinuity:**
   - **Issue:** Because each panel is generated independently from text prompts without shared latent conditioning, character appearance and room geometry shift between shots.
   - **Evidence:** In *The Minute Hand*, the repairman in the wide establishing shot (`seed=20260701`) is a younger, thinner figure facing left in a dark jacket, whereas the medium shot (`seed=20260702`) renders an older South Asian man in a tan short-sleeved shirt facing right.

---

## 4. Step 9 Targeted Revision Experiment & Global Attention Drift

To test controlled scene editing, we executed `experiments/run_revision_test.py` on *The Minute Hand* Panel 2 (`seed=20260702`):

| Metric | Observation |
| :--- | :--- |
| **Baseline Artifact** | `outputs/cyberrealistic_seed20260702_73af710b.jpg` (`seed=20260702`) |
| **Revision Artifact** | `outputs/cyberrealistic_seed20260702_3ab13630.jpg` (`seed=20260702`) |
| **Targeted Prompt Edit** | Added `"with a clearly visible round analog wall clock mounted on the wooden wall directly above the workbench"` while keeping seed, steps, and character tokens identical. |
| **Target Achieved?** | **Partial / Inaccurate.** Circular wall plaques/frames appeared behind the lamp, but not a clean, legible analog clock face. |
| **Unintended Visual Drift** | **Severe.** Inserting new tokens into the prompt shifted the CLIP text embeddings and altered cross-attention maps at Step 1 of denoising: (1) Dev's shirt changed from tan to white; (2) his gray hair turned dark with a white beard; (3) the secondary desk lamp disappeared; and (4) background bookshelves morphed into framed wall pictures. |
| **Engineering Verdict** | Locking the random seed in text-to-image generation does **not** lock spatial layout when the prompt length changes. Production revisions require masked inpainting (`StableDiffusionInpaintPipeline`) or spatial conditioning (`ControlNet`). |

---

## 5. Layout & Stitching Tooling Evolution (Bugs Fixed)

During development of the Pillow (`PIL`) storyboard stitchers, we encountered and resolved three specific engineering defects:
1. **`ImportError: cannot import name 'Font' from 'PIL'`:** Fixed in `experiments/stitch_storyboard.py` by importing `ImageFont` instead of `Font`.
2. **Low-Contrast Dark Sheet Readability:** Our initial `minute_hand_storyboard_sheet.jpg` used a dark gray (`#1E1E1E`) background with small unbordered text. We upgraded the layout to a publication-ready white canvas (`#FFFFFF`) with `4px` black comic panel borders, structured header metadata, and bold shot titles (`minute_hand_professional_storyboard.jpg`).
3. **Multi-Row Grid Duplication Bug:** In `full_storyboard_multipanel_sheet.jpg`, hardcoding 6 shot slots against only 3 existing image prefixes caused Row 1 to duplicate onto Row 2. We fixed this in `stitch_multipanel_grid.py` and `storyboard_engine.py` using dynamic grid math (`cols = min(total, max_cols)`, `rows = math.ceil(total / cols)`) and `textwrap.fill(caption, width=52)` so the canvas scales to the exact number of unique panels ($1 \dots N$) with zero duplication.

---

## 6. Summary of Generated Artifacts & Deliverables
- **Documentation:** `docs/week_02_code_audit.md`, `docs/week_02_correction_log.md`, `docs/week_02_hardware.md`, `docs/week_02_environment_matrix.md`, `docs/week_02_baseline.md`, `docs/model_candidates.md`, `docs/week_02_storyboard_report.md`
- **Storyboards & Revision Sheets (in `outputs/`):**
  - *The Minute Hand* Panels (`ae801592`, `4fe0a94d`, `079a4ee5`) & Professional Sheet (`minute_hand_professional_storyboard.png`)
  - Step 9 Revision Pair (`73af710b` baseline vs. `3ab13630` revision)
  - *The Compilation Run* Sheet (`compilation_run_storyboard_sheet.png`)
- **Executable Pipeline & Summaries (in `experiments/`):**
  - `storyboard_engine.py` (Universal config/JSON-driven storyboard generator & auto-grid stitcher)
  - `run_minute_hand_storyboard.py`, `run_revision_test.py`, `stitch_multipanel_grid.py`
  - `minute_hand_storyboard_summary.json`, `compilation_run_summary.json`