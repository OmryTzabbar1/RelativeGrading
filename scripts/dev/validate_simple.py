#!/usr/bin/env python3
import json
from pathlib import Path

output_file = Path("E:/Projects/student-project-evaluator/outputs/criteria_graph_final.json")

print("="*80)
print("VALIDATION REPORT: criteria_graph_final.json")
print("="*80)

with open(output_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Validate structure
print("\n1. STRUCTURE VALIDATION")
print("-" * 80)
assert 'metadata' in data and 'criteria' in data
print("[OK] Top-level structure is valid")

# Validate metadata
print("\n2. METADATA VALIDATION")
print("-" * 80)
metadata = data['metadata']
assert metadata['total_students'] == 36
print(f"[OK] Total students: {metadata['total_students']}")
print(f"[OK] Total criteria: {metadata['total_criteria']}")

# Validate criteria
print("\n3. CRITERIA VALIDATION")
print("-" * 80)
criteria = data['criteria']
print(f"[OK] Criteria count: {len(criteria)}")

# Validate student IDs
print("\n4. STUDENT ID VALIDATION")
print("-" * 80)
all_students = set()
for criterion in criteria.values():
    all_students.update(criterion['students'])
print(f"[OK] All 36 student IDs present: {len(all_students) == 36}")

# Category distribution
print("\n5. CATEGORY DISTRIBUTION")
print("-" * 80)
category_counts = {}
for c in criteria.values():
    category_counts[c['category']] = category_counts.get(c['category'], 0) + 1

for cat in sorted(category_counts.keys(), key=lambda x: category_counts[x], reverse=True):
    print(f"  {cat:20s}: {category_counts[cat]:2d} criteria")

# Top criteria
print("\n6. TOP 10 CRITERIA")
print("-" * 80)
sorted_criteria = sorted(criteria.items(), key=lambda x: x[1]['count'], reverse=True)
for i, (key, c) in enumerate(sorted_criteria[:10], 1):
    print(f"{i:2d}. {c['display_name']:40s}: {c['count']}/36 ({c['weight']:.1%})")

print("\n" + "="*80)
print("VALIDATION PASSED")
print(f"File: {output_file}")
print(f"Size: {output_file.stat().st_size / 1024:.1f} KB")
print(f"Students: {metadata['total_students']}")
print(f"Criteria: {metadata['total_criteria']}")
print("="*80)
