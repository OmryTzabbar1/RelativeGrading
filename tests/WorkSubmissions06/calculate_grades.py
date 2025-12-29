#!/usr/bin/env python3
"""
Calculate student grades based on criteria graph
"""
import json
import pandas as pd
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(r"E:\Projects\student-project-evaluator\tests\WorkSubmissions06")
OUTPUT_DIR = Path(r"E:\Projects\student-project-evaluator\tests\WorkSubmissions06\outputs")

def load_data():
    """Load the criteria graph"""
    with open(OUTPUT_DIR / "criteria_graph_final.json", 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_scores(data):
    """Calculate raw scores for each student"""
    criteria_graph = data["criteria_graph"]
    student_data = data["student_data"]

    scores = {}

    for student_id, student_info in student_data.items():
        raw_score = 0.0
        criteria_list = student_info["criteria"]

        # Sum weights for all criteria this student has
        for criterion in criteria_list:
            if criterion in criteria_graph:
                weight = criteria_graph[criterion]["weight"]
                raw_score += weight

        scores[student_id] = {
            "raw_score": round(raw_score, 2),
            "criteria_count": len(criteria_list),
            "criteria": criteria_list,
            "md_files_count": len(student_info["md_files"])
        }

    # Calculate max possible score (sum of all weights)
    max_possible = sum(c["weight"] for c in criteria_graph.values())

    # Calculate percentages
    for student_id, score_data in scores.items():
        percentage = (score_data["raw_score"] / max_possible) * 100
        scores[student_id]["percentage"] = round(percentage, 2)

    # Calculate relative grades
    best_percentage = max(s["percentage"] for s in scores.values())

    for student_id, score_data in scores.items():
        relative_grade = (score_data["percentage"] / best_percentage) * 100
        scores[student_id]["relative_grade"] = round(relative_grade, 2)

    # Rank students
    sorted_students = sorted(scores.items(), key=lambda x: x[1]["relative_grade"], reverse=True)

    current_rank = 1
    previous_grade = None
    for i, (student_id, score_data) in enumerate(sorted_students):
        if previous_grade is not None and score_data["relative_grade"] < previous_grade:
            current_rank = i + 1
        scores[student_id]["rank"] = current_rank
        previous_grade = score_data["relative_grade"]

    return scores, max_possible

def generate_grades_excel(data, scores, max_possible):
    """Generate grades.xlsx"""
    # Prepare data for DataFrame
    rows = []
    for student_id, score_data in scores.items():
        rows.append({
            "Rank": score_data["rank"],
            "Student": student_id,
            "Grade": score_data["relative_grade"],
            "Percentage": score_data["percentage"],
            "Raw Score": score_data["raw_score"],
            "Criteria Count": score_data["criteria_count"],
            "MD Files": score_data["md_files_count"]
        })

    df = pd.DataFrame(rows)
    df = df.sort_values("Rank")

    # Save to Excel
    output_file = OUTPUT_DIR / "grades.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Grades', index=False)

        # Format the sheet
        worksheet = writer.sheets['Grades']
        for col in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in col)
            worksheet.column_dimensions[col[0].column_letter].width = max_length + 2

    print(f"Saved grades to {output_file}")
    return df

