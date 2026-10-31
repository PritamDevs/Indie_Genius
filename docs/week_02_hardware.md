# Week 02 — Step 4: Windows Hardware Profile

**Repository:** \https://github.com/PritamDevs/Indie_Genius.git\  
**Branch:** \week-02-storyboard-experiments\  
**Baseline Commit:** \f47a91\  
**Verification Status:** **[VERIFIED WORKING]** (Measured directly on Pritam's Windows host)

---

## 1. Raw PowerShell Hardware Outputs

### 1.1 OS & System Summary (\systeminfo\)
\\\	ext
OS Name:                       Microsoft Windows 11 Home Single Language
OS Version:                    10.0.26300 N/A Build 26300
System Type:                   x64-based PC
BIOS Version:                  AMI F.25, 21-04-2026
Total Physical Memory:         15,610 MB
\\\

### 1.2 Processor (\Get-CimInstance Win32_Processor\)
\\\	ext
Name                      : AMD Ryzen 5 7520U with Radeon Graphics         
NumberOfCores             : 4
NumberOfLogicalProcessors : 8
\\\

### 1.3 Physical Memory (\Get-CimInstance Win32_ComputerSystem\)
\\\	ext
TotalPhysicalMemory : 16368566272
\\\
* **Interpretation:** 16,368,566,272 bytes = 15,610 MB (~15.24 GiB) usable system RAM.

### 1.4 Video Controller (\Get-CimInstance Win32_VideoController\)
\\\	ext
Name          : AMD Radeon(TM) Graphics
AdapterRAM    : 536870912
DriverVersion : 32.0.21045.5002
\\\
* **Interpretation:** 536870912 bytes = **512 MB** fixed BIOS hardware-reserved UMA frame buffer **[KNOWN LIMITATION]**. There is no discrete VRAM; system RAM hosts model weights via CPU execution.

### 1.5 Storage Drive (\Get-PSDrive -Name C\)
\\\	ext
Name            : C
Root            : C:\\
Used            : 140525920256
Free            : 74222440448
\\\
* **Interpretation:** **74.22 GB (69.12 GiB) free disk space** on C:\, which easily accommodates multiple SD 1.5 checkpoints **[VERIFIED WORKING]**.

---

## 2. Inference Backend Assessment
- **CPU Execution (\device=\"cpu\"\):** AMD Ryzen 5 7520U running PyTorch 2.14.1+cpu in 	orch.float32 with enable_attention_slicing() **[VERIFIED WORKING]**.
- **CUDA Support:** False (	orch.cuda.is_available() == False) **[KNOWN LIMITATION]**.
- **AMD GPU Acceleration:** Unverified / Not active in baseline equirements.txt **[NOT TESTED]**.
