# Criteria Extraction Rules

This document defines how to extract criteria from markdown files and validate their context.

## ⚠️ CRITICAL: Thoroughness Requirements

**When extracting criteria, you MUST:**

1. **Read EVERY .md file found** - Don't skip files in subdirectories
2. **Check filenames FIRST** - PRD.md exists = PRD Document criterion (see table below)
3. **Scan for section headers** - `## Testing` = Testing Documentation (see table below)
4. **Look for file references** - If README links to `TESTING.md`, credit it
5. **Be liberal with matching** - "This project includes unit tests" should match "includes" pattern
6. **Extract from tables of contents** - Documentation indexes show what exists
7. **Read the full file** - Don't stop after the first section
8. **Case-insensitive matching** - "Unit Tests" = "unit tests" = "UNIT TESTS"

**Common mistake to avoid:**
- ❌ Only reading README.md and stopping
- ❌ Requiring exact phrase matches
- ❌ Ignoring files in subdirectories like `Documentation/`, `docs/`, etc.
- ❌ Missing documentation that's organized into multiple files
- ✅ Read ALL markdown, check ALL filenames, match patterns liberally

## Extraction Principles

1. **Be granular** - Extract specific items, not broad topics
2. **Validate context** - Only count what's actually implemented
3. **Normalize names** - Keep criterion names consistent
4. **Track sources** - Note which file each criterion came from
5. **Be thorough** - Better to over-extract than under-extract
6. **Capabilities over implementation details** - Extract WHAT was accomplished, not HOW it was built

### Implementation-Specific vs Capability-Based Criteria

**CRITICAL RULE:** Only extract criteria that represent capabilities or accomplishments, not implementation choices.

**❌ DO NOT extract (implementation-specific):**
- Technology stack choices: "Built with React", "Powered by FastAPI", "Uses PostgreSQL"
- Framework choices: "Built using Express.js", "Created with Next.js"
- Language choices: "Written in Python", "Built with TypeScript"
- Library choices: "Uses Pandas", "Powered by TensorFlow"

These are HOW the project was built, not WHAT was accomplished. Different students may use different tech stacks to achieve the same capability.

**✅ DO extract (capability-based):**
- "Frontend implementation" (regardless of React/Vue/Angular)
- "Backend API" (regardless of Express/FastAPI/Flask)
- "Database integration" (regardless of PostgreSQL/MongoDB/MySQL)
- "Machine learning model" (regardless of TensorFlow/PyTorch/scikit-learn)
- "Real-time updates" (capability, regardless of WebSocket/SSE/polling implementation)
- "Authentication system" (capability, regardless of JWT/OAuth/session-based)

**General judgment:** If it's specific to how the project was built (tech choice), don't extract it. If it's useful to the project and relevant to what was accomplished (capability), extract it.

**Example:**
- ❌ "Built with React and TypeScript" → Don't extract "React" or "TypeScript"
- ✅ "Built with React and TypeScript for a responsive frontend" → Extract "Frontend implementation" + "Responsive design"
- ❌ "Powered by Claude API" → Don't extract as a criterion
- ✅ "LLM integration for intelligent responses" → Extract "LLM integration" or "AI-powered features"

## CRITICAL: Filename-Based Detection

**ALWAYS check filenames first!** If a student has these files, automatically credit them:

| Filename Pattern | Criterion to Credit | Notes |
|-----------------|-------------------|-------|
| `PRD.md`, `prd.md`, `ProductRequirements.md` | PRD Document | Product requirements |
| `TESTING.md`, `testing.md`, `TEST.md` | Testing Documentation | Testing guide |
| `CONTRIBUTING.md`, `contributing.md` | Contributing Guide | Contribution guidelines |
| `QUICKSTART.md`, `QuickStart.md`, `quick-start.md` | Quick Start Guide | Quick setup guide |
| `ARCHITECTURE.md`, `architecture.md`, `DESIGN.md` | Architecture Documentation | Architecture/design docs |
| `CHANGELOG.md`, `changelog.md`, `CHANGES.md` | Changelog | Version history |
| `API.md`, `api.md`, `API_DOCS.md` | API Documentation | API documentation |
| `ROADMAP.md`, `roadmap.md` | Roadmap | Project roadmap |
| `DEPLOYMENT.md`, `deployment.md`, `DEPLOY.md` | Deployment Guide | Deployment instructions |
| `TROUBLESHOOTING.md`, `troubleshooting.md`, `FAQ.md` | Troubleshooting Guide | Problem-solving guide |

