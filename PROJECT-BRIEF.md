# Project Brief: Student Project Evaluator

Generated: 2024-12-15

---

## Executive Summary

A Claude Code skill for comparative evaluation of student coding projects. Complements existing strict-criteria grading by assessing assignment relevance and providing relative quality scores. Processes batches of up to 30 students in under 30 minutes, dynamically updating the baseline as better projects are discovered.

---

## 1. Vision & Purpose

### Problem Statement

Current grading systems check for the existence of specific elements (strict criteria) but fail to assess:
1. How well the project addresses the actual assignment requirements (relevance)
2. Relative quality compared to peer submissions
3. Overall class performance distribution

This creates an incomplete picture of student achievement and makes it difficult to apply nuanced weighting to final grades.

### Target Users

**Primary User**: Course instructor who:
- Already uses a strict-criteria grading tool
- Wants to add a relative quality dimension to grading
- Needs to process 20-30 student submissions efficiently
- Is comfortable with command-line tools and Claude Code

**Secondary Users**: Other educators in the department who will use the tool as-is (no customization or code changes expected)

### Value Proposition

Combines conventional grading (strict criteria) with relative grading (quality comparison) to create a holistic assessment system, revealing which students excel beyond just meeting requirements.

### Success Criteria

1. **Performance**: Grade batches of 30 students in under 30 minutes without errors
2. **Accuracy**: Relative scores correlate with instructor intuition about project quality
3. **Utility**: Generated scores can be used as additional weight in final grading calculations
4. **Reliability**: Baseline correctly updates to the best project encountered

---

## 2. Core Functionality

### Must-Have Features (P0)

| Feature | User Story | Acceptance Criteria |
|---------|------------|---------------------|
| Comparative Evaluation | As an instructor, I want to compare student projects against the current best submission so that grades reflect relative quality | Each student graded against current baseline; baseline updates when better project found |
| Assignment Relevance Checking | As an instructor, I want to assess how well projects address the assignment requirements so that I can identify off-topic submissions | Tool analyzes project against assignment description provided by instructor |
| Automatic Baseline Updates | As an instructor, I want the baseline to automatically update when a superior project is found so that all comparisons use the highest standard | When evaluated project > baseline grade, it becomes new baseline for subsequent comparisons |
| Batch Processing | As an instructor, I want to process students in batches of 5 so that I can review progress and manage context | Tool automatically processes 5 students, then continues to next batch without manual intervention |
| CSV Export | As an instructor, I want grades exported to CSV so that I can import them into my gradebook system | CSV includes: student name, ID, relative grade, rank, notes, and any additional metadata (e.g., team names) |
| Markdown Report | As an instructor, I want a comprehensive markdown report so that I can review evaluations and statistics | Report includes: summary stats (avg, median, high, low, std dev), individual evaluations with reasoning, students needing manual review |
| Assignment Config Generation | As an instructor, I want the tool to generate a YAML config after evaluating the baseline student so that future assignments can be customized | After baseline evaluation, tool creates assignment-config.yml with grading weights, focus files, project type, and observed criteria |

### Should-Have Features (P1)

| Feature | User Story | Acceptance Criteria |
|---------|------------|---------------------|
| Error Handling | As an instructor, I want the tool to skip problematic submissions and continue so that one broken project doesn't halt the entire batch | If error occurs: skip to next student, log note for manual review, continue processing |
| Flexible Metadata | As an instructor, I want the tool to capture team names and other metadata so that I can grade group projects | Tool detects and includes any additional fields found (team names, group IDs, etc.) in output |
| Config File Overwrite Protection | As an instructor, I want to be prompted before overwriting existing grade files so that I don't accidentally lose previous evaluations | Tool checks for existing CSV/markdown and asks for confirmation before overwriting |

### Nice-to-Have Features (P2)

