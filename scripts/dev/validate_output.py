#!/usr/bin/env python3
"""
Validation script for criteria_graph_final.json
Ensures data integrity and completeness
"""

import json
from pathlib import Path

def validate_criteria_graph():
    """Validate the criteria graph JSON file"""

    output_file = Path("E:/Projects/student-project-evaluator/outputs/criteria_graph_final.json")

    print("="*80)
    print("VALIDATION REPORT: criteria_graph_final.json")
    print("="*80)

    # Load the file
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validate structure
    print("\n1. STRUCTURE VALIDATION")
    print("-" * 80)

    assert 'metadata' in data, "Missing 'metadata' key"
    assert 'criteria' in data, "Missing 'criteria' key"
    print("✓ Top-level structure is valid")

    # Validate metadata
    print("\n2. METADATA VALIDATION")
    print("-" * 80)

    metadata = data['metadata']
    assert 'total_students' in metadata, "Missing 'total_students' in metadata"
    assert 'total_criteria' in metadata, "Missing 'total_criteria' in metadata"
    assert metadata['total_students'] == 36, f"Expected 36 students, got {metadata['total_students']}"
    print(f"✓ Total students: {metadata['total_students']}")
    print(f"✓ Total criteria: {metadata['total_criteria']}")
    print(f"✓ Evaluation date: {metadata.get('evaluation_date', 'N/A')}")

    # Validate criteria
    print("\n3. CRITERIA VALIDATION")
    print("-" * 80)

    criteria = data['criteria']
    assert len(criteria) == metadata['total_criteria'], \
        f"Criteria count mismatch: {len(criteria)} vs {metadata['total_criteria']}"
    print(f"✓ Criteria count matches metadata: {len(criteria)}")

    # Validate each criterion
    required_fields = ['display_name', 'students', 'count', 'weight', 'category']
    for key, criterion in criteria.items():
        for field in required_fields:
            assert field in criterion, f"Missing '{field}' in criterion '{key}'"

        # Validate counts
        assert criterion['count'] == len(criterion['students']), \
            f"Count mismatch for {key}: {criterion['count']} vs {len(criterion['students'])}"

        # Validate weight
        expected_weight = len(criterion['students']) / metadata['total_students']
        assert abs(criterion['weight'] - expected_weight) < 0.001, \
            f"Weight mismatch for {key}: {criterion['weight']} vs {expected_weight}"

    print(f"✓ All {len(criteria)} criteria have valid structure")
    print(f"✓ All student counts and weights are consistent")

    # Validate student IDs
    print("\n4. STUDENT ID VALIDATION")
    print("-" * 80)

    all_students = set()
    for criterion in criteria.values():
        all_students.update(criterion['students'])

    expected_students = {
        '38950', '38951', '38952', '38953', '38954', '38955', '38957', '38958',
        '38959', '38960', '38961', '38962', '38963', '38964', '38966', '38969',
        '38970', '38971', '38973', '38977', '38979', '38980', '38981', '38982',
        '38984', '38985', '38986', '38988', '38989', '38990', '38992', '38993',
        '59373', '59375', '59376', '59378'
    }

    assert all_students == expected_students, \
        f"Student ID mismatch: {all_students.symmetric_difference(expected_students)}"
    print(f"✓ All 36 student IDs are present and correct")
    print(f"✓ Student IDs: {sorted(all_students)[:5]}... (showing first 5)")

    # Validate categories
    print("\n5. CATEGORY VALIDATION")
    print("-" * 80)

    categories = set(c['category'] for c in criteria.values())
    expected_categories = {
        'Documentation', 'Testing', 'Features', 'Code Quality', 'DevOps',
        'Architecture', 'Frontend', 'Backend', 'Database', 'Research'
    }

    print(f"✓ Found {len(categories)} categories")
    print(f"  Categories: {sorted(categories)}")

    # Category distribution
    category_counts = {}
    for c in criteria.values():
        category_counts[c['category']] = category_counts.get(c['category'], 0) + 1

    print("\nCategory Distribution:")
    for cat in sorted(category_counts.keys(), key=lambda x: category_counts[x], reverse=True):
        print(f"  {cat:20s}: {category_counts[cat]:2d} criteria")

    # Validate ranges
    print("\n6. RANGE VALIDATION")
    print("-" * 80)

    counts = [c['count'] for c in criteria.values()]
    weights = [c['weight'] for c in criteria.values()]

    print(f"✓ Student counts range: {min(counts)} to {max(counts)}")
    print(f"✓ Weights range: {min(weights):.3f} to {max(weights):.3f}")

    # Most and least common
    sorted_criteria = sorted(criteria.items(), key=lambda x: x[1]['count'], reverse=True)

    print("\nMost common criteria:")
    for key, c in sorted_criteria[:5]:
        print(f"  {c['display_name']:40s}: {c['count']}/36 ({c['weight']:.1%})")

    print("\nLeast common criteria:")
    for key, c in sorted_criteria[-5:]:
        print(f"  {c['display_name']:40s}: {c['count']}/36 ({c['weight']:.1%})")

    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)
    print("✓ All validations PASSED")
    print(f"✓ File: {output_file}")
    print(f"✓ File size: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"✓ Students: {metadata['total_students']}")
    print(f"✓ Criteria: {metadata['total_criteria']}")
    print(f"✓ Categories: {len(categories)}")
    print("="*80)

    return True

if __name__ == "__main__":
    try:
        validate_criteria_graph()
        print("\n✓ Validation completed successfully!")
    except AssertionError as e:
        print(f"\n✗ Validation failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        exit(1)
