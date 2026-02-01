# Product Requirements Document (PRD)
**Project:** LABS-Hybrid-QC  
**Team:** MIT-Quackhacks  

---

## 1. Project Overview

**Project Name:** LABS-Hybrid-QC  
**Team Name:** MIT-Quackhacks  
**GitHub Repository:** https://github.com/alal29/2026-NVIDIA

This project implements a **hybrid quantum–classical optimization pipeline** for the **Low Autocorrelation Binary Sequences (LABS)** problem using **CUDA-Q** and a **classical Memetic Tabu Search (MTS)** optimizer.

The focus of this work is on:
- correctness  
- scalability  
- disciplined GPU acceleration  

rather than claims of near-term quantum advantage. The quantum component is used as a **structured sampler**, while classical heuristics perform local optimization.

---

## 2. Team Roles & Responsibilities

**Owner:** Project Lead (Shrikar Swami)

| Role | Name | GitHub | Discord |
|---|---|---|---|
| Project Lead (Architect) | Shrikar Swami | @ShrikarSwami | @awesomestudio |
| GPU Acceleration PIC (Builder) | Akash Lal | @alal29 | @Akash Lal |
| Quality Assurance PIC (Verifier) | Adithya Pillai | @adithyap02 | @adithyap02 |
| Technical Marketing PIC (Storyteller) | Abhiram Kandadi | @bobbycache | @bobbycache |

Roles are explicitly defined to ensure clear ownership across system architecture, GPU acceleration, verification, and technical communication.

---

## 3. Architecture

**Owner:** Project Lead (Shrikar Swami)

### 3.1 Choice of Quantum Algorithm

**Algorithm:**  
QAOA-inspired hybrid sampling using a **Trotterized LABS Hamiltonian** implemented in **CUDA-Q**.

**Description:**  
The LABS objective decomposes into:
- two-body interaction terms  
- four-body interaction terms  

These interactions are implemented directly as CUDA-Q kernels. A **Trotterized evolution** biases the quantum sampling distribution toward lower-energy LABS configurations.

The quantum circuit is **not** used to directly solve the optimization problem. Instead, it serves as a **structured sampler** whose outputs seed a classical **Memetic Tabu Search (MTS)** optimizer.

**Motivation:**  
This design aligns with near-term quantum capabilities and avoids over-claiming quantum advantage. Quantum sampling is used where it is strongest, while classical heuristics handle local optimization.

---

### 3.2 Literature Context

**Reference:**  
Bernasconi, J. *Low Autocorrelation Binary Sequences: Statistical Mechanics and Computational Complexity.*

This work formalizes the LABS energy landscape and motivates a physics-inspired sampling approach approximated using shallow, parameterized quantum circuits.

---

## 4. Acceleration Strategy

**Owner:** GPU Acceleration PIC (Akash Lal)

### 4.1 Quantum Acceleration (CUDA-Q)

**Strategy:**
- Implement LABS Hamiltonian terms using explicit two-qubit and four-qubit CUDA-Q kernels  
- Apply Trotterized evolution to shape the sampling distribution  
- Increase sequence length N and sampling depth (shots) using GPUs via Brev  

The circuit structure from Phase 1 is preserved exactly in Phase 2; only scale parameters are modified.

---

### 4.2 Classical Acceleration (Memetic Tabu Search)

**Strategy:**
- Retain MTS as the core classical optimizer  
- Use quantum-generated bitstrings as the initial population  
- Compare against random initialization under equal resource budgets  

If time permits, batching energy evaluations and parallel neighborhood exploration may be explored.

---

### 4.3 Hardware Targets

- **Development / Validation:** CPU-only (local or qBraid) for Phase 1 correctness validation  
- **Scaling / Production:** NVIDIA L4 GPU on Brev for Phase 2 experiments  

---

## 5. Verification Plan

**Owner:** Quality Assurance PIC (Adithya Pillai)

### 5.1 Unit Testing Strategy

**Framework:**  
Python assertions and lightweight tests embedded directly in experiment scripts.

**AI-Assisted Code Guardrails:**
- Cross-check against known LABS energies for small N  
- Symmetry validation  
- Cross-validation between quantum-sampled energies and classical scoring  

---

### 5.2 Core Correctness Checks

- **Symmetry Invariance:**  
  LABS energy is invariant under global sign flip and sequence reversal:  
  - E(S) = E(-S)  
  - E(S) = E(reverse(S))  

- **Ground Truth Validation:**  
  Known optimal energies for small N are used to validate both CPU and GPU execution paths.

---

## 6. Execution Strategy & Success Metrics

**Owner:** Technical Marketing PIC (Abhiram Kandadi)

### 6.1 Execution Workflow

1. Validate the hybrid pipeline on CPU  
2. Log experiments with fixed seeds and budgets  
3. Port the unchanged pipeline to Brev GPU  
4. Increase scale while maintaining reproducibility  

---

### 6.2 Success Metrics

- **Correctness:** Convergence to known optima for small N  
- **Convergence Behavior:** Improved consistency or speed using quantum-seeded initialization  
- **Scale:** Successful execution at larger N on GPU  

---

### 6.3 Visualization Plan

- Best energy vs. time (quantum-seeded vs. random initialization)  
- Energy vs. iteration count across multiple random seeds  

---

## 7. Resource Management Plan

**Owner:** GPU Acceleration PIC (Akash Lal)

- Complete all debugging on CPU before GPU usage  
- Use a single NVIDIA L4 GPU instance for Phase 2 scaling  
- Incrementally increase N, shots, and runtime budgets  
- Manually stop Brev instances when idle  

---

## 8. Current Status

**Owner:** Project Lead (Shrikar Swami)

- **Phase 1:** Completed and verified  
- **Phase 2 (CPU):** Completed  
- **Phase 2 (GPU on Brev):** Completed  