def generate_student_evaluation_report(data, scores, max_possible):
    """Generate detailed Student_Evaluation_Report.xlsx"""
    criteria_graph = data["criteria_graph"]

    # Sheet 1: Student Grades
    grades_rows = []
    for student_id, score_data in scores.items():
        grades_rows.append({
            "Rank": score_data["rank"],
            "Student": student_id,
            "Grade": score_data["relative_grade"],
            "Percentage": score_data["percentage"],
            "Raw Score": score_data["raw_score"],
            "Criteria Count": score_data["criteria_count"],
            "MD Files": score_data["md_files_count"]
        })
    df_grades = pd.DataFrame(grades_rows).sort_values("Rank")

    # Sheet 2: Criteria Details
    criteria_rows = []
    for criterion, crit_data in sorted(criteria_graph.items(), key=lambda x: x[1]["count"], reverse=True):
        criteria_rows.append({
            "Criterion": criterion,
            "Category": crit_data["category"],
            "Student Count": crit_data["count"],
            "Prevalence": f"{crit_data['prevalence']*100:.1f}%",
            "Weight": crit_data["weight"],
            "Rarity Bonus": crit_data.get("rarity_bonus", 0),
            "Students": ", ".join(crit_data["students"][:3]) + ("..." if len(crit_data["students"]) > 3 else "")
        })
    df_criteria = pd.DataFrame(criteria_rows)

    # Sheet 3: Student-Criteria Matrix
    matrix_data = []
    all_criteria = sorted(criteria_graph.keys())
    for student_id, score_data in sorted(scores.items(), key=lambda x: x[1]["rank"]):
        row = {"Student": student_id, "Rank": score_data["rank"], "Grade": score_data["relative_grade"]}
        for criterion in all_criteria:
            row[criterion] = "X" if criterion in score_data["criteria"] else ""
        matrix_data.append(row)
    df_matrix = pd.DataFrame(matrix_data)

    # Sheet 4: Category Summary
    category_counts = defaultdict(lambda: {"criteria_count": 0, "total_weight": 0})
    for criterion, crit_data in criteria_graph.items():
        cat = crit_data["category"]
        category_counts[cat]["criteria_count"] += 1
        category_counts[cat]["total_weight"] += crit_data["weight"]

    category_rows = []
    for category, counts in sorted(category_counts.items()):
        category_rows.append({
            "Category": category,
            "Criteria Count": counts["criteria_count"],
            "Total Weight": round(counts["total_weight"], 2),
            "Avg Weight": round(counts["total_weight"] / counts["criteria_count"], 3)
        })
    df_categories = pd.DataFrame(category_rows)

    # Write all sheets
    output_file = OUTPUT_DIR / "Student_Evaluation_Report.xlsx"
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_grades.to_excel(writer, sheet_name='Student Grades', index=False)
        df_criteria.to_excel(writer, sheet_name='Criteria Details', index=False)
        df_categories.to_excel(writer, sheet_name='Category Summary', index=False)
        df_matrix.to_excel(writer, sheet_name='Student-Criteria Matrix', index=False)

        # Format all sheets
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            for col in worksheet.columns:
                max_length = max(len(str(cell.value)) for cell in col)
                worksheet.column_dimensions[col[0].column_letter].width = min(max_length + 2, 50)

    print(f"Saved detailed report to {output_file}")
    return df_grades, df_criteria, df_categories

def generate_evaluation_summary(data, scores, max_possible, df_grades):
    """Generate EVALUATION_SUMMARY.md"""
    total_students = data["metadata"]["total_students"]
    total_criteria = data["metadata"]["total_criteria"]
    total_md_files = data["metadata"]["total_md_files"]

    criteria_graph = data["criteria_graph"]

    # Count CodeQuality criteria
    code_quality_criteria = [c for c, d in criteria_graph.items() if d["category"] == "CodeQuality"]

    # Grade distribution
    grade_dist = {
        "90-100": 0,
        "80-89": 0,
        "70-79": 0,
        "60-69": 0,
        "Below 60": 0
    }
    for score_data in scores.values():
        grade = score_data["relative_grade"]
        if grade >= 90:
            grade_dist["90-100"] += 1
        elif grade >= 80:
            grade_dist["80-89"] += 1
        elif grade >= 70:
            grade_dist["70-79"] += 1
        elif grade >= 60:
            grade_dist["60-69"] += 1
        else:
            grade_dist["Below 60"] += 1

    # Top 3 students
    top3 = df_grades.head(3)

    # Category breakdown
    category_counts = defaultdict(int)
    for criterion, crit_data in criteria_graph.items():
        category_counts[crit_data["category"]] += 1

    # Rare criteria
    rare_criteria = [(c, d) for c, d in criteria_graph.items() if d["prevalence"] <= 0.15]

    # Generate markdown
    md_content = f"""# Evaluation Summary - WorkSubmissions06

## Overview

**Evaluation Date:** {data["metadata"]["evaluation_date"]}
**Total Students Evaluated:** {total_students}
**Total Criteria Discovered:** {total_criteria}
**Total Markdown Files Processed:** {total_md_files}
**Average MD Files per Student:** {total_md_files / total_students:.1f}

---

## Criteria Breakdown by Category

"""

    for category in sorted(category_counts.keys()):
        count = category_counts[category]
        md_content += f"- **{category}**: {count} criteria\n"

    md_content += f"""
**CodeQuality Criteria Found:** {len(code_quality_criteria)}

CodeQuality criteria identified:
"""
    for criterion in sorted(code_quality_criteria):
        count = criteria_graph[criterion]["count"]
        prevalence = criteria_graph[criterion]["prevalence"] * 100
        md_content += f"  - {criterion} ({count}/{total_students} students, {prevalence:.1f}%)\n"

    md_content += f"""
---

## Top 3 Students

"""

    for i, row in top3.iterrows():
        md_content += f"""### {row['Rank']}. {row['Student']}
- **Grade:** {row['Grade']}/100
- **Criteria Count:** {row['Criteria Count']}/{total_criteria}
- **Raw Score:** {row['Raw Score']:.2f} / {max_possible:.2f}
- **Percentage:** {row['Percentage']:.2f}%

"""

    md_content += f"""---

## Grade Distribution

"""

    for grade_range, count in grade_dist.items():
        percentage = (count / total_students) * 100
        md_content += f"- **{grade_range}:** {count} students ({percentage:.1f}%)\n"

    md_content += f"""
**Average Grade:** {df_grades['Grade'].mean():.2f}/100
**Median Grade:** {df_grades['Grade'].median():.2f}/100
**Standard Deviation:** {df_grades['Grade'].std():.2f}

---

## Rare Criteria (≤15% prevalence)

These {len(rare_criteria)} criteria received a +1 bonus weight for rarity:

"""

    for criterion, crit_data in sorted(rare_criteria, key=lambda x: x[1]["count"]):
        count = crit_data["count"]
        prevalence = crit_data["prevalence"] * 100
        category = crit_data["category"]
        md_content += f"- **{criterion}** ({category}) - {count}/{total_students} students ({prevalence:.1f}%)\n"

    md_content += f"""
---

## Most Common Criteria

Top 10 criteria by student count:

"""

    sorted_criteria = sorted(criteria_graph.items(), key=lambda x: x[1]["count"], reverse=True)
    for i, (criterion, crit_data) in enumerate(sorted_criteria[:10], 1):
        count = crit_data["count"]
        prevalence = crit_data["prevalence"] * 100
        category = crit_data["category"]
        weight = crit_data["weight"]
        md_content += f"{i}. **{criterion}** ({category}) - {count}/{total_students} ({prevalence:.1f}%) - Weight: {weight:.2f}\n"

    md_content += """
---

## Output Files Generated

1. **criteria_graph_final.json** - Complete criteria data with metadata
2. **grades.xlsx** - Simple grades spreadsheet
3. **Student_Evaluation_Report.xlsx** - Comprehensive 4-sheet Excel report
   - Student Grades
   - Criteria Details
   - Category Summary
   - Student-Criteria Matrix
4. **EVALUATION_SUMMARY.md** - This file

---

## Notes

- Weights calculated based on prevalence (count / total_students)
- Rare criteria (≤15% prevalence) received +1 bonus weight
- Relative grades normalized so top student = 100
- Students ranked by relative grade (ties share same rank)
"""

    output_file = OUTPUT_DIR / "EVALUATION_SUMMARY.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Saved evaluation summary to {output_file}")
    return md_content