**File reference detection:**
If markdown contains links or references to these files (e.g., `[TESTING.md](TESTING.md)` or `See TESTING.md for details`), credit the corresponding criterion.

## Section Header Detection

**Look for major section headers** that indicate implemented features:

| Header Pattern | Criterion | Context Required |
|---------------|----------|------------------|
| `## Testing`, `## Tests`, `# Testing` | Testing Documentation | Section must have content, not TODO |
| `## Unit Tests`, `### Unit Tests` | Unit Tests | Must describe actual tests |
| `## Installation`, `## Setup`, `## Getting Started` | Installation Instructions | Must have actual steps |
| `## Usage`, `## How to Use` | Usage Guide | Must have examples/instructions |
| `## Features`, `## Functionality` | Scan content for specific features | List features individually |
| `## Screenshots`, `## Demo`, `## Examples` | Screenshots/Visuals | Must reference actual images/demos |
| `## Architecture`, `## Design` | Architecture Documentation | Must have design details |
| `## CI/CD`, `## Deployment`, `## DevOps` | DevOps elements | Scan for specific tools |
| `## API`, `## Endpoints`, `## API Reference` | API Documentation | Must have endpoint details |
| `## Contributing`, `## Development` | Contributing Guide | Must have contribution info |
| `## Problem Statement`, `## Problem` | Problem Statement | Must describe the problem |
| `## Solution`, `## Proposed Solution` | Solution Overview | Must describe solution approach |
| `## Requirements`, `## Functional Requirements` | Requirements Documentation | Must list requirements |
| `## Use Cases`, `## Use Case` | Use Case Documentation | Must describe use cases |
| `## Cost Analysis`, `## Budget`, `## Costs` | Cost Analysis | Must have cost breakdown |
| `## Assumptions`, `## Constraints` | Assumptions/Constraints | Must list assumptions |
| `## Success Metrics`, `## KPIs`, `## Metrics` | Success Metrics | Must define metrics |
| `## Risk Analysis`, `## Risks` | Risk Analysis | Must identify risks |
| `## Roadmap`, `## Future Work`, `## Next Steps` | Roadmap | Must outline future plans |
| `## User Stories`, `## User Personas` | User Research | Must define users/stories |
| `## Design Decisions`, `## Trade-offs` | Design Rationale | Must explain decisions |

## What to Extract

### Features & Functionality

Look for mentions of implemented features:

**Positive indicators (case-insensitive matching):**

**Implementation indicators:**
- "We built...", "We created...", "We developed...", "We implemented..."
- "The project includes...", "This project includes...", "Project includes..."
- "Features:", "Key features:", "Main features:", "Implemented features:"
- "Implemented...", "Created...", "Developed...", "Built..."
- "Added...", "Integrated...", "Incorporated..."
- "Supports...", "Provides...", "Offers...", "Enables..."
- "Has...", "Contains...", "Comes with..."
- "Complete...", "Comprehensive...", "Full..."
- "Available:", "Includes:", "Featuring:"
- "With support for...", "Capable of..."
- "Total tests:", "Test cases:", "~X tests", "X+ tests"
- "Coverage:", "Code coverage:", "Test coverage:"
- "Version X.X includes...", "Version X features..."

