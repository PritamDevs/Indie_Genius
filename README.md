Indie-Genius: AI Capability Runner (Week 01)

This repository is the foundational engineering prototype for Indie-Genius. It wraps a local AI image-generation model (CyberRealistic) into a programmatic, reproducible FastAPI capability contract, bypassing manual desktop GUIs like DiffusionBee.

💻 Hardware Compatibility & Requirements

This project is explicitly engineered to run on standard consumer hardware.
* **OS:** Windows, macOS, or Linux.
* **Compute:** Tested successfully on a Windows host with an integrated AMD Radeon GPU (512MB VRAM) utilizing CPU fallback.
* **Architecture Note:** We use the `EulerDiscreteScheduler` to achieve clear, cinematic image convergence in just 8 steps. This prevents the "deep-fried" noise artifacts common when using default schedulers (like PNDM) on low-step CPU executions.
* **Storage:** Requires at least ~3 GB of free disk space (the Hugging Face pipeline downloads a 2.13 GB model on the first run).
* **Software:** Python 3.10 or higher, Git.

---

🚀 Quickstart: Installation

Do not install dependencies globally. Use a Python virtual environment to ensure dependency isolation and reproducibility.

**1. Clone the repository and enter the directory:**
```powershell
git clone <your-github-repo-url>
cd Indie_Genius
2. Create and activate a Python virtual environment:

PowerShell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
3. Install dependencies:

PowerShell
pip install -r requirements.txt
⚙️ How to Run and Test the System
⚠️ CRITICAL PATHING NOTE: Always run Python scripts from the root Indie_Genius directory using the -m (module) flag. This ensures Python resolves internal folder imports (like capabilities/) correctly and prevents ModuleNotFoundError.

1. Start the Live API Server (FastAPI / Uvicorn)
To run the capability as a live local web service:

PowerShell
uvicorn backend.api:app --host 127.0.0.1 --port 8000
Interactive Dashboard: Open http://127.0.0.1:8000/docs in your browser to test endpoints visually.

Readiness Check: GET http://127.0.0.1:8000/health

2. Developer Testing: Run the Capability Directly
To test the core image generation service in isolation (without starting the web server) and verify the Euler scheduler output:

PowerShell
python -m capabilities.image_generation.service
(Note: The first time you run this, it will take a few minutes to download the 2.13 GB .safetensors model to your local cache).

3. Run the Automated Validation Suite
To verify that the Pydantic capability contract correctly catches and rejects invalid dimensions, missing prompts, or negative steps:

PowerShell
python -m pytest tests/test_api.py -v
4. Run the Filmmaking Benchmark Suite
To batch-generate 5 specific pre-production use cases (location scouting, wardrobe, set extension) and automatically log the metadata to the experiment tracker:

PowerShell
python -m experiments.run_filmmaking_tests
📁 Repository Architecture
backend/ - The FastAPI web server, routing, and HTTP exception handling.

capabilities/image_generation/ - The generic input/output Pydantic contract (contract.py) and the replaceable Diffusers model adapter (service.py).

experiments/ - Automated batch scripts (run_filmmaking_tests.py) and the structured JSON database (experiment_log.json).

outputs/ - Ignored by Git; stores locally generated .png artifacts.

docs/ - Architecture notes, licence provenance, tool comparisons, and the Week 01 CTO Report.

⚖️ Model Provenance
This capability currently defaults to CyberRealistic V9 (SD 1.5). It is governed by the CreativeML Open RAIL-M licence. See docs/model_card_cyberrealistic.md for commercial use restrictions, including the requirement to implement safety filters if exposing unfiltered results to public users.