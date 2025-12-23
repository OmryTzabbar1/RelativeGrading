---
name: evaluating-student-projects
description: Evaluate student programming projects by analyzing markdown documentation. Use when grading student submissions, evaluating coding projects, comparing student work, generating grades from project folders, or assessing assignment completeness. Discovers criteria from .md files, weights by class prevalence, and generates relative grades.
---

# Student Project Evaluator

Evaluate student projects by reading their markdown documentation (.md files) and discovering what criteria each student has implemented.

## When to Use This Skill

- User asks to "evaluate", "grade", or "assess" student projects
- User provides a folder containing multiple student submission folders
- User wants to compare students against each other
- User needs grades based on project documentation

## Quick Start

```
Evaluation Workflow:
- [ ] Step 1: Get master folder path from user
- [ ] Step 2: Discover all student folders
- [ ] Step 3: For each student, find and read all .md files
- [ ] Step 4: Extract criteria from markdown content
- [ ] Step 4b: Discover and save new extraction patterns
- [ ] Step 5: Build criteria graph (who has what)
- [ ] Step 6: Smart Grouping - Consolidate tech variations
- [ ] Step 7: Categorize criteria into broad topics
- [ ] Step 8: Calculate prevalence-based weights
- [ ] Step 9: Score and grade each student
- [ ] Step 10: Generate output files
```

## Execution Flow

### Step 1: Collect Input

Ask the user for the master folder path containing student submissions.

**Expected structure:**
```
master_folder/
├── student_alice/
│   ├── README.md
│   ├── docs/
│   │   └── ARCHITECTURE.md
│   └── ...
├── student_bob/
│   ├── README.md
│   └── ...
└── student_N/
    └── ...
```

### Step 2: Discover Students

1. List all subdirectories in the master folder
2. Each subdirectory = one student
3. Exclude hidden folders (starting with `.`)
4. Confirm count with user: "Found X student folders. Proceed?"

### Step 3: Read Markdown Files

For each student folder:
1. Recursively find all `.md` files
2. Read each markdown file
3. Store content for criteria extraction

**Important:** Read ALL .md files, not just README.md. Students may have:
- README.md
- docs/PRD.md
- docs/ARCHITECTURE.md
- CONTRIBUTING.md
- CHANGELOG.md
- Any other .md files

### Step 4: Extract Criteria

For each markdown file, extract **granular criteria** - specific features, elements, and accomplishments mentioned.

**What to extract:**
- Features implemented ("We built X", "The project includes Y")
- Testing ("unit tests", "integration tests", "test coverage")
- Documentation types ("API docs", "user guide")
- DevOps elements ("CI/CD", "Docker", "deployment")
- Research work ("analysis", "findings", "data exploration")
- Visual elements ("screenshots", "diagrams", "charts")
- Planning artifacts ("PRD", "architecture", "design decisions")
- Business considerations ("cost analysis", "ROI", "market research")

**Context Validation - CRITICAL:**

Only count criteria that are ACTUALLY IMPLEMENTED. Check the context around each mention.

**DO count (valid):**
- "We implemented unit tests"
- "The project includes CI/CD via GitHub Actions"
- "Test coverage is at 85%"
- "Screenshots are in the /images folder"
- "Architecture diagram below:"

**DO NOT count (invalid):**
- "TODO: add unit tests"
- "Unit tests not yet implemented"
- "We plan to add CI/CD"
- "Future work: integration tests"
- "Out of scope: deployment"
- "FIXME: need to add docs"

For detailed extraction rules, see [EXTRACTION.md](EXTRACTION.md).

### Step 4b: Discover New Extraction Patterns

**IMPORTANT:** As you analyze student markdown files, you will encounter new ways students describe their work that aren't in EXTRACTION.md. When you find these, UPDATE EXTRACTION.md.

**When to add new patterns:**

1. **New positive indicators** - Phrases indicating something IS implemented:
   - "Powered by X"
   - "Leverages X"
   - "Equipped with X"
   - "Comes with X"
   - Any phrase you see students use to claim implemented features

2. **New negative indicators** - Phrases indicating something is NOT implemented:
   - "Coming soon: X"
   - "Stretch goal: X"
   - "Nice to have: X"
   - "If time permits: X"
   - Any phrase indicating future/planned/incomplete work

3. **New criteria types** - Categories of work not previously captured:
   - New documentation types students create
   - New testing approaches
   - New DevOps tools/practices
   - Domain-specific elements

**How to update EXTRACTION.md:**

After processing the first few students (or whenever you discover new patterns), append them to the "Discovered Patterns" section at the end of EXTRACTION.md.

Format to use:
```markdown
### [Date] - Discovered from [student_name]

**New positive indicators:**
- "Phrase found" → Indicates: [what it means]

**New negative indicators:**
- "Phrase found" → Indicates: [what it means]

**New criteria types:**
- [Criterion name]: [description]
```