**Planning & analysis indicators:**
- "The problem is...", "Problem statement:", "We identified the following problem..."
- "Our solution...", "Proposed solution:", "We propose..."
- "The objective is...", "Goals:", "Our goal is to..."
- "Success will be measured by...", "KPIs:", "Metrics include..."
- "We assume...", "Assumptions:", "Based on the assumption that..."
- "Constraints include...", "Limitations:", "We are constrained by..."
- "Use cases:", "Use case 1:", "The user can...", "The system shall..."
- "Requirements:", "Functional requirements:", "The system must..."
- "Cost analysis shows...", "Budget:", "Estimated cost:", "Total cost:"
- "ROI:", "Return on investment:", "Expected savings:"
- "Risks include...", "Risk analysis:", "Potential risks:"
- "Timeline:", "Schedule:", "Milestones:", "We plan to..."
- "Design decision:", "We chose X because...", "Trade-offs:", "Alternatives considered:"

**Table of Contents / Index patterns:**
- If a README/index file lists other .md files (e.g., `[PRD.md](PRD.md)`), credit those as existing
- Section headers with links indicate implemented documentation

**Examples:**

**Implementation features:**
- "We built a real-time chat feature" → "Real-time chat"
- "The project includes user authentication" → "User authentication"
- "Supports dark mode" → "Dark mode"
- "This project includes comprehensive unit tests" → "Unit tests"
- "Total tests: ~75 test cases" → "Unit tests" + "Test coverage metrics"

**Planning & analysis:**
- "## Problem Statement\nThe current system lacks efficient routing..." → "Problem Statement"
- "Our solution uses A* algorithm to optimize..." → "Solution Overview"
- "Success metrics: 90% accuracy, <100ms response time" → "Success Metrics"
- "We identified three primary use cases..." → "Use Case Documentation"
- "Cost analysis: $0.50/1000 API calls, estimated $150/month" → "Cost Analysis"
- "Assumptions: Users have GPS-enabled devices" → "Assumptions Documentation"
- "Constraints: Limited to 100 concurrent users" → "Constraints Documentation"
- "The system must handle 1000 requests/second" → "Functional Requirements"
- "Trade-offs: We chose simplicity over feature richness" → "Trade-offs Analysis"

### Documentation Elements

Look for documentation mentions:

- "See the README for..." → "README"
- "API documentation is in /docs" → "API documentation"
- "Architecture described in ARCHITECTURE.md" → "Architecture document"

### Planning & Analysis Artifacts

**IMPORTANT:** Problem statements, requirements, analysis, and planning documentation are equally important as technical implementation. Extract these as criteria:

**Planning Documents:**
- "Problem Statement" section/header → "Problem Statement"
- "Solution Overview", "Proposed Solution" → "Solution Overview"
- "Project Goals", "Objectives" → "Project Goals"
- "Success Metrics", "KPIs", "Evaluation Criteria" → "Success Metrics"
- "Assumptions" section → "Assumptions Documentation"
- "Constraints", "Limitations" → "Constraints Documentation"
- "Scope" section → "Scope Documentation"

**Business & Economics:**
- "Cost Analysis", "Cost Breakdown", "Budget" → "Cost Analysis"
- "ROI Analysis", "Return on Investment" → "ROI Analysis"
- "Market Research", "Market Analysis" → "Market Research"
- "Competitive Analysis", "Competitor Comparison" → "Competitive Analysis"
- "Business Model", "Revenue Model" → "Business Model"
- "Risk Analysis", "Risk Assessment" → "Risk Analysis"

**Requirements & Use Cases:**
- "Use Cases" section → "Use Case Documentation"
- "User Stories" → "User Stories"
- "Functional Requirements" → "Functional Requirements"
- "Non-functional Requirements" → "Non-functional Requirements"
- "User Personas", "Target Users" → "User Personas"
- "User Flow", "User Journey" → "User Flow Documentation"

**Design Rationale:**
- "Design Decisions", "Design Rationale" → "Design Decision Documentation"
- "Trade-offs", "Alternatives Considered" → "Trade-offs Analysis"
- "Technology Selection", "Why we chose X" → "Technology Justification"

