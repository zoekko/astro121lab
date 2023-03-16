import glob
import numpy as np
import os
import regex as re

'''
instructions
1. pip install regex
2. cd to scripts folder
3. run this file
'''

def get_folders(dir, path=True):
    result = []
    for subdir_name in os.listdir(dir):
        subdir_path = os.path.join(dir, subdir_name)
        if os.path.isdir(subdir_path):
            if path:
                result = np.append(result, subdir_path)
            else:
                result = np.append(result, subdir_name)
    return result   

def run():
    data_folder = '../data'
    save_folder = '../combined_data'
    
    # create save dir
    os.makedirs(save_folder, exist_ok = True)
    
    # iterate through target dirs: ['moon', 'sun']
    for target_name in get_folders(data_folder, path=False): 
        
        # create save subdir
        save_subdir = f'{save_folder}/{target_name}'
        os.makedirs(save_subdir, exist_ok = True)
        
        # iterate through data dirs
        data_dir_paths = get_folders(os.path.join(data_folder, target_name), path=True)
        for fpath in data_dir_paths:
            name = re.findall(r'[a-zA-Z0-9_]*$', fpath)[0]
            
            # iterate through data in data dir
            fnames = glob.glob(fpath + '/*.npy')
            result = []
            for f in fnames:
                data = np.load(f, allow_pickle=True).tolist()
                result = np.append(result, data)
                
            # sort data by time
            sorted_result = sorted(result, key=lambda d: d.get('time'))
            
            # save sorted data
            np.save(f'{save_subdir}/{name}', sorted_result)
            print(f'{name}: {int(len(result))}')
            
run()