#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan WorkSubmissions05 folders and list PDFs"""

import sys
import codecs
from pathlib import Path
import re

# Set UTF-8 encoding for stdout on Windows
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def extract_participant_id(folder_name):
    """Extract participant ID from folder name."""
    match = re.search(r'Participant_(\d+)', folder_name)
    return match.group(1) if match else folder_name

def main():
    base_path = Path('.')
    participant_folders = sorted([
        d for d in base_path.iterdir()
        if d.is_dir() and d.name.startswith('Participant_')
    ])

    print(f"Found {len(participant_folders)} participant folders\n")

    submissions = []
    for folder in participant_folders:
        participant_id = extract_participant_id(folder.name)
        pdf_files = list(folder.glob('*.pdf'))

        if pdf_files:
            # Filter out submission_keys.pdf if there are multiple PDFs
            main_pdfs = [p for p in pdf_files if 'submission_keys' not in p.name.lower()]
            pdf_file = main_pdfs[0] if main_pdfs else pdf_files[0]

            submissions.append({
                'participant_id': participant_id,
                'folder': folder.name,
                'pdf_path': str(pdf_file),
                'pdf_filename': pdf_file.name
            })
            print(f"{participant_id}: {pdf_file.name}")
        else:
            print(f"{participant_id}: NO PDF FOUND")

    print(f"\nTotal: {len(submissions)} submissions with PDFs")
    return submissions

if __name__ == '__main__':
    main()