**Project Management:**
- "Timeline", "Schedule", "Project Plan" → "Timeline Documentation"
- "Milestones" section → "Milestones"
- "Roadmap", "Future Work" → "Roadmap"
- "Known Issues", "Known Limitations" → "Known Limitations"

**Examples:**
- "## Problem Statement\nThe current system lacks..." → "Problem Statement"
- "Cost analysis shows..." → "Cost Analysis"
- "We identified three use cases..." → "Use Case Documentation"
- "Success metrics: 90% accuracy, <100ms latency" → "Success Metrics"
- "Assumptions: API rate limit is 1000 req/min" → "Assumptions Documentation"

### Testing

Look for testing mentions:

**Test implementation indicators:**
- "Unit tests", "unit testing", "test suite"
- "Integration tests", "integration testing", "end-to-end tests", "E2E tests"
- "Test coverage", "code coverage", "~X% coverage", "X% covered"
- "Total tests:", "X test cases", "X+ tests", "~X tests"
- "Test files:", "test_*.py", "*.test.js", "*.spec.ts"
- "pytest", "unittest", "Jest", "Mocha", "JUnit"
- "Testing framework", "test runner"
- "Comprehensive tests", "thorough testing", "well-tested"
- "All tests pass", "tests passing", "✓ tests"

**Test documentation indicators:**
- TESTING.md file exists → "Testing Documentation"
- "## Testing" section → "Testing Documentation"
- "How to run tests", "Running tests", "Test execution"

**Coverage metrics:**
- "85% coverage" → "Test Coverage Metrics (85%)"
- "~90% code coverage" → "Test Coverage Metrics"
- Any specific percentage → Track as "Test Coverage Metrics"

**Examples:**
- "Unit tests in /tests" → "Unit tests"
- "85% code coverage" → "Test Coverage Metrics"
- "Integration tests for API endpoints" → "Integration tests"
- "E2E tests with Playwright" → "E2E tests"
- "This project includes comprehensive unit tests for all three versions" → "Unit tests" + "Testing Documentation"
- "Total tests: ~75 test cases" → "Unit tests" + "Test Coverage Metrics"

### Quality Standards & Best Practices

**IMPORTANT:** Code quality standards and best practices are critical criteria. Extract these when students mention them in their documentation.

**Linting & Code Quality:**
- "ESLint", "eslint configuration", ".eslintrc" → "ESLint Configuration"
- "Pylint", "pylint", ".pylintrc" → "Pylint Configuration"
- "Ruff", "ruff configuration" → "Ruff Linting"
- "Linting", "linter", "code linting" → "Linting Configuration"
- "Flake8", "Black", "isort" → "Python Code Quality Tools"
- "TSLint", "JSLint" → "JavaScript Linting"
- "SonarQube", "SonarCloud" → "Static Analysis Tools"

**Code Formatting:**
- "Prettier", "prettier configuration" → "Prettier Formatting"
- "Black", "black formatter" → "Black Formatting"
- "autopep8", "yapf" → "Python Formatting"
- "Code formatting", "auto-formatting", "format on save" → "Code Formatting"

**Code Style & Standards:**
- "Code style guide", "style guide", "coding standards" → "Code Style Guide"
- "CONTRIBUTING.md" (as a style/standards doc) → "Contributing Guide" + "Code Style Guide"
- "PEP 8", "PEP8 compliant", "follows PEP 8" → "PEP8 Compliance"
- "Airbnb style guide", "Google style guide" → "Code Style Guide"
- "Consistent code style", "enforced style" → "Code Style Guide"

**Pre-commit & Git Hooks:**
- "Pre-commit hooks", "pre-commit", ".pre-commit-config.yaml" → "Pre-commit Hooks"
- "Git hooks", "commit hooks", "husky" → "Git Hooks"
- "Pre-commit configuration", "pre-commit framework" → "Pre-commit Hooks"
- "Lint-staged", "lint on commit" → "Pre-commit Hooks"

