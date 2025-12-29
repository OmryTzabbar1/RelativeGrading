#!/usr/bin/env python3
"""
Populate all student folders with individual submission_info.xlsx files
Based on extracted data from PDFs
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from create_individual_excels import create_student_excel, extract_participant_id

# All extracted data from PDFs
submissions_data = [
    {
        'participant_id': '87681',
        'folder': 'Participant_87681_assignsubmission_file',
        'group_code': 'LLM_Agents_Tom_Igor_Roie',
        'student1': 'Tom Ohayon 209033445',
        'student2': 'Igor Liberchuk 206984404, Roie Dayan 322977636',
        'github': 'https://github.com/TomOhayon/llm_travel_recomendations',
        'grade': '94',
        'pdf': 'Assignment_4_Cover_Page.pdf'
    },
    {
        'participant_id': '87682',
        'folder': 'Participant_87682_assignsubmission_file',
        'group_code': 'אריאלנפדנסקיואביפרדמן',
        'student1': 'Ariel Nefdinski 209210009',
        'student2': 'Avi Friedman 034568931',
        'github': 'https://github.com/avinep123/LLMs_Course/tree/main/Assignment_4',
        'grade': '85',
        'pdf': 'מטלה4 אריאל נפדנסקי ואבי פרדמן.pdf'
    },
    {
        'participant_id': '87683',
        'folder': 'Participant_87683_assignsubmission_file',
        'group_code': 'scubadivers',
        'student1': 'Hibner Tal 026548446',
        'student2': 'Yomtov Dvir 209399872',
        'github': 'https://github.com/DVIRO44/llmcourse-hw4-google-maps',
        'grade': '93',
        'pdf': 'scubadivers.pdf'
    },
    {
        'participant_id': '87684',
        'folder': 'Participant_87684_assignsubmission_file',
        'group_code': 'asiroli2025',
        'student1': 'Asaf Shirizly 030539774',
        'student2': 'Ron Olshansky 208974648, Lior Dahari 046457070',
        'github': 'https://github.com/aolshansky/geo-context-media-orchestrator',
        'grade': '100',
        'pdf': 'HW4_asiroli2025_Geo_Contextual_Media_Orchestrator.pdf'
    },
    {
        'participant_id': '87685',
        'folder': 'Participant_87685_assignsubmission_file',
        'group_code': 'talkeren',
        'student1': 'Tal Sheldon 302317284',
        'student2': 'Keren Or 319039814',
        'github': 'https://github.com/keren-or1/route-stories',
        'grade': '97',
        'pdf': 'מטלה 4.pdf'
    },
    {
        'participant_id': '87687',
        'folder': 'Participant_87687_assignsubmission_file',
        'group_code': 'אריאלנפדנסקיואביפרדמן (Duplicate)',
        'student1': 'Ariel Nefdinski 209210009',
        'student2': 'Avi Friedman 034568931',
        'github': 'https://github.com/avinep123/LLMs_Course/tree/main/Assignment_4',
        'grade': '85',
        'pdf': 'מטלה4 אריאל נפדנסקי ואבי פרדמן.pdf'
    },
    {
        'participant_id': '87690',
        'folder': 'Participant_87690_assignsubmission_file',
        'group_code': '1998',
        'student1': 'Tal Barda 208974618',
        'student2': '',
        'github': 'https://github.com/TalBarda8/AgentOrchestrationProject',
        'grade': '94',
        'pdf': 'הגשת מטלה 4 - טל ברדה.pdf'
    },
    {
        'participant_id': '87691',
        'folder': 'Participant_87691_assignsubmission_file',
        'group_code': 'asiroli2025 (API Keys)',
        'student1': '',
        'student2': '',
        'github': '',
        'grade': '',
        'pdf': 'submission_keys.pdf'
    },
    {
        'participant_id': '87692',
        'folder': 'Participant_87692_assignsubmission_file',
        'group_code': 'roeiandguy',
        'student1': 'Roei Bracha 208933325',
        'student2': 'Guy Bilitski 2087332532',
        'github': 'https://github.com/Roei-Bracha/ollama-chat-hw',
        'grade': '90',
        'pdf': 'hw4 llms agents.pdf'
    },
    {
        'participant_id': '87694',
        'folder': 'Participant_87694_assignsubmission_file',
        'group_code': 'LLM_Agents_Tom_Igor_Roie (Duplicate)',
        'student1': 'Tom Ohayon 209033445',
        'student2': 'Igor Liberchuk 206984404, Roie Dayan 322977636',
        'github': 'https://github.com/TomOhayon/llm_travel_recomendations',
        'grade': '94',
        'pdf': 'HW4_Cover_page.pdf'
    },
    {
        'participant_id': '87696',
        'folder': 'Participant_87696_assignsubmission_file',
        'group_code': 'NOT PROCESSED (PDF too large)',
        'student1': '',
        'student2': '',
        'github': '',
        'grade': '',
        'pdf': 'Unknown PDF'
    },
    {
        'participant_id': '87698',
        'folder': 'Participant_87698_assignsubmission_file',
        'group_code': 'eldad_ron_bar_yacobi',
        'student1': 'Eldad Ron 207021916',
        'student2': 'Bar Yacobi 315471367',
        'github': 'https://github.com/er1009/LLMs-And-Multi-Agent-Orchestration-Course/tree/main/ex4',
        'grade': '100',
        'pdf': 'ex4_bar_eldad.pdf'
    },
    {
        'participant_id': '87703',
        'folder': 'Participant_87703_assignsubmission_file',
        'group_code': 'roeiandguy',
        'student1': 'Roei Bracha 208933325',
        'student2': 'Guy Bilitski 2087332532',
        'github': 'https://github.com/Roei-Bracha/llm-hw-travel-guide',
        'grade': '90',
        'pdf': 'hw4 llms agents.pdf'
    },
    {
        'participant_id': '87706',
        'folder': 'Participant_87706_assignsubmission_file',
        'group_code': '103050',
        'student1': 'Fouad Azem 040830861',
        'student2': 'Tal Goldengoren 207042573',
        'github': 'https://github.com/fouada/Assignment4-multi-agent-tour-guide-parallel',
        'grade': '98',
        'pdf': 'Assignment4-multi-agent-tour-guide-parallel.pdf'
    },
    {
        'participant_id': '87707',
        'folder': 'Participant_87707_assignsubmission_file',
        'group_code': 'The_Surfers',
        'student1': 'Ben Volublaski 209361864',
        'student2': 'Rafael Moreno 021387121',
        'github': 'https://github.com/volo10/Tour_Guide',
        'grade': '95',
        'pdf': 'Hw4_The_Surfers_209361864_021387121.pdf'
    },
    {
        'participant_id': '87714',
        'folder': 'Participant_87714_assignsubmission_file',
        'group_code': '103050 (Duplicate)',
        'student1': 'Fouad Azem 040830861',
        'student2': 'Tal Goldengoren 207042573',
        'github': 'https://github.com/fouada/Assignment4-multi-agent-tour-guide-parallel',
        'grade': '98',
        'pdf': 'Assignment4-multi-agent-tour-guide-parallel.pdf'
    },
    {
        'participant_id': '87715',
        'folder': 'Participant_87715_assignsubmission_file',
        'group_code': 'scubadivers (Duplicate)',
        'student1': 'Hibner Tal 026548446',
        'student2': 'Yomtov Dvir 209399872',
        'github': 'https://github.com/DVIRO44/llmcourse-hw4-google-maps',
        'grade': '93',
        'pdf': 'scubadivers.pdf'
    },
    {
        'participant_id': '87716',
        'folder': 'Participant_87716_assignsubmission_file',
        'group_code': 'eldad_ron_bar_yacobi (Duplicate)',
        'student1': 'Eldad Ron 207021916',
        'student2': 'Bar Yacobi 315471367',
        'github': 'https://github.com/er1009/LLMs-And-Multi-Agent-Orchestration-Course/tree/main/ex4',
        'grade': '100',
        'pdf': 'ex4_bar_eldad.pdf'
    },
    {
        'participant_id': '87719',
        'folder': 'Participant_87719_assignsubmission_file',
        'group_code': 'talkeren (Duplicate)',
        'student1': 'Tal Sheldon 302317284',
        'student2': 'Keren Or 319039814',
        'github': 'https://github.com/keren-or1/route-stories',
        'grade': '97',
        'pdf': 'מטלה 4.pdf'
    },
    {
        'participant_id': '87721',
        'folder': 'Participant_87721_assignsubmission_file',
        'group_code': 'The_Surfers (Duplicate)',
        'student1': 'Ben Volublaski 209361864',
        'student2': 'Rafael Moreno 021387121',
        'github': 'https://github.com/volo10/Tour_Guide',
        'grade': '95',
        'pdf': 'Hw4_The_Surfers_209361864_021387121.pdf'
    }
]

def main():
    """Create individual Excel files in each participant folder."""
    base_path = Path('.')
    created_count = 0
    failed_count = 0

    print(f"\nCreating individual submission_info.xlsx files in each participant folder...")
    print("=" * 70)

    for submission in submissions_data:
        folder_path = base_path / submission['folder']

        if not folder_path.exists():
            print(f"[X] Folder not found: {submission['folder']}")
            failed_count += 1
            continue

        try:
            output_path = create_student_excel(
                folder_path=folder_path,
                participant_id=submission['participant_id'],
                group_code=submission['group_code'],
                student1=submission['student1'],
                student2=submission['student2'],
                github=submission['github'],
                grade=submission['grade'],
                pdf_filename=submission['pdf']
            )
            print(f"[OK] Created: {submission['folder']}/submission_info.xlsx")
            created_count += 1
        except Exception as e:
            print(f"[ERROR] Error creating Excel for {submission['folder']}: {e}")
            failed_count += 1

    print("=" * 70)
    print(f"\n[OK] Successfully created {created_count} Excel files")
    if failed_count > 0:
        print(f"[ERROR] Failed to create {failed_count} Excel files")
    print(f"\nTotal submissions processed: {len(submissions_data)}")

if __name__ == '__main__':
    main()
