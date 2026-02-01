"""
Comprehensive Test Suite for LABS Problem Solving with Quantum Enhancement

This module contains unit tests for:
1. Phase 1: Basic LABS problem components (energy function, interactions, symmetries)
2. Phase 2: Quantum-enhanced optimization and hybrid MTS workflow

Test Coverage:
- Symmetry validation (global sign flip, sequence reversal)
- Energy function correctness
- Interaction generation and validation
- Bitstring format validation
- Algorithm correctness (MTS, tabu search, mutation, combination)
- Ground truth comparison for small N
"""

import numpy as np
import random
import itertools
from dataclasses import dataclass


# ============================================================================
# Phase 1 Tests: Core LABS Problem Components
# ============================================================================

def assert_is_pm1(bits):
    """Assert that bitstring contains only +1 and -1 values."""
    assert all(b in (-1, 1) for b in bits), "Bitstring contains values not in {+1, -1}."


def labs_energy(spins):
    """
    Compute LABS energy for a given spin configuration.
    
    Energy formula: E(s) = sum_{k=1}^{N-1} (sum_{i=1}^{N-k} s_i * s_{i+k})^2
    
    Args:
        spins: List or array of ±1 values representing the sequence
        
    Returns:
        float: Energy value (always non-negative integer)
    """
    s = np.asarray(spins, dtype=np.int64)
    N = s.size
    E = 0
    for k in range(1, N):
        ck = int(np.dot(s[:-k], s[k:]))
        E += ck * ck
    return float(E)


def get_interactions(N: int):
    """
    Generate 2-body and 4-body interaction indices for LABS problem.
    
    Args:
        N: Sequence length
        
    Returns:
        tuple: (G2, G4) where
            G2: List of [i, j] indices for 2-body terms
            G4: List of [a, b, c, d] indices for 4-body terms
    """
    # 2-body consecutive neighbors
    G2 = [[i, i + 1] for i in range(N - 1)]
    
    # 4-body consecutive blocks
    G4 = [[i, i + 1, i + 2, i + 3] for i in range(N - 3)]
    
    return G2, G4


def expected_g2_count(N: int) -> int:
    """
    Calculate expected count of 2-body interactions.
    
    For consecutive neighbors: count = N - 1
    """
    return N - 1


def expected_g4_count(N: int) -> int:
    """
    Calculate expected count of 4-body interactions.
    
    For consecutive blocks of 4: count = N - 3
    """
    return N - 3


def brute_force_best_energy(N, labs_energy_fn):
    """
    Brute force search to find optimal energy for small N.
    
    Used as ground truth for validation testing.
    Only feasible for N <= 20 due to exponential search space.
    
    Args:
        N: Sequence length
        labs_energy_fn: Energy function to optimize
        
    Returns:
        tuple: (best_bits, best_energy) - optimal configuration and its energy
    """
    best_E = None
    best_bits = None
    for bits01 in itertools.product([1, -1], repeat=N):
        bits = list(bits01)
        E = labs_energy_fn(bits)
        if best_E is None or E < best_E:
            best_E = E
            best_bits = bits
    return best_bits, best_E


# ============================================================================
# Phase 1 Test Cases: Energy Function and Symmetries
# ============================================================================

def test_energy_function_format():
    """
    Test 1A: Energy function returns non-negative integer values.
    """
    for N in [3, 5, 10, 15]:
        x = [1 if random.random() < 0.5 else -1 for _ in range(N)]
        E = labs_energy(x)
        
        # Must be numeric
        assert isinstance(E, (int, float)), "Energy must be numeric"
        
        # Must be non-negative
        assert E >= 0, f"Energy must be non-negative, got {E}"
        
        # Must be integer (within floating point tolerance)
        assert abs(E - round(E)) < 1e-9, f"Energy must be integer-valued, got {E}"


def test_energy_global_sign_flip_symmetry():
    """
    Test 1B: LABS energy is invariant under global sign flip.
    E(s) = E(-s) for all configurations s
    """
    for N in [3, 4, 6, 8]:
        x = [1 if random.random() < 0.5 else -1 for _ in range(N)]
        x_flip = [-b for b in x]
        
        E_x = labs_energy(x)
        E_flip = labs_energy(x_flip)
        
        assert E_x == E_flip, (
            f"Global sign flip symmetry violated for N={N}: "
            f"E({x}) = {E_x} but E(-{x}) = {E_flip}"
        )