**Type Checking:**
- "TypeScript", "TypeScript strict mode", "strict type checking" → "TypeScript Type Checking"
- "Mypy", "type hints", "type annotations" → "Mypy Type Checking"
- "Type checking", "static type checking" → "Type Checking"
- "Pyright", "Pyre" → "Python Type Checking"

**Code Review & Quality Practices:**
- "Code review", "peer review", "pull request reviews" → "Code Review Process"
- "Code review guidelines", "review checklist" → "Code Review Process"
- "Quality gates", "quality checks" → "Quality Gates"
- "Code standards enforced", "automated quality checks" → "Automated Quality Checks"

**Project Setup & Configuration:**
- "setup.py", "pyproject.toml", "package.json" (mentioned as quality config) → "Project Setup Configuration"
- "Requirements files", "dependency management" → "Dependency Management"
- "Virtual environment", "venv", "conda environment" → "Environment Management"

**Examples:**
- "We use ESLint to maintain code quality" → "ESLint Configuration"
- "Code formatted with Black and checked with Pylint" → "Black Formatting" + "Pylint Configuration"
- "Pre-commit hooks ensure code quality before commits" → "Pre-commit Hooks"
- "TypeScript in strict mode for type safety" → "TypeScript Type Checking"
- "All PRs require code review" → "Code Review Process"
- "Following PEP 8 style guide" → "PEP8 Compliance"
- "Prettier and ESLint configured" → "Prettier Formatting" + "ESLint Configuration"

### DevOps & Infrastructure

Look for DevOps elements:

- "CI/CD via GitHub Actions" → "CI/CD pipeline"
- "Dockerized application" → "Docker containerization"
- "Deployed to AWS" → "Cloud deployment"
- "Kubernetes orchestration" → "Kubernetes"

### Research & Analysis

Look for research work:

- "Analysis in notebooks/" → "Data analysis notebooks"
- "Benchmark results show..." → "Performance benchmarking"
- "User research findings" → "User research"

### Visual Elements

Look for visuals:

- "Screenshots in /images" → "Screenshots"
- "Architecture diagram below" → "Architecture diagram"
- "Demo video: [link]" → "Demo video"

---

## Context Validation

### VALID Patterns (Count These)

**Affirmative statements:**
```
"We implemented X"
"X is included"
"The project has X"
"X is complete"
"Successfully added X"
"X works as expected"
"Fully functional X"
```

**Present tense claims:**
```
"The app includes..."
"Users can..."
"The system provides..."
"Features: X, Y, Z"
```

**Evidence of completion:**
```
"Screenshot of X below:"
"See X in action:"
"X test results: PASSED"
"Coverage: 85%"
"X deployed at [url]"
```

**File/folder references:**
```
"X is in the /folder directory"
"See X.md for details"
"X configuration in config/"
```

### INVALID Patterns (Do NOT Count)

**Future intentions:**
```
"TODO: add X"
"FIXME: implement X"
"Will add X later"
"Planning to implement X"
"X is planned for v2"
"Future work: X"
"Next steps: X"
```

**Explicit negatives:**
```
"X not yet implemented"
"X is not complete"
"Missing X"
"X out of scope"
"Skipped X"
"X omitted"
"No X currently"
"X not working"
```

**Conditional/uncertain:**
```
"X might be added"
"Considering X"
"If time permits, X"
"X would be nice to have"
"Ideally X"
"X is optional"
```

**References to others:**
```
"Similar projects have X"
"Best practice suggests X"
"We could use X like [other project]"
"X is commonly used for..."
```

---

## Normalization Rules

### Naming Consistency

Normalize similar terms to a single canonical name:

| Variations | Canonical Name |
|------------|----------------|
| unit test, unit tests, unit testing | Unit tests |
| readme, README, README.md | README |
| ci/cd, CI/CD, continuous integration | CI/CD pipeline |
| docker, dockerfile, containerized | Docker |
| e2e, E2E, end-to-end, end to end | E2E tests |
| typescript, TypeScript, TS | TypeScript |
| api docs, API documentation | API documentation |

