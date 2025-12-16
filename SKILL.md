---
name: student-evaluator-v2
description: Evaluate student projects using sliding window criteria discovery with true relative grading
---

# Student Project Evaluator v2.0 - Sliding Window Skill

## When to Use This Skill

Use this skill when the user wants to:
- Evaluate multiple student coding projects fairly and comprehensively
- Grade student submissions with relative scoring (best = 100)
- Generate evaluation reports with criteria evolution tracking
- Discover quality criteria organically from actual student work

## Overview

This skill implements a **two-phase sliding window evaluation approach**:

**Phase 1: Criteria Discovery**
- Analyze students in overlapping windows of 3
- Build comprehensive criteria from all projects
- Track which student introduced each quality dimension

**Phase 2: Final Evaluation**
- Evaluate ALL students against complete discovered criteria
- Assign TRUE relative grades (only best student gets 100)
- Generate comprehensive reports

## Execution Flow

### Step 1: Gather Information

Ask the user for:
1. **Master folder path**: Location of student project folders
2. **Window size** (optional): Number of students per window (default: 3)
3. **Output directory** (optional): Where to save results (default: ./outputs)
4. **Exclusions** (optional): Folders to skip (e.g., baseline, .git)

Example questions:
```
I'll help you evaluate student projects using the sliding window approach.

1. What is the path to the folder containing student projects?
2. What window size would you like to use? (default: 3)
3. Where should I save the output files? (default: ./outputs)
4. Are there any folders I should exclude from evaluation?
```

### Step 2: Validate and Confirm

Use the Bash tool to verify the master folder exists and count student folders:

```bash
ls "<master_folder>" | grep -c "^[^.]"
```

Display configuration to user for confirmation:
```
Configuration:
- Master folder: <path>
- Window size: <N>
- Output directory: <path>
- Student folders found: <count>

Should I proceed with the evaluation? (yes/no)
```

### Step 3: Run Phase 1 - Criteria Discovery

Execute the sliding window analyzer using the Bash tool:

```bash
cd "<project_root>" && python -c "
import sys
sys.path.insert(0, '.')
from scripts.sliding_window_analyzer import analyze_sliding_windows, save_discovered_criteria
from scripts.utils import scan_student_folders

# Scan folders
student_folders = scan_student_folders('<master_folder>', exclude=[<exclusions>])
print(f'Found {len(student_folders)} students')

# Run Phase 1
criteria = analyze_sliding_windows(student_folders, window_size=<window_size>)

# Save criteria
save_discovered_criteria(criteria, '<output_dir>/discovered_criteria.yml')
"
```

**Expected output:**
- Progress messages showing each window analysis
- "[NEW]" messages when students add new criteria dimensions
- Summary of total dimensions discovered

**Display to user:**
```
Phase 1 Complete: Criteria Discovery

Discovered <N> quality dimensions:
- documentation (introduced by <student>)
- testing (introduced by <student>)
- graphics (introduced by <student>)
- research (introduced by <student>)
- code_quality (introduced by <student>)

Criteria saved to: <output_dir>/discovered_criteria.yml

Would you like to review the discovered criteria before proceeding to Phase 2?
```

### Step 4: (Optional) Review Criteria

If user wants to review, use the Read tool to display the discovered_criteria.yml file:

```
Here are the discovered criteria:

<display criteria YAML>

The criteria shows all quality dimensions found across student projects.
Each dimension has properties that will be used for scoring.

Proceed to Phase 2? (yes/no)
```

### Step 5: Run Phase 2 - Final Evaluation

Execute the final evaluation:

```bash
cd "<project_root>" && python -c "
import sys
sys.path.insert(0, '.')
from scripts.sliding_window_analyzer import load_discovered_criteria
from scripts.final_evaluator import evaluate_all_students
from scripts.analyze_project import analyze_project
from scripts.utils import scan_student_folders
from scripts.output_generator import generate_csv, generate_markdown_report

# Load criteria
criteria = load_discovered_criteria('<output_dir>/discovered_criteria.yml')

# Scan and analyze all students
student_folders = scan_student_folders('<master_folder>', exclude=[<exclusions>])
project_features = {}

for path in student_folders:
    project_features[path] = analyze_project(path)

# Evaluate all students
evaluations = evaluate_all_students(student_folders, criteria, project_features)

# Generate outputs
generate_csv(evaluations, '<output_dir>/grades.csv')
generate_markdown_report(evaluations, criteria, '<output_dir>/evaluation_report.md')

# Display summary
print(f'\\nEvaluated {len(evaluations)} students')
print(f'Best grade: {evaluations[0].grade} ({evaluations[0].student_name})')
print(f'Mean grade: {sum(e.grade for e in evaluations)/len(evaluations):.2f}')
print(f'\\nTop 5 students:')
for e in evaluations[:5]:
    print(f'  {e.rank}. {e.student_name}: {e.grade}/100')
"
```

**Display to user:**
```
Phase 2 Complete: Final Evaluation

Evaluated <N> students
Best grade: <grade> (<student_name>)
Mean grade: <mean>

Top 5 Students:
1. <student>: <grade>/100
2. <student>: <grade>/100
3. <student>: <grade>/100
4. <student>: <grade>/100
5. <student>: <grade>/100

Output files generated:
✓ discovered_criteria.yml
✓ grades.csv
✓ evaluation_report.md
```

