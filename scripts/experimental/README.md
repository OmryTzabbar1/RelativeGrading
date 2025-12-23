# Experimental Evaluation Scripts

These are alternative implementations and experimental approaches to student project evaluation. They are **not** part of the standard workflow defined in SKILL.md.

## Scripts

### comprehensive_evaluation.py
**Purpose:** Alternative evaluation implementation with enhanced extraction rules.

**Features:**
- Filename-based criteria detection
- Section header detection
- Liberal pattern matching
- Case-insensitive matching

**Status:** Experimental - not used in current workflow

---

### granular_evaluation.py
**Purpose:** Extracts very specific, granular criteria rather than broad categories.

**Examples:**
- "31 unit tests" (not just "Unit Tests")
- "80% code coverage" (not just "Test Coverage")
- "Docker Compose support" (not just "Docker")

**Status:** Experimental - may be too granular for fair comparison

---

### evaluate_criteria.py
**Purpose:** Criteria discovery script for WorkSubmissions01.

**Features:**
- Analyzes markdown documentation
- Discovers and categorizes criteria
- Hardcoded for WorkSubmissions01 path

**Status:** Legacy - WorkSubmissions01-specific implementation

---

## Usage

These scripts are not part of the standard workflow. They may be useful for:
- Experimenting with alternative extraction approaches
- Testing new evaluation methodologies
- Research and comparison with the standard approach

**Warning:** These scripts may have hardcoded paths and may not work with the current data structure without modification.