### Casing

- Use Title Case for criterion names: "Unit Tests" not "unit tests"
- Exception: Acronyms stay uppercase: "CI/CD", "API", "E2E"

### Specificity

Keep criteria specific but not overly detailed:

| Too Vague | Too Specific | Just Right |
|-----------|--------------|------------|
| "Tests" | "Unit test for UserService.getUser()" | "Unit tests" |
| "Docs" | "README section 3.2.1" | "README" |
| "Cloud" | "AWS us-east-1 t2.micro EC2" | "AWS deployment" |

---

## Extraction Process

### Step-by-Step

1. **Read the entire markdown file**
2. **Identify potential criteria mentions**
3. **Check context around each mention**
4. **Validate using patterns above**
5. **Normalize the criterion name**
6. **Add to student's criteria list (if valid)**
7. **Track the source file**

### Example Extraction

**Markdown content:**
```markdown
## Features

Our project includes:
- User authentication with JWT
- Real-time notifications via WebSocket
- Dark mode support

## Testing

We have comprehensive unit tests covering 80% of the codebase.
Integration tests are planned for the next sprint.

## Deployment

TODO: Set up CI/CD pipeline
The app is currently deployed on Heroku.
```

**Extracted criteria:**
| Criterion | Valid? | Reason |
|-----------|--------|--------|
| User authentication | ✅ | "project includes" |
| Real-time notifications | ✅ | "project includes" |
| Dark mode | ✅ | "project includes" |
| Unit tests | ✅ | "We have...unit tests" |
| 80% test coverage | ✅ | Specific metric stated |
| Integration tests | ❌ | "planned for next sprint" = future |
| CI/CD pipeline | ❌ | "TODO" = not implemented |
| Heroku deployment | ✅ | "is currently deployed" |

---

## Edge Cases

### Partial Implementation

If something is partially done, use judgment:

- "Basic X implemented, advanced features pending" → Count "X (basic)"
- "X works but has bugs" → Count "X" (it exists)
- "X is 50% complete" → Don't count (not done)

### Third-Party Integrations

Count if the student integrated it:

- "Integrated Stripe for payments" → "Stripe integration"
- "Uses React" → "React" (only if notable for the assignment)
- "Built on top of Express" → Framework choice, may or may not count

### Screenshots/Evidence

If markdown includes images:

- Image of working feature → Validates the feature exists
- Image of diagram → "Architecture diagram" or similar
- Placeholder image → Don't count as evidence

### Links

If markdown includes links:

- Link to live demo → "Live deployment"
- Link to documentation → Validates docs exist
- Broken links → Note but still count if text claims it exists

---

## Code Verification Patterns

**CRITICAL:** Don't just trust markdown documentation - verify implementation by analyzing actual code repositories.

This section defines criteria that are VERIFIED through code analysis rather than relying solely on documentation claims. These verified criteria receive a "(verified)" suffix and provide ground truth validation.

### Why Code Verification is Needed

**The "README-Driven Development" Problem:**
- Students sometimes claim features they didn't implement
- Documentation can be aspirational rather than factual
- Marketing language ("Production ready!", "Enterprise-grade!") vs actual implementation
- Code analysis provides objective verification

### Three Types of Verification

Use the `code_analysis.py` module for automated verification:

#### 1. Git Repository Analysis (`analyze_git_repository`)

**Verified Criteria:**

| Criterion | Verification Method | Points | Category |
|-----------|-------------------|--------|----------|
| Git Commits 10+ (verified) | Count commits: `git rev-list --count HEAD` ≥ 10 | 2 | CodeQuality |
| Meaningful Commit Messages (verified) | Check for multi-word messages (not just "update", "fix") | 2 | CodeQuality |
| PROMPT_BOOK.md (verified) | Check for PROMPT_BOOK.md, PROMPTBOOK.md, docs/PROMPT_BOOK.md | 5 | Documentation |
| Branching Strategy (verified) | Check for multiple branches beyond main | 1 | DevOps |

