# Image Generation Service
## Hardware constraints
- **OS:** Windows
- **GPU:** AMD Radeon(TM) Graphics (Integrated)
- **VRAM:** 512MB Dedicated
- **CUDA:** Not Available

**Engineering Decision:** Due to the lack of an NVIDIA GPU and sufficient VRAM, GPU acceleration is not possible. The Day 2 DiffusionBee baseline cannot be executed as the software is macOS-exclusive. Programmatic inference will be configured for CPU execution, with the understanding that execution times will be severely degraded or fail gracefully due to memory limits.
