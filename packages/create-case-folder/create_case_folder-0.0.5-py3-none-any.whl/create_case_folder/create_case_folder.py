import os
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=str, help='Name of the case folder')
    parser.add_argument('--evidence', type=str, help='Name of the evidence folder')
    args = parser.parse_args()
    
    parent_folder = args.case
    if not parent_folder:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        parent_folder = f'{timestamp}_NEWCASE'
    
    evidence_folder = args.evidence
    if not evidence_folder:
        evidence_folder = 'EVIDENCE'
    
    try:
        os.makedirs(parent_folder)
        os.makedirs(os.path.join(parent_folder, evidence_folder))
        folders = ['Documents', 'Extracts', 'Pictures', 'Videos', 'Reports']
        for folder in folders:
            os.makedirs(os.path.join(parent_folder, evidence_folder, folder))
    except Exception as e:
        print(f'Error: {e}')
    else:
        print(f'Successfully created case folder "{parent_folder}" with evidence "{evidence_folder}" and sub-folders.')

if __name__ == '__main__':
    main()
