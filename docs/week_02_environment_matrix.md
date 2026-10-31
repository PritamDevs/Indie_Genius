# Week 02 — Windows-Only Environment Matrix

**Repository:** `https://github.com/PritamDevs/Indie_Genius.git`  
**Branch:** `week-02-storyboard-experiments`  
**Baseline Commit Hash:** `af47a91`  
**Verification Status:** **[VERIFIED WORKING]** (All values measured directly on Pritam's Windows machine)

---

## 1. Host, Runtime & Dependency Matrix

| Parameter | Measured Value on Pritam's Machine | Status Label |
| :--- | :--- | :--- |
| **Windows Edition & Build** | Microsoft Windows 11 Home Single Language — Version `10.0.26300` (Build `26300`, x64-based PC) | **[VERIFIED WORKING]** |
| **BIOS Version** | `AMI F.25, 21-04-2026` | **[VERIFIED WORKING]** |
| **PowerShell Version** | Windows PowerShell `5.1.26100.9711` | **[VERIFIED WORKING]** |
| **Python Version** | `Python 3.14.3` | **[VERIFIED WORKING]** |
| **Python Executable Path** | `C:\Users\USER\Downloads\Indie_Genius\Indie_Genius\venv\Scripts\python.exe` | **[VERIFIED WORKING]** |
| **Virtual Environment Path** | `C:\Users\USER\Downloads\Indie_Genius\Indie_Genius\venv` | **[VERIFIED WORKING]** |
| **pip Version** | `pip 25.3` (`...\venv\Lib\site-packages\pip (python 3.14)`) | **[VERIFIED WORKING]** |
| **Installed Package: `torch`** | `2.14.1+cpu` (`torch.cuda.is_available() == False`) | **[VERIFIED WORKING]** |
| **Installed Package: `diffusers`** | `0.41.0` | **[VERIFIED WORKING]** |
| **Installed Package: `transformers`** | `5.19.0` | **[VERIFIED WORKING]** |
| **Installed Package: `accelerate`** | `1.15.0` | **[VERIFIED WORKING]** |
| **Installed Package: `fastapi`** | `0.143.0` | **[VERIFIED WORKING]** |
| **Installed Package: `pydantic`** | `2.14.0` | **[VERIFIED WORKING]** |
| **Installed Package: `pytest`** | `9.1.1` (`pluggy-1.6.0`, `anyio-4.15.1`) | **[VERIFIED WORKING]** |
| **Repository Commit Hash** | `af47a91` (`docs: finalize setup instructions and fix scheduler artifacting`) | **[VERIFIED WORKING]** |
| **CPU Processor** | `AMD Ryzen 5 7520U with Radeon Graphics` (4 Cores, 8 Logical Processors) | **[VERIFIED WORKING]** |
| **GPU Name & Driver** | `AMD Radeon(TM) Graphics` (Integrated) — Driver `32.0.21045.5002`, `AdapterRAM: 536,870,912` bytes (512 MB UMA) | **[KNOWN LIMITATION]** |
| **Inference Device / Backend Used** | `cpu` (PyTorch `2.14.1+cpu` with `enable_attention_slicing()`) | **[VERIFIED WORKING]** |
| **GPU Acceleration Status** | No NVIDIA GPU (`cuda: False`); integrated AMD GPU acceleration (`DirectML`/`ROCm`) unvalidated | **[NOT TESTED]** |
| **Available Physical RAM** | `15,610 MB` (`16,368,566,272` bytes usable out of 16 GB physical RAM) | **[VERIFIED WORKING]** |
| **Free Disk Space (`C:\`)** | `74,222,440,448` bytes (`~74.22 GB` / `69.12 GiB` free; `140.53 GB` used) | **[VERIFIED WORKING]** |
| **Model Cache Path** | `C:\Users\USER\.cache\huggingface\hub\` | **[VERIFIED WORKING]** |
| **Output Artifact Path** | `C:\Users\USER\Downloads\Indie_Genius\Indie_Genius\outputs\` (relative: `outputs/`) | **[VERIFIED WORKING]** |
| **Experiment Log Path** | `C:\Users\USER\Downloads\Indie_Genius\Indie_Genius\experiments\experiment_log.json` | **[VERIFIED WORKING]** |
| **Exact Service Launch Command** | `python -m uvicorn backend.api:app --host 127.0.0.1 --port 8000` | **[VERIFIED WORKING]** |
| **Exact Automated Test Command** | `python -m pytest tests/test_api.py -v` (`4 passed, 4 warnings in 13.31s`) | **[VERIFIED WORKING]** |
| **Administrator Rights Required?** | **No.** All virtualenv, pip, pytest, and uvicorn commands execute under standard user privileges. | **[VERIFIED WORKING]** |

---

## 2. Model Precision / `dtype` Verification (File Storage vs. Runtime Memory)

Per the Week 02 specification (*"Record model precision/dtype as observed at load/inference time where the code exposes it. Do not assume a filename containing FP16 proves the pipeline is running in float16"*):

1. **Disk Storage Format (`FP16`):** The checkpoint file `CyberRealistic_V9_FP16.safetensors` is serialized on disk in 16-bit floating point (`FP16`) to reduce download and cache size to `2.13 GB` **[VERIFIED WORKING]**.
2. **Runtime Inference Precision (`torch.float32`):** In `capabilities/image_generation/service.py` (line 44), `StableDiffusionPipeline.from_single_file()` is explicitly invoked with `torch_dtype=torch.float32` **[VERIFIED WORKING]**.
3. **Consequences:**
   * **Compatibility:** Avoids PyTorch CPU `RuntimeError: "LayerNormKernelImpl" not implemented for 'Half'`, which occurs when running `float16` tensors on x86 CPUs **[VERIFIED WORKING]**.
   * **Memory & Runtime Impact:** Unpacking `FP16` weights into `float32` tensors in system RAM roughly doubles the in-memory weight footprint from `~2.13 GB` on disk to `~4.2 GB` in RAM (comfortably within the `15,610 MB` available RAM) and executes matrix multiplications in 32-bit float precision on the 4-core Ryzen 5 7520U CPU **[KNOWN LIMITATION]**.