def main():
    print("=" * 80)
    print("CALCULATING GRADES - WorkSubmissions06")
    print("=" * 80)

    # Load data
    print("\n[Step 1] Loading criteria graph...")
    data = load_data()

    # Calculate scores
    print("[Step 2] Calculating student scores...")
    scores, max_possible = calculate_scores(data)

    print(f"\nMax possible score: {max_possible:.2f}")
    print(f"Students evaluated: {len(scores)}")

    # Generate outputs
    print("\n[Step 3] Generating Excel reports...")
    df_grades = generate_grades_excel(data, scores, max_possible)
    df_grades_detail, df_criteria, df_categories = generate_student_evaluation_report(data, scores, max_possible)

    print("\n[Step 4] Generating markdown summary...")
    summary = generate_evaluation_summary(data, scores, max_possible, df_grades)

    # Print preview
    print("\n" + "=" * 80)
    print("GRADING COMPLETE")
    print("=" * 80)
    print(f"\nTop 5 Students:")
    for i, (idx, row) in enumerate(df_grades.head(5).iterrows(), 1):
        print(f"  {row['Rank']}. {row['Student']:<45s} Grade: {row['Grade']:6.2f} ({row['Criteria Count']:2d}/{data['metadata']['total_criteria']} criteria)")

    print(f"\nGrade Distribution:")
    grade_ranges = ["90-100", "80-89", "70-79", "60-69", "Below 60"]
    for grade_range in grade_ranges:
        count = len([s for s in scores.values() if
                    (grade_range == "90-100" and s["relative_grade"] >= 90) or
                    (grade_range == "80-89" and 80 <= s["relative_grade"] < 90) or
                    (grade_range == "70-79" and 70 <= s["relative_grade"] < 80) or
                    (grade_range == "60-69" and 60 <= s["relative_grade"] < 70) or
                    (grade_range == "Below 60" and s["relative_grade"] < 60)])
        print(f"  {grade_range:>10s}: {count:2d} students")

    print(f"\nOutput files:")
    print(f"  - {OUTPUT_DIR / 'criteria_graph_final.json'}")
    print(f"  - {OUTPUT_DIR / 'grades.xlsx'}")
    print(f"  - {OUTPUT_DIR / 'Student_Evaluation_Report.xlsx'}")
    print(f"  - {OUTPUT_DIR / 'EVALUATION_SUMMARY.md'}")

if __name__ == "__main__":
    main()
