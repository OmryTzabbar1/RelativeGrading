import json

with open('E:/Projects/student-project-evaluator/outputs/criteria_graph_final.json', 'r') as f:
    data = json.load(f)

print(f"Total criteria: {len(data['criteria'])}\n")

print("Least common criteria (bottom 20):")
for i, (k, v) in enumerate(list(data['criteria'].items())[-20:], 1):
    display_name = v['display_name']
    count = v['count']
    weight = v['weight']
    category = v['category']
    print(f"{i:2d}. {display_name:40s} - {count:2d} students ({weight:.1%}) - {category}")

print("\n" + "="*80)
print("\nAll criteria by category:")
print("="*80)

from collections import defaultdict
by_category = defaultdict(list)
for k, v in data['criteria'].items():
    by_category[v['category']].append((v['display_name'], v['count'], v['weight']))

for category in sorted(by_category.keys()):
    print(f"\n{category}:")
    for name, count, weight in sorted(by_category[category], key=lambda x: x[1], reverse=True):
        print(f"  {name:45s} - {count:2d} students ({weight:.1%})")
