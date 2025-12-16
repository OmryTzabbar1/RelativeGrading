# Architecture and Technical Planning
# Student Project Evaluator - Sliding Window v2.0

**Version:** 2.0
**Date:** 2025-12-16
**Status:** Active

---

## 1. System Architecture

### 1.1 Overview

The Student Project Evaluator v2.0 uses a **two-phase sliding window architecture**:

**Phase 1: Criteria Discovery**
- Analyze students in overlapping windows of 3
- Build comprehensive criteria organically
- Track what each student adds to criteria

**Phase 2: Final Evaluation**
- Evaluate ALL students against complete discovered criteria
- Assign relative grades (best = 100, others scaled)
- Generate outputs

### 1.2 High-Level Architecture

```
User Input → Phase 1: Sliding Window Discovery → Phase 2: Final Evaluation → Outputs
    ↓                 ↓                                ↓                        ↓
Master Folder    Window [1,2,3]                  Discovered Criteria      CSV + Report
                 Window [2,3,4]                   Score All Students       + Criteria YAML
                 ...                              Relative Grading
                 Window [N-2,N-1,N]
                 → Complete Criteria
```

### 1.3 Core Principles

1. **Organic Criteria Discovery**: Criteria emerges from actual student work, not predetermined rubrics
2. **Fairness Through Completeness**: All students judged by same complete criteria
3. **Sliding Window Continuity**: Overlapping windows ensure no features are missed
4. **Relative Grading**: Only best student gets 100, others scaled proportionally

---

## 2. Detailed Architecture

### 2.1 Phase 1: Sliding Window Discovery

**Input**: List of N student folders

**Process**:
```python
criteria = {}  # Start with empty criteria
students = [1, 2, 3, ..., N]
window_size = 3

for i in range(0, N - window_size + 1):
    window = students[i:i+window_size]

    # Analyze window
    for student in window:
        features = analyze_project(student)

        # Update criteria with new features
        criteria = merge_criteria(criteria, features)

        # Log new additions
        if has_new_features(features, criteria):
            log(f"Student {student} added: {new_features}")

# Save discovered criteria
save_criteria_yaml(criteria)
```

**Output**: `discovered_criteria.yml` with all quality dimensions

**Example Criteria Structure**:
```yaml
criteria:
  documentation:
    readme:
      present: true
      min_lines: 200
      excellent_lines: 700
    prd:
      present: in 28/35 students
      weight: 5
    architecture:
      present: in 18/35 students
      weight: 10
    prompt_book:
      present: in 12/35 students
      weight: 8

  testing:
    test_files:
      min: 0
      excellent: 10+
      present_in: 25/35 students

  graphics:
    images:
      min: 1
      excellent: 20+
      present_in: 30/35 students

  research:
    notebooks:
      present_in: 8/35 students
      weight: 10
    analysis_docs:
      present_in: 5/35 students
      weight: 10
```

### 2.2 Phase 2: Final Evaluation

**Input**:
- All N student folders
- `discovered_criteria.yml`

**Process**:
```python
criteria = load_criteria_yaml()
student_scores = []

for student in all_students:
    scores = {}

    # Score against each discovered dimension
    for dimension in criteria:
        score = calculate_score(student, dimension, criteria)
        scores[dimension] = score

    # Calculate composite quality score
    quality_score = sum(scores.values())
    student_scores.append({
        'student': student,
        'quality_score': quality_score,
        'dimension_scores': scores
    })

# Find best student
best = max(student_scores, key=lambda x: x['quality_score'])
best_score = best['quality_score']

# Assign relative grades
for student in student_scores:
    if student == best:
        student['grade'] = 100
    else:
        # Scale relative to best
        percent_of_best = student['quality_score'] / best_score
        student['grade'] = calculate_grade_from_percent(percent_of_best)
```

**Output**:
- `grades.csv`: Student, Grade, Rank, [Dimension Scores]
- `evaluation_report.md`: Detailed analysis

---

## 3. Data Structures

### 3.1 Discovered Criteria Object