### Step 6: Present Results

Use the Read tool to show key parts of the evaluation report:

```
## Summary Statistics

<display summary section from evaluation_report.md>

## Top 10 Projects

<display top 10 table>

Would you like me to:
1. Show the full evaluation report
2. Show specific student details
3. Export results to a different format
4. Run the evaluation again with different settings
```

### Step 7: Follow-up Actions

Offer additional actions based on user needs:

**Option 1: Show Full Report**
- Use Read tool to display complete evaluation_report.md

**Option 2: Show Specific Student**
- Ask for student name
- Extract and display their section from the report

**Option 3: Compare with Manual Grades**
- If user has manual grades, offer to add them to the CSV
- Use pandas or csv manipulation to merge data

**Option 4: Re-run Evaluation**
- Offer different window sizes
- Option to exclude certain students
- Adjust output directory

## Error Handling

### No Student Folders Found

If scan returns 0 folders:
```
I couldn't find any student folders in <master_folder>.

Please check:
1. Is the path correct?
2. Are student projects in subdirectories?
3. Should I exclude any folders? (e.g., .git, baseline)

Would you like to try a different folder path?
```

### Student Analysis Errors

If a student folder causes errors during analysis:
```
Warning: Could not analyze <student_name>
Reason: <error_message>

This student will receive a score of 0.
Should I continue with the remaining students? (yes/no)
```

### Missing Dependencies

If Python modules are missing:
```
Error: Required Python packages not installed.

Please run: pip install -r requirements.txt

Then try the evaluation again.
```

## Example Session

```
User: I need to evaluate student projects in E:/Assignments/WebDev_A1/

Claude: I'll help you evaluate the student projects using the sliding window approach.

First, let me check the folder...

[runs ls command]

I found 35 student project folders in E:/Assignments/WebDev_A1/

Configuration:
- Master folder: E:/Assignments/WebDev_A1/
- Window size: 3 (default)
- Output directory: ./outputs
- Students to evaluate: 35

Should I proceed with Phase 1 (Criteria Discovery)? (yes/no)

User: yes

Claude: Starting Phase 1: Criteria Discovery...

[executes sliding window analysis]

============================================================
Phase 1: Sliding Window Criteria Discovery
============================================================
Total students: 35
Window size: 3
Number of windows: 33
============================================================

Window 1/33: Analyzing ['student_1', 'student_2', 'student_3']
  [NEW] student_1 added: documentation, testing, graphics, code_quality

Window 2/33: Analyzing ['student_2', 'student_3', 'student_4']
  [NEW] student_4 added: research

...

============================================================
Criteria Discovery Complete
============================================================
Total dimensions discovered: 5
Dimensions: documentation, testing, graphics, research, code_quality
============================================================

Phase 1 Complete!

Discovered 5 quality dimensions:
- documentation (introduced by student_1)
- testing (introduced by student_1)
- graphics (introduced by student_1)
- research (introduced by student_4)
- code_quality (introduced by student_1)

Should I proceed to Phase 2 (Final Evaluation)? (yes/no)

User: yes

Claude: Starting Phase 2: Final Evaluation...

[executes final evaluation]

Phase 2 Complete!

Evaluated 35 students
Best grade: 100 (student_alice)
Mean grade: 73.2

Top 5 Students:
1. student_alice: 100/100
2. student_bob: 92/100
3. student_carol: 87/100
4. student_dave: 84/100
5. student_eve: 81/100

Output files generated:
✓ discovered_criteria.yml
✓ grades.csv
✓ evaluation_report.md

All files saved to: ./outputs/

Would you like to see the full evaluation report?
```

## Important Notes

1. **Only ONE student gets 100**: This is TRUE relative grading - the best student sets the standard
2. **Criteria evolves**: Each window may add new quality dimensions
3. **All students re-evaluated**: After discovery, everyone is scored against the same complete criteria
4. **Progress tracking**: The skill shows real-time progress during analysis
5. **Transparent results**: Evolution log shows exactly which student introduced each criterion

## Technical Details

**Helper Scripts Used:**
- `scripts/sliding_window_analyzer.py`: Phase 1 implementation
- `scripts/final_evaluator.py`: Phase 2 implementation
- `scripts/analyze_project.py`: Feature extraction from projects
- `scripts/criteria_builder.py`: Criteria management
- `scripts/output_generator.py`: CSV and markdown generation
- `scripts/utils.py`: Helper functions

**Quality Dimensions Detected:**
- Documentation (README, PRD, Architecture, PROMPT_BOOK)
- Testing (test files, coverage)
- Graphics (images, diagrams, screenshots)
- Research (notebooks, analysis documents)
- Code Quality (file count, structure, organization)

**Grading Scale:**
- 100%: Best student only
- 95-99%: 90-99 grade
- 80-94%: 75-89 grade
- 60-79%: 60-74 grade
- <60%: proportional

## Version History

- **v2.0** (2025-12-16): Sliding window criteria discovery approach
- **v1.0** (2024-12-15): Original baseline comparison approach