| Feature | User Story | Notes |
|---------|------------|-------|
| Identical Submission Detection | As an instructor, I want to be notified of identical submissions so that I can investigate academic integrity issues | Deferred to v1.1 - skip identical projects and note in summary |
| PDF/ZIP Support | As an instructor, I want to evaluate non-code submissions (reports, designs) so that I can use this tool for all assignment types | Deferred to v1.1 - MVP focuses on git repositories only |
| LMS Integration | As an instructor, I want to export directly to Canvas/Moodle so that I can skip manual grade entry | Deferred to v2.0 - future enhancement for production version |

### Guardrails & Constraints

- **No overwriting without confirmation**: Prevent accidental data loss
- **Skip errors, don't crash**: Resilience is critical for batch processing
- **Cross-platform compatibility**: Must work on any OS with Claude Code installed
- **Max 50 repositories**: Performance guarantee only up to 50 students
- **Git repositories only (MVP)**: Other submission types in future versions

---

## 3. Data Architecture

### Core Entities

| Entity | Description | Key Attributes |
|--------|-------------|----------------|
| **Assignment** | The coding assignment students are completing | `description`, `requirements`, `criteria` |
| **Student Submission** | A single student's project folder | `folder_path`, `student_name`, `student_id`, `submission_type`, `team_name` (optional), `additional_metadata` (flexible) |
| **Evaluation** | Assessment result for one student | `student_name`, `grade`, `reasoning`, `compared_to_baseline`, `notes`, `status` (evaluated/skipped/manual_review) |
| **Baseline** | Current reference standard for comparisons | `student_name`, `grade`, `folder_path`, `features_observed`, `timestamp_set` |
| **Assignment Config** | YAML file defining grading parameters | `assignment_name`, `grading_weights`, `focus_files`, `project_type`, `criteria` |

### Relationships

```
Assignment (1) ---> (Many) Student Submissions
    |
    |---> (1) Baseline (changes dynamically during evaluation)
    |
Student Submission (1) ---> (1) Evaluation
    |
    |---> Compared against current Baseline
    |
    |---> If Evaluation.grade > Baseline.grade:
           Update Baseline to this submission
```

### Data Flow

```
1. User provides:
   - Assignment description
   - Master folder path
   - Baseline student (name + manual grade + folder path)

2. Tool evaluates baseline:
   - Analyzes baseline project
   - Generates assignment-config.yml
   - Sets initial Baseline entity

3. For each remaining student:
   - Read Student Submission
   - Compare to current Baseline
   - Generate Evaluation
   - If grade > baseline: Update Baseline

4. Output:
   - CSV: All Evaluations (sorted by rank)
   - Markdown: Summary stats + Individual evaluations
```

### Data Sensitivity

- **Student Privacy**: Student names/IDs are stored in outputs - ensure files are secured
- **Academic Integrity**: Notes about identical submissions must be handled confidentially
- **Grade Confidentiality**: CSV and markdown reports contain sensitive grade information

---

## 4. MVP Specification

### Core Workflow

```
1. Instructor invokes: "I need to grade student projects"

2. Tool prompts for (or accepts all at once):
   - Assignment description
   - Path to master folder (containing all student subfolders)
   - Baseline student name + manual grade + folder path

3. Tool evaluates baseline:
   - Reads baseline project files
   - Matches manual grade to project quality (calibration)
   - Generates assignment-config.yml
   - Displays: "✓ Baseline established: [student] - [grade]/100"

4. Tool auto-detects remaining student folders

5. For each student (in batches of 5):
   - Read project files (focus on key files)
   - Compare to current baseline:
     * Assignment relevance (50% weight)
     * Functionality (50% weight)
   - Assign relative grade
   - Display: "Evaluating student 5/30..."
   - If grade > baseline: Update baseline, display: "✓ New baseline: [student] - [grade]/100"
   - If error: Skip, log for manual review

6. After all students:
   - Generate CSV (student, ID, grade, rank, notes, metadata)
   - Generate markdown report (stats + individual evaluations)
   - Display: "✅ Evaluation complete! [file paths] [quick stats]"
```

