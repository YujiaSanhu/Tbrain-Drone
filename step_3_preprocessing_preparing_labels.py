import numpy as np
import shutil
import cv2
import os

# 新增偵測資料集的資料夾

#data_dir = './datasets_1/' #使用第二步的擴增資料請反註解此行
data_dir = './datasets/'    #使用原始資料

if(not os.path.exists(data_dir)):
    os.mkdir(data_dir)

#phase_list = ['train_1', 'val'] #使用第二步的擴增資料請反註解此行
phase_list = ['train', 'val']  #使用原始資料

folder_list = ['images','annotations','labels','img_gt']

for phase in phase_list:
    phase_dir = data_dir+phase
    if(not os.path.exists(phase_dir)):
        os.mkdir(phase_dir)
    for folder in folder_list:
        new_dir = data_dir+phase+'/'+folder
        if(not os.path.exists(new_dir)):
            os.mkdir(new_dir)

# 類別與名稱對照
label_class = {0:'car', 1:'hov', 2:'person', 3:'motorcycle'}
# 類別與顏色對照 {0:cyan, 1:yellow, 2:red, 3:blue}
label_color = {0:(255,255,0), 1:(0,255,255), 2:(0,0,255), 3:(255,0,0)}

# 整理檔案歸類
from_dir = './original_data/'
for phase in phase_list:
    print(phase)
    phase_dir = from_dir+phase+'/'
    to_dir = data_dir+phase
    all_files = os.listdir(phase_dir)
    for file_name in all_files:
        case_name = file_name.split('.')[0]
        file_ext = file_name.split('.')[-1]
        #print(case_name)
        if(file_ext=='png'):
            img = cv2.imread(phase_dir+file_name)
            width = img.shape[1]
            height = img.shape[0]
            txt_name = case_name +'.txt'
            # [class_num, upper_left_x, upper_left_y, width, height]
            bbox_info = np.loadtxt(phase_dir+txt_name, delimiter=',')
            if(bbox_info.ndim==1):
                if(bbox_info.shape[0]==0):
                    shutil.copy(phase_dir+file_name, to_dir+'/images/'+file_name)
                    shutil.copy(phase_dir+txt_name, to_dir+'/annotations/'+txt_name)
                    shutil.copy(phase_dir+file_name, to_dir+'/img_gt/'+file_name)
                    shutil.copy(phase_dir+txt_name, to_dir+'/labels/'+txt_name)
                    continue
                else:
                    bbox_info = bbox_info.reshape(1,-1)
            n_candidates = bbox_info.shape[0]
            canvas = img.copy()
            label_txt = []
            for j in range(n_candidates):
                lab = int(bbox_info[j,0])
                pt1 = (int(bbox_info[j,1]),int(bbox_info[j,2]))
                pt2 = (int(bbox_info[j,1]+bbox_info[j,3]),int(bbox_info[j,2]+bbox_info[j,4]))
                set_color = label_color[lab]
                cv2.rectangle(canvas, pt2, pt1, set_color, 1)
                # yolo txt [class_num, xc, yc, w, h]
                xc = (bbox_info[j,1]+bbox_info[j,3]/2)/width
                yc = (bbox_info[j,2]+bbox_info[j,4]/2)/height
                w = bbox_info[j,3]/width
                h = bbox_info[j,4]/height
                label_txt.append([lab, xc, yc, w, h])
            np.savetxt(to_dir+'/labels/'+txt_name, label_txt, fmt='%1.3f', delimiter=' ')
            shutil.copy(phase_dir+file_name, to_dir+'/images/'+file_name)
            shutil.copy(phase_dir+txt_name, to_dir+'/annotations/'+txt_name)
            cv2.imwrite(to_dir+'/img_gt/'+file_name, canvas)
    
