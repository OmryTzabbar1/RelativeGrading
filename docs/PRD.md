# Product Requirements Document (PRD)
# Student Project Evaluator

**Version:** 1.0
**Date:** 2024-12-15
**Status:** Draft
**Author:** Development Team

---

## 1. Project Overview

### 1.1 Context and Background

Academic institutions require efficient, fair, and consistent methods for evaluating student programming assignments. Traditional
grading approaches fall into two categories:

1. **Strict Criteria Checking**: Automated tools that verify the presence of specific elements (functions, files, features) but
   fail to assess whether the project actually addresses the assignment requirements or demonstrates quality implementation
2. **Manual Grading**: Time-intensive instructor review that provides nuanced assessment but is difficult to scale and maintain
   consistency across large classes

The **Student Project Evaluator** bridges this gap by providing a **comparative evaluation system** that assesses both assignment
relevance and relative quality, complementing existing strict-criteria tools.

### 1.2 Problem Statement

Instructors using strict-criteria grading tools face three critical limitations:

1. **No Relevance Assessment**: Tools cannot determine if a project addresses the actual assignment requirements or is off-topic
2. **No Quality Differentiation**: Cannot distinguish between a minimal implementation and an exceptional one that exceeds
   requirements
3. **Incomplete Performance Picture**: Missing the relative quality dimension makes it impossible to apply nuanced weighting to
   final grades or identify truly outstanding work

This results in incomplete student evaluations and prevents instructors from rewarding students who demonstrate mastery beyond
basic requirement fulfillment.

---

## 2. Market Analysis

### 2.1 Competitive Landscape

| Tool Type | Examples | Strengths | Weaknesses |
|-----------|----------|-----------|------------|
| **Autograders** | Gradescope, CodeHS | Fast, scalable, objective | No qualitative assessment, can't judge relevance |
| **Static Analysis** | SonarQube, ESLint | Code quality metrics | No assignment-specific context, no comparison |
| **Manual Review** | Rubrics, peer review | Nuanced, contextual | Time-intensive, consistency issues |
| **LMS Grading** | Canvas, Moodle | Integrated workflow | No code analysis capabilities |

**Strategic Positioning**: Student Project Evaluator uniquely combines AI-powered code analysis with comparative grading to
provide the quality assessment dimension missing from automated tools, while maintaining the efficiency advantage over manual
review.

### 2.2 Innovation

- **Dynamic Baseline**: Automatically updates comparison standard as better projects are discovered
- **Assignment-Aware**: Uses provided assignment description to assess relevance
- **AI-Powered Analysis**: Leverages Claude Code's natural language understanding for qualitative assessment
- **Complementary Design**: Works alongside existing tools rather than replacing them

---

## 3. Target Audience

### 3.1 Stakeholders

| Stakeholder | Role | Interest | Influence |
|-------------|------|----------|-----------|
| **Course Instructor** | Primary user | Efficient grading, fair assessment, insight into class performance | High - defines requirements, validates outputs |
| **Teaching Assistants** | Secondary users | Streamlined grading workflow, consistent standards | Medium - use tool as configured by instructor |
| **Students** | Evaluated subjects | Fair grading, transparency | Low - indirect recipients of tool outputs |
| **Department Admin** | Oversight | Quality assurance, academic integrity | Medium - may review grading methodologies |
| **Future Educators** | Potential adopters | Reusable grading infrastructure | Low - will use in future terms |

### 3.2 Primary User Persona

**Name**: Dr. Sarah Chen
**Role**: Assistant Professor, Computer Science
**Context**:
- Teaches 2-3 programming courses per semester (30-50 students each)
- Already uses automated strict-criteria checker for basic compliance
- Spends 15-20 hours manually grading assignments to assess quality
- Comfortable with command-line tools and Claude Code

**Pain Points**:
- Cannot scale manual quality assessment beyond 30 students
- Difficult to maintain consistency when reviewing 50+ projects
- No systematic way to identify standout projects for recognition
- Relative quality scores needed for weighted grading calculations

**Success Scenario**: Dr. Chen processes 30 student projects in 25 minutes, obtaining relative quality scores that align with her
intuition. She uses these scores to weight final grades and identifies the top 3 projects for bonus recognition.

---

## 4. Project Goals

### 4.1 Objectives

