# SUBMISSION ENTRY POINT FOR JUDGES

All materials needed to evaluate this submission are in the `team-submissions/` directory.

## Quick Start (3 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Tests
```bash
# Option A: Comprehensive test suite (11 tests, ~2 sec)
python tests_comprehensive.py

# Option B: Pytest-based invariants (17 tests, ~0.1 sec)
pytest test_invariants.py -v
```

**Expected Result:** ALL TESTS PASSED ✓

### 3. Review Documentation
- **README:** [`SUBMISSION_README.md`](SUBMISSION_README.md) ← Start here for complete overview
- **Checklist:** [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) ← Verify all deliverables
- **AI Workflow:** [`AI_REPORT_SUMMARY.md`](AI_REPORT_SUMMARY.md) ← See AI-assisted workflow details

## What's Here

| File | Purpose |
|------|---------|
| `SUBMISSION_README.md` | Complete quickstart & repo map |
| `SUBMISSION_CHECKLIST.md` | Deliverables tracker |
| `AI_REPORT_SUMMARY.md` | AI assistance documentation + code examples |
| `AI_Report_Phase1.txt` | Phase 1 details |
| `AI_Report_Phase2.txt` | Phase 2 details |
| `PRD.md` | Product Requirements Document |
| `TEST_SUITE.md` | Testing strategy |
| `tests_comprehensive.py` | Full test suite (Phase 1 & 2) |
| `test_invariants.py` | Pytest-based invariant tests |
| `requirements.txt` | Python dependencies |

## Key Results

- ✅ **28 Tests Passing** (11 comprehensive + 17 pytest)
- ✅ **Energy Symmetries Validated** (global flip, sequence reversal)
- ✅ **Ground Truth Verified** (brute-force comparison N=3-5)
- ✅ **CPU-Ready** (no GPU required for Phase 1)
- ✅ **AI Workflow Transparent** (documented with examples)

## Next Steps

1. Read [`SUBMISSION_README.md`](SUBMISSION_README.md) for full context
2. Run the tests (above) to verify everything works
3. Check [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) to confirm deliverables
4. Review [`AI_REPORT_SUMMARY.md`](AI_REPORT_SUMMARY.md) for AI workflow insights

---

**All judge-facing materials are in this directory. Nothing else needs to be accessed.**
