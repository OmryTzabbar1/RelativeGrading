# Implementation Task Breakdown
# Student Project Evaluator - Markdown Criteria Discovery v3.0

**Project**: Student Project Evaluator v3.0
**Version**: 3.0
**Last Updated**: 2025-12-17

---

## Task Overview

This document breaks down the implementation for the **Markdown-Based Criteria Discovery** approach.

**Key Changes from v2.0**:
- Only read `.md` files (not entire project structure)
- Single-pass discovery (no re-evaluation phase)
- Prevalence-based weighting (more students = higher weight)
- Claude as the extraction agent

---

## Phase 1: Project Setup & Configuration

**Goal**: Establish project structure and configuration files

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P1.1** | Create config/ directory | P0 | Pending | For categories.yml |
| **P1.2** | Create categories.yml | P0 | Pending | Predefined category keywords |
| **P1.3** | Update outputs/ directory structure | P0 | Pending | Ensure proper output paths |
| **P1.4** | Create sample test fixtures | P0 | Pending | 3-5 sample student folders with .md files |
| **P1.5** | Update .gitignore | P1 | Pending | Exclude output files with real data |

---

## Phase 2: SKILL.md Implementation

**Goal**: Create the main Claude Code skill that orchestrates the evaluation

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P2.1** | Create SKILL.md frontmatter | P0 | Pending | name, description, triggers |
| **P2.2** | Implement Step 1: Input Collection | P0 | Pending | Get master folder path |
| **P2.3** | Implement Step 2: Student Discovery | P0 | Pending | Find all student folders |
| **P2.4** | Implement Step 3: Markdown Discovery | P0 | Pending | Find all .md files per student |
| **P2.5** | Implement Step 4: Criteria Extraction | P0 | Pending | Read files, extract criteria |
| **P2.6** | Implement context validation rules | P0 | Pending | Filter out "TODO", "not implemented" |
| **P2.7** | Implement criteria graph building | P0 | Pending | Track which students have which criteria |
| **P2.8** | Implement Step 5: Categorization | P0 | Pending | Match criteria to categories |
| **P2.9** | Implement flagged criteria handling | P0 | Pending | Save uncategorized for review |
| **P2.10** | Implement Step 6: Weighting | P0 | Pending | Calculate prevalence weights |
| **P2.11** | Implement Step 7: Grading | P0 | Pending | Score students, assign grades |
| **P2.12** | Implement Step 8: Output Generation | P0 | Pending | CSV, markdown report, JSON |
| **P2.13** | Add progress indicators | P1 | Pending | "Processing student X of Y" |
| **P2.14** | Add error handling | P0 | Pending | Skip errors, continue processing |

---

## Phase 3: Criteria Extraction Logic

**Goal**: Define how Claude extracts and validates criteria

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P3.1** | Define extraction patterns | P0 | Pending | What phrases indicate criteria |
| **P3.2** | Define exclusion patterns | P0 | Pending | "TODO", "not implemented", etc. |
| **P3.3** | Implement granular extraction | P0 | Pending | Extract specific items, not broad topics |
| **P3.4** | Implement source tracking | P1 | Pending | Track which .md file each criterion came from |
| **P3.5** | Handle duplicate criteria | P0 | Pending | Normalize names (unit tests = Unit Tests) |
| **P3.6** | Test extraction accuracy | P0 | Pending | Verify correct extraction on samples |

---

## Phase 4: Categorization System

**Goal**: Implement category matching and flagging

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P4.1** | Load categories from YAML | P0 | Pending | Read config/categories.yml |
| **P4.2** | Implement fuzzy matching | P1 | Pending | "unit test" matches "unit tests" |
| **P4.3** | Implement keyword matching | P0 | Pending | Match criteria to category keywords |
| **P4.4** | Flag uncategorized criteria | P0 | Pending | Save to flagged_criteria.md |
| **P4.5** | Generate category report | P1 | Pending | Show criteria per category |

---

## Phase 5: Weighting & Grading

**Goal**: Calculate weights and assign grades

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P5.1** | Calculate prevalence weights | P0 | Pending | weight = count / total_students |
| **P5.2** | Calculate student raw scores | P0 | Pending | Sum of weights for criteria present |
| **P5.3** | Calculate max possible score | P0 | Pending | Sum of all valid criterion weights |
| **P5.4** | Calculate percentages | P0 | Pending | raw_score / max_possible * 100 |
| **P5.5** | Implement relative grading | P0 | Pending | Best = 100, others scaled |
| **P5.6** | Assign ranks | P0 | Pending | Based on grade ordering |
| **P5.7** | Handle ties | P1 | Pending | Same grade = same rank |

