import os
import argparse
import datetime

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', type=str, default=None, help='Name of the parent folder')
    args = parser.parse_args()
    
    parent_folder = args.name
    if not parent_folder:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        parent_folder = f'{timestamp}_NEWCASE'
    
    try:
        os.makedirs(parent_folder)
        folders = ['Documents', 'Extracts', 'Pictures', 'Videos', 'Reports']
        for folder in folders:
            os.makedirs(os.path.join(parent_folder, folder))
    except Exception as e:
        print(f'Error: {e}')
    else:
        print(f'Successfully created parent folder "{parent_folder}" with sub-folders.')

if __name__ == '__main__':
    main()
