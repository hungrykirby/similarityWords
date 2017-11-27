import os
IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/tests/'
files = os.listdir(IMG_DIR)
for f in files:
    if f == '.DS_Store':
        continue
    else:
        #root_path, ext = os.path.splitext( os.path.basename(file_path))
        print(f.split("."))

#IMG_DIR = os.path.abspath(os.path.dirname(__file__)) + '/images/'