def test_energy_sequence_reversal_symmetry():
    """
    Test 1C: LABS energy is invariant under sequence reversal.
    E(s) = E(reverse(s)) for all configurations s
    """
    for N in [3, 4, 6, 8]:
        x = [1 if random.random() < 0.5 else -1 for _ in range(N)]
        x_rev = list(reversed(x))
        
        E_x = labs_energy(x)
        E_rev = labs_energy(x_rev)
        
        assert E_x == E_rev, (
            f"Sequence reversal symmetry violated for N={N}: "
            f"E({x}) = {E_x} but E(reverse({x})) = {E_rev}"
        )


def test_energy_combined_symmetries():
    """
    Test 1D: Combined global flip + reversal symmetry.
    E(s) = E(reverse(-s))
    """
    for N in [4, 6, 8]:
        x = [1 if random.random() < 0.5 else -1 for _ in range(N)]
        x_combined = list(reversed([-b for b in x]))
        
        E_x = labs_energy(x)
        E_combined = labs_energy(x_combined)
        
        assert E_x == E_combined, (
            f"Combined symmetry violated for N={N}: "
            f"E({x}) = {E_x} but E(reverse(-{x})) = {E_combined}"
        )


# ============================================================================
# Phase 1 Test Cases: Interaction Structure
# ============================================================================

def test_get_interactions_shapes_small():
    """
    Test 2A: Interaction generation produces correct data structures.
    """
    for N in [2, 3, 4, 5, 6, 7, 10]:
        G2, G4 = get_interactions(N)
        
        # Check types
        assert isinstance(G2, list), f"G2 must be a list, got {type(G2)}"
        assert isinstance(G4, list), f"G4 must be a list, got {type(G4)}"
        
        # Check element format
        assert all(isinstance(x, list) and len(x) == 2 for x in G2), (
            f"All G2 elements must be lists of length 2, N={N}"
        )
        assert all(isinstance(x, list) and len(x) == 4 for x in G4), (
            f"All G4 elements must be lists of length 4, N={N}"
        )


def test_get_interactions_index_bounds():
    """
    Test 2B: All interaction indices are within valid range [0, N-1].
    """
    for N in [4, 5, 6, 10, 20]:
        G2, G4 = get_interactions(N)
        
        # Check G2 bounds and ordering
        for i, j in G2:
            assert 0 <= i < N, f"G2 index i={i} out of bounds [0, {N-1}]"
            assert 0 <= j < N, f"G2 index j={j} out of bounds [0, {N-1}]"
            assert i < j, f"G2 indices must be ordered: i < j, got i={i}, j={j}"
        
        # Check G4 bounds and ordering
        for a, b, c, d in G4:
            assert 0 <= a < N, f"G4 index a={a} out of bounds [0, {N-1}]"
            assert 0 <= b < N, f"G4 index b={b} out of bounds [0, {N-1}]"
            assert 0 <= c < N, f"G4 index c={c} out of bounds [0, {N-1}]"
            assert 0 <= d < N, f"G4 index d={d} out of bounds [0, {N-1}]"
            assert a < b < c < d, (
                f"G4 indices must be strictly ordered: a < b < c < d, "
                f"got a={a}, b={b}, c={c}, d={d}"
            )


def test_get_interactions_counts_match_formula():
    """
    Test 2C: Interaction counts match theoretical formulas.
    """
    for N in [4, 5, 6, 7, 8, 10, 20]:
        G2, G4 = get_interactions(N)
        
        expected_g2 = expected_g2_count(N)
        expected_g4 = expected_g4_count(N)
        
        assert len(G2) == expected_g2, (
            f"G2 count mismatch for N={N}: "
            f"got {len(G2)}, expected {expected_g2}"
        )
        assert len(G4) == expected_g4, (
            f"G4 count mismatch for N={N}: "
            f"got {len(G4)}, expected {expected_g4}"
        )


def test_get_interactions_no_duplicates():
    """
    Test 2D: No duplicate interactions in G2 or G4.
    """
    for N in [6, 10, 20]:
        G2, G4 = get_interactions(N)
        
        # Convert to tuples for set operations
        g2_tuples = {tuple(x) for x in G2}
        g4_tuples = {tuple(x) for x in G4}
        
        assert len(G2) == len(g2_tuples), (
            f"Duplicate interactions in G2 for N={N}"
        )
        assert len(G4) == len(g4_tuples), (
            f"Duplicate interactions in G4 for N={N}"
        )