```python
class DiscoveredCriteria:
    def __init__(self):
        self.dimensions = {}
        self.evolution_log = []

    def add_dimension(self, name: str, properties: dict, discovered_by: str):
        """Add a new quality dimension."""
        if name not in self.dimensions:
            self.dimensions[name] = properties
            self.evolution_log.append({
                'student': discovered_by,
                'dimension': name,
                'properties': properties
            })

    def update_dimension(self, name: str, new_properties: dict):
        """Update existing dimension with new information."""
        if name in self.dimensions:
            self.dimensions[name].update(new_properties)

    def to_yaml(self) -> str:
        """Export criteria to YAML format."""
        return yaml.dump({
            'criteria': self.dimensions,
            'evolution': self.evolution_log
        })
```

### 3.2 Student Evaluation Object

```python
class StudentEvaluation:
    def __init__(self, student_name: str, student_path: str):
        self.student_name = student_name
        self.student_path = student_path
        self.dimension_scores = {}
        self.quality_score = 0
        self.grade = 0
        self.rank = 0

    def calculate_quality_score(self, criteria: DiscoveredCriteria):
        """Calculate composite quality score across all dimensions."""
        for dimension_name, dimension_criteria in criteria.dimensions.items():
            score = self._score_dimension(dimension_name, dimension_criteria)
            self.dimension_scores[dimension_name] = score

        self.quality_score = sum(self.dimension_scores.values())
        return self.quality_score

    def _score_dimension(self, name: str, criteria: dict) -> float:
        """Score a single dimension."""
        # Implementation depends on dimension type
        pass
```

---

## 4. Component Design

### 4.1 Module: `sliding_window_analyzer.py`

**Purpose**: Analyze students in overlapping windows

```python
def analyze_sliding_windows(student_folders: List[str], window_size: int = 3) -> DiscoveredCriteria:
    """
    Analyze students in sliding windows to discover criteria.

    Args:
        student_folders: List of paths to student project folders
        window_size: Number of students per window (default: 3)

    Returns:
        DiscoveredCriteria object with all discovered quality dimensions
    """
    criteria = DiscoveredCriteria()

    for i in range(0, len(student_folders) - window_size + 1):
        window = student_folders[i:i+window_size]

        print(f"Analyzing window {i+1}: Students {i+1}-{i+window_size}")

        for student_path in window:
            features = analyze_project(student_path)

            # Check for new criteria
            new_features = find_new_features(features, criteria)
            if new_features:
                print(f"  Student {get_student_name(student_path)} added: {new_features}")

            # Update criteria
            criteria.merge(features)

    return criteria
```

### 4.2 Module: `criteria_builder.py`

**Purpose**: Build and manage discovered criteria

```python
def merge_features_into_criteria(criteria: DiscoveredCriteria, new_features: dict, student_name: str):
    """Merge newly discovered features into criteria."""

    for feature_name, feature_data in new_features.items():
        if feature_name not in criteria.dimensions:
            # New dimension discovered
            criteria.add_dimension(feature_name, feature_data, student_name)
        else:
            # Update existing dimension
            criteria.update_dimension(feature_name, feature_data)
```

### 4.3 Module: `final_evaluator.py`

**Purpose**: Evaluate all students against complete criteria

```python
def evaluate_all_students(student_folders: List[str], criteria: DiscoveredCriteria) -> List[StudentEvaluation]:
    """
    Evaluate all students against discovered criteria.

    Args:
        student_folders: All student project folders
        criteria: Complete discovered criteria

    Returns:
        List of StudentEvaluation objects with grades assigned
    """
    evaluations = []

    # Phase 1: Score all students
    for student_path in student_folders:
        eval = StudentEvaluation(get_student_name(student_path), student_path)
        eval.calculate_quality_score(criteria)
        evaluations.append(eval)

    # Phase 2: Assign relative grades
    evaluations.sort(key=lambda x: x.quality_score, reverse=True)

    best_score = evaluations[0].quality_score

    for i, eval in enumerate(evaluations):
        eval.rank = i + 1

        if eval.quality_score == best_score:
            eval.grade = 100
        else:
            eval.grade = calculate_relative_grade(eval.quality_score, best_score)

    return evaluations
```

---

## 5. Algorithm Design

### 5.1 Sliding Window Algorithm

