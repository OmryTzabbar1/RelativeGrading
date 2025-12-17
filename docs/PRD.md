# Product Requirements Document (PRD)
# Student Project Evaluator - Markdown Criteria Discovery

**Version:** 3.0
**Date:** 2025-12-17
**Status:** Active
**Author:** Development Team

---

## 1. Project Overview

### 1.1 Context and Background

Academic project evaluation requires fair, comprehensive criteria that reflect the collective work demonstrated across all student submissions. Traditional approaches face key limitations:

1. **Predetermined Rubrics**: Define criteria before seeing student work, missing innovative approaches
2. **Code-Based Analysis**: Scanning files/folders is slow and misses the "big picture"
3. **Incomplete Context**: File presence doesn't indicate quality or completeness

The **Student Project Evaluator v3.0** uses a **Markdown-Based Criteria Discovery** approach that:
- Reads `.md` files (README, PRD, Architecture, etc.) which provide holistic project summaries
- Extracts criteria organically from what students document
- Weights criteria by prevalence across the class

### 1.2 Problem Statement

Current evaluation approaches have three issues:

1. **Slow Analysis**: Scanning entire project structures is time-consuming
2. **Missing Context**: File existence doesn't prove implementation quality
3. **Predetermined Bias**: Fixed rubrics miss what students actually built

### 1.3 Innovation: Markdown-Based Criteria Discovery

**Core Concept**: Markdown files summarize projects better than file trees. A README mentions testing, architecture, research, costs - giving a complete picture.

**Process**:
```
For each student:
    Read all .md files
    Extract mentioned criteria (with context validation)
    Add student to each criterion's list

Result: Criteria graph showing who has what
Weight: Based on prevalence (more students = higher weight)
Grade: Weighted score of criteria present
```

**Benefits**:
- Fast: Only reads markdown files, not entire codebase
- Holistic: Markdown summarizes the full project
- Fair: Criteria discovered from actual student work
- Weighted: Common criteria matter more than rare ones

---

## 2. Target Audience

### 2.1 Primary User Persona

**Name**: Dr. Sarah Chen
**Role**: Assistant Professor, Computer Science

**Use Case**:
- 35 students submitted coding projects
- Each has README.md and other documentation
- Wants fair grading based on what students documented

**Success Scenario**: Tool reads all markdown files, discovers 50+ criteria, weights them by prevalence, and generates relative grades. Students with comprehensive documentation score higher.

---

## 3. Project Goals

### 3.1 Objectives

| Goal | Description | Success Metric |
|------|-------------|----------------|
| **Speed** | Analyze projects quickly via markdown only | 35 students in <20 minutes |
| **Fairness** | Weight criteria by class prevalence | Common criteria weighted higher |
| **Transparency** | Show exactly what criteria were found | Criteria list with student counts |
| **Accuracy** | Context-aware extraction | "Not implemented" doesn't count |

---

## 4. Functional Requirements

### 4.1 Must-Have Features (P0)

| Feature ID | Feature | Acceptance Criteria |
|------------|---------|---------------------|
| **P0.1** | Markdown File Discovery | Find all .md files in each student project |
| **P0.2** | Criteria Extraction | Extract specific features/elements mentioned in markdown |
| **P0.3** | Context Validation | Only count criteria that are documented as implemented |
| **P0.4** | Single-Pass Population | Build criteria list AND track which students have each |
| **P0.5** | Broad Category Grouping | Group granular criteria into categories (Testing, Docs, etc.) |
| **P0.6** | Irrelevant Criteria Flagging | Flag uncategorized criteria for manual review |
| **P0.7** | Prevalence-Based Weighting | Weight = students_with_criterion / total_students |
| **P0.8** | Relative Grading | Calculate grades from weighted criteria scores |
| **P0.9** | CSV Export | Student, Grade, Rank, Criteria breakdown |
| **P0.10** | Criteria Report | Markdown showing all criteria, categories, weights |

### 4.2 Criteria Categories (Broad Topics)

| Category | Example Granular Criteria |
|----------|--------------------------|
| **Documentation** | README, API docs, user guide, changelog |
| **Planning** | PRD, architecture doc, design decisions, roadmap |
| **Testing** | Unit tests, integration tests, E2E tests, test coverage |
| **DevOps** | CI/CD, Docker, deployment scripts, monitoring |
| **Research** | Analysis notebooks, findings, data exploration |
| **Visuals** | Screenshots, diagrams, charts, demo videos |
| **Code Quality** | Linting, type checking, code review, refactoring |
| **Business** | Cost analysis, ROI, market research, user personas |

### 4.3 Context Validation Rules

| Pattern | Counts? | Reason |
|---------|---------|--------|
| "We implemented unit tests" | ✅ Yes | Documented as done |
| "Unit tests cover 80% of code" | ✅ Yes | Specific claim of implementation |
| "Unit tests not yet implemented" | ❌ No | Explicitly not done |
| "TODO: add unit tests" | ❌ No | Future work, not done |
| "We plan to add unit tests" | ❌ No | Future intention |
| "Unit tests are out of scope" | ❌ No | Explicitly excluded |