**Why this matters:**
- Early students help train the extraction for later students
- Patterns discovered in student 1 will help find similar features in student 35
- Builds a comprehensive extraction ruleset over time
- Makes the skill smarter with each evaluation

### Step 5: Build Criteria Graph

As you extract criteria, build a graph structure:

```
criteria_graph = {
    "criterion_name": {
        "students": ["alice", "bob", "carol"],
        "count": 3,
        "category": null,  // assigned in Step 6
        "weight": null     // calculated in Step 7
    },
    ...
}
```

**Key rules:**
- Normalize criterion names (lowercase, consistent naming)
- "Unit tests" and "unit testing" = same criterion
- Track which students have each criterion
- One student can only be counted once per criterion

### Step 6: Smart Grouping - Consolidate Tech Variations

**CRITICAL:** Before categorizing, consolidate tech-specific variations to ensure fair, capability-based comparison.

**The Problem:**
Extracting granular criteria like "Black", "Ruff", "ESLint", "MyPy", "Type Hints", "Pydantic" as separate items unfairly rewards students who used MORE tools for the SAME purpose (code quality).

**The Solution:**
Group technology choices that serve the same capability into consolidated criteria.

**Consolidation Rules:**

| Raw Criteria (Tech Choices) | Consolidated Criterion | Rationale |
|------------------------------|------------------------|-----------|
| Black, Ruff, ESLint, Prettier, MyPy, Type Hints, Pydantic, Pre-commit | **Code Quality Tools** | All serve code quality/linting/typing |
| Unit Tests, Integration Tests, E2E Tests, Pytest, Jest, Mocha | Keep separate TYPES, consolidate FRAMEWORKS | Test types are different capabilities; frameworks are tech choices |
| Google Maps API, YouTube API, Spotify API, Claude API, OpenAI API | **External API Integrations** | All are API integrations (capability) |
| YAML Config, JSON Config, .env files, Multiple config files | **Configuration Management** | All serve configuration (capability) |
| Nested ThreadPoolExecutor, Queue-based, Multiprocessing, Parallel Processing | **Concurrency Patterns** | All are concurrency approaches |
| CI/CD, Docker, Deployment Scripts, One-step Setup | **DevOps Infrastructure** | All are deployment/ops capabilities |
| React, Next.js, Vue, Angular, Responsive Design, Dark Mode | **Frontend Implementation** | All are frontend capabilities |
| FastAPI, Flask, Express, WebSocket, REST API | **Backend Services** | All are backend capabilities |

**When to Consolidate:**
- ✅ **DO consolidate:** Different tools serving the SAME purpose
  - Black + Ruff + ESLint → "Code Quality Tools"
  - pytest + jest + mocha → "Testing Framework"
  - Docker + Kubernetes → "Containerization"

- ❌ **DO NOT consolidate:** Different types/levels of the same category
  - Unit Tests vs Integration Tests (different test TYPES)
  - README vs API Docs (different doc TYPES)
  - Circuit Breakers vs Retry Logic (different resilience PATTERNS)

**How to Apply:**
```
For each criteria type:
    Find all tech-specific variations
    If they serve the same capability:
        Create consolidated criterion
        Merge student lists (union of all students)
        Remove individual tech criteria

Example:
Before:
  - "Black Code Formatting": [alice, bob]
  - "Ruff Linting": [bob, carol]
  - "ESLint": [carol]
  - "MyPy": [alice, bob]

After:
  - "Code Quality Tools (Formatting/Linting/Type Checking)": [alice, bob, carol]
```

**Result:** Fair comparison based on CAPABILITIES, not tool count.

**Implementation:**
Use the `smart_grouping.py` script to perform this consolidation automatically:
```bash
cd .claude/skills/evaluating-student-projects/scripts
python smart_grouping.py
```

This script reads `outputs/criteria_graph_final.json` and outputs `outputs/criteria_graph_grouped.json` with consolidated criteria.

### Step 7: Categorize Criteria

Match each criterion to a broad category. See [CATEGORIES.md](CATEGORIES.md) for full list.

**Categories:**
| Category | Example Criteria |
|----------|------------------|
| Documentation | README, API docs, user guide, changelog |
| Planning | PRD, architecture, design docs, roadmap |
| Testing | unit tests, integration tests, E2E, coverage |
| DevOps | CI/CD, Docker, deployment, monitoring |
| Research | analysis, notebooks, findings, experiments |
| Visuals | screenshots, diagrams, charts, demos |
| CodeQuality | linting, type checking, code review |
| Business | cost analysis, ROI, market research |

**Uncategorized criteria:**
- Save to `flagged_criteria.md` for manual review
- Include in output but mark as "Uncategorized"
- These criteria still count toward student scores

### Step 8: Calculate Weights

Weight each criterion by prevalence (how many students have it):

```
weight = count / total_students

Example (35 students):
- README: 35/35 = 1.0 (everyone has it, critical)
- Unit tests: 28/35 = 0.8 (most have it, important)
- Cost analysis: 5/35 = 0.14 (few have it, bonus)
```

