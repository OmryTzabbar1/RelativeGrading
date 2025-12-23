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

## What to Extract

### Features & Functionality

Look for mentions of implemented features:

**Positive indicators (case-insensitive matching):**
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

**Table of Contents / Index patterns:**
- If a README/index file lists other .md files (e.g., `[PRD.md](PRD.md)`), credit those as existing
- Section headers with links indicate implemented documentation

**Examples:**
- "We built a real-time chat feature" → "Real-time chat"
- "The project includes user authentication" → "User authentication"
- "Supports dark mode" → "Dark mode"
- "This project includes comprehensive unit tests" → "Unit tests"
- "Total tests: ~75 test cases" → "Unit tests" + "Test coverage metrics"
- "Complete guide for..." → Relevant documentation criterion

### Documentation Elements

Look for documentation mentions:

- "See the README for..." → "README"
- "API documentation is in /docs" → "API documentation"
- "Architecture described in ARCHITECTURE.md" → "Architecture document"

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
"Built with X"
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
- "Built with [X]" → Indicates: Technology/framework is used in the project
- "Powered by [X]" → Indicates: Underlying technology/service is integrated
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
