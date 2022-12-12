## [YOLOv5](https://github.com/ultralytics/yolov5)無人機影像辨識


### 0.環境配置

安裝必要的python package和配置相關環境

```
# python3.9
# Pytorch

# git clone yolo v5 repo
git clone https://github.com/ultralytics/yolov5 # clone repo
# 安裝必要的Pytorch套件
pip install -r requirements.txt

安裝完Python及Pytorch後即可使用
```

### 1.下載檔案和模型

先到[Google雲端](https://drive.google.com/file/d/1fEzqibY4f4cPhFUk-V3eVRywVwaG8esJ/view?usp=share_link)下載模型，之後下載github內的檔案後再將模型移入...\Tbrain-Drone-main路徑下。

### 2. 資料集設定

- 在...\Tbrain-Drone-main下，建立新資料夾並命名「original_data」並將大會提供訓練資料集train移入。
- 在...\Tbrain-Drone-main\original_data路徑下新建資料夾「test」
- 將Public Testing Dataset_v2 和 Private Testing Dataset_v2解壓縮後的圖檔全部移入...\Tbrain-Drone-main\original_data\test內
- 若要訓練模型，依序執行前置處理程式step_1_preprocessing_data_split.py、step_2_preprocessing_data_augmentation.py、step_3_preprocessing_preparing_labels.py   (若無需使用擴增，則不必執行step_2_preprocessing_data_augmentation.py)
- 在YOLOv5下，若有需要重新訓練模型，則需開啟...\Tbrain-Drone-main\YOLOv5路徑下的train.py，並調整參數後執行即可

### 3.影像偵測辨識`detect.py`

在...\Tbrain-Drone-main\YOLOv5路徑下開啟此檔案後，按下執行即可開始進行辨識。

 ```python
 def parse_opt():
     ...
    將從雲端上下載的訓練完的模型安裝到指定路徑後，使用預設參數即可進行辨識。
    ...
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='../R_4_2_x.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default='../original_data/test/', help='file/dir/URL/glob/screen/0(webcam)')
    #parser.add_argument('--source', type=str, default='2', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'data/coco128.yaml', help='(optional) dataset.yaml path')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[1080,1920], help='inference size h,w')
    parser.add_argument('--conf-thres', type=float, default=0.35, help='confidence threshold')
    parser.add_argument('--iou-thres', type=float, default=0.35, help='NMS IoU threshold')
    parser.add_argument('--max-det', type=int, default=1000, help='maximum detections per image')
 ```
 
 ### 4.偵測辨識圖檔
 
 至...\Tbrain-Drone-main\YOLOv5\runs路徑下，第一次執行結果在exp資料夾下，第二次在exp2資料夾下，
開啟對應資料夾後即可讀取偵測圖檔。
 
  ### 5.辨識結果文檔（.csv檔）
  
  偵測辨識完畢後會將要上傳的偵測結果csv文檔輸出至...\Tbrain-Drone-main\YOLOv5路徑下，檔名預設為R_5_3_test.csv。
  
 ```python
  ...
  detect.py檔名設定
  ...
  
  df.to_csv('R_5_3_test.csv', header=None, index=False)  #預設csv檔名為R_5_3_test.csv
  
 ```