---

## 5. Use Cases

### 5.1 Evaluating 35 Web Development Projects

**Preconditions**:
- 35 student folders in `/Assignments/WebDev_A1/`
- Each contains at least README.md

**Main Flow**:

1. **Discovery Phase** (10-15 minutes)
   - For each student folder:
     - Find all .md files (README.md, PRD.md, ARCHITECTURE.md, etc.)
     - Read each file, extract criteria with context validation
     - Add student to each criterion's list
   - Build criteria graph: `{criterion: [students...]}`

2. **Categorization Phase** (2-3 minutes)
   - Group criteria into broad categories
   - Flag uncategorized criteria for manual review
   - Save flagged items to review file

3. **Weighting Phase** (1 minute)
   - For each criterion: weight = count(students) / total_students
   - Higher prevalence = higher weight

4. **Grading Phase** (2-3 minutes)
   - For each student: sum weighted scores for criteria they have
   - Best student = 100, others scaled relative
   - Generate outputs

**Postconditions**:
- `discovered_criteria.yml` - All criteria with categories and weights
- `criteria_graph.json` - Which students have which criteria
- `flagged_criteria.md` - Uncategorized items for manual review
- `grades.csv` - Final grades
- `evaluation_report.md` - Complete analysis

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

| Requirement | Target |
|-------------|--------|
| **Per Student** | <30 seconds to read and extract |
| **Total (35 students)** | <20 minutes end-to-end |
| **Memory** | Handle projects with 50+ .md files |

### 6.2 Accuracy Requirements

- Context validation catches 95%+ of "not implemented" cases
- Criteria extraction captures 90%+ of mentioned features
- Only 1 student at 100/100 (best overall)

---

## 7. Weight System Design

### 7.1 Prevalence-Based Weights

```
weight(criterion) = students_with_criterion / total_students

Example (35 students):
- "README.md": 35/35 = 1.0 weight (everyone has it, critical)
- "Unit tests": 28/35 = 0.8 weight (most have it, important)
- "Cost analysis": 5/35 = 0.14 weight (few have it, bonus)
```

### 7.2 Scoring Formula

```
For each student:
    score = 0
    max_possible = 0

    for each criterion in valid_criteria:
        max_possible += weight(criterion)
        if student has criterion:
            score += weight(criterion)

    percentage = score / max_possible * 100
```

### 7.3 Relative Grading

```
best_percentage = max(all_student_percentages)

for each student:
    if student.percentage == best_percentage:
        grade = 100
    else:
        grade = (student.percentage / best_percentage) * 100
```

---

## 8. Data Structures

### 8.1 Criteria Graph

```yaml
criteria_graph:
  "Unit tests":
    students: ["alice", "bob", "carol", "diana"]
    count: 4
    weight: 0.8  # 4/5 students
    category: "Testing"

  "CI/CD pipeline":
    students: ["bob", "diana"]
    count: 2
    weight: 0.4  # 2/5 students
    category: "DevOps"

  "Cost analysis":
    students: ["carol"]
    count: 1
    weight: 0.2  # 1/5 students
    category: "Business"
```

### 8.2 Student Scores

```yaml
student_scores:
  alice:
    criteria_present: ["Unit tests", "README", "Architecture"]
    criteria_missing: ["CI/CD pipeline", "Cost analysis"]
    raw_score: 2.3
    max_possible: 3.4
    percentage: 67.6
    grade: 85
    rank: 3
```

---

## 9. Assumptions

1. **Markdown is accurate**: Students document what they actually built
2. **Context validation works**: Claude can detect "not implemented" patterns
3. **Categories are sufficient**: Predefined categories cover most criteria
4. **Single pass is enough**: No need to re-evaluate after discovery

---

## 10. Constraints

### 10.1 Technical Constraints

- Relies on Claude Code as execution platform
- Limited by Claude's context window for very large markdown files
- Categories are predefined (can be extended)

### 10.2 Methodology Constraints

- Only analyzes .md files (ignores code quality)
- Trusts documentation accuracy
- Manual review needed for uncategorized criteria

---

## 11. Out-of-Scope (MVP)

- **Code analysis**: Not scanning actual code files
- **Plagiarism detection**: Not comparing student work
- **LMS integration**: Export only
- **Multi-assignment tracking**: Each run is independent

---

## 12. Success Criteria

MVP is successful when:

1. ✅ Tool processes 35 students in <20 minutes
2. ✅ Discovers 50+ unique criteria from markdown files
3. ✅ Correctly categorizes 90%+ of criteria
4. ✅ Weights reflect actual class prevalence
5. ✅ Only 1 student receives 100/100 (the best)
6. ✅ Flagged criteria are saved for manual review
7. ✅ Final grades correlate with manual assessment at ≥0.80

---

**End of Product Requirements Document**
