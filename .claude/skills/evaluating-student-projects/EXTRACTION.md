# Criteria Extraction Rules

This document defines how to extract criteria from markdown files and validate their context.

## Extraction Principles

1. **Be granular** - Extract specific items, not broad topics
2. **Validate context** - Only count what's actually implemented
3. **Normalize names** - Keep criterion names consistent
4. **Track sources** - Note which file each criterion came from

## What to Extract

### Features & Functionality

Look for mentions of implemented features:

**Positive indicators:**
- "We built..."
- "The project includes..."
- "Features:"
- "Implemented..."
- "Created..."
- "Developed..."
- "Added..."
- "Supports..."
- "Provides..."

**Examples:**
- "We built a real-time chat feature" → "Real-time chat"
- "The project includes user authentication" → "User authentication"
- "Supports dark mode" → "Dark mode"

### Documentation Elements

Look for documentation mentions:

- "See the README for..." → "README"
- "API documentation is in /docs" → "API documentation"
- "Architecture described in ARCHITECTURE.md" → "Architecture document"

### Testing

Look for testing mentions:

- "Unit tests in /tests" → "Unit tests"
- "85% code coverage" → "Test coverage (85%)"
- "Integration tests for API endpoints" → "Integration tests"
- "E2E tests with Playwright" → "E2E tests"

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