**Interpretation:**
- High weight (>0.7): Core requirement, missing it hurts
- Medium weight (0.3-0.7): Common feature, good to have
- Low weight (<0.3): Bonus feature, rewards those who have it

### Step 9: Score and Grade

## Grading Formula

### Base Score
Base Score = (sum of weighted criteria student has) / (total possible weight) × 100

### Rarity Bonuses
Students receive bonus points for having rare/distinguishing criteria:

| Prevalence | Bonus |
|------------|-------|
| ≤ 15% | +1 point |

### Final Score
Final Score = Base Score + Sum of Rarity Bonuses (capped at 100)

**Assign ranks:**
- Sort by final score descending
- Rank 1 = highest score
- Handle ties: same score = same rank

**Implementation:**
Use the `recalculate_grades.py` script to calculate grades with rarity bonuses:
```bash
cd .claude/skills/evaluating-student-projects/scripts
python recalculate_grades.py
```

This script reads `outputs/criteria_graph_grouped.json` and outputs grade rankings to console.

### Step 10: Generate Outputs

Generate the following files in the `outputs/` directory:

1. **criteria_graph_final.json** - Complete raw criteria data
2. **criteria_graph_grouped.json** - Consolidated criteria (after smart grouping)
3. **grades.xlsx** - Comprehensive Excel report with rankings and analysis
4. **evaluation_report.md** - Full analysis report in Markdown

**Implementation:**
Use the `create_excel_report.py` script to generate the comprehensive Excel report:
```bash
cd .claude/skills/evaluating-student-projects/scripts
python create_excel_report.py
```

This script creates a multi-sheet Excel workbook with:
- Final grades and rankings
- Detailed criteria breakdown
- Comparison charts
- Category distribution
- Before/after consolidation comparison

For detailed output formats, see [OUTPUT-FORMATS.md](OUTPUT-FORMATS.md).

**Note:** For development and validation, additional utility scripts are available in `scripts/dev/`. See `scripts/README.md` for the complete script organization.

## Progress Reporting

After each major step, report progress to the user:

```
[Step 2/10] Found 35 student folders
[Step 3/10] Reading markdown files... (student 15/35)
[Step 4/10] Extracted 127 unique criteria
[Step 6/10] Consolidated 127 criteria into 45 capability groups
[Step 7/10] Categorized 42 criteria, flagged 3 for review
[Step 9/10] Grading complete. Top score: 87.0 (alice)
[Step 10/10] Generated 4 output files in outputs/
```

## Error Handling

**Missing markdown files:**
- Log: "Warning: No .md files found in student_X"
- Give student 0 criteria (they still appear in results)
- Continue with other students

**Unreadable files:**
- Log: "Warning: Could not read file_path"
- Skip file, continue with others
- Do not fail entire process

**Empty folders:**
- Treat as student with 0 criteria
- Include in final grades (will be lowest ranked)

## Example Session

**User:** "Evaluate the student projects in /Assignments/WebDev_A1/"

**Claude:**
1. Scans folder, finds 35 student directories
2. "Found 35 student folders. Proceeding with evaluation..."
3. Reads all .md files from each student
4. Extracts criteria: "Discovered 127 unique criteria across all students"
5. Smart Grouping: "Consolidated 127 criteria into 45 capability groups"
6. Categorizes: "Categorized 42 criteria into 8 categories. 3 flagged for review."
7. Calculates weights and grades
8. "Evaluation complete!"
   - Best student: alice (87.0)
   - Average grade: 62.4
   - Generated files in outputs/

## Output Summary

After completion, provide a summary:

```
## Evaluation Complete

**Students evaluated:** 35
**Criteria extracted:** 127 (raw)
**Consolidated:** 45 capability groups
**Categorized:** 42 | **Flagged:** 3

**Grade Distribution:**
- 80-100: 3 students
- 70-79: 2 students
- 60-69: 5 students
- 50-59: 8 students
- Below 50: 17 students

**Top 5 Students:**
1. alice (87.0) - 31/45 criteria (69%)
2. bob (76.4) - 25/45 criteria (56%)
3. carol (75.5) - 24/45 criteria (53%)
4. diana (61.6) - 17/45 criteria (38%)
5. eve (54.0) - 15/45 criteria (33%)

**Consolidation Impact:**
- Fair comparison based on capabilities, not tool count
- Students rewarded for what they can do, not how many tools they used

**Output files:**
- outputs/criteria_graph_final.json (raw criteria)
- outputs/criteria_graph_grouped.json (consolidated)
- outputs/flagged_criteria.md
- outputs/grades.xlsx
- outputs/evaluation_report.md
```

## Tips for Best Results

1. **Be thorough with extraction** - Read carefully, don't miss criteria
2. **Validate context** - "TODO" mentions don't count
3. **Normalize names** - Keep criterion names consistent
4. **Include all students** - Even empty folders get scored (0)
5. **Save progress** - Write outputs incrementally if possible