### MVP Feature Set

- [x] Comparative evaluation against dynamic baseline
- [x] Assignment relevance checking
- [x] Automatic student folder detection
- [x] Batch processing (5 students at a time)
- [x] CSV export with flexible metadata
- [x] Basic markdown report (summary stats + evaluations)
- [x] Assignment config generation (YAML)
- [x] Error handling (skip and log)
- [x] Overwrite protection for grade files
- [x] Git repository reading (local, already cloned)

### Explicitly Excluded from MVP

- **Identical submission detection** - Deferred to v1.1
- **Comprehensive markdown report** - MVP has basic stats only
- **PDF/ZIP submission support** - Git repos only for MVP
- **LMS integration** - Future enhancement
- **Real-time AI feedback generation** - Future enhancement

### MVP Success Metric

**30 students graded in under 30 minutes with zero errors, producing relative scores that align with instructor intuition about project quality.**

---

## 5. User Experience

### User Journey Map

1. **Entry point** → Instructor says: "I need to grade student projects"

2. **Tool prompts** → User provides (if not already given):
   - Assignment description (paste text or file path)
   - Master folder path (e.g., `/path/to/Assignment1/`)
   - Baseline student name + grade + folder path

3. **Baseline calibration** → Tool reads baseline project:
   - Displays key features observed
   - Shows: "✓ Baseline established: [student] - [grade]/100"
   - Generates assignment-config.yml

4. **Auto-detection** → Tool finds student folders:
   - Displays: "Found 29 remaining students. Beginning evaluation..."

5. **Batch processing** → For each student:
   - Shows: "Evaluating student 5/30..."
   - If baseline changes: "✓ New baseline: student_bob - 92/100"
   - Silent processing otherwise (no spam)

6. **Completion** → Tool displays:
   ```
   ✅ Evaluation complete!

   Generated files:
   - grades.csv (/path/to/Assignment1/grades.csv)
   - evaluation_summary.md (/path/to/Assignment1/evaluation_summary.md)

   📊 Quick Stats:
   - Students evaluated: 30
   - Average grade: 78/100
   - Highest: student_bob (92/100)
   - Lowest: student_dan (58/100)
   ```

### Key Screens/States

| State | Purpose | Key Elements |
|-------|---------|--------------|
| **Initial Prompt** | Gather required inputs | Assignment description, master folder path, baseline student info |
| **Baseline Calibration** | Understand quality level of manual baseline grade | Baseline project analysis, feature list, config generation |
| **Progress Indicator** | Show evaluation progress during batch processing | "Evaluating student X/30...", baseline update notifications |
| **Completion Summary** | Provide output file paths and quick stats | File paths, summary statistics, next steps |

### UX Priorities

1. **Clarity on "relative grade" concept**: Document and explain that relative grades are comparative, not absolute
2. **Minimal interruptions**: Automatic batching, no pauses for confirmation
3. **Transparent baseline updates**: Always notify user when baseline changes
4. **Actionable error handling**: Clear notes on which students need manual review and why

---

## 6. Project Scope

### Timeline

- **Type**: Small-to-Medium Project
- **Estimated Duration**: 1-2 weeks for MVP proof of concept
- **Intent**: Start as proof of concept, evolve into long-term grading infrastructure

### Maintenance Philosophy

- **For MVP**: Between minimal and moderate
- **Focus**: Functional and usable now, doesn't need to be flawless
- **Expectation**: Seasonal updates before each term, critical bug fixes as needed

### Future Roadmap

| Phase | Features | Timing |
|-------|----------|--------|
| **MVP (v1.0)** | Git repos, comparative grading, CSV/markdown output, auto-config generation | 1-2 weeks |
| **v1.1** | PDF/ZIP support, identical submission detection, comprehensive markdown reports | Next semester |
| **v1.2** | Template system (custom rubrics), multi-language support, improved error recovery | Future |
| **v2.0** | LMS integration (Canvas/Moodle), AI feedback generation, web dashboard | Long-term (production version) |

