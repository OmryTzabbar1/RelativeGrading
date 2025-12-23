import json

with open('E:/Projects/student-project-evaluator/outputs/criteria_graph_final.json', 'r') as f:
    data = json.load(f)

student_id = '38953'
print(f'Student {student_id} has these criteria:')
criteria_for_student = [k for k, v in data['criteria'].items() if student_id in v['students']]
print(f'Total: {len(criteria_for_student)} criteria\n')

print('All criteria for this student:')
for c in sorted(criteria_for_student, key=lambda x: data['criteria'][x]['count'], reverse=True):
    count = data['criteria'][c]['count']
    category = data['criteria'][c]['category']
    name = data['criteria'][c]['display_name']
    print(f'  [{category:15s}] {name:40s} ({count:2d}/36 students)')
