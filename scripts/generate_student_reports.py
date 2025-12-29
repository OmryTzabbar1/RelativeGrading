#!/usr/bin/env python3
"""
Student Report Generator
Generates individual Markdown and PDF reports for each student
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import openpyxl

# Category ordering (logical development lifecycle)
CATEGORY_ORDER = [
    "Planning",
    "Documentation",
    "CodeQuality",
    "Testing",
    "Research",
    "DevOps",
    "Visuals",
    "Security",
    "Uncategorized"
]

def load_criteria_graph(work_submissions_folder):
    """Load criteria graph from JSON file"""
    json_path = Path("outputs") / work_submissions_folder / "criteria_graph_final.json"

    if not json_path.exists():
        print(f"ERROR: {json_path} not found")
        print(f"Please run: python scripts/run_evaluation.py tests/{work_submissions_folder}")
        sys.exit(1)

    with open(json_path, 'r') as f:
        return json.load(f)

def load_student_grades(work_submissions_folder):
    """Load student grades from Excel file"""
    xlsx_path = Path("outputs") / work_submissions_folder / "grades.xlsx"

    if not xlsx_path.exists():
        print(f"ERROR: {xlsx_path} not found")
        print(f"Please run: python scripts/run_evaluation.py tests/{work_submissions_folder}")
        sys.exit(1)

    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb.active

    grades = {}
    for row in ws.iter_rows(min_row=2, values_only=True):  # Skip header
        if row[0] is None:
            continue

        student_name = str(row[0])
        grades[student_name] = {
            'raw_score': row[1],
            'max_possible': row[2],
            'percentage': row[3],
            'rarity_bonus': row[4] if len(row) > 4 else 0,
            'grade': row[5] if len(row) > 5 else row[4],
            'rank': row[6] if len(row) > 6 else row[5],
            'criteria_count': row[7] if len(row) > 7 else (row[6] if len(row) > 6 else None)
        }

    return grades

def build_student_report_data(student_name, criteria_graph, student_grades):
    """
    Build report data structure for a single student

    Returns dict with:
    - grade_info: score, percentage, grade, rarity_bonus, criteria_count
    - strengths: {category: [criteria]} - rare criteria (<=15%)
    - improvements: {category: [criteria]} - missing criteria
    - category_breakdown: {category: (achieved, total)}
    """
    total_students = criteria_graph['metadata']['total_students']
    total_criteria = criteria_graph['metadata']['total_criteria']

    # Get student's criteria
    student_criteria = set()
    for criterion, crit_data in criteria_graph['criteria'].items():
        if student_name in crit_data['students']:
            student_criteria.add(criterion)

    # Identify strengths (rare criteria, <=15% prevalence)
    strengths = defaultdict(list)
    for criterion in student_criteria:
        crit_data = criteria_graph['criteria'][criterion]
        prevalence = crit_data['count'] / total_students

        if prevalence <= 0.15:
            strengths[crit_data['category']].append({
                'name': criterion,
                'prevalence': prevalence,
                'count': crit_data['count'],
                'total_students': total_students
            })

    # Sort strengths by prevalence (rarest first)
    for category in strengths:
        strengths[category].sort(key=lambda x: x['prevalence'])

    # Identify improvements (missing criteria)
    improvements = defaultdict(list)
    for criterion, crit_data in criteria_graph['criteria'].items():
        if criterion not in student_criteria:
            prevalence = crit_data['count'] / total_students
            improvements[crit_data['category']].append({
                'name': criterion,
                'prevalence': prevalence,
                'count': crit_data['count'],
                'total_students': total_students
            })

    # Sort improvements by prevalence (most common first - highest priority)
    for category in improvements:
        improvements[category].sort(key=lambda x: x['prevalence'], reverse=True)

    # Category breakdown
    category_breakdown = {}
    for category in CATEGORY_ORDER:
        criteria_in_category = [
            c for c, data in criteria_graph['criteria'].items()
            if data['category'] == category
        ]
        achieved_in_category = [
            c for c in criteria_in_category
            if c in student_criteria
        ]
        if criteria_in_category:  # Only include categories that exist
            category_breakdown[category] = (len(achieved_in_category), len(criteria_in_category))

    return {
        'student_name': student_name,
        'grade_info': student_grades.get(student_name, {}),
        'strengths': dict(strengths),
        'improvements': dict(improvements),
        'category_breakdown': category_breakdown,
        'total_criteria': total_criteria,
        'achieved_criteria': len(student_criteria),
        'missing_criteria': total_criteria - len(student_criteria)
    }

def generate_markdown_report(report_data, output_path):
    """Generate markdown report for a student"""
    lines = []

    # Title (will be centered and large in PDF)
    lines.append("# STUDENT EVALUATION REPORT\n\n")

    # Header info (will be centered in PDF with custom CSS class)
    lines.append('<div class="header-info">\n\n')
    lines.append(f"**Student ID:** {report_data['student_name']}\n\n")
    lines.append(f"**Assessment Date:** {datetime.now().strftime('%Y-%m-%d')}\n\n")
    lines.append('</div>\n\n')

    # Final Score (large, orange, centered)
    grade_info = report_data['grade_info']
    if grade_info:
        lines.append(f'<div class="final-score">FINAL SCORE: {grade_info.get("grade", 0):.1f} / 100</div>\n\n')

    lines.append("---\n\n")

    # Strengths
    lines.append("## Strengths\n\n")

    if report_data['strengths']:
        lines.append("Notable accomplishments in your project:\n\n")

        # Iterate through categories in order
        for category in CATEGORY_ORDER:
            if category in report_data['strengths'] and report_data['strengths'][category]:
                lines.append(f"### {category}\n\n")
                for item in report_data['strengths'][category]:
                    lines.append(f"- **{item['name']}**\n")
                lines.append("\n")
    else:
        lines.append("*Focus on exploring advanced techniques and best practices in future projects.*\n\n")

    lines.append("---\n\n")

    # Areas for Improvement
    lines.append("## Areas for Improvement\n\n")

    if report_data['improvements']:
        lines.append("The following criteria were not found in your submission. These represent opportunities to enhance your project:\n\n")

        # Iterate through categories in order
        for category in CATEGORY_ORDER:
            if category in report_data['improvements'] and report_data['improvements'][category]:
                lines.append(f"### {category}\n\n")
                for item in report_data['improvements'][category]:
                    lines.append(f"- **{item['name']}**\n")
                lines.append("\n")
    else:
        lines.append("**Excellent!** You have achieved all criteria.\n\n")

    lines.append("---\n\n")

    # Category Breakdown (as table)
    lines.append("## Category Breakdown\n\n")
    lines.append("| Category | Criteria Achieved | Total | Percentage |\n")
    lines.append("|----------|-------------------|-------|------------|\n")
    for category in CATEGORY_ORDER:
        if category in report_data['category_breakdown']:
            achieved, total = report_data['category_breakdown'][category]
            pct = (achieved / total * 100) if total > 0 else 0
            lines.append(f"| {category} | {achieved} | {total} | {pct:.0f}% |\n")

    lines.append("\n---\n\n")

    # Footer
    lines.append("*This report was generated automatically by the Student Project Evaluator.*\n")
    lines.append("*For questions about this evaluation, please contact your instructor.*\n")

    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

def convert_markdown_to_pdf(md_path, pdf_path):
    """Convert markdown file to PDF with professional styling"""
    try:
        import markdown2
        from xhtml2pdf import pisa
    except ImportError as e:
        raise ImportError(f"Missing dependency: {e}. Install with: pip install markdown2 xhtml2pdf")

    # Read markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert to HTML
    html_content = markdown2.markdown(
        md_content,
        extras=['tables', 'fenced-code-blocks']
    )

    # Professional CSS styling matching Detailed_Grade_Breakdown.pdf
    css_style = """
    @page {
        size: A4;
        margin: 2.5cm;
    }

    body {
        font-family: 'Arial', sans-serif;
        font-size: 11pt;
        line-height: 1.6;
        color: #333;
    }

    h1 {
        color: #000;
        text-align: center;
        font-size: 28pt;
        font-weight: bold;
        margin: 20px 0 30px 0;
        padding: 0;
        border: none;
        letter-spacing: 1px;
    }

    h2 {
        color: #000;
        font-size: 20pt;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        padding: 0;
        border: none;
    }

    h3 {
        color: #000;
        font-size: 16pt;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    ul {
        margin-left: 0;
        padding-left: 20px;
    }

    li {
        margin-bottom: 8px;
    }

    strong {
        color: #2c3e50;
        font-weight: 600;
    }

    hr {
        border: none;
        border-top: 1px solid #bdc3c7;
        margin: 20px 0;
    }

    p {
        margin: 10px 0;
    }

    /* Header info styling */
    .header-info {
        text-align: center;
        margin-bottom: 30px;
    }

    .header-info p {
        margin: 5px 0;
        font-size: 11pt;
        color: #555;
    }

    /* Final score styling */
    .final-score {
        text-align: center;
        font-size: 32pt;
        font-weight: bold;
        color: #f39c12;
        margin: 30px 0;
        letter-spacing: 1px;
    }

    /* Table styling */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }

    th {
        background-color: #5b9bd5;
        color: white;
        font-weight: bold;
        padding: 10px;
        text-align: left;
        border: 1px solid #ddd;
    }

    td {
        padding: 8px 10px;
        border: 1px solid #ddd;
    }

    tr:nth-child(even) {
        background-color: #f9f9f9;
    }

    /* Status indicators */
    .status-excellent {
        color: #27ae60;
        font-weight: bold;
    }

    .status-fair {
        color: #f39c12;
        font-weight: bold;
    }

    .status-poor {
        color: #e74c3c;
        font-weight: bold;
    }
    """

    # Create full HTML document
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>{css_style}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Convert to PDF
    with open(pdf_path, 'wb') as pdf_file:
        pisa_status = pisa.CreatePDF(full_html, dest=pdf_file)

    if pisa_status.err:
        raise Exception(f"PDF conversion failed with {pisa_status.err} errors")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/generate_student_reports.py <WorkSubmissionsXX>")
        print("\nExample:")
        print("  python scripts/generate_student_reports.py WorkSubmissions05")
        sys.exit(1)

    work_submissions_folder = sys.argv[1]

    print("\n" + "="*80)
    print("STUDENT REPORT GENERATOR")
    print("="*80)

    # Step 1: Load data
    print(f"\n[1/5] Loading criteria graph and grades...")
    criteria_graph = load_criteria_graph(work_submissions_folder)
    student_grades = load_student_grades(work_submissions_folder)
    print(f"  Loaded data for {len(student_grades)} students")

    # Step 2: Create output directory
    print(f"\n[2/5] Creating output directory...")
    output_dir = Path("outputs") / work_submissions_folder / "student_reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"  Created: {output_dir}")

    # Step 3: Generate markdown reports
    print(f"\n[3/5] Generating markdown reports...")
    student_names = sorted(student_grades.keys())

    for i, student_name in enumerate(student_names, 1):
        print(f"  [{i}/{len(student_names)}] {student_name}...")

        report_data = build_student_report_data(
            student_name, criteria_graph, student_grades
        )

        md_path = output_dir / f"{student_name}.md"
        generate_markdown_report(report_data, md_path)

    print(f"  Generated {len(student_names)} markdown reports")

    # Step 4: Convert to PDF
    print(f"\n[4/5] Converting to PDF...")

    # Check if dependencies are available
    try:
        import markdown2
        from xhtml2pdf import pisa
        pdf_available = True
    except ImportError:
        pdf_available = False
        print("  WARNING: markdown2 or xhtml2pdf not installed")
        print("  Install with: pip install markdown2 xhtml2pdf")
        print("  Skipping PDF generation...")

    failed_conversions = []

    if pdf_available:
        for i, student_name in enumerate(student_names, 1):
            print(f"  [{i}/{len(student_names)}] {student_name}...", end='', flush=True)

            md_path = output_dir / f"{student_name}.md"
            pdf_path = output_dir / f"{student_name}.pdf"

            try:
                convert_markdown_to_pdf(md_path, pdf_path)
                print(" OK")
            except Exception as e:
                failed_conversions.append(student_name)
                print(f" FAILED - {e}")

        if failed_conversions:
            print(f"\n  WARNING: {len(failed_conversions)} PDF conversions failed")
            print(f"  Markdown files available for manual conversion")
        else:
            print(f"  Generated {len(student_names)} PDF reports")

    # Step 5: Summary
    print(f"\n[5/5] Summary")
    print(f"  Generated files:")
    print(f"    - {len(student_names)} markdown reports (.md)")
    if pdf_available and not failed_conversions:
        print(f"    - {len(student_names)} PDF reports (.pdf)")
    elif pdf_available:
        print(f"    - {len(student_names) - len(failed_conversions)} PDF reports (.pdf)")
    print(f"  Location: {output_dir.absolute()}")

    print("\n" + "="*80)
    print("REPORT GENERATION COMPLETE!")
    print("="*80)
    print(f"\nReports saved to: {output_dir.absolute()}")

if __name__ == "__main__":
    main()
