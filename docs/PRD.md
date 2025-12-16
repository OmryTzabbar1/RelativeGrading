# Product Requirements Document (PRD)
# Student Project Evaluator - Dynamic Criteria Builder

**Version:** 2.0
**Date:** 2025-12-16
**Status:** Active
**Author:** Development Team

---

## 1. Project Overview

### 1.1 Context and Background

Academic project evaluation requires fair, comprehensive criteria that reflect the collective capabilities demonstrated across all student submissions. Traditional approaches either:

1. **Predetermined Rubrics**: Define criteria before seeing student work, missing innovative approaches students may take
2. **Baseline Comparison**: Compare all students to a single baseline, which may not represent the full spectrum of quality

The **Student Project Evaluator v2.0** uses a **sliding window criteria discovery approach** that builds evaluation criteria dynamically by analyzing all projects first, then evaluating everyone against the complete discovered criteria.

### 1.2 Problem Statement

Current evaluation systems face three critical issues:

1. **Premature Criteria**: Defining criteria before seeing student work may miss important dimensions
2. **Baseline Bias**: Single baseline may not capture full range of possible approaches and quality levels
3. **Incomplete Picture**: Early students are evaluated without knowing what later students will demonstrate

This results in potentially unfair grading where students are compared to incomplete criteria.

### 1.3 Innovation: Sliding Window Criteria Discovery

**Core Concept**: Build evaluation criteria organically by examining all projects in overlapping groups.

**Process**:
```
Students: [1, 2, 3, 4, 5, 6, ..., N]

Window 1: [1, 2, 3] → Initial criteria C1
Window 2: [2, 3, 4] → Updated criteria C2 = C1 + new_from_4
Window 3: [3, 4, 5] → Updated criteria C3 = C2 + new_from_5
...
Window N-2: [N-2, N-1, N] → Final criteria CF

Then: Evaluate ALL students against CF
```

**Benefits**:
- Criteria emerges from actual student work
- No single student defines the standard
- All students judged by same complete criteria
- Discovers full spectrum of quality dimensions

---

## 2. Target Audience

### 2.1 Primary User Persona

**Name**: Dr. Sarah Chen
**Role**: Assistant Professor, Computer Science

**Use Case**:
- 35 students submitted coding projects
- Wants fair grading based on what students collectively demonstrated
- Needs to understand full range of approaches before finalizing criteria

**Success Scenario**: Tool analyzes all 35 projects in overlapping windows, builds comprehensive criteria capturing all quality dimensions, then grades each student against the complete criteria. Final grades reflect true comparative performance.

---

## 3. Project Goals

### 3.1 Objectives

| Goal | Description | Success Metric |
|------|-------------|----------------|
| **Fairness** | All students evaluated against same complete criteria | Zero complaints about inconsistent standards |
| **Comprehensiveness** | Capture all quality dimensions present in submissions | Criteria includes features from 90%+ of projects |
| **Efficiency** | Complete discovery + evaluation in reasonable time | Process 35 students in <45 minutes |
| **Transparency** | Clear explanation of discovered criteria | Instructors can review and understand criteria |

---

## 4. Functional Requirements

### 4.1 Must-Have Features (P0)

| Feature ID | Feature | Acceptance Criteria |
|------------|---------|---------------------|
| **P0.1** | Sliding Window Analysis | Process students in overlapping windows of 3; Window 1: [1,2,3], Window 2: [2,3,4], etc. |
| **P0.2** | Dynamic Criteria Building | Each window updates collective criteria; track: documentation types, features, testing, graphics, research |
| **P0.3** | Criteria Evolution Tracking | Log what each student adds to criteria; display "Student X added: [new criteria]" |
| **P0.4** | Final Criteria Generation | After all windows: produce complete criteria YAML with all discovered dimensions |
| **P0.5** | Comprehensive Re-evaluation | Evaluate ALL students against final criteria; assign grades 0-100 |
| **P0.6** | Relative Grading | Only best student gets 100; others scaled relative to best |
| **P0.7** | CSV Export | Export: Student, Grade, Rank, with all discovered criteria scores |
| **P0.8** | Criteria Report | Generate markdown showing criteria evolution and final evaluation |

