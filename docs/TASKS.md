# Implementation Task Breakdown
# Student Project Evaluator - Sliding Window v2.0

**Project**: Student Project Evaluator v2.0
**Version**: 2.0
**Last Updated**: 2025-12-16

---

## Task Overview

This document breaks down the implementation into phases for the **Sliding Window Criteria Discovery** approach.

**Total Estimated Duration**: 12-18 days (2-3 weeks)

---

## Phase 1: Project Setup & Infrastructure

**Duration**: 2-3 days
**Goal**: Establish new sliding window architecture foundation

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P1.1** | Update project structure | P0 | Pending | Add: sliding_window_analyzer.py, criteria_builder.py, final_evaluator.py |
| **P1.2** | Create DiscoveredCriteria class | P0 | Pending | Data structure for dynamic criteria building |
| **P1.3** | Create StudentEvaluation class | P0 | Pending | Track scores across all discovered dimensions |
| **P1.4** | Update analyze_project.py | P0 | Pending | Return comprehensive feature dict |
| **P1.5** | Create utils.py | P0 | Pending | Helper functions for feature comparison, merging |
| **P1.6** | Update requirements.txt | P0 | Pending | Add pyyaml>=6.0, ensure Python 3.8+ |
| **P1.7** | Test data structures manually | P0 | Pending | Verify DiscoveredCriteria, StudentEvaluation work |

---

## Phase 2: Sliding Window Discovery Implementation

**Duration**: 3-4 days
**Goal**: Implement Phase 1 of evaluation (criteria discovery)

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P2.1** | Implement sliding_window_analyzer.py | P0 | Pending | Core sliding window logic |
| **P2.2** | Implement window iteration | P0 | Pending | Loop through students [i:i+3] |
| **P2.3** | Implement feature extraction | P0 | Pending | Extract: docs, tests, images, notebooks, research |
| **P2.4** | Implement criteria merging | P0 | Pending | Merge new features into existing criteria |
| **P2.5** | Implement new feature detection | P0 | Pending | Identify what each student adds |
| **P2.6** | Add progress indicators | P1 | Pending | Display "Window X/Y: Students [A,B,C]" |
| **P2.7** | Implement criteria evolution logging | P0 | Pending | Log what each student contributed |
| **P2.8** | Generate discovered_criteria.yml | P0 | Pending | Save complete criteria after discovery |
| **P2.9** | Add caching for analyzed projects | P1 | Pending | Avoid re-analyzing same project |

---

## Phase 3: Final Evaluation Implementation

**Duration**: 2-3 days
**Goal**: Implement Phase 2 of evaluation (grade all students)

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P3.1** | Implement final_evaluator.py | P0 | Pending | Score all students against discovered criteria |
| **P3.2** | Implement dimension scoring | P0 | Pending | Score each quality dimension |
| **P3.3** | Implement composite score calculation | P0 | Pending | Sum of all dimension scores |
| **P3.4** | Implement relative grading logic | P0 | Pending | Best = 100, others scaled |
| **P3.5** | Add grading curve implementation | P0 | Pending | 95%+ → 90-99, 80-95% → 75-89, etc. |
| **P3.6** | Implement rank assignment | P0 | Pending | Assign ranks 1-N based on grades |
| **P3.7** | Add progress indicators | P1 | Pending | Display "Evaluating student X/N" |

---

## Phase 4: Output Generation

**Duration**: 2 days
**Goal**: Generate all required output files

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P4.1** | Implement CSV generation | P0 | Pending | Format: Student, Grade, Rank, [Dimension Scores] |
| **P4.2** | Implement evaluation report (markdown) | P0 | Pending | Show criteria evolution + final grades |
| **P4.3** | Add summary statistics | P0 | Pending | Mean, median, range, grade distribution |
| **P4.4** | Generate criteria evolution log | P1 | Pending | What each student added to criteria |
| **P4.5** | Add top 10 projects section | P1 | Pending | Show highest-scoring students with reasoning |
| **P4.6** | Implement discovered_criteria.yml export | P0 | Pending | Complete criteria with all dimensions |
| **P4.7** | Add overwrite protection | P1 | Pending | Prompt before overwriting existing files |

---

## Phase 5: SKILL.md Orchestration

**Duration**: 2-3 days
**Goal**: Build Claude Code skill orchestration

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P5.1** | Create SKILL.md frontmatter | P0 | Pending | name: sliding-window-evaluator, description |
| **P5.2** | Implement Step 1: Input Collection | P0 | Pending | Get master folder path from user |
| **P5.3** | Implement Step 2: Student Discovery | P0 | Pending | Scan folders, confirm count |
| **P5.4** | Implement Step 3: Phase 1 Execution | P0 | Pending | Run sliding window discovery |
| **P5.5** | Implement criteria review step | P1 | Pending | Show discovered criteria to user for approval |
| **P5.6** | Implement Step 4: Phase 2 Execution | P0 | Pending | Run final evaluation |
| **P5.7** | Implement output generation step | P0 | Pending | Generate CSV, markdown, YAML |
| **P5.8** | Add completion summary | P1 | Pending | Show file paths, statistics, top students |
| **P5.9** | Implement error handling | P0 | Pending | Skip problematic students, continue processing |

