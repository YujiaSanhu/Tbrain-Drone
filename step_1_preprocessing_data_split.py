import numpy as np
import shutil
import os

# 新增val資料夾
val_dir = './original_data/val/'
if(not os.path.exists(val_dir)):
    os.mkdir(val_dir)

# random split
random_list = np.random.permutation(1000)+1
case_dict = {'train':random_list[:750], 'val':random_list[750:]}

# 重新分配samples至val資料夾
from_dir = './original_data/train/'
for case_idx in case_dict['val']:
    img_name = 'img'+str(case_idx).zfill(4)+'.png'
    txt_name = 'img'+str(case_idx).zfill(4)+'.txt'
    shutil.move(from_dir+img_name, val_dir+img_name)
    shutil.move(from_dir+txt_name, val_dir+txt_name)