| Goal | Description | Success Metric |
|------|-------------|----------------|
| **Efficiency** | Process 30 students in under 30 minutes | Throughput: ≥1 student/minute |
| **Accuracy** | Relative scores match instructor intuition | Correlation: ≥0.85 with manual grades |
| **Reliability** | Error-free batch processing | Zero crashes during evaluation runs |
| **Utility** | Enable weighted grading calculations | CSV export compatible with gradebook systems |
| **Transparency** | Explainable grade assignments | Detailed reasoning for each evaluation |

### 4.2 Key Performance Indicators (KPIs)

| KPI | Target | Measurement Method |
|-----|--------|-------------------|
| Processing Time | ≤30 min for 30 students | Timestamp comparison (start to completion) |
| Grade Correlation | ≥0.85 Pearson correlation | Compare tool grades vs. manual instructor grades |
| Error Rate | 0% crashes | Count unhandled exceptions during batch runs |
| Adoption Rate | 3+ instructors by end of term | User registration tracking |
| CSV Compatibility | 100% gradebook import success | Test with Canvas, Moodle, Excel |

---

## 5. Acceptance Criteria

### 5.1 MVP Acceptance

The MVP is accepted when:

1. ✅ Tool successfully processes 30 git repositories in ≤30 minutes without errors
2. ✅ Generates valid CSV file importable to Canvas/Moodle
3. ✅ Baseline automatically updates when superior project is encountered
4. ✅ Markdown report includes summary statistics and individual evaluations
5. ✅ Assignment config YAML is generated after baseline evaluation
6. ✅ Instructor can provide assignment description, master folder path, and baseline info in one prompt

### 5.2 Quality Gates

| Gate | Criteria | Validation Method |
|------|----------|-------------------|
| **Functional Correctness** | All P0 features working | Manual testing on real student projects |
| **Performance** | 30 students in 30 minutes | Timed execution with 30 sample repos |
| **Accuracy** | Grades correlate with manual assessment | Instructor reviews 10 random evaluations |
| **Usability** | Instructor can use without documentation | Observe first-time user session |
| **Robustness** | Handles edge cases gracefully | Test with empty repos, missing files, large repos |

---

## 6. Functional Requirements

### 6.1 Must-Have Features (P0)

| Feature ID | Feature | User Story | Acceptance Criteria |
|------------|---------|------------|---------------------|
| **P0.1** | Comparative Evaluation | As an instructor, I want to compare student projects against the current best submission so that grades reflect relative quality | Each student graded against current baseline; baseline updates when grade > baseline_grade; update notification displayed |
| **P0.2** | Assignment Relevance | As an instructor, I want to assess how well projects address the assignment requirements so that I can identify off-topic work | Tool analyzes project against provided assignment description; relevance score (0-50 points) included in grade |
| **P0.3** | Dynamic Baseline Updates | As an instructor, I want the baseline to auto-update when a superior project is found so that comparisons use highest standard | When evaluated_grade > baseline_grade: update baseline student/grade/features; display "✓ New baseline: [student] - [grade]/100" |
| **P0.4** | Batch Processing | As an instructor, I want to process students in batches of 5 so that I can manage context and review progress | Auto-process 5 students, continue to next batch; display "Evaluating student X/30..." |
| **P0.5** | CSV Export | As an instructor, I want grades exported to CSV so that I can import into my gradebook system | CSV includes: student_name, student_id, grade, rank, notes, metadata (team_name if present); sorted by rank descending |
| **P0.6** | Markdown Report | As an instructor, I want a comprehensive report so that I can review evaluations and statistics | Report includes: summary stats (avg, median, high, low, std dev), individual evaluations with reasoning, students needing manual review |
| **P0.7** | Config Generation | As an instructor, I want assignment config generated after baseline evaluation so that I can customize future runs | After baseline eval: create assignment-config.yml with grading_weights, focus_files, project_type, criteria |
| **P0.8** | Auto Folder Detection | As an instructor, I want the tool to auto-detect student folders so that I don't manually list them | Scan master folder for subdirectories; list all folders except baseline; confirm count with user |
| **P0.9** | Git Repository Reading | As an instructor, I want to evaluate locally cloned git repositories so that I can grade student code | Read files from student folders using Claude Read/Glob/Grep; focus on key files (README, src/, configs) |
| **P0.10** | Error Handling | As an instructor, I want the tool to skip problematic submissions and continue so that one error doesn't halt grading | On error: skip student, log note for manual review, continue to next; display error count in summary |

