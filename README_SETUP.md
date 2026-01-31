# Phase 2 CPU Environment Setup

Quick setup guide for the NVIDIA iQuHACK LABS Challenge Phase 2 CPU experiments.

## Prerequisites

- Python 3.9 or higher installed
- No GPU/CUDA drivers needed (CPU-only)

## Setup Instructions

### Mac / Linux

```bash
# Navigate to repo root
cd /path/to/2026-NVIDIA

# Run setup script
./setup_env.sh
```

### Windows

```cmd
# Navigate to repo root
cd C:\path\to\2026-NVIDIA

# Run setup script
setup_env.bat
```

## What Gets Installed

The setup script creates a virtual environment and installs:

- **cudaq** - CUDA-Q quantum computing framework (CPU backend)
- **jupyter** - Jupyter notebook server
- **ipykernel** - Jupyter kernel support
- **numpy** - Numerical computing
- **matplotlib** - Visualization

## Using the Environment

### Option 1: Jupyter Notebook

```bash
# Activate environment (Mac/Linux)
source venv/bin/activate

# Or on Windows
venv\Scripts\activate.bat

# Launch Jupyter
jupyter notebook

# Open LABS_Phase2_CPU.ipynb
# Select: Kernel → Change Kernel → "LABS CPU"
```

### Option 2: VS Code

1. Open `LABS_Phase2_CPU.ipynb` in VS Code
2. Click the kernel selector in the top-right corner
3. Choose **"LABS CPU"** from the list

### Option 3: Command Line

```bash
# Activate environment
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate.bat  # Windows

# Run Python scripts
python your_script.py
```

## Running Phase 2 Experiments

Once the environment is set up:

1. Open `LABS_Phase2_CPU.ipynb`
2. Select the "LABS CPU" kernel
3. Run all cells sequentially
4. Results will be saved to `results/phase2_cpu_results.json`

## Troubleshooting

**Python not found:**
```bash
# Install Python 3.9+ from python.org or via package manager
brew install python@3.9  # Mac
sudo apt install python3.9  # Ubuntu/Debian
```

**Permission denied (Mac/Linux):**
```bash
chmod +x setup_env.sh
```

**CUDA-Q installation issues:**
- Ensure you're using Python 3.9-3.11 (CUDA-Q compatibility)
- Check your platform is supported: `python --version`

## Deactivating the Environment

When you're done working:

```bash
deactivate
```

## Notes

- This setup is **CPU-only** (no GPU drivers required)
- The virtual environment is isolated from your system Python
- The Jupyter kernel "LABS CPU" is registered globally for your user
- GPU-accelerated experiments will use a separate Brev environment (Phase 2 GPU)

---

**iQuHACK 2026 - NVIDIA LABS Challenge**
