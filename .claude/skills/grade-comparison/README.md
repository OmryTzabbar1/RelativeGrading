# Grade Comparison Skill

Compares automated evaluator grades with actual grades from PDF grading breakdowns.

## Quick Start

```bash
# From project root
python .claude/skills/grade-comparison/scripts/compare_grades.py tests/WorkSubmissions01
```

## What It Does

1. **Loads evaluator grades** from `outputs/grades.xlsx`
2. **Scans student folders** in WorkSubmissions directory
3. **Extracts actual grades** from `Detailed_Grade_Breakdown_{student_id}.pdf` files
4. **Calculates comparison metrics**:
   - Mean difference
   - Correlation coefficient
   - RMSE
   - Accuracy within ±5 and ±10 points
5. **Generates Excel report** with comparison, statistics, and discrepancies

## Prerequisites

```bash
pip install openpyxl pdfplumber numpy
```

## Usage

### As a Skill (Recommended)

Invoke from Claude Code:

```
User: "Compare the evaluator grades with actual grades for WorkSubmissions01"
```

Claude will use the `grade-comparison` skill automatically.

### As a Standalone Script

```bash
cd E:\Projects\student-project-evaluator
python .claude/skills/grade-comparison/scripts/compare_grades.py tests/WorkSubmissions01
```

## Input Requirements

1. **Evaluator Grades**: `outputs/grades.xlsx` must exist (run `evaluating-student-projects` first)
2. **Student Folders**: WorkSubmissions folder with structure:
   ```
   WorkSubmissions01/
   ├── Participant_38951_assignsubmission_file/
   │   ├── Detailed_Grade_Breakdown_38951.pdf  ← Grade PDF
   │   └── ...
   ├── Participant_38953_assignsubmission_file/
   │   ├── Detailed_Grade_Breakdown_38953.pdf
   │   └── ...
   ```

## Output

### Console Output

```
================================================================================
GRADE COMPARISON TOOL
================================================================================

Loading evaluator grades from: outputs/grades.xlsx
Found 36 students in evaluator results

Scanning WorkSubmissions folder: E:\...\WorkSubmissions01
Found 36 student folders

Extracting actual grades from PDFs...
[1/36] Student 38951: Actual=85.0, Evaluator=77.8, Diff=-7.2
[2/36] Student 38953: Actual=70.0, Evaluator=61.6, Diff=-8.4
...

================================================================================
SUMMARY STATISTICS
================================================================================

Mean Evaluator Grade:   64.5
Mean Actual Grade:      72.3
Mean Difference:        -7.8 (evaluator grades LOWER on average)
Mean Absolute Error:    9.2
Correlation:            0.85 (strong correlation)
RMSE:                   10.4

Students within ±5 points:   12/36 (33.3%)
Students within ±10 points:  28/36 (77.8%)

================================================================================

Saved: outputs/grade_comparison.xlsx
```

### Excel Report (`outputs/grade_comparison.xlsx`)

**Sheet 1: Comparison**
- Student-by-student comparison
- Color-coded by accuracy (green: ±5, yellow: ±10, red: >10)

**Sheet 2: Statistics**
- Mean grades
- Correlation coefficient
- RMSE
- Accuracy metrics

**Sheet 3: Discrepancies**
- Students with >15 point differences
- Sorted by magnitude of discrepancy

## Interpretation

### Correlation Coefficient

- **0.9-1.0**: Excellent agreement
- **0.7-0.9**: Strong correlation
- **0.5-0.7**: Moderate correlation
- **<0.5**: Weak correlation

### Mean Difference

- **Positive**: Evaluator over-grades on average
- **Negative**: Evaluator under-grades on average
- **Near 0**: Well-calibrated

### Mean Absolute Error

- **<5**: Excellent accuracy
- **5-10**: Good accuracy
- **10-15**: Fair accuracy
- **>15**: Needs calibration

## Troubleshooting

**Error: "Could not find outputs/grades.xlsx"**
- Run `evaluating-student-projects` skill first to generate grades

**Warning: "PDF not found for student X"**
- Check that `Detailed_Grade_Breakdown_{student_id}.pdf` exists in student folder

**Warning: "Could not parse grade from PDF"**
- PDF may be scanned image (not text-based)
- Grade format may not match expected patterns
- Manually check PDF to verify grade format

**Error: "WorkSubmissions path does not exist"**
- Verify the path is correct
- Use absolute path if relative path fails

## Grade Extraction Patterns

The script looks for these patterns in PDFs:

- `Total Grade: XX.X`
- `Final Grade: XX.X`
- `Overall Grade: XX.X`
- `Grade: XX.X%`
- `Grade: XX.X/100`
- `Score: XX.X`

If your PDFs use a different format, edit the `parse_grade_from_text()` function in `compare_grades.py`.

## Example Use Cases

1. **Validate evaluator accuracy**: Compare automated grades with instructor grades
2. **Calibrate evaluation criteria**: Identify which criteria correlate with actual performance
3. **Find outliers**: Identify students where automated evaluation significantly differs
4. **Improve evaluation**: Use discrepancies to refine criteria weights and extraction rules

## Dependencies

- **openpyxl**: Excel file generation
- **pdfplumber** (preferred) or **PyPDF2**: PDF parsing
- **numpy**: Statistical calculations

Install all:
```bash
pip install openpyxl pdfplumber numpy
```
