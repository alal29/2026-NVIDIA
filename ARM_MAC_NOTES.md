# ARM Mac (Apple Silicon) - CUDA-Q Installation Notes

## ⚠️ Current Limitation

**CUDA-Q does not currently support ARM64 (Apple Silicon) Macs natively.** The package requires x86_64 architecture.

## Workarounds for Running Phase 2 CPU Experiments

### Option 1: Use Your Existing Jupyter Environment (Recommended if Phase 1 worked)

If your Phase 1 notebook (`01_quantum_enhanced_optimization_LABS.ipynb`) already runs successfully, use that same environment:

```bash
# Check your current jupyter kernels
jupyter kernelspec list

# Use the kernel that worked for Phase 1
```

Then open `LABS_Phase2_CPU.ipynb` and select the same kernel you used for Phase 1.

### Option 2: Docker with x86 Emulation

Run CUDA-Q in a Docker container with x86 emulation (Rosetta 2):

```bash
# Pull CUDA-Q Docker image
docker pull nvcr.io/nvidia/nightly/cuda-quantum:latest

# Run container with your repo mounted
docker run -it --platform linux/amd64 \
  -v /Users/akash/repos/2026-NVIDIA:/workspace \
  nvcr.io/nvidia/nightly/cuda-quantum:latest

# Inside container:
cd /workspace
pip install jupyter ipykernel numpy matplotlib
jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root
```

### Option 3: Google Colab (Free, Cloud-based)

1. Upload `LABS_Phase2_CPU.ipynb` to Google Colab
2. Add installation cell at the top:

```python
!pip install cudaq jupyter numpy matplotlib
!cp -r /content/drive/MyDrive/2026-NVIDIA/tutorial_notebook/auxiliary_files .
```

3. Run all cells

### Option 4: Cloud VM (Linux x86_64)

Use a cloud provider with x86 architecture:
- AWS EC2 (t2.micro for free tier)
- Google Compute Engine
- Azure VM
- DigitalOcean Droplet

Install Python 3.10 and run:
```bash
pip install cudaq jupyter ipykernel numpy matplotlib
```

### Option 5: Use a Linux/Intel Mac Machine

If you have access to an Intel Mac or Linux machine:

```bash
cd /path/to/2026-NVIDIA
./setup_env.sh  # Will work on x86_64
```

## Verifying Your Setup

After setting up any of the above options, verify CUDA-Q works:

```python
import cudaq

# Should print 'qpp-cpu' or similar
print("Target:", cudaq.get_target().name)

@cudaq.kernel
def test():
    q = cudaq.qubit()
    h(q)
    mz(q)

counts = cudaq.sample(test, shots_count=100)
print(counts)  # Should show ~50% |0⟩ and ~50% |1⟩
```

## For iQuHACK Submission

Since Phase 2 requires CPU-only experiments (no GPU), you have several good options:

1. **Best for quick testing**: Google Colab (free, instant)
2. **Best for reproducibility**: Docker (consistent environment)
3. **Best for development**: Cloud VM (full control)

For GPU-accelerated experiments (if needed), you'll use Brev or similar cloud platforms anyway, which will have x86 architecture.

## Questions?

If you're blocked on this, consider:
- Asking organizers if they have recommended ARM Mac workarounds
- Using the Phase 1 tutorial notebook environment if it's working
- Pairing with a teammate who has an x86 machine

---

**Note**: This is a platform limitation, not an issue with your setup or code. CUDA-Q team is aware of ARM Mac requests.
