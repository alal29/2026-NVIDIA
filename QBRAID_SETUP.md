# qBraid Execution Guide for LABS Phase 2 CPU Experiments

## Prerequisites

This notebook is designed to run on **qBraid** (Linux x86_64) with CPU-only execution.

## Quick Start on qBraid

### 1. Upload Repository to qBraid

```bash
# Clone your repository
git clone https://github.com/iQuHACK/2026-NVIDIA.git
cd 2026-NVIDIA
```

### 2. Install Dependencies

In a qBraid terminal or notebook cell:

```bash
pip install cudaq numpy matplotlib pandas jupyter
```

Or create a requirements file:
```bash
pip install -r requirements_qbraid.txt
```

### 3. Open and Run Notebook

1. Open `LABS_Phase2_CPU.ipynb` in JupyterLab
2. Select Python 3 kernel
3. Run all cells sequentially
4. Results will be saved to `results/phase2_cpu_results.json`

## Notebook Structure

The notebook contains:

1. **Setup & Imports** - Sets `cudaq.set_target("qpp-cpu")` for CPU execution
2. **LABS Energy Function** - Core optimization objective
3. **MTS Implementation** - Memetic Tabu Search optimizer
4. **Quantum Sampling** - CUDA-Q counterdiabatic circuit
5. **Experiment Loop** - Automated runs for N ∈ {32, 48, 64} with 5 seeds each
6. **Results Export** - JSON output to `results/phase2_cpu_results.json`
7. **Visualization** - Energy and runtime comparison plots

## Expected Output Files

After successful execution:

```
results/
├── phase2_cpu_results.json          # Main results data
├── phase2_cpu_energy_comparison.png # Energy bar charts
└── phase2_cpu_runtime_comparison.png # Runtime scaling plot
```

## Verification

To verify the notebook ran correctly:

```python
import json

# Load results
with open('results/phase2_cpu_results.json', 'r') as f:
    data = json.load(f)

# Check metadata
print("Experiment:", data['metadata']['experiment'])
print("Target:", data['metadata']['target'])
print("Total runs:", len(data['results']))

# Should show 30 total runs:
# 3 sequence lengths × 5 seeds × 2 init types (random + quantum)
```

## Configuration Parameters

The notebook uses these fixed parameters:

```python
SEQUENCE_LENGTHS = [32, 48, 64]
RANDOM_SEEDS = [42, 123, 456, 789, 1024]
POPULATION_SIZE = 30
MTS_STEPS = 150
LOCAL_ITERS = 100
TABU_LEN = 10
QUANTUM_SHOTS = 300
TROTTER_STEPS = 1
EVOLUTION_TIME = 1.0
```

## CPU-Only Constraints

**Verified CPU-only setup:**
- ✅ `cudaq.set_target("qpp-cpu")` explicitly set
- ✅ No GPU, CUDA, or Brev dependencies
- ✅ No GPU-specific libraries imported
- ✅ Pure CPU sampling and classical optimization

## Troubleshooting

### Import Error: cudaq not found

```bash
pip install cudaq --upgrade
```

### Import Error: labs_utils module

Ensure the auxiliary files are accessible:
```python
import sys
sys.path.append('tutorial_notebook/auxiliary_files')
import labs_utils as utils
```

### Results directory not found

The notebook automatically creates `results/` directory, but if needed:
```bash
mkdir -p results
```

### Memory Issues (Large N)

If you encounter memory issues on qBraid:
- Reduce `QUANTUM_SHOTS` (e.g., 300 → 200)
- Reduce `POPULATION_SIZE` (e.g., 30 → 20)
- Run smaller sequence lengths first

## Runtime Estimates

Expected runtime on qBraid (approximate):

| N  | Random MTS | Quantum MTS | Total per seed |
|----|------------|-------------|----------------|
| 32 | ~10s       | ~15s        | ~25s           |
| 48 | ~30s       | ~45s        | ~75s           |
| 64 | ~60s       | ~90s        | ~150s          |

**Total for all experiments**: ~30-40 minutes

## Submission Checklist

- [ ] Notebook runs without errors on qBraid
- [ ] `results/phase2_cpu_results.json` is generated
- [ ] JSON contains 30 entries (3 N × 5 seeds × 2 types)
- [ ] Target confirmed as "qpp-cpu" in metadata
- [ ] Visualizations are generated
- [ ] Repository pushed to GitHub

## Support

For qBraid-specific issues:
- qBraid Docs: https://docs.qbraid.com
- qBraid Slack: iQuHACK workspace

For LABS challenge questions:
- See challenge documentation in repo root
- Contact organizers via iQuHACK channels

---

**Ready to run!** The notebook is fully configured for qBraid execution.
