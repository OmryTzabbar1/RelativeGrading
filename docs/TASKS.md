# Implementation Task Breakdown
# Student Project Evaluator

**Project**: Student Project Evaluator
**Version**: 1.0
**Last Updated**: 2024-12-15

---

## Task Overview

This document breaks down the MVP implementation into 5 phases with specific, actionable tasks.

**Total Estimated Duration**: 10-15 days (1.5-2 weeks)

---

## Phase 1: Project Setup & Infrastructure

**Duration**: 1-2 days
**Goal**: Establish project structure, dependencies, and helper scripts

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P1.1** | Initialize project structure | P0 | Pending | Create folders: scripts/, examples/, docs/, tests/ |
| **P1.2** | Create scan_folders.py | P0 | Pending | Auto-detect student folders in master directory |
| **P1.3** | Create analyze_repo.py | P0 | Pending | Detect project type, extract metadata |
| **P1.4** | Set up requirements.txt | P0 | Pending | Add pyyaml>=6.0 |
| **P1.5** | Create .gitignore | P0 | Pending | Exclude venv/, __pycache__/, *.pyc, .env |
| **P1.6** | Write example assignment-config.yml | P1 | Pending | Template for generated configs |
| **P1.7** | Test helper scripts manually | P0 | Pending | Verify scan_folders and analyze_repo work independently |

---

## Phase 2: Core Development

**Duration**: 3-4 days
**Goal**: Implement main evaluation logic in SKILL.md

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P2.1** | Create SKILL.md frontmatter | P0 | Pending | name, description fields |
| **P2.2** | Implement Step 1: Input Collection | P0 | Pending | Gather assignment, folder path, baseline info |
| **P2.3** | Implement Step 2: Baseline Calibration | P0 | Pending | Read baseline, generate config.yml |
| **P2.4** | Implement Step 3: Student Discovery | P0 | Pending | Call scan_folders.py, list students |
| **P2.5** | Implement Step 4: Comparative Evaluation | P0 | Pending | Compare student to baseline, assign grade |
| **P2.6** | Implement baseline update logic | P0 | Pending | If grade > baseline_grade: update baseline |
| **P2.7** | Implement batch processing (5 at a time) | P0 | Pending | Process students in batches |
| **P2.8** | Add progress indicators | P1 | Pending | Display "Evaluating student X/30..." |
| **P2.9** | Implement error handling (skip & log) | P0 | Pending | On error: skip student, continue, log for manual review |

---

## Phase 3: Output Generation

**Duration**: 1-2 days
**Goal**: Generate CSV, Markdown, and YAML outputs

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P3.1** | Implement CSV generation | P0 | Pending | Format: Student, ID, Grade, Rank, Team, Notes |
| **P3.2** | Implement Markdown report generation | P0 | Pending | Include summary stats + individual evaluations |
| **P3.3** | Implement YAML config generation | P0 | Pending | Create assignment-config.yml after baseline |
| **P3.4** | Add summary statistics calculations | P0 | Pending | Avg, median, high, low, std dev |
| **P3.5** | Implement overwrite protection | P1 | Pending | Prompt before overwriting existing files |
| **P3.6** | Add completion summary display | P1 | Pending | Show file paths, quick stats |
| **P3.7** | Sort CSV by rank (descending) | P0 | Pending | Rank 1 = highest grade |

---

## Phase 4: Testing & Quality Assurance

**Duration**: 2-3 days
**Goal**: Achieve 70%+ test coverage, handle edge cases

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P4.1** | Create test fixtures | P0 | Pending | Sample student projects (3-5 examples) |
| **P4.2** | Write tests for scan_folders.py | P0 | Pending | Test basic, empty, nonexistent, exclusion |
| **P4.3** | Write tests for analyze_repo.py | P0 | Pending | Test JS, Python, Java, unknown project types |
| **P4.4** | Manual end-to-end test with sample data | P0 | Pending | Run full evaluation on 10 fake students |
| **P4.5** | Test edge case: Empty student folder | P0 | Pending | Should skip, log for manual review |
| **P4.6** | Test edge case: Missing README | P1 | Pending | Should continue evaluation, note in report |
| **P4.7** | Test edge case: Large repository (>100MB) | P1 | Pending | Should warn, may take longer |
| **P4.8** | Verify 70%+ code coverage | P0 | Pending | Run pytest --cov |
| **P4.9** | Manual test with real student projects | P0 | Pending | Use actual course data (if available) |