---

## Phase 6: Testing & Quality Assurance

**Duration**: 2-3 days
**Goal**: Comprehensive testing of sliding window approach

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P6.1** | Create test fixtures | P0 | Pending | 10 sample student projects with varied features |
| **P6.2** | Test sliding window iteration | P0 | Pending | Verify windows overlap correctly |
| **P6.3** | Test criteria building | P0 | Pending | Verify new features are detected and merged |
| **P6.4** | Test criteria evolution logging | P0 | Pending | Verify logging tracks additions correctly |
| **P6.5** | Test final evaluation | P0 | Pending | Verify all students scored against complete criteria |
| **P6.6** | Test relative grading | P0 | Pending | Verify only best gets 100, others scaled |
| **P6.7** | Test with real data | P0 | Pending | Run on WorkSubmissions01 (35 students) |
| **P6.8** | Verify output correctness | P0 | Pending | Check CSV, markdown, YAML are correct |
| **P6.9** | Test edge cases | P0 | Pending | Empty projects, missing files, large repos |
| **P6.10** | Performance test | P1 | Pending | Verify 35 students complete in <45 minutes |

---

## Phase 7: Documentation & Polish

**Duration**: 1-2 days
**Goal**: Complete user documentation

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P7.1** | Write comprehensive README.md | P0 | Pending | Explain sliding window approach clearly |
| **P7.2** | Add usage examples | P0 | Pending | Show sample sessions with before/after |
| **P7.3** | Document discovered_criteria.yml format | P1 | Pending | Explain all fields and structure |
| **P7.4** | Create sample outputs | P1 | Pending | examples/sample_discovered_criteria.yml |
| **P7.5** | Add troubleshooting guide | P1 | Pending | Common errors and solutions |
| **P7.6** | Document criteria discovery process | P1 | Pending | Explain how window analysis works |
| **P7.7** | Final code review | P0 | Pending | Check for hardcoded values, missing docstrings |
| **P7.8** | Verify no files exceed 150 lines | P0 | Pending | Refactor if needed |

---

## Phase 8: Deployment & Testing (Post-MVP)

**Duration**: 1-2 days
**Goal**: Deploy and validate with real data

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P8.1** | Run full evaluation on WorkSubmissions01 | P0 | Pending | 36 students, compare with manual grades |
| **P8.2** | Verify criteria discovery completeness | P0 | Pending | Check that 90%+ of features are captured |
| **P8.3** | Validate relative grading | P0 | Pending | Verify only 1 student at 100 |
| **P8.4** | Compare with manual grades | P0 | Pending | Check correlation ≥0.80 |
| **P8.5** | Generate comparison report | P1 | Pending | Show discovered criteria vs manual evaluation |
| **P8.6** | Push to GitHub | P0 | Pending | Update repository with v2.0 |
| **P8.7** | Create release notes | P1 | Pending | Document new sliding window approach |

---

## Critical Milestones

| Milestone | Completion Criteria | Target Day |
|-----------|-------------------|------------|
| **M1: Data Structures Complete** | DiscoveredCriteria, StudentEvaluation classes working | Day 3 |
| **M2: Phase 1 (Discovery) Works** | Can analyze 10 students in windows, build criteria | Day 7 |
| **M3: Phase 2 (Evaluation) Works** | Can score all students against criteria, assign grades | Day 10 |
| **M4: Full Integration Complete** | Both phases work end-to-end | Day 13 |
| **M5: Tested with Real Data** | WorkSubmissions01 evaluation successful | Day 16 |
| **M6: Documentation Complete** | README, examples ready for users | Day 18 |

---

## Key Differences from v1.0

| Aspect | v1.0 (Baseline) | v2.0 (Sliding Window) |
|--------|-----------------|----------------------|
| **Approach** | Single baseline comparison | Sliding window criteria discovery |
| **Phases** | 1 phase (compare all to baseline) | 2 phases (discovery + evaluation) |
| **Criteria** | Predetermined from baseline | Discovered from all projects |
| **Fairness** | Students compared to one project | All students judged by same complete criteria |
| **Window Size** | N/A | 3 students per window |
| **Re-evaluation** | Baseline updates during evaluation | All students re-evaluated after discovery |

---

## Daily Progress Log

### Week 1

#### Day 1 - [Date]
**Tasks Completed**:
- [ ] P1.1: Update project structure
- [ ] P1.2: Create DiscoveredCriteria class
- [ ] P1.3: Create StudentEvaluation class

**Blockers**: None

**Tomorrow's Plan**:
- Complete data structures
- Begin sliding window analyzer

#### Day 2 - [Date]
**Tasks Completed**:
- [ ] Task ID

**Blockers**: None

**Tomorrow's Plan**:
- Task descriptions

---

**End of Task Breakdown**
