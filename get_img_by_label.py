import shutil
import os
import random
import glob
images_folder = "Process_data/data_corner_BSX/images/train" #folder chua tat ca anh 
labels_folder = "Process_data/labels_plate" # folder labels goc
labels_folder_result="D:/labels/train" #copy  labels
#Lấy ảnh tương ứng với nhãn
total_files = len(os.listdir(images_folder))
print(total_files)
for file in os.listdir(images_folder):
# Copy labels
    try:
     shutil.copy(os.path.join(labels_folder, file[:-3] + 'txt'), os.path.join(labels_folder_result, file[:-3] + 'txt'))
     print("copy labels :",file[:-3] + 'txt')
    except: print("anh ko label ",file)
#
print(len(os.listdir(labels_folder_result)))
print("done")
