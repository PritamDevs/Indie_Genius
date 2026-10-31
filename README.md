# Indie-Genius: AI Capability & Storyboard Runner (Week 01 – Week 02)

This repository is the foundational engineering prototype for **Indie-Genius**. It wraps a local AI image-generation pipeline (`CyberRealistic` / Stable Diffusion 1.5) into a programmatic, reproducible **FastAPI capability contract** and a **Config-Driven Multi-Panel Storyboard Engine**, bypassing manual desktop GUIs.

---

## 💻 Hardware Compatibility & Requirements

This project is explicitly engineered to run reliably on standard consumer hardware without requiring a dedicated NVIDIA CUDA GPU.

- **OS:** Windows 11, macOS, or Linux.
- **Compute:** Verified on Windows 11 with an AMD Ryzen 5 7520U and integrated AMD Radeon Graphics (512 MB UMA VRAM) utilizing `torch.float32` CPU execution and memory attention slicing.
- **Architecture Note:** We use the `EulerDiscreteScheduler` to achieve clean image convergence in `4–8 steps` on CPU, preventing the noise/NaN artifacts common with default schedulers on low-step CPU runs.
- **Storage:** Requires at least **~3 GB of free disk space** (the Hugging Face Diffusers pipeline caches the `~2.13 GB` model weights on initial execution).
- **Software:** Python 3.10+ (tested on Python 3.14), Git.

---

## 🚀 Quickstart: Installation

Do not install dependencies globally. Always use a Python virtual environment to ensure dependency isolation and reproducibility.

### 1. Clone the repository and enter the directory:
```powershell
git clone [https://github.com/PritamDevs/Indie_Genius.git](https://github.com/PritamDevs/Indie_Genius.git)
cd Indie_Genius
```

### 2. Create and activate a Python virtual environment:
**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies:
```powershell
pip install -r requirements.txt
```

---

## ⚙️ How to Run and Test the System

> ⚠️ **CRITICAL PATHING NOTE:** Always run Python scripts from the root `Indie_Genius` directory using the `-m` module flag so internal package imports resolve cleanly.

### 1. Start the Live API Server (FastAPI / Uvicorn)
To run the capability as a local HTTP microservice:
```powershell
uvicorn backend.api:app --host 127.0.0.1 --port 8000
```
- **Interactive Swagger UI:** Open `http://127.0.0.1:8000/docs` in your browser to test endpoints visually.
- **Readiness Health Check:** `GET http://127.0.0.1:8000/health`

### 2. Run the Automated API Validation Suite
To verify that the Pydantic capability contract catches and rejects invalid dimensions, missing prompts, and out-of-range parameters:
```powershell
python -m pytest tests/test_api.py -v
```

### 3. Generate Multi-Panel Storyboards (Week 02 Universal Engine)
Our config-driven storyboard engine (`experiments/storyboard_engine.py`) generates individual scene panels, logs execution metadata, and automatically stitches a publication-ready comic storyboard sheet (with white background, black borders, shot headers, and wrapped screenplay captions).

- **Run the built-in preset storyboard (*The Compilation Run*):**
  ```powershell
  python -m experiments.storyboard_engine
  ```
- **Generate any custom storyboard from a JSON specification:**
  Edit `experiments/custom_request.json` (supports 1 to N panels with automatic R x C grid scaling) and run:
  ```powershell
  python -m experiments.storyboard_engine experiments/custom_request.json
  ```
  *(Tip: For fast live demos on CPU, set `"width": 256, "height": 256, "steps": 4` in your JSON panel config to generate each panel in ~28 seconds).*

### 4. Re-Run Specific Storyboard & Revision Experiments
```powershell
# Generate 'The Minute Hand' 3-panel sequence
python -m experiments.run_minute_hand_storyboard

# Re-stitch 'The Minute Hand' into a dynamic multi-panel comic sheet
python -m experiments.stitch_multipanel_grid

# Run the Step 9 Targeted Revision & Global Attention Drift test
python -m experiments.run_revision_test

# Run the Week 01 Filmmaking Benchmark Suite
python -m experiments.run_filmmaking_tests
```

---

## 📁 Repository Architecture

- **`backend/`** — FastAPI web server, routing (`api.py`), and HTTP exception handling.
- **`capabilities/image_generation/`** — Input/output Pydantic contracts (`contract.py`) and the core Diffusers execution service (`service.py`).
- **`experiments/`** — Universal storyboard engine (`storyboard_engine.py`), custom JSON specs (`custom_request.json`), dynamic Pillow grid stitchers (`stitch_multipanel_grid.py`), revision experiments, and structured telemetry logs (`experiment_log.json`).
- **`outputs/`** — Stores generated panel artifacts and stitched `.png` storyboard sheets (raw weights and bulk outputs ignored by Git; reference storyboard sheets tracked).
- **`docs/`** — Week 01 CTO report & architecture notes, plus Week 02 code audit, hardware verification, baseline tests, model provenance (`model_candidates.md`), and the comprehensive Week 02 Storyboard Engineering Report (`week_02_storyboard_report.md`).
- **`tests/`** — Automated `pytest` validation suite (`test_api.py`).

---

## ⚖️ Model Provenance & Licensing

This capability defaults to **CyberRealistic V9 (Stable Diffusion 1.5 architecture)**, governed by the **CreativeML Open RAIL-M** license. Full model evaluation, provenance details, and hardware boundary analyses are documented in `docs/model_candidates.md` and `docs/week_02_storyboard_report.md`.