### 6.2 Should-Have Features (P1)

| Feature ID | Feature | User Story | Acceptance Criteria |
|------------|---------|------------|---------------------|
| **P1.1** | Flexible Metadata | As an instructor, I want the tool to capture team names and other metadata so that I can grade group projects | Auto-detect additional fields (team_name, group_id, etc.) from README or folder; include in CSV |
| **P1.2** | Overwrite Protection | As an instructor, I want to be prompted before overwriting existing files so that I don't lose previous evaluations | Check for existing grades.csv and evaluation_summary.md; if found, ask "Overwrite? (y/n)" |
| **P1.3** | Manual Review Tracking | As an instructor, I want clear notes on which students need manual review so that I can follow up efficiently | Separate section in markdown: "Students Requiring Manual Review" with reasons (error, missing files, etc.) |

### 6.3 Nice-to-Have Features (P2)

| Feature ID | Feature | User Story | Notes |
|------------|---------|------------|-------|
| **P2.1** | Identical Detection | As an instructor, I want to detect identical submissions for academic integrity | Deferred to v1.1 - skip identical projects, note in summary |
| **P2.2** | PDF/ZIP Support | As an instructor, I want to evaluate non-code submissions so that I can use for all assignment types | Deferred to v1.1 - MVP focuses on git repos only |
| **P2.3** | LMS Integration | As an instructor, I want to export directly to Canvas/Moodle so that I skip manual entry | Deferred to v2.0 - API integration for production version |
| **P2.4** | Custom Rubrics | As an instructor, I want to define custom evaluation criteria so that I can adapt to different courses | Deferred to v1.2 - template system for rubrics |

---

## 7. Use Cases

### 7.1 Use Case 1: Grading a Web Development Assignment

**Actor**: Course Instructor (Dr. Chen)
**Preconditions**:
- 30 student folders exist in `/Assignments/WebDev_A1/` directory
- Each folder contains a git repository (already cloned)
- Assignment description available as text
- Claude Code installed and running

**Main Flow**:
1. Instructor invokes: "I need to grade student projects"
2. Tool prompts for inputs (assignment description, master folder path, baseline student + grade)
3. Instructor provides:
   - Assignment: "Create a todo list web app with CRUD operations, LocalStorage, responsive design"
   - Master folder: `/Assignments/WebDev_A1/`
   - Baseline: `student_alice`, grade 85, folder `/Assignments/WebDev_A1/student_alice/`
4. Tool reads baseline project, analyzes features, displays: "✓ Baseline established: student_alice - 85/100"
5. Tool generates `assignment-config.yml` with observed criteria
6. Tool auto-detects 29 remaining student folders, confirms: "Found 29 students. Beginning evaluation..."
7. For each student (batches of 5):
   - Reads project files (README, src/, package.json)
   - Compares to current baseline (relevance + functionality)
   - Assigns relative grade
   - If grade > baseline: updates baseline, displays notification
   - Displays: "Evaluating student 12/30..."
8. After all students: generates `grades.csv` and `evaluation_summary.md`
9. Tool displays completion summary with file paths and quick stats

**Postconditions**:
- CSV file created at `/Assignments/WebDev_A1/grades.csv`
- Markdown report created at `/Assignments/WebDev_A1/evaluation_summary.md`
- Config file created at `/Assignments/WebDev_A1/assignment-config.yml`
- Instructor has relative grades ready for weighted grading calculation

**Alternative Flows**:
- **A1**: Student folder is empty → Skip student, log "Empty folder" in manual review section
- **A2**: README missing → Continue evaluation based on code analysis, note missing README in evaluation
- **A3**: Project won't compile → Skip student, log "Build failure - requires manual review"

### 7.2 Use Case 2: Re-running Evaluation with Adjusted Config

**Actor**: Course Instructor
**Preconditions**:
- Initial evaluation completed
- `assignment-config.yml` exists
- Instructor wants to adjust grading weights

**Main Flow**:
1. Instructor edits `assignment-config.yml`:
   ```yaml
   grading_weights:
     assignment_relevance: 40  # was 50
     functionality: 60          # was 50
   ```
