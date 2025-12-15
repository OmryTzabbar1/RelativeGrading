# Architecture and Technical Planning
# Student Project Evaluator

**Version:** 1.0
**Date:** 2024-12-15
**Status:** Active

---

## Table of Contents

1. [System Architecture](#1-system-architecture)
2. [C4 Model Diagrams](#2-c4-model-diagrams)
3. [Architectural Decision Records](#3-architectural-decision-records)
4. [Component Design](#4-component-design)
5. [Data Architecture](#5-data-architecture)
6. [Technology Stack](#6-technology-stack)
7. [API Documentation](#7-api-documentation)
8. [Deployment Architecture](#8-deployment-architecture)
9. [Cost Analysis](#9-cost-analysis)
10. [Extensibility and Plugin Architecture](#10-extensibility-and-plugin-architecture)

---

## 1. System Architecture

### 1.1 Overview

The Student Project Evaluator is a **Claude Code Skill** - a hybrid system combining:
- Declarative skill definition (SKILL.md) that orchestrates the evaluation workflow
- Python helper scripts for file system operations
- Claude's AI capabilities for code analysis and qualitative assessment

**Architectural Style**: Pipeline architecture with dynamic baseline management

### 1.2 High-Level Architecture

```
User Input → Skill Orchestration → Evaluation Pipeline → Output Generation
    ↓              ↓                      ↓                    ↓
Assignment     SKILL.md              Baseline Mgmt        CSV + MD + YAML
Master Folder  (Claude Code)         Comparative          Reports
Baseline Info  Helper Scripts        Analysis
```

### 1.3 Core Principles

1. **Separation of Concerns**: Skill orchestration (SKILL.md) vs. file operations (Python scripts)
2. **Stateful Baseline**: Baseline updates dynamically as better projects are discovered
3. **Fail-Safe Processing**: Skip errors, continue evaluation, log for manual review
4. **Batch Context Management**: Process 5 students at a time to manage Claude's token limits
5. **Extensibility**: Config-driven evaluation criteria, modular for future submission types

---

## 2. C4 Model Diagrams

### 2.1 Context Diagram (Level 1)

```
                         ┌──────────────────────────┐
                         │                          │
                         │   Course Instructor      │
                         │                          │
                         └────────────┬─────────────┘
                                      │
                    Provides assignment, folders,
                    baseline info; receives grades
                                      │
                                      ▼
                        ┌─────────────────────────────┐
                        │                             │
                        │  Student Project Evaluator  │
                        │  (Claude Code Skill)        │
                        │                             │
                        └──────────┬──────────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
                ▼                  ▼                  ▼
        ┌───────────────┐  ┌──────────────┐  ┌─────────────┐
        │               │  │              │  │             │
        │ File System   │  │ Claude Code  │  │ Git Repos   │
        │ (Student      │  │ Platform     │  │ (Student    │
        │  Folders)     │  │ (AI Engine)  │  │  Projects)  │
        │               │  │              │  │             │
        └───────────────┘  └──────────────┘  └─────────────┘
```

**External Actors**:
- **Course Instructor**: Primary user who initiates grading, provides inputs, receives outputs
- **File System**: Contains student project folders and receives output files (CSV, markdown, YAML)
- **Claude Code Platform**: Execution environment providing AI analysis capabilities
- **Git Repositories**: Student project code (already cloned locally)

### 2.2 Container Diagram (Level 2)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     Student Project Evaluator Skill                      │
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                        SKILL.md                                  │    │
│  │                   (Claude Code Skill Logic)                      │    │
│  │                                                                  │    │
│  │  • Input validation                                             │    │
│  │  • Orchestration workflow                                       │    │
│  │  • Baseline management                                          │    │
│  │  • Comparative evaluation logic                                 │    │
│  │  • Output formatting                                            │    │
│  └──────────────────┬───────────────────────────┬──────────────────┘    │
│                     │                           │                       │
│                     ▼                           ▼                       │
│     ┌───────────────────────────┐  ┌──────────────────────────┐        │
│     │  Helper Scripts (Python)  │  │  Claude Code Tools       │        │
│     │                           │  │                          │        │
│     │  • scan_folders.py        │  │  • Read (file reading)   │        │
│     │  • analyze_repo.py        │  │  • Glob (file patterns)  │        │
│     │                           │  │  • Grep (code search)    │        │
│     └───────────┬───────────────┘  └────────────┬─────────────┘        │
│                 │                               │                       │
│                 └───────────────┬───────────────┘                       │
│                                 │                                       │
└─────────────────────────────────┼───────────────────────────────────────┘
                                  │
                                  ▼
                    ┌──────────────────────────────┐
                    │     File System              │
                    │                              │
                    │  Input:                      │
                    │  • Student folders           │
                    │  • Project files             │
                    │                              │
                    │  Output:                     │
                    │  • grades.csv                │
                    │  • evaluation_summary.md     │
                    │  • assignment-config.yml     │
                    └──────────────────────────────┘
```

**Containers**:
1. **SKILL.md**: Main orchestration logic, Claude Code skill definition
2. **Helper Scripts**: Python utilities for file system operations
3. **Claude Code Tools**: Built-in Read/Glob/Grep tools for code analysis
4. **File System**: Storage for inputs and outputs

### 2.3 Component Diagram (Level 3) - SKILL.md Internals

```
┌──────────────────────────────────────────────────────────────────────┐
│                            SKILL.md                                  │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │              1. Input Collection & Validation              │     │
│  │  • Gather assignment description                           │     │
│  │  • Validate master folder path                             │     │
│  │  • Collect baseline student info                           │     │
│  └──────────────────────────┬─────────────────────────────────┘     │
│                             │                                       │
│                             ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │              2. Baseline Calibration                       │     │
│  │  • Read baseline project files                             │     │
│  │  • Analyze features & quality                              │     │
│  │  • Generate assignment-config.yml                          │     │
│  │  • Set initial baseline state                              │     │
│  └──────────────────────────┬─────────────────────────────────┘     │
│                             │                                       │
│                             ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │              3. Student Discovery                          │     │
│  │  • Call scan_folders.py                                    │     │
│  │  • List remaining student folders                          │     │
│  │  • Confirm count with user                                 │     │
│  └──────────────────────────┬─────────────────────────────────┘     │
│                             │                                       │
│                             ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │              4. Batch Evaluation Loop                      │     │
│  │  ┌──────────────────────────────────────────────────┐      │     │
│  │  │  For each student (batches of 5):               │      │     │
│  │  │  • Read project files (analyze_repo.py)          │      │     │
│  │  │  • Comparative analysis vs. baseline             │      │     │
│  │  │  • Calculate grade (relevance + functionality)   │      │     │
│  │  │  • Update baseline if grade > baseline_grade     │      │     │
│  │  │  • Handle errors (skip, log for manual review)   │      │     │
│  │  └──────────────────────────────────────────────────┘      │     │
│  └──────────────────────────┬─────────────────────────────────┘     │
│                             │                                       │
│                             ▼                                       │
│  ┌────────────────────────────────────────────────────────────┐     │
│  │              5. Output Generation                          │     │
│  │  • Generate grades.csv (all students, sorted by rank)      │     │
│  │  • Generate evaluation_summary.md (stats + evaluations)    │     │
│  │  • Display completion summary                              │     │
│  └────────────────────────────────────────────────────────────┘     │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Architectural Decision Records (ADRs)

### ADR-001: Use Claude Code Skill Instead of Standalone Script

**Status**: Accepted

**Context**:
We need to evaluate student code qualitatively (assignment relevance, code quality) rather than just syntactically. Options:
1. Standalone Python script with static analysis tools (Pylint, ESLint)
2. Claude Code skill leveraging AI for semantic understanding
3. Hybrid: Python script calling Claude API

**Decision**:
Implement as a **Claude Code skill** (option 2).

**Rationale**:
- **Semantic Understanding**: Claude can read code and assess whether it addresses assignment requirements (static analysis cannot)
- **Natural Language Input**: Assignment descriptions can be provided as natural language text
- **Context Awareness**: Claude understands project structure, coding patterns, and quality beyond syntax
- **Integrated Environment**: Leverages existing Claude Code tools (Read, Glob, Grep) without reinventing file operations

**Consequences**:
- **Positive**:
  - High-quality qualitative assessment
  - Flexible to different programming languages
  - Natural instructor interface (conversational prompts)
- **Negative**:
  - Depends on Claude Code platform availability
  - Context limits require batch processing
  - Slower than pure static analysis

**Alternatives Considered**:
- **Static Analysis**: Fast but cannot assess relevance or quality, only syntax/style
- **Standalone API Calls**: More complex auth, requires API key management, loses Claude Code tool integration

**Trade-offs**:
- **Gained**: Semantic code understanding, flexibility
- **Sacrificed**: Some processing speed, standalone portability

---

### ADR-002: Dynamic Baseline Updates vs. Fixed Baseline

**Status**: Accepted

**Context**:
When comparing student projects, we need a reference standard. Options:
1. **Fixed Baseline**: Compare all students to the initial baseline (instructor-chosen student)
2. **Dynamic Baseline**: Update baseline to highest-graded project encountered so far
3. **Average Baseline**: Compare to rolling average of all evaluated students

**Decision**:
Implement **dynamic baseline updates** (option 2).

**Rationale**:
- **Adaptive Standard**: Ensures all students are compared against the best work in the class, not just the first student
- **Fair Grading**: If the initial baseline is mediocre, exceptional students later in the list get appropriate recognition
- **Instructor Intent**: User explicitly requested this feature for discovering the best projects

**Consequences**:
- **Positive**:
  - More accurate relative grading
  - Identifies true standout projects
  - Fair to students evaluated later in the list
- **Negative**:
  - Grade order-dependency: student evaluated 1st vs. 30th might get different grades if evaluated in reverse order
  - More complex logic to manage baseline state

**Alternatives Considered**:
- **Fixed Baseline**: Simpler, but unfair if baseline is weak
- **Average Baseline**: No single exemplar, harder to explain "compared to average" concept

**Trade-offs**:
- **Gained**: Fairness, best project identification
- **Sacrificed**: Deterministic ordering (though order still matters in batch processing)

---

### ADR-003: Batch Processing Size of 5 Students

**Status**: Accepted

**Context**:
Claude Code has token context limits. Processing 30 students in one request may exceed limits. Options:
1. **Process all at once**: Send all 30 student folders in one request
2. **Batch processing (5 students)**: Process 5, then next 5, etc.
3. **One at a time**: Process 1 student, then next

**Decision**:
Implement **batch processing with 5 students per batch** (option 2).

**Rationale**:
- **Context Management**: 5 students ≈ manageable token usage for Claude Code
- **Progress Visibility**: User sees updates every 5 students, knows tool is working
- **Error Isolation**: If one batch has issues, doesn't affect all 30 students
- **User Testing**: User specifically requested batches of 5

**Consequences**:
- **Positive**:
  - Stays within Claude context limits
  - Provides progress feedback
  - More resilient to errors
- **Negative**:
  - Slightly slower than single-batch (context switching overhead)
  - Baseline may update mid-batch, affecting subsequent batches

**Alternatives Considered**:
- **All at once**: Likely to exceed context limits, no progress visibility
- **One at a time**: Too slow, excessive context resets, poor user experience

**Trade-offs**:
- **Gained**: Reliability, progress transparency
- **Sacrificed**: Marginal processing speed

---

## 4. Component Design

### 4.1 SKILL.md (Main Orchestrator)

**Responsibilities**:
- Input validation and collection
- Baseline calibration and config generation
- Comparative evaluation logic
- Baseline state management
- Output formatting (CSV, Markdown)
- Error handling and user notifications

**Key Functions** (expressed as sections in SKILL.md):
1. `Gather Information`: Collect assignment, master folder, baseline info
2. `Calibrate Baseline`: Read baseline project, generate config, set initial state
3. `Discover Students`: List folders, filter out baseline, confirm count
4. `Evaluate Batch`: Process 5 students, compare to baseline, update if needed
5. `Generate Outputs`: Create CSV, markdown, display summary

### 4.2 scan_folders.py (Helper Script)

**Purpose**: Auto-detect student folders in master directory

**Interface**:
```python
def scan_student_folders(master_folder: str, exclude: list[str] = None) -> list[dict]:
    """
    Scan master folder for student subdirectories.

    Args:
        master_folder: Path to directory containing student folders
        exclude: List of folder names to exclude (e.g., baseline student)

    Returns:
        List of dicts: [{'name': 'student_bob', 'path': '/full/path/to/student_bob'}, ...]

    Raises:
        FileNotFoundError: If master_folder doesn't exist
    """
```

**Implementation**:
- Use `os.listdir()` to get all subdirectories
- Filter out hidden folders (start with `.`)
- Exclude baseline folder if provided
- Return sorted list (alphabetical order)

### 4.3 analyze_repo.py (Helper Script)

**Purpose**: Extract metadata and detect project characteristics

**Interface**:
```python
def analyze_repository(folder_path: str) -> dict:
    """
    Analyze a student repository to extract metadata and project type.

    Args:
        folder_path: Path to student project folder

    Returns:
        Dict containing:
        {
            'project_type': 'javascript_web' | 'python_cli' | 'java_app' | 'unknown',
            'key_files': ['README.md', 'src/index.js', 'package.json'],
            'metadata': {'team_name': 'Team Alpha', 'student_id': '12345'},
            'size_mb': 5.2,
            'file_count': 147
        }
    """
```

**Detection Logic**:
```python
# JavaScript/Node
if 'package.json' exists and 'src/index.js' or 'app.js':
    project_type = 'javascript_web'

# Python
if 'requirements.txt' or 'setup.py' exists and 'main.py' or 'app.py':
    project_type = 'python_app'

# Java
if 'pom.xml' or 'build.gradle' exists:
    project_type = 'java_app'

# Default
else:
    project_type = 'unknown'
```

**Metadata Extraction**:
- Parse README.md for `Team:`, `Group:`, `Student ID:` patterns
- Extract from folder name if follows pattern `studentID_name`

---

## 5. Data Architecture

### 5.1 Entity Relationships

```
Assignment
    │
    │ (1)
    │
    ├─────► (many) Student Submissions
    │
    │ (1)
    │
    └─────► (1) Baseline (changes dynamically)
                 │
                 │ (references)
                 │
                 └─────► Student Submission (current best)

Student Submission (1) ──────► (1) Evaluation
                                    │
                                    │ (compared against)
                                    │
                                    └──► Baseline (at time of eval)
```

### 5.2 Data Models

#### Assignment
```yaml
assignment:
  name: "Web Development - Assignment 1"
  description: "Full text of assignment requirements..."
  evaluated_date: "2024-12-15"
  grading_weights:
    assignment_relevance: 50
    functionality: 50
  focus_files:
    - "src/**/*.js"
    - "README.md"
    - "package.json"
  project_type: "javascript_web"
  criteria:
    - "CRUD operations"
    - "LocalStorage persistence"
    - "Responsive design"
```

#### Student Submission
```python
{
    'student_name': 'student_alice',
    'student_id': '12345',         # optional
    'team_name': 'Team Alpha',     # optional
    'folder_path': '/path/to/student_alice/',
    'submission_type': 'git_repo',
    'project_type': 'javascript_web',
    'key_files': ['README.md', 'src/index.js', 'package.json'],
    'size_mb': 3.5,
    'file_count': 89
}
```

#### Evaluation
```python
{
    'student_name': 'student_alice',
    'grade': 85,
    'rank': 3,
    'relevance_score': 42,  # out of 50
    'functionality_score': 43,  # out of 50
    'reasoning': 'Implements all CRUD operations...',
    'compared_to_baseline': 'student_bob (92/100)',
    'status': 'evaluated' | 'skipped' | 'manual_review',
    'notes': 'Excellent error handling',
    'errors': None | 'Missing README'
}
```

#### Baseline
```python
{
    'student_name': 'student_bob',
    'grade': 92,
    'folder_path': '/path/to/student_bob/',
    'features_observed': [
        'CRUD operations',
        'LocalStorage persistence',
        'Dark mode toggle',
        'Responsive design'
    ],
    'timestamp_set': '2024-12-15T14:32:15'
}
```

### 5.3 File Formats

#### grades.csv
```csv
Student,ID,Grade,Rank,Team,Notes
student_bob,12345,92,1,Team Alpha,"Excellent implementation, exceeds requirements"
student_alice,12346,85,2,Team Beta,"Solid work, meets all criteria"
student_carol,12347,78,3,,"Good effort, minor issues with error handling"
```

#### assignment-config.yml
```yaml
assignment:
  name: "Web Development - Assignment 1"
  description: "Create a todo list web app..."
  evaluated_date: "2024-12-15"

baseline:
  student: "student_alice"
  grade: 85
  features_observed:
    - "CRUD operations"
    - "LocalStorage persistence"
    - "Responsive design"

grading_weights:
  assignment_relevance: 50
  functionality: 50

focus_files:
  - "src/**/*.js"
  - "README.md"
  - "package.json"

project_type: "javascript_web"

evaluation_criteria:
  - "CRUD operations implemented"
  - "LocalStorage persistence working"
  - "Responsive design"
  - "Code organization"
  - "Documentation quality"
```

---

## 6. Technology Stack

### 6.1 Core Technologies

| Layer | Technology | Version | Justification |
|-------|------------|---------|---------------|
| **Execution Platform** | Claude Code | Latest | Provides AI analysis, integrated tools, natural language interface |
| **Skill Definition** | Markdown (SKILL.md) | N/A | Standard format for Claude Code skills |
| **Helper Scripts** | Python | 3.8+ | Cross-platform, easy file ops, YAML parsing |
| **Config Format** | YAML | 1.2 | Human-readable, supports complex structures, standard for config |
| **Output: Grades** | CSV | RFC 4180 | Universal compatibility with gradebook systems |
| **Output: Report** | Markdown | CommonMark | Human-readable, version-controllable |
| **Version Control** | Git | 2.0+ | Standard for code versioning |

### 6.2 Python Dependencies

**requirements.txt**:
```
pyyaml>=6.0
```

**Rationale**: Minimize dependencies, use standard library where possible

### 6.3 Claude Code Tools Used

| Tool | Purpose |
|------|---------|
| **Read** | Read individual files (README.md, source code, configs) |
| **Glob** | Pattern matching for key files (src/**/*.js) |
| **Grep** | Search for specific code patterns or keywords |
| **Bash** | Execute helper scripts (scan_folders.py, analyze_repo.py) |
| **Write** | Generate CSV, Markdown, YAML outputs |

---

## 7. API Documentation

### 7.1 Internal Component APIs

#### SKILL.md → scan_folders.py

**Function**: `scan_student_folders(master_folder, exclude=None)`

**Input**:
```json
{
  "master_folder": "/path/to/Assignment1/",
  "exclude": ["student_alice", ".git", "__pycache__"]
}
```

**Output**:
```json
[
  {"name": "student_bob", "path": "/path/to/Assignment1/student_bob"},
  {"name": "student_carol", "path": "/path/to/Assignment1/student_carol"}
]
```

**Error Cases**:
- `FileNotFoundError`: master_folder doesn't exist
- `PermissionError`: No read access to folder

---

#### SKILL.md → analyze_repo.py

**Function**: `analyze_repository(folder_path)`

**Input**:
```json
{
  "folder_path": "/path/to/student_bob/"
}
```

**Output**:
```json
{
  "project_type": "javascript_web",
  "key_files": ["README.md", "src/index.js", "package.json"],
  "metadata": {
    "team_name": "Team Alpha",
    "student_id": "12345"
  },
  "size_mb": 3.5,
  "file_count": 89
}
```

**Error Cases**:
- `FileNotFoundError`: folder doesn't exist
- `ValueError`: Empty folder

---

### 7.2 Output File Schemas

#### grades.csv Schema

```csv
Column,Type,Required,Description
Student,string,Yes,Student folder name
ID,string,No,Student ID if found in metadata
Grade,integer,Yes,Relative grade (0-100)
Rank,integer,Yes,Ranking (1 = highest grade)
Team,string,No,Team name if group project
Notes,string,Yes,Brief evaluation summary
```

---

## 8. Deployment Architecture

### 8.1 Deployment Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                  Instructor's Local Machine                     │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              Claude Code Installation                  │    │
│  │                                                        │    │
│  │  ┌──────────────────────────────────────────────┐     │    │
│  │  │  .claude/skills/student-project-evaluator/   │     │    │
│  │  │                                              │     │    │
│  │  │  • SKILL.md                                  │     │    │
│  │  │  • README.md                                 │     │    │
│  │  │  • scripts/                                  │     │    │
│  │  │      - scan_folders.py                       │     │    │
│  │  │      - analyze_repo.py                       │     │    │
│  │  │  • examples/                                 │     │    │
│  │  │      - assignment-config.yml                 │     │    │
│  │  └──────────────────────────────────────────────┘     │    │
│  │                                                        │    │
│  │  Python 3.8+ Runtime                                  │    │
│  │  Git 2.0+                                             │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              File System                               │    │
│  │                                                        │    │
│  │  /Assignments/Assignment1/                            │    │
│  │  ├── student_alice/     (git repo)                    │    │
│  │  ├── student_bob/       (git repo)                    │    │
│  │  ├── ...                                              │    │
│  │  ├── grades.csv         (output)                      │    │
│  │  ├── evaluation_summary.md  (output)                  │    │
│  │  └── assignment-config.yml   (output)                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 8.2 Installation Process

1. **Prerequisites Check**:
   - Claude Code installed
   - Python 3.8+ available
   - Git installed (for repository operations)

2. **Skill Installation**:
   ```bash
   # Clone into WorkEnv or directly into skills directory
   cd ~/.claude/skills/
   git clone [repo-url] student-project-evaluator
   cd student-project-evaluator
   pip install -r requirements.txt
   ```

3. **Verification**:
   ```bash
   python scripts/scan_folders.py --help
   python scripts/analyze_repo.py --help
   ```

### 8.3 Runtime Environment

- **OS**: Cross-platform (Windows, macOS, Linux)
- **Memory**: <2GB for 50 repositories
- **Disk**: Minimal (outputs are KB-MB range)
- **Network**: None required (all local operations)

---

## 9. Cost Analysis

### 9.1 Token Usage Estimation

**Assumptions**:
- Average student repository: 50 files, ~5000 lines of code
- Files read per student: README (200 tokens) + 5-10 key source files (2000 tokens) + configs (200 tokens) ≈ **2500 tokens input**
- Evaluation output per student: ~500 tokens
- Baseline calibration: ~3000 tokens (more detailed analysis)

**Per Batch (5 students)**:
```
Input tokens:  5 × 2500 = 12,500 tokens
Output tokens: 5 × 500  = 2,500 tokens
Total per batch:         15,000 tokens
```

**For 30 students (6 batches)**:
```
Total input:   6 × 12,500 = 75,000 tokens
Total output:  6 × 2,500  = 15,000 tokens
Baseline:                   3,000 tokens
Grand total:               93,000 tokens ≈ 0.09M tokens
```

### 9.2 Cost Breakdown (If Using Claude API)

**Note**: This skill runs in Claude Code, which may have different pricing. These are estimates if using API directly.

| Model | Input Cost | Output Cost | Total (30 students) |
|-------|------------|-------------|---------------------|
| Claude Sonnet 4.5 | 75K tokens × $3/MTok | 15K tokens × $15/MTok | $0.225 + $0.225 = **$0.45** |
| Claude Haiku | 75K tokens × $0.25/MTok | 15K tokens × $1.25/MTok | $0.019 + $0.019 = **$0.04** |

**Optimization Strategies**:
1. **Use focus_files** in config to read only relevant files (reduces input tokens by ~30%)
2. **Batch processing** already minimizes context duplication
3. **Skip non-code files** (images, binaries) to reduce token usage

### 9.3 Budget Management

- **For 100 students/semester**: ~$1.50 using Sonnet (assuming 3 batches of 30 students)
- **For 5 courses**: ~$7.50/semester
- **Annual cost** (2 semesters): ~$15

**Conclusion**: Cost is negligible for academic use.

---

## 10. Extensibility and Plugin Architecture

### 10.1 Extension Points

#### 10.1.1 Submission Type Plugins (Future)

**Current**: Git repositories only

**Extensibility Design**:
```python
# submission_types/git_repo.py
class GitRepoSubmission(SubmissionType):
    def read_files(self, folder_path):
        # Implementation for reading git repos
        pass

    def detect_project_type(self, folder_path):
        # Auto-detect JavaScript, Python, Java, etc.
        pass

# submission_types/pdf_submission.py (v1.1)
class PDFSubmission(SubmissionType):
    def read_files(self, file_path):
        # Extract text from PDF
        pass

    def detect_project_type(self, file_path):
        # Determine report type
        pass
```

**Config-Based Selection**:
```yaml
submission_type: "git_repo"  # or "pdf", "zip", etc.
```

#### 10.1.2 Evaluation Criteria Plugins

**Current**: Assignment relevance (50%) + Functionality (50%)

**Extensibility**:
```yaml
grading_weights:
  assignment_relevance: 40
  functionality: 40
  code_quality: 10        # New criterion (future)
  documentation: 10       # New criterion (future)
```

SKILL.md reads these weights and applies proportionally.

#### 10.1.3 Output Format Plugins

**Current**: CSV + Markdown

**Extensibility**:
```yaml
output_formats:
  - csv
  - markdown
  - json          # Future: machine-readable API
  - excel         # Future: .xlsx export
```

### 10.2 Maintainability Features

| Feature | Implementation |
|---------|----------------|
| **Modularity** | SKILL.md (orchestration) separate from scripts (file ops) |
| **Separation of Concerns** | Each script has single responsibility (scan vs. analyze) |
| **Reusability** | Helper scripts can be reused in other skills |
| **Analyzability** | Clear component boundaries, documented APIs |
| **Testability** | Scripts are pure functions, easy to unit test |

### 10.3 Future Enhancements (Roadmap)

**v1.1 (Next Semester)**:
- PDF submission support
- Identical submission detection (plagiarism checking)
- Comprehensive markdown reports (detailed graphs)

**v1.2**:
- Template system for custom rubrics
- Multi-language support (evaluate in languages other than English)

**v2.0 (Production Version)**:
- LMS integration (Canvas, Moodle APIs)
- Web dashboard (visualize class performance)
- AI-powered student feedback generation

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-15 | Initial architecture for MVP |

---

**End of Planning Document**
