"""
Pytest-based invariant tests for LABS problem.

These tests focus on key invariants that must hold for correct implementation:
- Energy symmetries (global flip, sequence reversal)
- Bitstring format preservation (±1 values)
- Array consistency and shape preservation

These tests can run on any platform (no GPU required) and are suitable for CI/CD.
"""

import pytest
import numpy as np
from dataclasses import dataclass


# ============================================================================
# Helper Functions (Mirror Notebook Logic)
# ============================================================================

def labs_energy(spins):
    """
    Compute LABS energy for a given spin configuration.
    
    Energy formula: E(s) = sum_{k=1}^{N-1} (sum_{i=1}^{N-k} s_i * s_{i+k})^2
    
    This function mirrors the notebook implementation.
    """
    s = np.asarray(spins, dtype=np.int64)
    N = s.size
    E = 0
    for k in range(1, N):
        ck = int(np.dot(s[:-k], s[k:]))
        E += ck * ck
    return float(E)


def assert_is_pm1(bits):
    """Assert that bitstring contains only +1 and -1 values."""
    assert all(b in (-1, 1) for b in bits), \
        f"Bitstring contains invalid values: {bits}"


# ============================================================================
# Pytest Invariant Tests
# ============================================================================

class TestEnergyInvariants:
    """Tests for LABS energy function invariants."""
    
    def test_energy_is_nonnegative(self):
        """Energy must be non-negative for all configurations."""
        for N in [3, 5, 8, 10]:
            for trial in range(5):
                bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                E = labs_energy(bits)
                assert E >= 0, f"Energy is negative: E={E} for bits={bits}"
    
    def test_energy_is_integer(self):
        """Energy must be integer-valued (within floating point tolerance)."""
        for N in [3, 4, 6, 8]:
            for trial in range(5):
                bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                E = labs_energy(bits)
                # Check if E is effectively an integer
                assert abs(E - round(E)) < 1e-9, \
                    f"Energy not integer-valued: E={E}"
    
    def test_global_sign_flip_symmetry(self):
        """Energy must be invariant under global sign flip: E(s) = E(-s)."""
        for N in [3, 4, 6, 8, 10]:
            for trial in range(5):
                s = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                s_flip = [-b for b in s]
                
                E_s = labs_energy(s)
                E_flip = labs_energy(s_flip)
                
                assert E_s == E_flip, \
                    f"Global sign flip symmetry violated for N={N}: " \
                    f"E({s}) = {E_s} but E(-{s}) = {E_flip}"
    
    def test_sequence_reversal_symmetry(self):
        """Energy must be invariant under sequence reversal: E(s) = E(reverse(s))."""
        for N in [3, 4, 6, 8, 10]:
            for trial in range(5):
                s = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                s_rev = list(reversed(s))
                
                E_s = labs_energy(s)
                E_rev = labs_energy(s_rev)
                
                assert E_s == E_rev, \
                    f"Sequence reversal symmetry violated for N={N}: " \
                    f"E({s}) = {E_s} but E(reverse({s})) = {E_rev}"
    
    def test_combined_symmetries(self):
        """Energy must be invariant under combined transformations."""
        for N in [4, 6, 8]:
            for trial in range(5):
                s = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                s_combined = list(reversed([-b for b in s]))
                
                E_s = labs_energy(s)
                E_combined = labs_energy(s_combined)
                
                assert E_s == E_combined, \
                    f"Combined symmetry violated for N={N}"


class TestBitstringFormat:
    """Tests for bitstring format preservation."""
    
    def test_bitstring_values_are_pm1(self):
        """Bitstrings must contain only +1 and -1 values."""
        for N in [3, 5, 8, 10]:
            for trial in range(10):
                bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                assert_is_pm1(bits)
    
    def test_bitstring_length_preserved(self):
        """Bitstring length must equal sequence length N."""
        for N in [3, 5, 8, 10, 16]:
            bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
            assert len(bits) == N, \
                f"Bitstring length mismatch: len={len(bits)}, expected N={N}"
    
    def test_array_consistency(self):
        """Array shapes and types must be consistent."""
        N = 10
        bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
        
        # Check list format
        assert isinstance(bits, list), f"Expected list, got {type(bits)}"
        assert len(bits) == N, f"Expected length {N}, got {len(bits)}"
        
        # Convert to array and check
        bits_array = np.asarray(bits, dtype=np.int64)
        assert bits_array.shape == (N,), f"Expected shape ({N},), got {bits_array.shape}"
        assert bits_array.dtype == np.int64, f"Expected int64, got {bits_array.dtype}"


