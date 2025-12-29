# Criteria Categories

This document defines the broad categories for grouping extracted criteria.

## Category Definitions

### Documentation

Project documentation and guides that help users understand the project.

**Keywords to match:**
- readme
- api docs, api documentation
- user guide, usage guide
- changelog, change log
- contributing, contribution guide
- license
- installation guide, setup guide
- getting started
- faq, frequently asked questions
- wiki
- manual
- reference docs

**Example criteria:**
- "Comprehensive README"
- "API documentation with examples"
- "Step-by-step installation guide"

---

### Planning

Planning, design, and requirements documentation showing project forethought and analysis.

**Keywords to match:**
- prd, product requirements
- architecture, architectural design
- design document, design doc
- technical spec, technical specification
- roadmap, project roadmap
- milestones
- requirements, requirements document, functional requirements, non-functional requirements
- system design
- database schema, db schema
- wireframes
- mockups (planning context)
- user stories
- use cases, use case
- problem statement, problem
- solution overview, proposed solution
- project goals, objectives
- success metrics, kpis, evaluation criteria
- assumptions, assumptions documentation
- constraints, limitations, scope
- design decisions, design rationale
- trade-offs, alternatives considered
- technology selection, technology justification
- user personas, target users
- user flow, user journey
- timeline, schedule, project plan

**Example criteria:**
- "PRD document"
- "Problem Statement"
- "Solution Overview"
- "Use Case Documentation"
- "Functional Requirements"
- "Success Metrics"
- "Design Decision Documentation"
- "Assumptions Documentation"
- "Project Timeline"

---

### Testing

Testing and quality assurance efforts.

**Keywords to match:**
- unit test, unit tests, unit testing
- integration test, integration tests
- e2e test, e2e tests, end-to-end
- test coverage, code coverage
- pytest, jest, mocha, junit
- testing framework
- test suite
- automated tests, automated testing
- manual testing
- regression tests
- smoke tests
- load testing, performance testing
- test cases
- tdd, test-driven

**Example criteria:**
- "Unit tests with pytest"
- "85% test coverage"
- "Integration tests for API"

---

### DevOps

DevOps, deployment, and infrastructure elements.

**Keywords to match:**
- ci/cd, ci cd, continuous integration, continuous deployment
- github actions, gitlab ci, jenkins
- docker, dockerfile, containerization
- kubernetes, k8s
- deployment, deploy script
- aws, azure, gcp, cloud
- terraform, infrastructure as code
- monitoring, logging
- nginx, apache
- load balancer
- ssl, https
- environment variables, env config
- build pipeline
- release automation

**Example criteria:**
- "CI/CD with GitHub Actions"
- "Docker containerization"
- "Deployed to AWS"

---

### Research

Research, analysis, and data exploration work.

**Keywords to match:**
- research, research findings
- analysis, data analysis
- jupyter notebook, notebook
- data exploration
- experiment, experimentation
- hypothesis
- findings, results
- literature review
- benchmarking, benchmark
- comparison study
- survey, user research
- insights
- statistical analysis
- machine learning experiments
- model evaluation

**Example criteria:**
- "Data analysis in Jupyter notebooks"
- "Benchmark comparison with competitors"
- "User research findings"

---

### Visuals

Visual documentation and demonstration materials.

**Keywords to match:**
- screenshot, screenshots
- diagram, diagrams
- flowchart, flow chart
- chart, charts, graph, graphs
- demo video, video demo
- gif, animated gif
- mockup (visual context)
- wireframe (visual context)
- ui preview
- before/after
- architecture diagram (visual)
- sequence diagram
- erd, entity relationship diagram
- class diagram
- infographic

**Example criteria:**
- "Screenshots of the application"
- "Architecture diagram"
- "Demo video walkthrough"

---

### CodeQuality

Code quality, standards, and maintainability practices.

**Keywords to match:**
- linting, linter, eslint, pylint, ruff, flake8
- prettier, code formatting, black, autopep8, yapf
- type checking, typescript, mypy, pyright, pyre
- code review, peer review
- pre-commit, git hooks, husky, lint-staged
- refactoring
- clean code
- solid principles
- design patterns
- code style, style guide, coding standards
- pep 8, pep8, airbnb style, google style
- documentation strings, docstrings
- comments, code comments
- static analysis, sonarqube, sonarcloud
- code complexity
- technical debt
- quality gates, quality checks
- project setup, setup.py, pyproject.toml, package.json
- dependency management, requirements
- environment management, venv, virtual environment

**Example criteria:**
- "ESLint Configuration"
- "Pylint Configuration"
- "TypeScript Type Checking"
- "Pre-commit Hooks"
- "Code Style Guide"
- "PEP8 Compliance"
- "Prettier Formatting"
- "Black Formatting"
- "Code Review Process"
- "Quality Gates"
- "Project Setup Configuration"

---

### Business

Business, market, commercial, and risk considerations.

**Keywords to match:**
- cost analysis, cost breakdown, budget
- roi, return on investment
- market research, market analysis
- user personas, customer personas
- business case, business model
- pricing, pricing strategy
- monetization
- competitive analysis, competitor comparison
- swot analysis
- value proposition
- target audience
- stakeholder analysis
- budgeting
- revenue model
- go-to-market
- risk analysis, risk assessment, risks
- risk mitigation

**Example criteria:**
- "Cost Analysis"
- "ROI Analysis"
- "Market Research"
- "Competitive Analysis"
- "Risk Analysis"
- "Business Model"

---

## Matching Rules

1. **Case-insensitive matching** - "README" matches "readme"
2. **Partial matching** - "unit test" matches "unit tests" and "unit testing"
3. **First match wins** - If a criterion could match multiple categories, use the first match
4. **Context matters** - "mockup" in planning context vs visual context

## Uncategorized Criteria

If a criterion doesn't match any category:
1. Add to `flagged_criteria.md`
2. Still include in student scores
3. Mark as "Uncategorized" in reports
4. User can manually categorize later

## Extending Categories

To add new categories or keywords:
1. Add a new section following the format above
2. Include clear keywords to match
3. Provide example criteria
4. Update SKILL.md if needed
