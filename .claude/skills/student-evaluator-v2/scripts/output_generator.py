"""
Output Generator Module
Generates CSV, markdown reports, and other output files.
"""

import os
from typing import List, Dict, Any
from scripts.final_evaluator import StudentEvaluation
from scripts.criteria_builder import DiscoveredCriteria


def generate_csv(evaluations: List[StudentEvaluation], output_path: str) -> None:
    """
    Generate CSV file with grades and dimension scores.

    Args:
        evaluations: List of StudentEvaluation objects
        output_path: Path to output CSV file
    """
    if not evaluations:
        raise ValueError("evaluations cannot be empty")

    # Create output directory if needed
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get all dimension names from first evaluation
    dimension_names = list(evaluations[0].dimension_scores.keys())

    # Write CSV
    with open(output_path, 'w', encoding='utf-8') as f:
        # Header row
        header = ['Student', 'Grade', 'Rank', 'Quality Score']
        header.extend(dimension_names)
        f.write(','.join(header) + '\n')

        # Data rows
        for eval_obj in evaluations:
            row = [
                eval_obj.student_name,
                str(eval_obj.grade),
                str(eval_obj.rank),
                f"{eval_obj.quality_score:.2f}"
            ]

            # Add dimension scores
            for dim_name in dimension_names:
                score = eval_obj.dimension_scores.get(dim_name, 0.0)
                row.append(f"{score:.2f}")

            f.write(','.join(row) + '\n')

    print(f"Generated CSV: {output_path}")


def generate_markdown_report(
    evaluations: List[StudentEvaluation],
    criteria: DiscoveredCriteria,
    output_path: str
) -> None:
    """
    Generate comprehensive markdown evaluation report.

    Args:
        evaluations: List of StudentEvaluation objects
        criteria: DiscoveredCriteria object
        output_path: Path to output markdown file
    """
    # Create output directory if needed
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output_path, 'w', encoding='utf-8') as f:
        # Title
        f.write("# Student Project Evaluation Report\n\n")
        f.write(f"**Total Students**: {len(evaluations)}\n\n")
        f.write("---\n\n")

        # Summary Statistics
        f.write("## Summary Statistics\n\n")
        stats = calculate_statistics(evaluations)
        f.write(f"- **Mean Grade**: {stats['mean']:.2f}\n")
        f.write(f"- **Median Grade**: {stats['median']:.2f}\n")
        f.write(f"- **Grade Range**: {stats['min']}-{stats['max']}\n")
        f.write(f"- **Standard Deviation**: {stats['std']:.2f}\n\n")

        # Grade Distribution
        f.write("### Grade Distribution\n\n")
        dist = calculate_grade_distribution(evaluations)
        for range_name, count in dist.items():
            f.write(f"- **{range_name}**: {count} students\n")
        f.write("\n---\n\n")

        # Criteria Evolution
        f.write("## Criteria Evolution\n\n")
        f.write("The following quality dimensions were discovered during evaluation:\n\n")

        for entry in criteria.evolution_log:
            student = entry['student']
            dimension = entry['dimension']
            f.write(f"- **{dimension}**: Introduced by {student}\n")

        f.write("\n---\n\n")

        # Top 10 Projects
        f.write("## Top 10 Projects\n\n")
        top_10 = evaluations[:min(10, len(evaluations))]

        f.write("| Rank | Student | Grade | Quality Score |\n")
        f.write("|------|---------|-------|---------------|\n")

        for eval_obj in top_10:
            f.write(f"| {eval_obj.rank} | {eval_obj.student_name} | "
                   f"{eval_obj.grade} | {eval_obj.quality_score:.2f} |\n")

        f.write("\n---\n\n")

        # Individual Evaluations
        f.write("## Individual Student Evaluations\n\n")

        for eval_obj in evaluations:
            f.write(f"### {eval_obj.rank}. {eval_obj.student_name}\n\n")
            f.write(f"- **Grade**: {eval_obj.grade}/100\n")
            f.write(f"- **Quality Score**: {eval_obj.quality_score:.2f}\n")
            f.write(f"- **Rank**: {eval_obj.rank}/{len(evaluations)}\n\n")

            f.write("**Dimension Scores**:\n\n")
            for dim_name, score in eval_obj.dimension_scores.items():
                f.write(f"- {dim_name}: {score:.2f}\n")

            f.write("\n")

    print(f"Generated markdown report: {output_path}")


def calculate_statistics(evaluations: List[StudentEvaluation]) -> Dict[str, float]:
    """Calculate summary statistics."""
    grades = [e.grade for e in evaluations]

    mean = sum(grades) / len(grades)
    sorted_grades = sorted(grades)
    median = sorted_grades[len(sorted_grades) // 2]

    variance = sum((g - mean) ** 2 for g in grades) / len(grades)
    std = variance ** 0.5

    return {
        'mean': mean,
        'median': median,
        'min': min(grades),
        'max': max(grades),
        'std': std
    }


def calculate_grade_distribution(evaluations: List[StudentEvaluation]) -> Dict[str, int]:
    """Calculate grade distribution by range."""
    distribution = {
        '90-100 (A)': 0,
        '75-89 (B)': 0,
        '60-74 (C)': 0,
        'Below 60 (F)': 0
    }

    for eval_obj in evaluations:
        if eval_obj.grade >= 90:
            distribution['90-100 (A)'] += 1
        elif eval_obj.grade >= 75:
            distribution['75-89 (B)'] += 1
        elif eval_obj.grade >= 60:
            distribution['60-74 (C)'] += 1
        else:
            distribution['Below 60 (F)'] += 1

    return distribution
