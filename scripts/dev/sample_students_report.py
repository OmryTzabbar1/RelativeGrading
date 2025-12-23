#!/usr/bin/env python3
"""
Sample Student Report - Shows criteria for selected students
"""
import json

with open('E:/Projects/student-project-evaluator/outputs/criteria_graph_final.json', 'r') as f:
    data = json.load(f)

# Sample students with different performance levels
sample_students = ['38954', '38953', '38960', '38979', '38957', '38966']

print("="*80)
print("SAMPLE STUDENT CRITERIA REPORT")
print("="*80)

for student_id in sample_students:
    print(f"\n{'='*80}")
    print(f"STUDENT {student_id}")
    print('='*80)

    # Get criteria for this student
    criteria_list = []
    for key, criterion in data['criteria'].items():
        if student_id in criterion['students']:
            criteria_list.append({
                'name': criterion['display_name'],
                'category': criterion['category'],
                'count': criterion['count'],
                'weight': criterion['weight']
            })

    print(f"\nTotal Criteria Implemented: {len(criteria_list)}")

    # Group by category
    by_category = {}
    for c in criteria_list:
        if c['category'] not in by_category:
            by_category[c['category']] = []
        by_category[c['category']].append(c)

    print(f"Categories Covered: {len(by_category)}")

    # Show by category
    for category in sorted(by_category.keys()):
        items = by_category[category]
        print(f"\n{category} ({len(items)} criteria):")
        for item in sorted(items, key=lambda x: x['count'], reverse=True):
            rarity = "Common" if item['weight'] > 0.6 else "Uncommon" if item['weight'] > 0.3 else "Rare"
            print(f"  - {item['name']:40s} [{rarity:8s}] ({item['count']}/36)")

print("\n" + "="*80)
print("END OF REPORT")
print("="*80)
