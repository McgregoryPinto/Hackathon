from ultralytics import YOLO
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

biggerxidx = 0
biggeryidx = 1
xlargepos = 2
ylargepos = 3

def delete_files_in_directory(directory_path):
    # Verifica se o diretório existe
    if os.path.exists(directory_path):
        # Lista todos os arquivos no diretório
        files = os.listdir(directory_path)
        
        # Itera sobre os arquivos e os remove
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Arquivo {file_path} removido com sucesso.")
    else:
        print(f"Diretório {directory_path} não encontrado.")

def create_directories():
    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_prepared):
        # Cria a pasta
        os.makedirs(imagedir_prepared)
        print(f"Pasta '{imagedir_prepared}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_prepared}' já existe.")
        delete_files_in_directory(imagedir_prepared)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_detected):
        # Cria a pasta
        os.makedirs(imagedir_detected)
        print(f"Pasta '{imagedir_detected}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_detected}' já existe.")
        delete_files_in_directory(imagedir_detected)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_notdetected):
        # Cria a pasta
        os.makedirs(imagedir_notdetected)
        print(f"Pasta '{imagedir_notdetected}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_notdetected}' já existe.")
        delete_files_in_directory(imagedir_notdetected)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_images):
        # Cria a pasta
        os.makedirs(imagedir_images)
        print(f"Pasta '{imagedir_images}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_images}' já existe.")
        delete_files_in_directory(imagedir_images)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_images_train):
        # Cria a pasta
        os.makedirs(imagedir_images_train)
        print(f"Pasta '{imagedir_images_train}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_images_train}' já existe.")
        delete_files_in_directory(imagedir_images_train)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_images_val):
        # Cria a pasta
        os.makedirs(imagedir_images_val)
        print(f"Pasta '{imagedir_images_val}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_images_val}' já existe.")
        delete_files_in_directory(imagedir_images_val)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_labels):
        # Cria a pasta
        os.makedirs(imagedir_labels)
        print(f"Pasta '{imagedir_labels}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_labels}' já existe.")
        delete_files_in_directory(imagedir_labels)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_labels_train):
        # Cria a pasta
        os.makedirs(imagedir_labels_train)
        print(f"Pasta '{imagedir_labels_train}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_labels_train}' já existe.")
        delete_files_in_directory(imagedir_labels_train)

    # Verifica se a pasta já existe
    if not os.path.exists(imagedir_labels_val):
        # Cria a pasta
        os.makedirs(imagedir_labels_val)
        print(f"Pasta '{imagedir_labels_val}' criada com sucesso.")
    else:
        print(f"A pasta '{imagedir_labels_val}' já existe.")
        delete_files_in_directory(imagedir_labels_val)

def normalize_yolo(pxcenter, pycenter, pxlarge, pylarge, pwidth, pheight):
    ixcenter = pxcenter / pwidth
    iycenter = pycenter / pheight
    ixlarge = pxlarge / pwidth
    iylarge = pylarge / pheight
    return ixcenter, iycenter, ixlarge, iylarge

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
    elif classe == 'val_notdetect':
        # cp jpg para destino nao tem txt
        src_path_jpg = os.path.join(orig_jpg_path, orig_jpg)
        dst_path_jpg = os.path.join(imagedir_images_val, orig_jpg)
    elif classe == 'train_notdetect':
        # cp jpg para destino nao tem txt
        src_path_jpg = os.path.join(orig_jpg_path, orig_jpg)
        dst_path_jpg = os.path.join(imagedir_images_train, orig_jpg)
    # faz a copia dos arquivos
    shutil.copyfile(src_path_jpg, dst_path_jpg)
    if classe == 'train' or classe == 'val': # notdetect nao tem txt
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

def cp_notdetected_files():
    # Copia os arquivos de treinamento para a pasta de destino
    count_files = 1
    for filename in os.listdir(imagedir_notdetected):
        if filename.endswith('.jpg'):
            # calcular os multiplos de 8 e 9 - mais ou menos 20% - fazendo os 80/20
            if count_files % 8 == 0 or count_files % 9 == 0:
                cp_file(filename, imagedir_notdetected, 'val_notdetect')
            else:
                cp_file(filename, imagedir_notdetected, 'train_notdetect')
            count_files += 1
# main 
# Carrega o modelo YOLO11s
#model = YOLO('yolo11s.pt')  # Substitua pelo caminho do seu modelo treinado YOLOv8
# cria as pastas de trabalho
create_directories()