### 4.2 Criteria Discovery Dimensions

**What to discover in each window:**

| Dimension | Examples | Scoring |
|-----------|----------|---------|
| **Documentation** | README, PRD, Architecture docs, PROMPT_BOOK | Quality + quantity |
| **Planning** | PRD.md, Architecture.md, design docs | Presence + depth |
| **Research** | Notebooks, analysis docs, findings | Depth + insights |
| **Visual Elements** | Screenshots, diagrams, charts | Quantity + relevance |
| **Testing** | Test files, test coverage, test types | Coverage + quality |
| **Code Quality** | Structure, organization, patterns | Complexity + clarity |
| **Innovation** | Novel approaches, creative solutions | Uniqueness |

---

## 5. Use Cases

### 5.1 Use Case 1: Evaluating 35 Web Development Projects

**Preconditions**:
- 35 student folders in `/Assignments/WebDev_A1/`
- Each contains git repository

**Main Flow**:

1. **Phase 1: Criteria Discovery** (20-25 minutes)
   - Window 1 [Students 1,2,3]:
     - Analyze all three projects
     - Create initial criteria C1
     - Track: Student 1 has README (excellent), Student 2 has PRD, Student 3 has tests
   - Window 2 [Students 2,3,4]:
     - Student 4 introduces Architecture.md
     - Update criteria: C2 = C1 + {architecture_docs: present}
   - Continue through Window 33 [Students 33,34,35]
   - Display evolution: "Total criteria dimensions discovered: 15"

2. **Phase 2: Final Evaluation** (15-20 minutes)
   - Load complete criteria CF
   - For each student (1-35):
     - Score against all 15 dimensions
     - Calculate composite quality score
   - Assign relative grades:
     - Best student = 100
     - Others scaled to best
   - Generate outputs

**Postconditions**:
- `discovered_criteria.yml` - Complete criteria with all dimensions
- `grades.csv` - Final grades for all students
- `evaluation_report.md` - Criteria evolution + individual evaluations

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

| Requirement | Target |
|-------------|--------|
| **Phase 1 (Discovery)** | Process 3-student windows in <1 min each; 35 students = ~12 windows = <15 min |
| **Phase 2 (Evaluation)** | Evaluate 1 student in <30 sec; 35 students = <20 min |
| **Total Time** | <45 minutes for 35 students |

### 6.2 Accuracy Requirements

- Criteria must capture features from 90%+ of projects
- Final grades correlate with manual grading at ≥0.80
- Only 1 student at 100/100 (best overall)

---

## 7. Assumptions

1. **Student folders accessible**: All projects pre-cloned locally
2. **Consistent structure**: Students follow similar project organization
3. **Window size of 3**: Balances thoroughness vs. processing time
4. **Overlap necessary**: Ensures continuity in criteria discovery

---

## 8. Constraints

### 8.1 Technical Constraints

- Processing time limited by Claude Code context and API rate limits
- Large projects (1000+ files) may slow analysis
- Window size fixed at 3 (not configurable in MVP)

### 8.2 Methodology Constraints

- Criteria cannot be manually edited during discovery phase
- All students must be in same master folder
- Order of students matters (affects discovery sequence)

---

## 9. Out-of-Scope (MVP)

- **Manual criteria adjustment**: Can't edit discovered criteria before final evaluation
- **Variable window size**: Fixed at 3 students per window
- **Multi-assignment tracking**: Each run is independent
- **LMS integration**: Export CSV only

---

## 10. Success Criteria

MVP is successful when:

1. ✅ Tool processes 35 students in two phases (discovery + evaluation) in <45 minutes
2. ✅ Discovered criteria captures features from 90%+ of projects
3. ✅ Only 1 student receives 100/100 (the best)
4. ✅ Criteria evolution is logged and transparent
5. ✅ Instructor can review discovered criteria before accepting results
6. ✅ Final grades correlate with manual assessment at ≥0.80

---

**End of Product Requirements Document**