**Why these matter:**
- **10+ commits**: Shows iterative development, not last-minute cramming
- **Meaningful messages**: Professional git hygiene ("Add user auth" not "update")
- **PROMPT_BOOK.md**: CRITICAL for AI-assisted development documentation (5 points!)
- **Branching**: Shows proper git workflow (feature branches, etc.)

#### 2. Security Scanning (`scan_for_secrets`)

**Verified Criteria:**

| Criterion | Verification Method | Points | Category |
|-----------|-------------------|--------|----------|
| No Hardcoded Secrets (verified) | Scan code files for API keys, tokens, passwords | 5 | Security |
| .env.example Exists (verified) | Check for .env.example, .env.template | 2 | DevOps |
| .gitignore Exists (verified) | Check for .gitignore file | 1 | DevOps |
| .gitignore Properly Configured (verified) | Verify excludes: .env, venv/, node_modules/, *.pyc | 2 | DevOps |

**Secret detection patterns:**
```python
secret_patterns = [
    r'api[_-]?key\s*=\s*["\'][\w\-]{20,}["\']',  # API keys
    r'sk-[a-zA-Z0-9]{20,}',                       # OpenAI keys
    r'ghp_[a-zA-Z0-9]{36,}',                      # GitHub tokens
    r'password\s*=\s*["\'][^"\']+["\']',          # Hardcoded passwords
    r'AKIA[0-9A-Z]{16}',                          # AWS access keys
]
```

**Why these matter:**
- **No hardcoded secrets**: CRITICAL security practice (5 points!)
- **.env.example**: Shows understanding of environment configuration
- **.gitignore**: Basic git hygiene
- **Proper .gitignore**: Excludes sensitive files, dependencies

#### 3. Code Quality Tools (`check_code_quality_tools`)

**Verified Criteria:**

| Tool Category | File Patterns | Criterion | Points |
|--------------|---------------|-----------|--------|
| **Linting** | .eslintrc.*, eslintConfig in package.json | ESLint Configuration (verified) | 2 |
|  | .pylintrc, pylintrc, pylint.cfg | Pylint Configuration (verified) | 2 |
|  | ruff.toml, .ruff.toml, pyproject.toml (ruff) | Ruff Linting (verified) | 2 |
|  | .flake8, setup.cfg (flake8) | Flake8 Configuration (verified) | 2 |
| **Formatting** | .prettierrc.*, prettier.config.* | Prettier Configuration (verified) | 2 |
|  | pyproject.toml (black), .black | Black Configuration (verified) | 2 |
| **Type Checking** | tsconfig.json | TypeScript Type Checking (verified) | 2 |
|  | mypy.ini, .mypy.ini, pyproject.toml (mypy) | MyPy Type Checking (verified) | 2 |
| **Pre-commit** | .pre-commit-config.yaml | Pre-commit Hooks (verified) | 2 |
| **Testing** | pytest.ini, setup.cfg (pytest) | Pytest Configuration (verified) | 2 |
|  | jest.config.js, package.json (jest) | Jest Configuration (verified) | 2 |

**Why these matter:**
- Shows professional code quality practices
- Automated enforcement of standards
- Indicates mature development workflow

### How Verified Criteria are Marked

**Suffix notation:**
- Documentation claim: "ESLint Configuration"
- Code-verified: "ESLint Configuration (verified)"

**Student comparison:**
- Student A: Claims "ESLint configured" in README (no .eslintrc file) = 0 points
- Student B: Has .eslintrc.json file = 2 points for "ESLint Configuration (verified)"

**Fair grading:**
Verified criteria ensure students who actually implemented tools get credit, while students who only claimed them in documentation don't.

### Integration with Markdown Extraction

**Workflow:**
1. Extract criteria from markdown documentation (existing process)
2. Run code verification analysis on repository
3. Add verified criteria with "(verified)" suffix
4. Combine both lists for final criteria graph