# inicia o reconhecimento dos objetos no dataset
model = YOLO('yolo12x.pt')  # Substitua pelo caminho do seu modelo treinado YOLOv8
model_names = model.names
print(model_names)


# Define os nomes das classes
class_names = ['knife', 'scissors', 'fork']
class_name = "undefined"
for filename in os.listdir(imagedir):
    if filename.endswith('.jpg'):
        img_filename = os.path.join(imagedir, filename)
        print(f' ################## img_filename {img_filename}')
        img = cv2.imread(img_filename)
        height, width, _ = img.shape
        results = model(img)

        # Define o limiar de confiança
        confidence_threshold = 0.7

        # Define as classes que você quer exibir
        class_to_show = ['knife', 'scissors', 'fork']

        # results.print()  # Removido para evitar erros

        biggerx = 0
        biggery = 0
        class_found = False

        for result in results:
            boxes = result.boxes
            # reservar biggerxidx e biggeryidx
            valores = np.array([[0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0],[0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0]])
            class_count = 0 
            for box in boxes:
                # Obtém as coordenadas da caixa delimitadora
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # Obtém a confiança da detecção
                confidence = box.conf[0].item()
                # Obtém o índice da classe
                class_index = int(box.cls[0].item())
                class_name = model_names[class_index]
                #print (f' ################## class_index {class_index} class_name {class_name}')

                # Obtém o nome da classe
                #class_name = class_names[class_index]

                if  class_name in class_to_show:
                    class_found = True
                    if class_count > 0:
                        filename_new = filename.replace('.jpg', f'_{class_count}.jpg')
                    else:
                        filename_new = filename
                    class_count = class_count + 1
                    print(f' ################## DETECTED {img_filename} class_name {class_name}')
                    #x1, y1, x2, y2 = map(int, xyxy) # removido pois ja foram mapeados
                    xcenter = ((x1 + x2) // 2)
                    ycenter = ((y1 + y2) // 2)
                    xlarge = x2 - x1
                    ylarge = y2 - y1
                    xcenter, ycenter, xlarge, ylarge = normalize_yolo(xcenter, ycenter, xlarge, ylarge, width, height)
                    # print(xcenter, ycenter, xlarge, ylarge)
                    txt_filename = filename_new.replace('.jpg', '.txt')
                    txt_filename = os.path.join(imagedir_detected, txt_filename)
                    #print(f' ################## txt_filename {txt_filename} xcenter {xcenter} ycenter {ycenter} xlarge {xlarge} ylarge {ylarge}')
                    with open(txt_filename, 'w') as f:
                        f.write(f'0 {xcenter} {ycenter} {xlarge} {ylarge}\n')
                    #f.close()
                    # salva uma imagem com o retangulo no objeto detectado e com o nome da classe identificado
                    img2 = img.copy()
                    output_filename = os.path.join(imagedir_detected, filename_new)
                    print(f' ################## output_filename {output_filename} x1 {x1} y1 {y1} x2 {x2} y2 {y2} ')
                    label = class_name
                    cv2.rectangle(img2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.imwrite(output_filename, img2)
                    cv2.putText(img2, label, (x1, (y1 + 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                    # salva a imagem no diretorio de prepared
                    img3 = img.copy()
                    output_filename3 = os.path.join(imagedir_prepared, filename_new)
                    cv2.imwrite(output_filename3, img3)
                    # salva o arquivo com os marcadores YOLO no prepared
                    txt_filename3 = filename_new.replace('.jpg', '.txt')
                    txt_filename3 = os.path.join(imagedir_prepared, txt_filename3)
                    #print(f' ################## txt_filename {txt_filename} xcenter {xcenter} ycenter {ycenter} xlarge {xlarge} ylarge {ylarge}')
                    with open(txt_filename3, 'w') as f:
                        f.write(f'0 {xcenter} {ycenter} {xlarge} {ylarge}\n')
                # salva a imagem nao detectada para analise
            if class_found == False:
                # salva a imagem no diretorio de notdetected
                img4 = img.copy()
                output_filename4 = os.path.join(imagedir_notdetected, filename)
                cv2.imwrite(output_filename4, img4)
                print(f' ################## NOT DETECTED {img_filename} class_name {class_name}')
# separa os arquivos em treino e teste
cp_train_files()
cp_notdetected_files()