---

## 7. Platform & Delivery

### Primary Platform

**Claude Code Skill** (CLI-based)

### Requirements

- **OS Support**: Cross-platform (Windows, macOS, Linux) - works on any OS with Claude Code installed
- **Dependencies**:
  - Claude Code installed
  - Git (for reading local repositories)
  - Python 3.x (for helper scripts)
- **Deployment**: Local installation in `.claude/skills/` directory

### Distribution (Future Consideration)

- **For now**: Not a concern, focus on getting it working locally
- **Later**: GitHub repository (https://github.com/OmryTzabbar1/RelativeGrading.git)
- **Installation**: Clone into WorkEnv (new folder), symlink or copy to `.claude/skills/`

### Performance Expectations

- **Throughput**: 1 minute per student (30 students in 30 minutes)
- **Priority**: Quality over speed
- **Batch size**: 5 students at a time
- **Repository size**: Optimized for MB-sized repos
- **Max capacity**: 50 repositories (performance guarantee)
- **Complex projects**: 2-3 minutes acceptable

### Integrations

- **None for MVP**: Standalone tool, no external APIs
- **File system only**: Reads local git repositories
- **Future**: LMS integration (Canvas, Moodle), spreadsheet export (Excel)

---

## 8. Technology Recommendations

### Recommended Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Core Skill** | SKILL.md (Claude Code) | Primary execution logic, leverages Claude's code analysis capabilities |
| **Helper Scripts** | Python 3.x | Cross-platform, easy file operations, YAML parsing |
| **Config Format** | YAML | Human-readable, easy to edit, standard for configuration |
| **Output Formats** | CSV + Markdown | CSV for gradebook import, Markdown for human review |
| **File Reading** | Claude Read/Glob/Grep tools | AI-powered code analysis, no need for static analysis tools |
| **Version Control** | Git | Standard, already in use, integrates with WorkEnv repository |

### Architecture

```
student-project-evaluator/
│
├── SKILL.md                       # Main Claude Code skill (execution logic)
│   ├── Prompts for inputs
│   ├── Orchestrates evaluation flow
│   ├── Calls helper scripts
│   └── Generates outputs
│
├── scripts/
│   ├── scan_folders.py            # Auto-detect student folders
│   │   ├── Lists subdirectories in master folder
│   │   └── Returns folder names/paths
│   │
│   └── analyze_repo.py            # Repository analysis helpers
│       ├── Detect project type (React, Python, Java, etc.)
│       ├── Find key files (main entry points, configs)
│       └── Extract metadata (team names, student IDs)
│
├── templates/                     # For future rubric templates (empty for MVP)
│
├── examples/
│   └── assignment-config.yml      # Example config generated after baseline eval
│
└── README.md                      # Usage instructions
```

### Assignment Config Format (YAML)

Generated after baseline evaluation:

```yaml
assignment:
  name: "Assignment 1 - Web Development"
  description: "Full assignment text here..."
  evaluated_date: "2024-12-15"

baseline:
  student: "student_alice"
  grade: 85
  features_observed:
    - "CRUD operations implemented"
    - "Responsive design with CSS Grid"
    - "LocalStorage persistence"

grading_weights:
  assignment_relevance: 50
  functionality: 50

focus_files:
  - "src/**/*.js"
  - "README.md"
  - "package.json"
  - "index.html"

project_type: "javascript_web"

evaluation_criteria:
  - "CRUD operations"
  - "LocalStorage persistence"
  - "Responsive design"
  - "Code organization"
  - "Documentation quality"
```

### Batch Processing Implementation

- **Automatic**: No pauses between batches
- **Context management**: Process 5 students, then continue
- **Progress output**: Display after each student evaluation
- **Baseline tracking**: Update immediately when better project found

### Deployment Strategy

1. **Development**: Build in WorkEnv repository under new folder
2. **Testing**: Use sample student repositories + real course data
3. **Installation**: Copy/symlink to `.claude/skills/student-project-evaluator/`
4. **Usage**: Invoke via Claude Code CLI
5. **Future**: Publish to https://github.com/OmryTzabbar1/RelativeGrading.git

---

## 9. Development Process

### Repository Structure

```
WorkEnv/
└── .claude/
    └── skills/
        └── student-project-evaluator/
            ├── SKILL.md                    # Main skill definition
            ├── README.md                   # Usage instructions
            ├── PROJECT-BRIEF.md            # This document
            ├── scripts/
            │   ├── scan_folders.py         # Auto-detect student folders
            │   └── analyze_repo.py         # Repository analysis helpers
            ├── templates/                  # For future use (empty for MVP)
            └── examples/
                └── assignment-config.yml   # Example YAML config
```

### Conventions

- **File naming**: snake_case for scripts, UPPERCASE.md for documentation
- **Commit messages**: `<type>(<scope>): <description>`
  - Types: `feat`, `fix`, `docs`, `test`, `refactor`
  - Example: `feat(evaluator): Add automatic baseline updates`

### Quality Assurance

- **Testing**:
  - Manual testing on real student projects during development
  - Sample data testing with fake student repositories
  - Test edge cases: empty repos, missing files, large repos
- **CI/CD**: Not needed for MVP (future consideration for production version)

### Development Workflow

1. **Generate project docs** using `project-docs-generator` skill with `academic-msc` guideline
2. **Follow generated CLAUDE.md** for coding conventions and rules
3. **Implement features** according to TASKS.md breakdown
4. **Test incrementally** with sample repos
5. **Document** in README.md as features are completed
6. **Commit regularly** with descriptive messages
7. **Push to GitHub** (https://github.com/OmryTzabbar1/RelativeGrading.git)

---

## 10. Open Questions & Risks

### Unresolved Questions

- [ ] How should the tool handle repositories with no README? (Skip or infer from code?)
- [ ] Should assignment description be a file path or pasted text? (Support both?)
- [ ] What if a student folder has multiple projects? (Use first/largest? Ask user?)
- [ ] Should the tool detect programming language automatically? (Yes, via analyze_repo.py)
- [ ] How to handle group projects where multiple students share one repo? (Tag all group members with same grade?)

### Identified Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| **Claude context limits** (too many files to read) | High | Focus on key files only (defined in config), batch processing |
| **Inconsistent grading** (Claude evaluates differently over time) | Medium | Use assignment-config.yml to standardize criteria, compare against fixed baseline |
| **Student folder naming variations** (StudentName vs student-name vs 12345) | Low | Auto-detect via scan_folders.py, handle multiple formats |
| **Large repositories** (1000+ files, 100+ MB) | Medium | Set focus_files in config, skip non-essential files, warn if repo > 100MB |
| **Missing dependencies** (Python/Git not installed) | Low | Check dependencies at skill start, provide clear error messages |

### Assumptions

- Git repositories are already cloned locally (no need to clone from GitHub)
- Student folders are immediate subdirectories of master folder (no nested structures)
- One student = one folder (no shared folders, except group projects)
- Instructor can provide baseline grade accurately (calibration relies on this)
- Relative grading approach will correlate with instructor's subjective assessment

---

## Ready for Documentation Generation

This Project Brief can now be passed to the **project-docs-generator** skill to create:
- **PRD.md** - Product Requirements Document
- **CLAUDE.md** - Development rules and conventions
- **PLANNING.md** - Architecture and technical planning
- **TASKS.md** - Implementation task breakdown

**Recommended guideline**: `academic-msc` (comprehensive, since this will become long-term infrastructure)

---

**End of Project Brief**