---

## Phase 6: Output Generation

**Goal**: Generate all required output files

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P6.1** | Generate criteria_graph.json | P0 | Pending | Full criteria with students, weights |
| **P6.2** | Generate flagged_criteria.md | P0 | Pending | Uncategorized items for review |
| **P6.3** | Generate grades.csv | P0 | Pending | Rank, Student, Grade, Percentage, etc. |
| **P6.4** | Generate evaluation_report.md | P0 | Pending | Summary, categories, distribution |
| **P6.5** | Add summary statistics | P0 | Pending | Mean, median, range |
| **P6.6** | Add grade distribution | P1 | Pending | Histogram of grades |
| **P6.7** | Add top students section | P1 | Pending | Top 5-10 with reasoning |
| **P6.8** | Add overwrite protection | P1 | Pending | Prompt before overwriting |

---

## Phase 7: Testing

**Goal**: Verify the skill works correctly

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P7.1** | Create test fixtures | P0 | Pending | 5+ sample student projects |
| **P7.2** | Test markdown discovery | P0 | Pending | Finds all .md files |
| **P7.3** | Test criteria extraction | P0 | Pending | Extracts correct criteria |
| **P7.4** | Test context validation | P0 | Pending | Filters out "TODO" items |
| **P7.5** | Test categorization | P0 | Pending | Correct category matching |
| **P7.6** | Test weighting | P0 | Pending | Correct prevalence calculation |
| **P7.7** | Test grading | P0 | Pending | Best = 100, others scaled |
| **P7.8** | Test output generation | P0 | Pending | All files generated correctly |
| **P7.9** | Test with real data | P0 | Pending | Run on actual student submissions |
| **P7.10** | Performance test | P1 | Pending | 35 students in <20 minutes |

---

## Phase 8: Documentation

**Goal**: Complete user and developer documentation

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P8.1** | Update README.md | P0 | Pending | Explain markdown-based approach |
| **P8.2** | Add usage examples | P0 | Pending | Sample commands and outputs |
| **P8.3** | Document categories.yml format | P1 | Pending | How to add/modify categories |
| **P8.4** | Document output formats | P1 | Pending | Explain each output file |
| **P8.5** | Add troubleshooting guide | P1 | Pending | Common issues and solutions |
| **P8.6** | Create sample outputs | P1 | Pending | Example files in examples/ |

---

## Critical Milestones

| Milestone | Completion Criteria | Target |
|-----------|-------------------|--------|
| **M1: Config Complete** | categories.yml created, test fixtures ready | Phase 1 |
| **M2: SKILL.md Core** | Can read .md files and extract criteria | Phase 2 |
| **M3: Categorization Works** | Criteria grouped, flagged items saved | Phase 4 |
| **M4: Grading Works** | Weights calculated, grades assigned | Phase 5 |
| **M5: Outputs Generated** | All output files created correctly | Phase 6 |
| **M6: Tested with Real Data** | Successful run on actual submissions | Phase 7 |

---

## Implementation Order

**Recommended sequence**:

1. **Phase 1**: Setup (config, fixtures)
2. **Phase 2.1-2.7**: Core SKILL.md (discovery, extraction, graph building)
3. **Phase 3**: Extraction logic refinement
4. **Phase 2.8-2.9**: Categorization integration
5. **Phase 4**: Category system
6. **Phase 2.10-2.11**: Weighting and grading
7. **Phase 5**: Weighting/grading refinement
8. **Phase 2.12-2.14**: Output generation, progress, errors
9. **Phase 6**: Output polish
10. **Phase 7**: Testing
11. **Phase 8**: Documentation

---

## Key Decisions

### D1: Single-Pass vs Two-Pass
**Decision**: Single-pass
**Rationale**: Extract criteria AND track students simultaneously. No need to re-evaluate.

### D2: Markdown Only vs Full Code Scan
**Decision**: Markdown only
**Rationale**: .md files provide holistic summaries. Faster, more context-aware.

### D3: Prevalence Weighting
**Decision**: weight = students_with_criterion / total_students
**Rationale**: Common criteria are core requirements; rare criteria are bonuses.

### D4: Relative Grading
**Decision**: Best student = 100, others scaled proportionally
**Rationale**: Fair comparison within the class, not against external standard.

---

## Daily Progress Log

### Day 1 - [Date]
**Tasks Completed**:
- [ ] P1.1: Create config/ directory
- [ ] P1.2: Create categories.yml
- [ ] P1.4: Create sample test fixtures

**Blockers**: None

**Tomorrow's Plan**:
- Start SKILL.md implementation

---

**End of Task Breakdown**