**Example:**
```python
# Student criteria after both steps
student_criteria = [
    "README",                                    # From markdown
    "Unit Tests",                                # From markdown
    "ESLint Configuration (verified)",           # From code analysis
    "Git Commits 10+ (verified)",                # From code analysis
    "No Hardcoded Secrets (verified)",           # From code analysis
    "PROMPT_BOOK.md (verified)",                 # From code analysis
]
```

### Error Handling

**Graceful degradation:**
- If git analysis fails (not a git repo): Skip gracefully, log warning
- If security scan fails (permissions): Log warning, continue
- If file access fails: Treat as "file not present"
- Never fail entire evaluation due to verification errors

**Performance:**
- Code analysis adds ~2-5 seconds per student
- Worth it for ±15 point accuracy improvement

### Expected Impact

**Before code verification (WorkSubmissions05):**
- Mean difference: -15.0 points (severe under-grading)
- Students with implementation but poor docs: Under-graded

**After code verification (expected):**
- Mean difference: ±2 points (excellent accuracy)
- Catches "README-driven development"
- Rewards actual implementation over marketing claims

---

## Discovered Patterns

This section is dynamically updated as new patterns are discovered during evaluations.
When you find new positive/negative indicators or criteria types while analyzing student
projects, append them here using the format below.

---

### Template for New Discoveries

```markdown
### [YYYY-MM-DD] - Discovered from [student_folder_name]

**New positive indicators:**
- "phrase found in markdown" → Indicates: [what it means]

**New negative indicators:**
- "phrase found in markdown" → Indicates: [what it means]

**New criteria types:**
- [Criterion name]: [description of what this criterion represents]

**New normalization rules:**
- [variation1], [variation2] → [Canonical Name]
```

---

### Instructions for Adding Patterns

1. **When to add**: After analyzing each student (especially early ones)
2. **What to add**: Any phrasing not already covered above
3. **Format**: Use the template above
4. **Be specific**: Include the exact phrase found
5. **Add context**: Explain what the phrase indicates

---

<!-- DISCOVERED PATTERNS START - Append new discoveries below this line -->

### 2025-12-17 - Discovered from WorkSubmissions01 Sample Evaluation

**New positive indicators:**
- "~X% code coverage" or "X% coverage" → Indicates: Test coverage metric achieved
- "X+ tests" or "X tests" → Indicates: Specific number of tests implemented
- "Works great on all screen sizes" → Indicates: Responsive design implemented
- "100% Local" or "100% Private" → Indicates: Privacy-focused implementation
- "Production Ready" or "Production-ready" → Indicates: Code quality claim
- "Comprehensive tests" → Indicates: Thorough testing implemented

**New negative indicators:**
- None identified in this sample batch

**New criteria types:**
- macOS Native App: Student created a native macOS application wrapper
- Automated Setup Scripts: Shell scripts for automated installation/setup
- User Profiles: Customizable user settings/avatars
- Multi-Session Support: Multiple conversation/session management
- Export Functionality: Ability to export data in multiple formats (TXT, MD, JSON)
- Uninstall Instructions: Documentation for removing/cleaning up the software
- Environment Variables Documentation: Configuration via environment variables
- Keyboard Shortcuts Documentation: List of supported keyboard shortcuts
- Test Coverage Metrics: Specific percentage of code covered by tests

**New normalization rules:**
- "unit test", "unit tests", "unit testing" → Unit Tests
- "e2e", "E2E", "end-to-end", "end to end" → E2E Tests
- "dark mode", "light mode", "dark/light theme", "theme toggle" → Dark/Light Theme
- "responsive", "mobile-friendly", "works on all devices" → Responsive Design
- "~93% coverage", "80% coverage", "test coverage" → Test Coverage Metrics
- "PRD", "product requirements", "Product Requirements Document" → PRD Document
- "troubleshooting", "common problems", "FAQ" → Troubleshooting Guide
