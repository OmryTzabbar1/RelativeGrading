---
name: student-project-evaluator
description: Comparative evaluation tool for grading student coding projects against assignment requirements using dynamic baseline updates
---

# Student Project Evaluator

Evaluates student coding projects through comparative grading, where each project is assessed relative to the highest-graded project encountered so far.

## When to Use This Skill

- Instructor needs to grade student programming assignments
- Want relative quality scores based on documentation and implementation quality
- Need to identify standout projects in a class
- Require CSV export for gradebook integration

## Grading Philosophy

This skill uses a **documentation and quality-focused** evaluation framework defined in `grading_scale.yml`:

- **All projects should have**: documentation, research, graphics, planning
- **Grades differentiate on**: quality and detail level of these elements
- **Grade distribution**: Most students should fall in 75-85 range for solid work
- **95-100 range**: Reserved for truly exceptional, picture-perfect projects

See `grading_scale.yml` for complete grading scale and criteria.

## Execution Flow

### Step 1: Gather Required Information

**Prompt the user for:**

1. **Assignment Description**
   - "Please provide the assignment description or requirements that students were given."
   - This will be used to assess how well each project addresses the assignment

2. **Master Folder Path**
   - "What is the path to the folder containing all student project folders?"
   - Example: `E:/Assignments/WebDev_A1/`
   - Each student should have their own subfolder (already cloned git repositories)

3. **Baseline Student Information**
   - "Which student folder should I use as the initial baseline for comparison?"
   - "What grade (0-100) would you assign to this baseline student?"
   - "What is the path to the baseline student's folder?"

**Validate inputs:**
- Master folder path exists and is readable
- Baseline student folder exists within master folder
- Baseline grade is between 0-100

**Store these values** for use in subsequent steps.

---

### Step 2: Calibrate Baseline

**Goal**: Understand what quality level the baseline grade represents using the grading scale criteria.

**Actions:**

1. Navigate to the baseline student's folder
2. Use `analyze_repo.py` to detect project type and find actual project directory:
   ```python
   from analyze_repo import analyze_repository
   # auto_find_root=True recursively searches for project markers
   # Handles nested structures like: Participant_123/LLM_course/app/
   repo_info = analyze_repository(baseline_folder_path, auto_find_root=True)
   # repo_info includes 'actual_project_path' showing where project was found
   ```

   **Note**: The analyzer now supports:
   - Angular projects (angular.json)
   - Nested project structures (up to 3 levels deep)
   - Automatic discovery of actual code directory

3. Read and evaluate ALL documentation from actual_project_path:
   - **README.md** - Assess detail level, completeness (installation, usage, examples)
   - **Planning docs** - Look for problem statements, design rationale, architecture docs
   - **Research files** - Jupyter notebooks, data analysis, documented findings
   - **Visual elements** - Count screenshots, diagrams, charts in docs or separate folders
   - **Code quality** - Implementation completeness, organization, comments

4. **Evaluate against grading scale** (see `grading_scale.yml`):

   **Documentation Quality:**
   - Is README detailed and comprehensive, or basic?
   - Are planning/architecture docs present?
   - Is there inline code documentation?

   **Research Depth:**
   - Is there relevant research/analysis for the assignment?
   - Are findings well-documented?
   - Any data work (notebooks, visualizations)?

   **Visual Elements:**
   - How many screenshots/diagrams are included?
   - Are they professional quality?
   - Is UI/UX documented visually?

   **Planning Documentation:**
   - Is there a clear problem statement?
   - Are design decisions explained with rationale?

   **Implementation Quality:**
   - Does it meet assignment requirements?
   - Is code well-organized and complete?

5. **Determine baseline grade tier** based on above:
   - 95-100: Picture perfect (amazing docs, thorough research, rich graphics, polished)
   - 85-95: Great (all docs present, good research, quality visuals)
   - 75-85: Solid (adequate docs, some research, basic visuals) ← Most students
   - 65-75: Mid-low (minimal docs, lacking research or graphics)
   - 0-65: Incomplete (missing core documentation or requirements)

   **Document specific observations** for each criterion to justify the baseline grade.

5. Generate `assignment-config.yml` in the master folder:

```yaml
assignment:
  name: "{assignment name}"
  description: "{assignment description}"
  evaluated_date: "{today's date}"

baseline:
  student: "{baseline_student_name}"
  grade: {baseline_grade}
  features_observed:
    - "{feature 1}"
    - "{feature 2}"
    - "{feature 3}"

grading_weights:
  assignment_relevance: 50
  functionality: 50

focus_files:
  - "{pattern1}"  # e.g., "src/**/*.js"
  - "{pattern2}"  # e.g., "README.md"

project_type: "{detected_type}"

evaluation_criteria:
  - "{criterion 1}"
  - "{criterion 2}"
```

6. Display to user:
   ```
   ✓ Baseline established: {baseline_student} - {baseline_grade}/100

   Key features observed:
   - {feature 1}
   - {feature 2}

   Alignment with assignment: {summary}
   ```

