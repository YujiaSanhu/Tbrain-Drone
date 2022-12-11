import numpy as np
import shutil
import cv2
import os

# 新增擴增訓練集的資料夾
to_dir = './original_data/train_1/'
if(not os.path.exists(to_dir)):
    os.mkdir(to_dir)

# 從原訓練集擴增
from_dir = './original_data/train/'
all_files = os.listdir(from_dir)
for file_name in all_files:
    shutil.copy(from_dir+file_name, to_dir+file_name)
    case_name = file_name.split('.')[0]
    file_ext = file_name.split('.')[-1]
    if(file_ext=='png'):
        img = cv2.imread(from_dir+file_name)
        h, w, c = img.shape
        # 截圖隨機選左上點
        x_min = np.random.rand()*0.2
        y_min = np.random.rand()*0.2
        # 隨機選擇截圖比例決定右下點
        rr = 1-np.random.rand()*0.1 # random ratio
        min_len = 1-x_min if (1-x_min)<(1-y_min) else 1-y_min
        ratio = min_len*rr
        x_max, y_max = x_min+ratio, y_min+ratio
        # 截圖
        from_row, to_row = int(y_min*h), int(y_max*h)
        from_col, to_col = int(x_min*w), int(x_max*w)
        crop_img = img[from_row:to_row, from_col:to_col,:]
        # 放大回原圖大小
        new_img = cv2.resize(crop_img, [w,h])
        new_img_name = case_name+'_1.png'
        cv2.imwrite(to_dir+new_img_name, new_img)
        # 調整截圖後的標註座標資訊
        txt_name = case_name + '.txt'
        bbox_info = np.loadtxt(from_dir+txt_name, delimiter=',')
        # [class_num, upper_left_x, upper_left_y, width, height]
        if(bbox_info.ndim==1):
            bbox_info = bbox_info.reshape(1,-1)
        n_obj, n_feat = bbox_info.shape
        new_bbox_info = []
        for j in range(n_obj):
            cls_ = bbox_info[j,0]
            new_x =  int((bbox_info[j,1]-from_col)/ratio)
            new_y =  int((bbox_info[j,2]-from_row)/ratio)
            new_w =  int(bbox_info[j,3]/ratio)
            new_h =  int(bbox_info[j,4]/ratio)
            # 處理可能被截掉的邊界
            if(new_x<(w-1) and new_y<(h-1) and (new_x+new_w)>1 and (new_y+new_h)>1):
                if(new_x<0):
                    new_w = new_x+new_w
                    new_x = 1
                if(new_y<0):
                    new_h = new_y+new_h
                    new_y = 1
                if((new_x+new_w)>w):
                    new_w = w-new_x-1
                if((new_y+new_h)>h):
                    new_h = h-new_y-1
                new_bbox_info.append([cls_, new_x, new_y, new_w, new_h])
        new_bbox_info = np.array(new_bbox_info)
        new_txt_name = case_name + '_1.txt'
        np.savetxt(to_dir+new_txt_name, new_bbox_info, delimiter=',', fmt='%d')