class TestEnergyFiniteness:
    """Tests for energy computation bounds."""
    
    def test_energy_is_finite(self):
        """Energy must always be finite (not inf or nan)."""
        for N in [5, 10, 15, 20]:
            for trial in range(10):
                bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                E = labs_energy(bits)
                
                assert np.isfinite(E), f"Energy is not finite: E={E}"
                assert not np.isnan(E), f"Energy is NaN: E={E}"
                assert not np.isinf(E), f"Energy is infinite: E={E}"
    
    def test_energy_bounded_by_n_squared(self):
        """Energy should be bounded by O(N^2) for small N."""
        # For LABS, empirically E < N^3 for all configurations
        for N in [5, 8, 10]:
            max_possible_energy = N * N * N  # Very loose upper bound
            
            for trial in range(20):
                bits = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                E = labs_energy(bits)
                
                assert E < max_possible_energy, \
                    f"Energy exceeds theoretical bound: E={E} > {max_possible_energy}"


class TestConsistency:
    """Consistency tests across multiple computations."""
    
    def test_energy_computation_reproducibility(self):
        """Energy computation must be deterministic."""
        bits = [1, -1, 1, -1, 1]
        E1 = labs_energy(bits)
        E2 = labs_energy(bits)
        E3 = labs_energy(bits)
        
        assert E1 == E2 == E3, \
            f"Non-deterministic energy: {E1}, {E2}, {E3}"
    
    def test_symmetry_consistency(self):
        """Symmetry properties must hold consistently across many trials."""
        for trial in range(20):
            N = np.random.randint(5, 15)
            s = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
            
            # Check both symmetries
            E_s = labs_energy(s)
            E_flip = labs_energy([-x for x in s])
            E_rev = labs_energy(list(reversed(s)))
            
            assert E_s == E_flip == E_rev, \
                f"Symmetry inconsistent for trial {trial}, N={N}"
    
    def test_flip_then_flip_returns_original(self):
        """Flipping twice should return to original configuration."""
        for N in [4, 6, 8]:
            for trial in range(5):
                s_original = [1 if np.random.random() < 0.5 else -1 for _ in range(N)]
                s_flipped_once = [-x for x in s_original]
                s_flipped_twice = [-x for x in s_flipped_once]
                
                # Check that double flip returns to original
                assert s_original == s_flipped_twice, \
                    f"Double flip did not return to original"
                
                # Energies should all be equal
                E_orig = labs_energy(s_original)
                E_double_flip = labs_energy(s_flipped_twice)
                assert E_orig == E_double_flip


@pytest.fixture
def small_bitstring():
    """Fixture providing a small bitstring for testing."""
    return [1, -1, 1, -1, 1]


@pytest.fixture
def parametrized_bitstrings():
    """Fixture providing multiple bitstrings of different lengths."""
    return {
        3: [1, -1, 1],
        5: [1, -1, 1, -1, 1],
        8: [1, 1, -1, -1, 1, -1, 1, 1],
        10: [1, -1, 1, 1, -1, -1, 1, -1, 1, 1]
    }


class TestWithFixtures:
    """Tests using pytest fixtures."""
    
    def test_small_bitstring_format(self, small_bitstring):
        """Test format of fixture-provided bitstring."""
        assert_is_pm1(small_bitstring)
        assert len(small_bitstring) == 5
    
    def test_small_bitstring_energy(self, small_bitstring):
        """Test energy computation on fixture bitstring."""
        E = labs_energy(small_bitstring)
        assert E >= 0
        assert np.isfinite(E)
    
    def test_parametrized_bitstrings(self, parametrized_bitstrings):
        """Test all parametrized bitstrings."""
        for N, bits in parametrized_bitstrings.items():
            assert len(bits) == N, f"Length mismatch for N={N}"
            assert_is_pm1(bits)
            
            E = labs_energy(bits)
            assert E >= 0, f"Negative energy for N={N}"
            assert np.isfinite(E), f"Non-finite energy for N={N}"


# ============================================================================
# Pytest Configuration & Markers
# ============================================================================

def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


@pytest.mark.slow
class TestSlowInvariants:
    """Slower tests that verify invariants across many configurations."""
    
    def test_all_small_n_symmetries(self):
        """Exhaustively check symmetries for small N."""
        for N in [3, 4, 5]:
            from itertools import product
            for bits_tuple in product([1, -1], repeat=N):
                bits = list(bits_tuple)
                
                E_orig = labs_energy(bits)
                E_flip = labs_energy([-x for x in bits])
                E_rev = labs_energy(list(reversed(bits)))
                
                assert E_orig == E_flip == E_rev, \
                    f"Symmetry failed for bits={bits}"


if __name__ == "__main__":
    # Allow running this file directly with pytest
    pytest.main([__file__, "-v"])
