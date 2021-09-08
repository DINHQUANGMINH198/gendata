from utils.general import scale_coords
from detection import Detection
import os
import cv2
import numpy as np
import json
import shutil
import glob

path_img_crop_car = "D:/data_motor/motobike/TN&MT_GAPA/train/images_crop"
path_labels_crop_car = "D:/data_motor/motobike/TN&MT_GAPA/train/labels_txt"
detector = Detection(path_weight="D:/yolov5/yolov5s.pt")
def cvt_points(p0,p1):
    x_crop = abs(p0[0] - p1[0])
    y_crop = abs(p0[1] - p1[1])
    return(x_crop,y_crop)
def access_json (path_json):
    with open(path_json, "r") as file:
        data = json.load(file)
        # print(data)
        obj = data["objects"]
        # print(type(obj))
        corner = obj[0]
        corner = corner["points"]
        # print(corner,type(corner))
        tl= corner['topleft']
        tr= corner['topright']
        br= corner['bottomright']
        bl= corner['bottomleft']
        list_points =[tl,tr,br,bl]
    return list_points    
def process_crop(path_img):
    img =cv2.imread(path_img)        
    img = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, channels = img.shape
    outs, img_shape = detector.detect(img)
    check = False
    roi = None
    size_img_crop = None
    c1 = None
    for i,det in enumerate(outs):
        if len(det):
            # print(len(det))
            det[:, :4]= scale_coords(img_shape,det[:, :4],img.shape).round()   
            for *xyxy,conf,cls in reversed(det):
                if cls==3 and conf > 0.4:
                    c1, c2 =(int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                    # print(c1,c2)
                    roi = img[c1[1]:c2[1], c1[0]:c2[0]]
                    w_crop = c2[0] - c1[0]
                    h_crop = c2[1] - c1[1]
                    size_img_crop = (w_crop,h_crop)
                    check = True
    # result = [check, roi , size_img_crop,c1]                
    return check,roi,size_img_crop,c1
labels_folder = "D:/data_motor/motobike/TN&MT_GAPA/train/json_annotations" # folder labels goc
images_folder ="D:/data_motor/motobike/TN&MT_GAPA/train/images_labeled" #copy anh tương ứng labels
for file_img in os.listdir( images_folder):
    name_img = file_img
    # print(file_img)
    path_img = images_folder + '/' + file_img
    name_json = name_img[:-3]+"json"
    path_json = labels_folder +'/'+name_json
    # print(path_img)
    # print(path_json)
    # list_points = access_json(path_json=path_json)
    check,img_crop,size_new,c1 = process_crop(path_img)   
    # check = outs[0] # check xem  detect được car trong ảnh ko
    if check ==True :
        print(file_img)
        list_points = access_json(path_json=path_json) # truy xuất lấy tọa độ 4 góc trong file json
        tl= list_points[0]
        tr= list_points[1]
        br= list_points[2]
        bl= list_points[3]
        # save img crop
        # img_crop = outs[1]
        img_crop_name = name_img
        cv2.imwrite(os.path.join(path_img_crop_car,img_crop_name),img_crop)
        # print("car")
        # size_new = outs[2]
        # print(size_new)
        # c1 = outs[3]
        tl_crop = cvt_points(tl,c1) 
        tr_crop = cvt_points(tr,c1) 
        br_crop = cvt_points(br,c1) 
        bl_crop = cvt_points(bl,c1) 

        # image = cv2.imread(os.path.join(path_img_crop_car,img_crop_name))
        # image = cv2.circle(image, tl_crop, radius = 10,  color = (0, 0, 255), thickness=-1)
        # image = cv2.circle(image, tr_crop, radius = 10,  color = (0, 0, 255), thickness=-1)
        # image = cv2.circle(image, br_crop, radius = 10,  color = (0, 0, 255), thickness=-1)
        # image = cv2.circle(image, bl_crop, radius = 10,  color = (0, 0, 255), thickness=-1)

        # cv2.imshow("window_name", image)
        # cv2.waitKey(0)
        label_1 = "0 " + str(tl_crop[0]/size_new[0]) +" "+ str(tl_crop[1]/size_new[1])+" " + str(15/size_new[0]) +" "+ str(15/size_new[1])+ '\n'
        label_2 = "1 " + str(tr_crop[0]/size_new[0]) +" "+ str(tr_crop[1]/size_new[1])+" " + str(15/size_new[0]) +" "+ str(15/size_new[1])+ '\n'
        label_3 = "2 " + str(br_crop[0]/size_new[0]) +" "+ str(br_crop[1]/size_new[1])+" " + str(15/size_new[0]) +" "+ str(15/size_new[1])+ '\n'
        label_4 = "3 " + str(bl_crop[0]/size_new[0]) +" "+ str(bl_crop[1]/size_new[1])+" " + str(15/size_new[0]) +" "+ str(15/size_new[1])
        labels = label_1 + label_2 +label_3 +label_4
        # print(labels)
        name_txt = name_img[:-3] + "txt"    
        print(name_txt)
        with open(path_labels_crop_car+ "/"+ name_txt, 'w') as f:
                f.write(labels)
        f.close()
