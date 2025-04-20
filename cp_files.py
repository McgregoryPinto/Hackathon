import cv2
import numpy as np
import os
import shutil

imagedir = 'dataset/archive'
imagedir_detected = 'dataset/archive_detected'
imagedir_notdetected = 'dataset/archive_notdetected'
imagedir_prepared = 'dataset/archive_prepared'
imagedir_images = 'dataset/images'
imagedir_labels = 'dataset/labels'
imagedir_images_train = 'dataset/images/train'
imagedir_labels_train = 'dataset/labels/train'
imagedir_images_val = 'dataset/images/val'
imagedir_labels_val = 'dataset/labels/val'
def cp_file(orig_jpg, orig_jpg_path, classe):
    src_path_jpg=''
    dst_path_jpg=''
    src_path_txt=''
    dst_path_txt=''
    txt_filename=''
    if classe == 'val':
        # cp jpg para destino
        src_path_jpg = os.path.join(orig_jpg_path, orig_jpg)
        dst_path_jpg = os.path.join(imagedir_images_val, orig_jpg)
        # cp txt para destino
        txt_filename = orig_jpg.replace('.jpg', '.txt')
        src_path_txt = os.path.join(orig_jpg_path, txt_filename)
        dst_path_txt = os.path.join(imagedir_labels_val, txt_filename)
    elif classe == 'train':
        # cp jpg para destino
        src_path_jpg = os.path.join(orig_jpg_path, orig_jpg)
        dst_path_jpg = os.path.join(imagedir_images_train, orig_jpg)
        # cp txt para destino
        txt_filename = orig_jpg.replace('.jpg', '.txt')
        src_path_txt = os.path.join(orig_jpg_path, txt_filename)
        dst_path_txt = os.path.join(imagedir_labels_train, txt_filename)
    shutil.copyfile(src_path_jpg, dst_path_jpg)
    shutil.copyfile(src_path_txt, dst_path_txt)

def cp_train_files():
    # Copia os arquivos de treinamento para a pasta de destino
    count_files = 1
    for filename in os.listdir(imagedir_detected):
        if filename.endswith('.jpg'):
            # calcular os multiplos de 8 e 9 - mais ou menos 20% - fazendo os 80/20
            if count_files % 8 == 0 or count_files % 9 == 0:
                cp_file(filename,imagedir_detected,'val')
            else:
                cp_file(filename,imagedir_detected,'train')
            count_files += 1

cp_train_files()