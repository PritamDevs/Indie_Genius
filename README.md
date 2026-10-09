# Indie-Genius: AI Capability Runner (Week 01)

This repository is the first foundational engineering prototype for Indie-Genius. It demonstrates how to take a community AI model (CyberRealistic), verify its commercial provenance, and wrap it in a programmatic, reproducible FastAPI capability contract without relying on manual desktop GUIs like DiffusionBee.

## 💻 Hardware Compatibility & Requirements

Can you run this on your machine? **Yes.** 
This project is explicitly engineered to run on standard consumer hardware, including machines without dedicated NVIDIA GPUs.

* **OS:** Windows, macOS, or Linux.
* **Compute:** Tested successfully on a Windows host with an integrated AMD Radeon GPU (512MB VRAM) via CPU fallback.
* **Storage:** Requires at least ~3 GB of free disk space (the Hugging Face pipeline will automatically download and cache a 2.13 GB `.safetensors` model on the first run).
* **Software:** Python 3.10 or higher. Git.

## 🚀 Quickstart: Local Setup

Do not install dependencies globally. Use a virtual environment to ensure reproducibility.

**1. Clone the repository and enter the directory:**
```powershell
git clone <your-github-repo-url>
cd Indie_Genius