---

## Phase 5: Documentation & Polish

**Duration**: 1 day
**Goal**: Complete user-facing documentation

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P5.1** | Write comprehensive README.md | P0 | Pending | Installation, usage, configuration, troubleshooting |
| **P5.2** | Add usage examples to README | P0 | Pending | Show sample session with input/output |
| **P5.3** | Document configuration options | P1 | Pending | Explain assignment-config.yml fields |
| **P5.4** | Create sample evaluation summary | P1 | Pending | examples/sample_evaluation_summary.md |
| **P5.5** | Add troubleshooting guide | P1 | Pending | Common errors and solutions |
| **P5.6** | Initialize prompt engineering log | P1 | Pending | Create prompts/ directory, initial README |
| **P5.7** | Final code review | P0 | Pending | Check for hardcoded values, missing docstrings |
| **P5.8** | Verify no files exceed 150 lines | P0 | Pending | Refactor if needed |

---

## Phase 6: Deployment & Release (Post-MVP)

**Duration**: 1 day
**Goal**: Prepare for production use and GitHub release

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P6.1** | Create LICENSE file | P1 | Pending | MIT License |
| **P6.2** | Add version tagging | P1 | Pending | Git tag v1.0 |
| **P6.3** | Push to GitHub | P0 | Pending | https://github.com/OmryTzabbar1/RelativeGrading.git |
| **P6.4** | Update WorkEnv README.md | P0 | Pending | Document new skill in main repository |
| **P6.5** | Update WorkEnv PROJECT.md | P0 | Pending | Add skill to project structure |
| **P6.6** | Create release notes | P1 | Pending | List features, known issues, future roadmap |

---

## Daily Progress Log

**Instructions**: Update this section daily to track actual progress.

### Day 1 - [Date]

**Tasks Completed**:
- [ ] Task ID
- [ ] Task ID

**Blockers**:
- Issue description, resolution plan

**Tomorrow's Plan**:
- Task ID: Description

---

### Day 2 - [Date]

**Tasks Completed**:
- [ ] Task ID

**Blockers**:
- None

**Tomorrow's Plan**:
- Task ID: Description

---

## Blockers Tracking

| Blocker ID | Description | Impact | Status | Resolution |
|------------|-------------|--------|--------|------------|
| B001 | Example blocker | High | Open | Plan to resolve |

---

## ISO/IEC 25010 Submission Checklist

**Note**: This checklist ensures compliance with international quality standards. Check off as each requirement is met.

### 1. Project Documents and Planning

- [ ] PRD.md complete with all sections
- [ ] PLANNING.md with C4 diagrams (Context, Container, Component)
- [ ] Minimum 2-3 ADRs documented
- [ ] Timeline and milestones defined

### 2. Code Documentation and Project Structure

- [ ] README.md serves as complete user manual
- [ ] No file exceeds 150 lines
- [ ] All functions have docstrings with type hints
- [ ] Project structure is modular (scripts/, tests/, examples/)

### 3. Configuration Management and Security

- [ ] Configuration separated from code (assignment-config.yml)
- [ ] No API keys or secrets in source code
- [ ] .gitignore configured to exclude sensitive files
- [ ] Student data privacy measures implemented

### 4. Testing and Software Quality

- [ ] Unit tests for helper scripts (scan_folders, analyze_repo)
- [ ] 70%+ test coverage achieved
- [ ] Edge cases handled (empty folders, missing files, large repos)
- [ ] Error handling is defensive and user-friendly

### 5. Research and Results Analysis

- [ ] N/A for this project (no parameter sensitivity analysis required)
- [ ] If applicable: Jupyter notebook for analysis

### 6. User Interface and User Experience

- [ ] Nielsen's heuristics applied to CLI interaction:
  - [ ] Visibility of system status (progress indicators)
  - [ ] Match between system and real world (natural language prompts)
  - [ ] User control (overwrite protection, confirmation prompts)
  - [ ] Error prevention (input validation)
  - [ ] Help and documentation (README, troubleshooting guide)

### 7. Version Management and Development Documentation

- [ ] 10-20+ meaningful git commits
- [ ] Commit format: `<type>(<scope>): <description> [TaskID]`
- [ ] Prompt engineering log initialized (prompts/ directory)
- [ ] Development progression documented

### 8. Costs and Pricing