**Set initial baseline state:**
- baseline_student = {student_name}
- baseline_grade = {grade}
- baseline_features = {list of observed features}

---

### Step 3: Discover Student Folders

**Actions:**

1. Use `scan_folders.py` to find all student folders:
   ```python
   from scan_folders import scan_student_folders
   students = scan_student_folders(master_folder, exclude=[baseline_student])
   ```

2. **RECOMMENDED: Pre-flight Validation** (prevents mid-evaluation issues)
   ```python
   from validate_structure import validate_student_folders, print_validation_report

   validation = validate_student_folders(master_folder, exclude=[baseline_student])
   print_validation_report(validation)
   ```

   This checks for:
   - Nested/inconsistent directory structures
   - Undetectable project types
   - Empty or malformed folders

   **If errors found**: Ask user if they want to continue or fix issues first.

3. Display found students:
   ```
   Found {count} student folders (excluding baseline).
   Beginning comparative evaluation...
   ```

4. Confirm with user if needed

---

### Step 4: Batch Evaluation Loop

**Process students in batches of 5** to manage context.

For each student in the current batch:

#### 4.1 Read Student Project

1. Use `analyze_repo.py` to get metadata and find actual project:
   ```python
   from analyze_repo import analyze_repository
   # Automatically finds project even if nested (e.g., student/code/app/)
   repo_info = analyze_repository(student_folder_path, auto_find_root=True)

   # Use repo_info['actual_project_path'] to read files from correct location
   actual_path = repo_info['actual_project_path']
   ```

   **Important**: `repo_info` now includes:
   - `project_type`: Now includes 'angular' in addition to existing types
   - `actual_project_path`: Where the project was actually found
   - Other metadata: team_name, student_id, size_mb, file_count

2. Read key files from actual_project_path (focus on those defined in assignment-config.yml):
   - README.md
   - Main source code files
   - Configuration files

#### 4.2 Comparative Analysis

Compare against **current baseline** (highest-graded student so far) using the grading scale criteria:

**Documentation Quality (Primary Factor):**
- Is README more/less detailed than baseline?
- Are planning docs better/worse/similar?
- More/fewer architecture or design documents?
- Better/worse inline code documentation?

**Research Depth:**
- More/less thorough research than baseline?
- Better/worse documented findings?
- More/fewer data analysis artifacts (notebooks, visualizations)?

**Visual Elements:**
- More/fewer screenshots than baseline?
- Better/worse quality diagrams and charts?
- More/less comprehensive UI/UX documentation?

**Planning Documentation:**
- Clearer/less clear problem statement than baseline?
- Better/worse explained design rationale?
- More/less detailed planning artifacts?

**Implementation Quality:**
- More/fewer features than baseline?
- Better/worse code organization?
- More/less complete implementation?

**Grade Adjustment Guidelines** (from `grading_scale.yml`):
- Significantly better across criteria: +5 to +15 points
- Moderately better: +2 to +8 points
- Similar quality: -2 to +2 points
- Moderately worse: -2 to -8 points
- Significantly worse: -5 to -15 points

**Remember**: Most students should fall in 75-85 range. Only truly exceptional work deserves 95-100.

#### 4.3 Calculate Grade

```
relevance_adjustment = {-10 to +20}
functionality_adjustment = {-10 to +20}
final_grade = baseline_grade + relevance_adjustment + functionality_adjustment
final_grade = max(0, min(100, final_grade))  # Clamp to 0-100
```

#### 4.4 Display Evaluation

```
Evaluating: {student_name} ({current_index}/{total_students})

Comparison to current baseline ({baseline_student} - {baseline_grade}/100):

Assignment Relevance:
- {specific observations}
- Adjustment: {+/-X points}

Functionality:
- {specific observations}
- Adjustment: {+/-X points}

GRADE: {final_grade}/100
Reasoning: {1-2 sentence summary}
```

#### 4.5 Store Evaluation

Store for each student:
- student_name
- student_id (if found)
- team_name (if found)
- grade
- relevance_score
- functionality_score
- reasoning
- compared_to_baseline
- notes

#### 4.6 Update Baseline If Better

```python
if final_grade > baseline_grade:
    baseline_student = current_student
    baseline_grade = final_grade
    baseline_features = current_student_features

    Display: "✓ New baseline: {student_name} - {grade}/100"
```

#### 4.7 Error Handling

