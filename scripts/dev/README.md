# Development & Testing Utilities

These scripts are development helpers for validating, testing, and analyzing evaluation results.

## Validation Scripts

### validate_output.py
**Purpose:** Comprehensive validation of `criteria_graph_final.json`

**Checks:**
- Structure validation (metadata, criteria keys)
- Metadata completeness
- Student ID validation
- Category distribution
- Data integrity

**Usage:**
```bash
python validate_output.py
```

---

### validate_simple.py
**Purpose:** Quick validation of `criteria_graph_final.json`

**Checks:**
- Basic structure validation
- Student count verification (hardcoded to 36)
- Top 10 criteria display

**Note:** Contains hardcoded student count - update as needed

**Usage:**
```bash
python validate_simple.py
```

---

## Analysis Scripts

### analyze_results.py
**Purpose:** Analyze criteria distribution by category

**Output:**
- Total criteria count
- Least common criteria (bottom 20)
- All criteria grouped by category

**Usage:**
```bash
python analyze_results.py
```

---

### verify_student.py
**Purpose:** Check criteria for a specific student

**Hardcoded Student:** 38953 (update in script to check others)

**Output:**
- Total criteria count for student
- All criteria with category, name, and prevalence

**Usage:**
```bash
# Edit script to change student_id first
python verify_student.py
```

---

### sample_students_report.py
**Purpose:** Generate detailed report for sample students

**Hardcoded Students:** 38954, 38953, 38960, 38979, 38957, 38966

**Output:**
- Criteria count per student
- Category coverage
- Rarity indicators (Common/Uncommon/Rare)

**Usage:**
```bash
# Edit script to change sample_students list
python sample_students_report.py
```

---

## Note on Hardcoded Values

Many of these scripts contain hardcoded:
- Student IDs
- Total student counts (e.g., 36)
- File paths (E:/Projects/student-project-evaluator/...)

Update these values as needed for your specific evaluation.

## Typical Development Workflow

1. Run evaluation
2. Validate output: `python validate_output.py`
3. Analyze results: `python analyze_results.py`
4. Check specific student: Edit and run `verify_student.py`
5. Sample report: Edit and run `sample_students_report.py`
