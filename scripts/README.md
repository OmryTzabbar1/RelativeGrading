# Student Project Evaluator Scripts

Production scripts for student project evaluation.

---

## Directory Structure

```
scripts/
├── run_evaluation.py      # Main integrated evaluation script
├── organize_outputs.py    # Organize outputs by submission
├── dev/                   # Development & testing utilities
└── README.md             # This file
```

---

## Main Scripts

### run_evaluation.py
**Purpose:** Main integrated evaluation script with code verification and assignment profiles.

**Features:**
- Markdown criteria extraction
- Code verification (Git analysis, security scanning, quality tools)
- Assignment-specific calibration profiles
- Rarity bonus system (no grading curve)
- Excel and JSON outputs

**Usage:**
```bash
python scripts/run_evaluation.py tests/WorkSubmissions05
```

**Outputs:**
- `outputs/criteria_graph_final.json` - Complete criteria data
- `outputs/grades.xlsx` - Student grades with rarity bonuses
- `outputs/EVALUATION_SUMMARY.md` - Summary report

---

### organize_outputs.py
**Purpose:** Organize evaluation outputs into submission-specific folders.

**Usage:**
```bash
python scripts/organize_outputs.py WorkSubmissions05
```

**What it does:**
- Creates `outputs/WorkSubmissions05/` directory
- Moves all evaluation outputs there
- Prevents overwriting when evaluating multiple submissions

---

## Development Utilities

**Location:** `scripts/dev/`

- `validate_output.py` - Comprehensive output validation
- `validate_simple.py` - Quick validation
- `analyze_results.py` - Criteria distribution analysis
- `verify_student.py` - Single student criteria verification
- `sample_students_report.py` - Generate sample reports

See `scripts/dev/README.md` for details.

---

## Standard Workflow

**Complete evaluation workflow:**

```bash
# 1. Run evaluation
python scripts/run_evaluation.py tests/WorkSubmissions05

# 2. Organize outputs
python scripts/organize_outputs.py WorkSubmissions05

# 3. Compare with actual grades
python compare_grades.py WorkSubmissions05
```

**Result:**
- All outputs in `outputs/WorkSubmissions05/`
- Grade comparison in `outputs/WorkSubmissions05/grade_comparison.xlsx`

---

## Core Evaluation Logic

The evaluation skill logic is located in:
```
.claude/skills/evaluating-student-projects/
├── code_analysis.py          # Code verification module
├── assignment_profiles.py    # Assignment-specific profiles
├── EXTRACTION.md            # Criteria extraction rules
├── CATEGORIES.md            # Category definitions
└── SKILL.md                 # Skill instructions
```

---

## Related Documentation

- `EVALUATION_WORKFLOW.md` - Complete workflow guide
- `IMPROVEMENT_RECOMMENDATIONS.md` - Accuracy improvements
- `docs/INTEGRATED_EVALUATION_RESULTS.md` - Results analysis
- `docs/grading_system_recommendation.md` - Grading system analysis

---

## Grading System

**Current system (implemented):**
- ❌ No grading curve (removed)
- ✅ Absolute percentage scores
- ✅ Rarity bonus: +1 point per rare criterion (≤15% prevalence)
- ✅ Final grade = Percentage + Rarity Bonus (capped at 100)

**Results:**
- WS05: -0.0 bias, 0.903 correlation (excellent!)
- WS04: +0.3 bias, 0.709 correlation
- WS06: -3.6 bias, 0.736 correlation