- [ ] Token usage estimation documented (PLANNING.md Section 9)
- [ ] Cost analysis for 30, 100 students calculated
- [ ] Optimization strategies identified

### 9. Extensibility and Maintainability

- [ ] Extension points documented (submission types, criteria, outputs)
- [ ] Plugin architecture designed for future enhancements
- [ ] Code is modular (scripts separate from orchestration)
- [ ] Reusability: Helper scripts can be used in other skills

### 10. International Quality Standards (ISO/IEC 25010)

- [ ] **Functional Suitability**: All P0 features implemented, acceptance criteria met
- [ ] **Performance Efficiency**: 30 students in ≤30 minutes
- [ ] **Usability**: First-time user can complete grading in 5 minutes
- [ ] **Reliability**: Error handling ensures no crashes during batch processing
- [ ] **Security**: Student data privacy measures implemented
- [ ] **Maintainability**: 150-line file limit, clear documentation
- [ ] **Portability**: Works on Windows, macOS, Linux

---

## Research Tasks (If Applicable)

**Note**: This section is for academic projects requiring experimentation or parameter analysis.

### Experiment 1: Grading Weight Sensitivity

**Goal**: Determine if different grading weights (relevance vs. functionality) significantly affect final rankings.

**Method**:
1. Evaluate 30 students with weights 50/50 (baseline)
2. Re-evaluate with weights 40/60
3. Re-evaluate with weights 60/40
4. Compare rank correlations (Spearman's rho)

**Expected Outcome**: Weights should not drastically change top/bottom rankings (correlation >0.9)

**Status**: Deferred to v1.1 (not required for MVP)

---

### Experiment 2: Baseline Selection Impact

**Goal**: Assess whether initial baseline selection affects final grade distribution.

**Method**:
1. Run evaluation with low-quality baseline (grade 60)
2. Run evaluation with high-quality baseline (grade 95)
3. Compare final grade distributions

**Expected Outcome**: Dynamic baseline updates should normalize results regardless of initial choice

**Status**: Deferred to v1.1

---

## Milestone Tracking

| Milestone | Target Date | Status | Completion Criteria |
|-----------|-------------|--------|---------------------|
| **M1: Baseline Evaluation Works** | Day 4 | Pending | Can analyze one student, generate config |
| **M2: Comparative Grading Works** | Day 7 | Pending | Can compare students, update baseline |
| **M3: Full Batch Processing** | Day 10 | Pending | Process 30 students end-to-end |
| **M4: MVP Complete** | Day 12 | Pending | All P0 features working, tested |
| **M5: Documentation Complete** | Day 14 | Pending | README, examples ready |

---

## Acceptance Criteria Checklist

**MVP is accepted when ALL of these are true**:

- [ ] Tool processes 30 git repositories in ≤30 minutes without crashing
- [ ] Generates valid CSV file importable to Canvas/Moodle
- [ ] Baseline automatically updates when superior project encountered
- [ ] Markdown report includes summary statistics (avg, median, high, low, std dev)
- [ ] Markdown report includes individual evaluations with reasoning
- [ ] Assignment config YAML generated after baseline evaluation
- [ ] Instructor can provide all inputs in one prompt
- [ ] Error handling: skips problematic submissions, continues processing
- [ ] Grades correlate with instructor intuition (tested on sample data)
- [ ] No files exceed 150 lines
- [ ] 70%+ test coverage for Python scripts
- [ ] README provides complete usage instructions
- [ ] Cross-platform compatibility (works on Windows, macOS, Linux)

---

## Known Issues (To Track During Development)

| Issue ID | Description | Severity | Status | Workaround |
|----------|-------------|----------|--------|------------|
| I001 | Example issue | Medium | Open | Temp solution |

---

## Future Enhancements (v1.1+)

**Not in MVP scope, but documented for future reference**:

### v1.1 Features

- [ ] PDF submission support
- [ ] ZIP file submission support
- [ ] Identical submission detection (plagiarism checking)
- [ ] Comprehensive markdown reports with graphs
- [ ] Grade distribution histogram
- [ ] Configurable batch size (not fixed at 5)

### v1.2 Features

- [ ] Custom rubric templates
- [ ] Multi-language support (evaluate in languages other than English)
- [ ] Historical grade tracking (database integration)

### v2.0 Features

- [ ] LMS integration (Canvas, Moodle API)
- [ ] Web dashboard for visualization
- [ ] AI-powered student feedback generation
- [ ] Multi-instructor support (team grading)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-15 | Initial task breakdown for MVP |

---

**End of Tasks Document**

---

## Phase 7: Real-World Evaluation Fixes (Post-MVP)

**Duration**: 2-3 days
**Goal**: Fix issues discovered during real student data evaluation
**Status**: ✅ **COMPLETED** (2025-12-16)

| ID | Task | Priority | Status | Notes |
|----|------|----------|--------|-------|
| **P7.1** | Enhance `analyze_repo.py` with Angular detection | P0 | ✅ Completed | Added `angular.json` detection in _detect_project_type |
| **P7.2** | Implement recursive project root discovery | P0 | ✅ Completed | Created find_project_root.py with up to 3-level search |
| **P7.3** | Add smart project directory selection | P0 | ✅ Completed | Selects candidate with highest confidence/most markers |
| **P7.4** | Handle arbitrary nesting levels | P0 | ✅ Completed | Supports structures like `/LLM_course/ollama-chatbot-angular/` |
| **P7.5** | Add project structure validation script | P1 | ✅ Completed | Created validate_structure.py for pre-flight checks |
| **P7.6** | Update discovery workflow in SKILL.md | P0 | ✅ Completed | Updated Steps 2, 3, and 4 with new workflow |
| **P7.7** | Create unit tests for nested structures | P0 | ✅ Completed | 17 tests passing (test_find_project_root.py, test_analyze_repo_nested.py) |
| **P7.8** | Add logging for project discovery decisions | P1 | Deferred | Can be added in future version if needed |

---

## Issues Discovered During Real Evaluation (2025-12-16)

**Context**: Tested skill on 36 real student submissions from `WorkSubmissions01/`

### Issue I001: Inconsistent Repository Paths

**Problem**: Each student has uniquely named code directories
- Participant_38950: `repo/`
- Participant_38951: `LLM_course/`
- Participant_38952: `local-llm-chat/`
- etc.

**Impact**: Cannot use simple scan of first subdirectory

**Solution**: Implement intelligent project root detection (P7.2, P7.3)

### Issue I002: Nested Project Structures

**Problem**: Some students have multi-level nesting
- Example: `Participant_38951/LLM_course/ollama-chatbot-angular/`
- The actual project is 2 levels deep, not 1 level

**Impact**: `analyze_repo.py` returns "unknown" project type when run on parent folder

**Solution**: Recursive search for project markers (P7.2, P7.4)

### Issue I003: Missing Angular Detection

**Problem**: `analyze_repo.py` only detects:
- JavaScript: `package.json`
- Python: `requirements.txt`, `setup.py`
- Java: `pom.xml`, `build.gradle`

**Missing**: Angular projects (`angular.json`, `tsconfig.json`)

**Impact**: Angular projects show as "unknown" type

**Solution**: Add Angular detection logic (P7.1)

### Issue I004: Manual Discovery Required

**Problem**: Current workflow requires manual inspection to find actual code directory

**Evidence**: Had to manually `ls` each student folder to find the real project

**Impact**: Skill cannot run fully automated on real data

**Solution**: Smart discovery algorithm that prioritizes folders with project markers (P7.3)

### Issue I005: No Pre-flight Validation

**Problem**: No way to validate all student folders before starting evaluation

**Impact**: Discover broken structures mid-evaluation, requiring manual intervention

**Solution**: Add validation script that reports problematic folders upfront (P7.5)

---

## Evaluation Test Results (2025-12-16)

**Test Dataset**: 36 real student submissions (Ollama ChatGPT interface assignment)

**Results**:
- ✅ Baseline analysis worked correctly (Participant_38950)
- ✅ Comparative grading logic functioned properly
- ✅ README analysis and feature extraction successful
- ❌ Automated discovery failed due to nested/inconsistent structures
- ❌ Had to manually locate actual project directories
- ⚠️ Found hidden message in student README attempting to influence grading (handled correctly by ignoring)

**Successful Comparison**: Participant_38951 vs Participant_38950
- Baseline: 60/100 (Next.js, full features, good testing)
- Student: 65/100 (Angular, excellent test coverage, missing some features)
- Grading logic worked as expected

**Recommendations**:
1. Prioritize Phase 7 tasks before production deployment
2. Add project structure documentation for students
3. Consider requiring standardized folder structure in future assignments