2. Instructor invokes: "Re-grade using updated config"
3. Tool detects existing `grades.csv`, prompts: "Overwrite existing grades? (y/n)"
4. Instructor confirms: "y"
5. Tool re-evaluates all students using new weights
6. Generates updated CSV and markdown report

**Postconditions**:
- Updated `grades.csv` with new weights applied
- Updated `evaluation_summary.md` with note about config changes

---

## 8. Non-Functional Requirements

### 8.1 Performance Requirements

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| **Throughput** | Process 1 student per minute (average) | 30 students in ≤30 minutes |
| **Latency** | Display progress updates every 30 seconds | User sees activity, not frozen terminal |
| **Scalability** | Handle up to 50 repositories | Performance guarantee for ≤50 students |
| **Repository Size** | Optimize for MB-sized repos | Warn if repo >100MB, may take longer |
| **Complex Projects** | 2-3 minutes for large codebases acceptable | User warned about extended processing time |

### 8.2 Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| **Data Privacy** | Grade files contain sensitive student data - save to local filesystem only, never cloud |
| **Access Control** | Instructor must have read access to student folders; tool inherits OS permissions |
| **API Key Security** | If using Claude API: load keys from environment variables, never hardcode |
| **Academic Integrity** | Notes about identical submissions must be confidential, not shared publicly |

### 8.3 Availability Requirements

| Requirement | Target |
|-------------|--------|
| **Uptime** | Not applicable (local CLI tool, no server) |
| **Error Recovery** | If error during student evaluation: skip student, continue batch processing |
| **Data Persistence** | CSV and markdown reports must be saved before tool exits |

### 8.4 Scalability Requirements

- **Horizontal Scaling**: Not applicable for MVP (single-user CLI tool)
- **Vertical Scaling**: Memory usage should remain <2GB for 50 repositories
- **Batch Size**: Process 5 students at a time to manage Claude Code context limits

### 8.5 Usability Requirements

- **Learnability**: First-time instructor should complete grading session within 5 minutes (including learning curve)
- **Error Prevention**: Clear prompts for required inputs; validate folder paths before starting
- **Error Messages**: User-friendly messages (e.g., "Folder not found: /path/" instead of "FileNotFoundError")
- **Accessibility**: CLI output should be screen-reader compatible (plain text, no ASCII art required for function)

### 8.6 Compatibility Requirements

| Requirement | Details |
|-------------|---------|
| **Operating Systems** | Windows, macOS, Linux (any OS with Claude Code installed) |
| **Claude Code Version** | Compatible with Claude Code v1.0+ |
| **Python Version** | Python 3.8+ for helper scripts |
| **Git Version** | Git 2.0+ for repository operations |

---

## 9. Assumptions

1. **Git repositories are pre-cloned**: Tool does not handle cloning from GitHub/GitLab
2. **One student = one folder**: No shared folders (except group projects where all members get same grade)
3. **Baseline grade accuracy**: Instructor provides accurate manual baseline grade for calibration
4. **Standard folder structure**: Student folders are immediate subdirectories of master folder
5. **Claude Code availability**: Tool runs within Claude Code environment (not standalone Python script)
6. **File system access**: Instructor has read permissions for all student folders

---

## 10. Dependencies

### 10.1 External Systems

| Dependency | Type | Risk Level | Mitigation |
|------------|------|------------|------------|
| **Claude Code** | Platform | High - tool won't work without it | Hard dependency, document in README |
| **Python 3.x** | Runtime | Medium - helper scripts require it | Check version at tool start, provide error if <3.8 |
| **Git** | Tool | Low - only for metadata extraction | Optional, skip git operations if not available |
| **File System** | Storage | Low - standard OS capability | Validate paths before writing files |

### 10.2 Third-Party Libraries

**Python Dependencies**:
- `pyyaml` - YAML config parsing
- `csv` (stdlib) - CSV generation
- Standard library only for MVP (minimize dependencies)

---

## 11. Constraints

### 11.1 Technical Constraints

- **Context Limits**: Claude Code has token limits; batch processing (5 students) required to manage context
- **File Reading**: Large repositories (1000+ files) may exceed reasonable processing time
- **API Rate Limits**: If using Claude API, must respect rate limits (batch processing helps)

### 11.2 Organizational Constraints

- **Privacy Regulations**: Must comply with FERPA (student grade privacy in US) or equivalent regulations
- **Academic Policies**: Grading methodology must be approved by department/university
- **Timeline**: MVP must be functional within 1-2 weeks for current semester use