```
INPUT: students = [S1, S2, S3, ..., SN]
OUTPUT: criteria = DiscoveredCriteria

ALGORITHM:
1. Initialize criteria = empty
2. window_size = 3
3. FOR i FROM 0 TO N - window_size:
     window = students[i : i + window_size]

     FOR student IN window:
         features = analyze_project(student)
         new_features = features NOT IN criteria

         IF new_features NOT empty:
             PRINT "Student {student} added: {new_features}"

         criteria = criteria UNION features

     END FOR
   END FOR
4. RETURN criteria
```

### 5.2 Relative Grading Algorithm

```
INPUT: students = [S1, S2, ..., SN], criteria
OUTPUT: grades = [(S1, grade1), ..., (SN, gradeN)]

ALGORITHM:
1. scores = []
2. FOR student IN students:
     score = 0
     FOR dimension IN criteria:
         score += evaluate_dimension(student, dimension)
     END FOR
     scores.append((student, score))
   END FOR

3. Sort scores by score DESC
4. best_score = scores[0].score

5. FOR (student, score) IN scores:
     IF score == best_score:
         grade = 100
     ELSE:
         percent = score / best_score

         IF percent >= 0.95:
             grade = 90 + (percent - 0.95) * 180
         ELSE IF percent >= 0.80:
             grade = 75 + (percent - 0.80) * 100
         ELSE IF percent >= 0.60:
             grade = 60 + (percent - 0.60) * 75
         ELSE:
             grade = percent * 100

     grades.append((student, grade))
   END FOR

6. RETURN grades
```

---

## 6. Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Orchestration** | SKILL.md (Claude Code) | Workflow coordination |
| **Analysis** | Python 3.8+ | Sliding window processing |
| **Data Storage** | YAML | Criteria storage |
| **Output** | CSV + Markdown | Grade reports |

---

## 7. File Structure

```
student-project-evaluator/
├── scripts/
│   ├── sliding_window_analyzer.py    # Phase 1: Discovery
│   ├── criteria_builder.py           # Build and manage criteria
│   ├── final_evaluator.py            # Phase 2: Evaluation
│   ├── analyze_project.py            # Analyze single project
│   └── utils.py                      # Helper functions
├── outputs/
│   ├── discovered_criteria.yml       # Complete criteria
│   ├── criteria_evolution.log        # What each student added
│   ├── grades.csv                    # Final grades
│   └── evaluation_report.md          # Detailed report
└── SKILL.md                          # Main orchestration
```

---

## 8. Performance Optimization

### 8.1 Caching Strategy

Cache analyzed projects to avoid re-analysis:

```python
project_cache = {}

def analyze_project_cached(student_path: str) -> dict:
    """Analyze project with caching."""
    if student_path in project_cache:
        return project_cache[student_path]

    features = analyze_project(student_path)
    project_cache[student_path] = features
    return features
```

### 8.2 Parallel Processing

Process windows in parallel when possible:

```python
from concurrent.futures import ThreadPoolExecutor

def analyze_windows_parallel(windows: List[List[str]]) -> DiscoveredCriteria:
    """Analyze multiple windows in parallel."""
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(analyze_window, windows)

    # Merge all results
    criteria = DiscoveredCriteria()
    for window_criteria in results:
        criteria.merge(window_criteria)

    return criteria
```

---

## 9. Error Handling

### 9.1 Missing Projects

```python
def analyze_project_safe(student_path: str) -> dict:
    """Analyze project with error handling."""
    try:
        return analyze_project(student_path)
    except FileNotFoundError:
        print(f"Warning: Project not found: {student_path}")
        return {'error': 'missing_project'}
    except Exception as e:
        print(f"Error analyzing {student_path}: {e}")
        return {'error': str(e)}
```

### 9.2 Incomplete Criteria

```python
def validate_criteria(criteria: DiscoveredCriteria) -> bool:
    """Ensure criteria has minimum required dimensions."""
    required = ['documentation', 'testing', 'graphics']

    for dim in required:
        if dim not in criteria.dimensions:
            print(f"Warning: Missing required dimension: {dim}")
            return False

    return True
```

---

**End of Architecture and Technical Planning**
