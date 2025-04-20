import torch
from ultralytics import YOLO
import cv2
import numpy as np
import os

def normalize_yolo(pxcenter, pycenter, pxlarge, pylarge, pwidth, pheight):
    ixcenter = pxcenter / pwidth
    iycenter = pycenter / pheight
    ixlarge = pxlarge / pwidth
    iylarge = pylarge / pheight
    return ixcenter, iycenter, ixlarge, iylarge
# Carrega o modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=True)
imagedir = 'dataset/archive'
imagedir_marcaddores = 'dataset/archive_detected'
biggerxidx = 0
biggeryidx = 1
xlargepos = 2
ylargepos = 3
# Define os nomes das classes
class_names = ['knife', 'scissors', 'fork']
 
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

        results.print()
        biggerx = 0
        biggery = 0
        class_found = False
        class_name = "undefined"
        for *xyxy, conf, cls in results.xyxy[0]:
            class_index = int(cls)
            class_name = model.names[class_index]
            if  class_name in class_to_show:
                class_found = True
                print(f' ################## DETECTED {img_filename} class_name {class_name}')
                x1, y1, x2, y2 = map(int, xyxy)
                xcenter = ((x1 + x2) // 2)
                ycenter = ((y1 + y2) // 2)
                xlarge = x2 - x1
                ylarge = y2 - y1
                xcenter, ycenter, xlarge, ylarge = normalize_yolo(xcenter, ycenter, xlarge, ylarge, width, height)
                # print(xcenter, ycenter, xlarge, ylarge)
                # reservar biggerxidx e biggeryidx
                valores = np.array([[0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0],[0.0, 0.0, 0.0, 0.0, 0, 0, 0, 0]])
                # Desenha as caixas delimitadoras na imagem
                if xlarge > biggerx:
                    biggerx = xlarge
                    valores[biggerxidx] = [xcenter, ycenter, xlarge, ylarge,int(x1), int(y1), int(x2), int(y2)]
                
                if ylarge > biggery:
                    biggery = ylarge
                    valores[biggeryidx] = [xcenter, ycenter, xlarge, ylarge,int(x1), int(y1), int(x2), int(y2)]
        # se encontrou a classe
        if class_found:
            # se os valores forem iguais copia do xlager 
            if valores[biggerxidx].all() == valores[biggeryidx].all():
                xcenter, ycenter, xlarge, ylarge,x1, y1, x2, y2 = valores[biggerxidx]
            # se ylager > xlarger copia de ylarger
            elif valores[biggeryidx,ylargepos] > valores[biggerxidx,xlargepos]:
                xcenter, ycenter, xlarge, ylarge,x1, y1, x2, y2 = valores[biggeryidx]
            else:
            # senao copia de xlarger
                xcenter, ycenter, xlarge, ylarge,x1, y1, x2, y2 = valores[biggerxidx]

            # criar um aquivo com o mesmo nome da img com extensão txt
            txt_filename = filename.replace('.jpg', '.txt')
            txt_filename = os.path.join(imagedir_marcaddores, txt_filename)
            print(f' ################## txt_filename {txt_filename} xcenter {xcenter} ycenter {ycenter} xlarge {xlarge} ylarge {ylarge}')
            with open(txt_filename, 'w') as f:
                f.write(f'0 {xcenter} {ycenter} {xlarge} {ylarge}\n')
            #f.close()
            img2 = img.copy()
            output_filename = os.path.join(imagedir_marcaddores, filename)
            print(f' ################## output_filename {output_filename} x1 {x1} y1 {y1} x2 {x2} y2 {y2} ')
            #label = f'{model.names[int(cls)]} {conf:.2f}'
            cv2.rectangle(img2, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.imwrite(output_filename, img2)
            #cv2.putText(img2, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        else:
            print(f' ################## NOT DETECTED {img_filename} class_name {class_name}')

    # # # Exibe a imagem com as detecções
    # # cv2.imshow('YOLOv5 Detection', img)
    # # cv2.waitKey(0)
    # # cv2.destroyAllWindows()