### 11.3 Resource Constraints

- **Development Time**: 1-2 weeks for proof of concept
- **Testing Resources**: Sample student projects available for testing
- **Documentation**: Must be sufficient for other instructors to use tool independently

---

## 12. Out-of-Scope

### 12.1 Explicitly Excluded from MVP

- **Identical submission detection**: Deferred to v1.1 (requires similarity algorithms)
- **PDF/ZIP submission support**: Deferred to v1.1 (git repos only for MVP)
- **Comprehensive markdown reports**: MVP has basic stats only, detailed reports in v1.1
- **LMS integration**: Deferred to v2.0 (API integration for production version)
- **Real-time AI feedback**: Deferred to v2.0 (generate student-facing feedback comments)
- **Web dashboard**: Deferred to v2.0 (CLI only for MVP)
- **Multi-instructor support**: Deferred to v2.0 (single-user tool for MVP)
- **Historical grade tracking**: Deferred to v2.0 (no database, each run is independent)

### 12.2 Will Never Be In Scope

- **Automated cloning from GitHub**: Instructors must clone repos manually (security/privacy reasons)
- **Direct grade entry to LMS**: Export CSV only, manual import to gradebook (avoid LMS API complexities)
- **Student-facing interface**: Tool is instructor-only

---

## 13. Timeline & Milestones

### 13.1 Development Phases

| Phase | Duration | Deliverables | Success Criteria |
|-------|----------|--------------|------------------|
| **Phase 1: Setup** | 1-2 days | Project structure, helper scripts, config templates | Scripts can scan folders and detect project types |
| **Phase 2: Core Logic** | 3-4 days | SKILL.md, baseline evaluation, comparative grading | Can evaluate 5 students and assign grades |
| **Phase 3: Batch Processing** | 2-3 days | Automatic batching, progress indicators, baseline updates | Can process 30 students end-to-end |
| **Phase 4: Outputs** | 1-2 days | CSV generation, markdown report, config YAML | Outputs match specification |
| **Phase 5: Testing** | 2-3 days | Manual testing, sample data, edge case handling | Passes all acceptance criteria |
| **Phase 6: Documentation** | 1 day | README, usage examples, troubleshooting | Other instructors can use without support |

**Total Duration**: 10-15 days (1.5-2 weeks)

### 13.2 Milestones

| Milestone | Date (Relative) | Criteria |
|-----------|-----------------|----------|
| **M1: Baseline Evaluation Works** | Day 4 | Can analyze one student project and generate config |
| **M2: Comparative Grading Works** | Day 7 | Can compare students and update baseline |
| **M3: Full Batch Processing** | Day 10 | Can process 30 students end-to-end |
| **M4: MVP Complete** | Day 12 | All P0 features working, tested with real data |
| **M5: Documentation Complete** | Day 14 | README, examples ready for other users |

---

## 14. Checkpoint Reviews

### 14.1 Review Schedule

| Checkpoint | Timing | Attendees | Focus |
|------------|--------|-----------|-------|
| **Kickoff Review** | Day 0 | Instructor, Developer | Confirm requirements understanding |
| **Design Review** | Day 3 | Instructor, Developer | Validate architecture and approach |
| **Midpoint Review** | Day 7 | Instructor, Developer | Demo baseline + comparative grading |
| **Pre-release Review** | Day 12 | Instructor, Developer, Test Users | Validate MVP against acceptance criteria |
| **Post-release Review** | Day 21 | Instructor, Early Adopters | Collect feedback for v1.1 |

### 14.2 Success Metrics Review

**Weekly Check-ins**:
- Review KPI progress (processing time, accuracy)
- Test on real student projects
- Adjust grading weights if needed

---

## 15. Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| **Claude context limits** | High | Medium | Batch processing (5 students), focus on key files only |
| **Inconsistent grading** | High | Medium | Use assignment-config.yml for standardization, fixed baseline |
| **Large repositories** | Medium | Medium | Set focus_files in config, warn if >100MB |
| **Missing dependencies** | Medium | Low | Check Python/Git at startup, clear error messages |
| **Privacy concerns** | High | Low | Save files locally only, document FERPA compliance |

---

## Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-12-15 | Development Team | Initial PRD for MVP |

---

**End of Product Requirements Document**
