import os
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--case', nargs='?', type=str, help='Name of the case folder')
    parser.add_argument('-e', '--evidence', nargs='+', type=str, help='Name of the evidence folder(s)')
    args = parser.parse_args()
    
    parent_folder = args.case
    if not parent_folder:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        parent_folder = f'{timestamp}_NEWCASE'
    
    evidence_folders = args.evidence
    if not evidence_folders:
        evidence_folders = ['EVIDENCE']
    
    try:
        if not os.path.exists(parent_folder):
            os.makedirs(parent_folder)
        
        for evidence_folder in evidence_folders:
            if not os.path.exists(os.path.join(parent_folder, evidence_folder)):
                os.makedirs(os.path.join(parent_folder, evidence_folder))
            
            folders = ['Documents', 'Extracts', 'Pictures', 'Videos', 'Reports']
            for folder in folders:
                if not os.path.exists(os.path.join(parent_folder, evidence_folder, folder)):
                    os.makedirs(os.path.join(parent_folder, evidence_folder, folder))
    except Exception as e:
        print(f'Error: {e}')
    else:
        print(f'Successfully created case folder "{parent_folder}" with evidence "{evidence_folders}" and sub-folders.')

if __name__ == '__main__':
    main()
