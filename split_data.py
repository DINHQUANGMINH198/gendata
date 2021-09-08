import shutil
import os
import random

images_folder = "D:/data_motor/motobike/TN&MT_GAPA/train/images_crop"
labels_folder ="D:/data_motor/motobike/TN&MT_GAPA/train/labels_txt"
train_folder = "D:/data_motor/motobike/TN&MT_GAPA/train/images/train"
val_folder = "D:/data_motor/motobike/TN&MT_GAPA/train/images/valid"
train_labels_folder = "D:/data_motor/motobike/TN&MT_GAPA/train/labels/train"
val_labels_folder = "D:/data_motor/motobike/TN&MT_GAPA/train/labels/valid"
################### STEP 1 ##########################
# for file in os.listdir(labels_folder):
#   # print(file)
# print(len(os.listdir(labels_folder)))
# total_files = len(os.listdir(images_folder))
# print(total_files)
# total_files_validation = int(1200)
# validaiton_files = random.choices(os.listdir(images_folder), k=total_files_validation)
# print(len(validaiton_files))
# for file in validaiton_files:
#     # print("Validation file ", file)
#     # Copy images
#     shutil.copy(os.path.join(images_folder, file), os.path.join(val_folder, file))

#     # Copy labels
#     try:
#      shutil.copy(os.path.join(labels_folder, file[:-3] + 'txt'), os.path.join(val_labels_folder, file[:-3] + 'txt'))
#     except:
#         print("Anh khong co label",file)
#         os.remove(os.path.join(val_folder,file))
############ STEP 2 ##########
for file in os.listdir(images_folder):
    if not (os.path.isfile(val_folder+'/'+file)):
        # print("Train img file ", file)
        # Copy images
        shutil.copy(os.path.join(images_folder, file), os.path.join(train_folder, file))
        try:
         shutil.copy(os.path.join(labels_folder, file[:-3] + 'txt'), os.path.join(train_labels_folder, file[:-3] + 'txt'))
        except:
         print("Anh khong co label",file)
       
print("done")
print(len(os.listdir(val_folder)))
print(len(os.listdir(val_labels_folder)))
print(len(os.listdir(train_folder)))
print(len(os.listdir(train_labels_folder)))
