"""
Final Evaluator Module
Evaluates all students against complete discovered criteria.
"""

from typing import Dict, List, Any
from scripts.criteria_builder import DiscoveredCriteria


class StudentEvaluation:
    """
    Tracks evaluation results for a single student.

    Attributes:
        student_name: Student identifier
        student_path: Full path to student project folder
        dimension_scores: Scores for each quality dimension
        quality_score: Composite score across all dimensions
        grade: Final grade (0-100)
        rank: Rank among all students (1 = best)
    """

    def __init__(self, student_name: str, student_path: str):
        """
        Initialize student evaluation.

        Args:
            student_name: Student identifier
            student_path: Full path to student project folder
        """
        self.student_name: str = student_name
        self.student_path: str = student_path
        self.dimension_scores: Dict[str, float] = {}
        self.quality_score: float = 0.0
        self.grade: int = 0
        self.rank: int = 0

    def calculate_quality_score(self, criteria: DiscoveredCriteria, project_features: Dict[str, Any]) -> float:
        """
        Calculate composite quality score across all dimensions.

        Args:
            criteria: Complete discovered criteria
            project_features: Features extracted from student project

        Returns:
            Total quality score (sum of all dimension scores)
        """
        for dimension_name, dimension_criteria in criteria.dimensions.items():
            score = self._score_dimension(
                dimension_name,
                dimension_criteria,
                project_features.get(dimension_name, {})
            )
            self.dimension_scores[dimension_name] = score

        self.quality_score = sum(self.dimension_scores.values())
        return self.quality_score

    def _score_dimension(self, name: str, criteria: Dict[str, Any], student_data: Dict[str, Any]) -> float:
        """
        Score a single dimension.

        Args:
            name: Dimension name
            criteria: Criteria for this dimension
            student_data: Student's data for this dimension

        Returns:
            Score for this dimension
        """
        # If student has no data for this dimension, score is 0
        if not student_data or student_data.get('present') is False:
            return 0.0

        # Start with base weight for having this dimension
        base_weight = 10.0
        score = base_weight

        # Add points for sub-features within the dimension
        for key, value in student_data.items():
            if key == 'present':
                continue

            # Handle nested dictionaries (e.g., documentation.readme)
            if isinstance(value, dict):
                if value.get('present'):
                    score += value.get('weight', 5.0)
            # Handle counts (e.g., test_file_count, image_count)
            elif isinstance(value, int) and 'count' in key:
                score += min(value, 10)  # Cap at 10 points per count
            # Handle weights
            elif key == 'weight':
                score += float(value)

        return score

    def set_grade(self, grade: int) -> None:
        """
        Set final grade.

        Args:
            grade: Grade value (0-100)
        """
        self.grade = max(0, min(100, grade))

    def set_rank(self, rank: int) -> None:
        """
        Set rank among all students.

        Args:
            rank: Rank value (1 = best)
        """
        self.rank = max(1, rank)

    def to_dict(self) -> Dict[str, Any]:
        """
        Export evaluation as dictionary.

        Returns:
            Dictionary with all evaluation data
        """
        return {
            'student': self.student_name,
            'path': self.student_path,
            'dimension_scores': self.dimension_scores,
            'quality_score': self.quality_score,
            'grade': self.grade,
            'rank': self.rank
        }


def evaluate_all_students(
    student_folders: List[str],
    criteria: DiscoveredCriteria,
    project_features_map: Dict[str, Dict[str, Any]]
) -> List[StudentEvaluation]:
    """
    Evaluate all students against discovered criteria.

    Args:
        student_folders: List of student folder paths
        criteria: Complete discovered criteria
        project_features_map: Dict mapping student path to their features

    Returns:
        List of StudentEvaluation objects with grades assigned
    """
    evaluations: List[StudentEvaluation] = []

    # Phase 1: Score all students
    for student_path in student_folders:
        student_name = student_path.split('\\')[-1]  # Extract folder name
        eval_obj = StudentEvaluation(student_name, student_path)

        # Get features for this student
        features = project_features_map.get(student_path, {})

        # Calculate quality score
        eval_obj.calculate_quality_score(criteria, features)
        evaluations.append(eval_obj)

    # Phase 2: Assign relative grades
    evaluations.sort(key=lambda x: x.quality_score, reverse=True)

    if not evaluations:
        return evaluations

    best_score = evaluations[0].quality_score

    for i, eval_obj in enumerate(evaluations):
        eval_obj.set_rank(i + 1)

        if eval_obj.quality_score == best_score:
            eval_obj.set_grade(100)
        else:
            grade = calculate_relative_grade(eval_obj.quality_score, best_score)
            eval_obj.set_grade(grade)

    return evaluations


def calculate_relative_grade(quality_score: float, best_score: float) -> int:
    """
    Calculate relative grade based on quality score.

    Args:
        quality_score: Student's quality score
        best_score: Best quality score among all students

    Returns:
        Grade (0-100)
    """
    if best_score == 0:
        return 0

    percent = quality_score / best_score

    # Best student (100% or more) gets 100
    if percent >= 1.0:
        return 100

    # Grading curve from PLANNING.md
    if percent >= 0.95:
        grade = 90 + int((percent - 0.95) * 180)
    elif percent >= 0.80:
        grade = 75 + int((percent - 0.80) * 100)
    elif percent >= 0.60:
        grade = 60 + int((percent - 0.60) * 75)
    else:
        grade = int(percent * 100)

    return max(0, min(100, grade))