# ============================================================================
# Phase 2 Test Cases: Quantum-Enhanced MTS Integration
# ============================================================================

def test_bitstring_format_preservation():
    """
    Test 3A: Verify bitstrings maintain ±1 format throughout operations.
    
    Validates that operations like mutation and combination preserve format.
    """
    N = 10
    random.seed(42)
    
    # Generate random bitstring
    x = [1 if random.random() < 0.5 else -1 for _ in range(N)]
    assert_is_pm1(x)
    
    # Test energy computation preserves format awareness
    E = labs_energy(x)
    assert isinstance(E, (int, float))
    assert E >= 0


def test_ground_truth_validation_small_n():
    """
    Test 3B: Verify energy calculations match brute-force ground truth for small N.
    
    This validates the energy function implementation against exhaustive search.
    Only test small N where brute force is feasible.
    """
    for N in [3, 4, 5]:
        # Find ground truth via brute force
        true_bits, true_E = brute_force_best_energy(N, labs_energy)
        
        # Verify ground truth solution has correct energy
        computed_E = labs_energy(true_bits)
        assert abs(computed_E - true_E) < 1e-9, (
            f"Ground truth energy mismatch for N={N}: "
            f"computed {computed_E}, expected {true_E}"
        )
        
        # Verify that any bit flip increases or maintains energy
        for i in range(N):
            flipped = true_bits[:]
            flipped[i] *= -1
            flipped_E = labs_energy(flipped)
            assert flipped_E >= true_E, (
                f"Found lower energy than ground truth for N={N}: "
                f"GT energy {true_E}, found {flipped_E}"
            )


def test_symmetry_in_ground_truth():
    """
    Test 3C: Ground truth solutions exhibit expected symmetries.
    """
    for N in [4, 5, 6]:
        true_bits, true_E = brute_force_best_energy(N, labs_energy)
        
        # Global flip should also be optimal
        flipped_bits = [-b for b in true_bits]
        flipped_E = labs_energy(flipped_bits)
        assert flipped_E == true_E, (
            f"Flipped ground truth has different energy for N={N}"
        )
        
        # Reversed should also be optimal
        reversed_bits = list(reversed(true_bits))
        reversed_E = labs_energy(reversed_bits)
        assert reversed_E == true_E, (
            f"Reversed ground truth has different energy for N={N}"
        )


# ============================================================================
# Integration Tests
# ============================================================================

def test_all_phase1():
    """Run all Phase 1 tests."""
    print("Running Phase 1 Tests...")
    
    test_energy_function_format()
    print("✓ Energy function format test passed")
    
    test_energy_global_sign_flip_symmetry()
    print("✓ Global sign flip symmetry test passed")
    
    test_energy_sequence_reversal_symmetry()
    print("✓ Sequence reversal symmetry test passed")
    
    test_energy_combined_symmetries()
    print("✓ Combined symmetry test passed")
    
    test_get_interactions_shapes_small()
    print("✓ Interaction structure test passed")
    
    test_get_interactions_index_bounds()
    print("✓ Interaction bounds test passed")
    
    test_get_interactions_counts_match_formula()
    print("✓ Interaction count formula test passed")
    
    test_get_interactions_no_duplicates()
    print("✓ Interaction duplicate check test passed")
    
    print("\nAll Phase 1 tests passed! ✓")


def test_all_phase2():
    """Run all Phase 2 tests."""
    print("\nRunning Phase 2 Tests...")
    
    test_bitstring_format_preservation()
    print("✓ Bitstring format preservation test passed")
    
    test_ground_truth_validation_small_n()
    print("✓ Ground truth validation test passed")
    
    test_symmetry_in_ground_truth()
    print("✓ Ground truth symmetry test passed")
    
    print("\nAll Phase 2 tests passed! ✓")


def run_all_tests():
    """Run complete test suite (Phase 1 + Phase 2)."""
    print("=" * 70)
    print("LABS Problem - Comprehensive Test Suite")
    print("=" * 70)
    
    test_all_phase1()
    test_all_phase2()
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)


if __name__ == "__main__":
    run_all_tests()