If error occurs (empty folder, missing files, can't read):
- Skip student
- Store status as 'manual_review'
- Log error: "⚠️  {student_name}: {error_reason} - flagged for manual review"
- Continue to next student

**Repeat for all students in batches of 5**

---

### Step 5: Generate Outputs

After evaluating all students:

#### 5.1 Generate CSV File

Create `grades.csv` in master folder:

```csv
Student,ID,Grade,Rank,Team,Notes
{student_name},{student_id},{grade},{rank},{team_name},"{brief_reasoning}"
...
```

- Sort by grade (descending) before assigning ranks
- Rank 1 = highest grade

#### 5.2 Generate Markdown Report

Create `evaluation_summary.md` in master folder:

```markdown
# Student Project Evaluation Summary

**Assignment**: {assignment_name}
**Date**: {date}
**Total Students**: {count}

---

## Statistics

- **Highest Grade**: {max}/100 ({student_name})
- **Lowest Grade**: {min}/100 ({student_name})
- **Average Grade**: {avg}/100
- **Median Grade**: {median}/100
- **Standard Deviation**: {std_dev}

---

## Grade Distribution

| Grade Range | Count | Percentage |
|-------------|-------|------------|
| 90-100      | {n}   | {%}        |
| 80-89       | {n}   | {%}        |
| 70-79       | {n}   | {%}        |
| 60-69       | {n}   | {%}        |
| Below 60    | {n}   | {%}        |

---

## Individual Evaluations

### {Student 1}
- **Grade**: {grade}/100
- **Compared to**: {baseline_at_time}
- **Strengths**: {list}
- **Reasoning**: {summary}

### {Student 2}
...

---

## Students Requiring Manual Review

{List students that were skipped with reasons}
```

#### 5.3 Display Completion Summary

```
✅ Evaluation complete!

Generated files:
- grades.csv ({full_path})
- evaluation_summary.md ({full_path})
- assignment-config.yml ({full_path})

📊 Quick Stats:
- Students evaluated: {count}
- Students flagged for review: {count}
- Average grade: {avg}/100
- Highest: {student} ({grade}/100)
- Lowest: {student} ({grade}/100)

Baseline progression: {show if baseline changed during evaluation}
```

---

## Important Guidelines

### Grading Principles

**Follow the grading scale** defined in `grading_scale.yml`:

1. **Documentation-focused**: Documentation quality is the primary differentiator
2. **Quality over presence**: All projects should have docs; grades reflect detail level
3. **Grade distribution**: Most students should fall in 75-85 range
4. **High bar for excellence**: 95-100 reserved for truly exceptional work

**Evaluation approach:**
1. **Be objective**: Base grades on observable characteristics (docs, research, graphics, code)
2. **Be specific**: Cite exact files, sections, and quality differences when comparing
3. **Be consistent**: Use the grading scale criteria across all students
4. **Be transparent**: Explain grade adjustments with specific evidence

### Comparative Evaluation Tips

- **Baseline reference**: Always compare to the current best, not the original baseline
- **Relative scoring**: Grades reflect quality relative to peers, not absolute perfection
- **Context matters**: Consider different approaches to the same problem
- **Feature parity**: If project has similar features to baseline, grade should be similar

### Error Handling

- **Empty folder**: Flag for manual review, note "Empty submission"
- **Missing README**: Still evaluate code, note "No documentation provided"
- **Build failures**: If project won't compile/run, note but continue with static analysis
- **Unexpected structure**: Adapt to find main files, note unusual structure

---

## Example Session

**User**: "I need to grade student projects for my web development assignment"

**Claude**:
```
I'll help you evaluate student projects comparatively. Let me gather the necessary information.

Please provide:
1. The assignment description or requirements
2. Path to the folder containing student project folders
3. Which student should be the initial baseline and their grade (0-100)
```

**User**:
```
Assignment: Create a todo list web app with CRUD functionality, LocalStorage, and responsive design.
Path: E:/Students/WebDev_A1/
Use student_alice as baseline with grade 85, path: E:/Students/WebDev_A1/student_alice
```

**Claude**:
```
✓ Reading baseline project: student_alice

{analyzes files...}

✓ Baseline established: student_alice - 85/100

Key features observed:
- Full CRUD operations (create, read, update, delete tasks)
- LocalStorage persistence working
- Responsive design with CSS Grid
- Clean code structure

Found 29 student folders. Beginning evaluation...

---

Evaluating: student_bob (1/29)

{reads and analyzes...}

Comparison to current baseline (student_alice - 85/100):

Assignment Relevance:
- Implements all CRUD operations ✓
- LocalStorage working ✓
- Added dark mode toggle (extra feature) ✓
- Adjustment: +8 points

Functionality:
- More polished UI than baseline
- Better error handling
- Adjustment: +7 points

GRADE: 100/100

✓ New baseline: student_bob - 100/100

---

{continues for all 29 students...}

---

✅ Evaluation complete!

Generated files:
- grades.csv (E:/Students/WebDev_A1/grades.csv)
- evaluation_summary.md (E:/Students/WebDev_A1/evaluation_summary.md)
- assignment-config.yml (E:/Students/WebDev_A1/assignment-config.yml)

📊 Quick Stats:
- Students evaluated: 29
- Average grade: 78/100
- Highest: student_bob (100/100)
- Lowest: student_dan (55/100)
```

---

**End of Skill**
