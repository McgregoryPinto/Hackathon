import torch
import cv2
import numpy as np
import os
imagedir = 'dataset/archive'
def normalize_yolo(pxcenter, pycenter, pxlarge, pylarge, pwidth, pheight):
    ixcenter = pxcenter / pwidth
    iycenter = pycenter / pheight
    ixlarge = pxlarge / pwidth
    iylarge = pylarge / pheight
    return ixcenter, iycenter, ixlarge, iylarge
# Carrega o modelo
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5s.pt', force_reload=True)
#model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
print(model.names  )

for filename in os.listdir(imagedir):
    if filename.endswith('.jpg'):
        img_filename = os.path.join(imagedir, filename)
        print(f' ################## img_filename {img_filename}')
        img = cv2.imread(img_filename)
        height, width, _ = img.shape
        # Define os nomes das classes
        class_names = ['knife', 'scissors', 'fork']
 
        results = model(img)    
        confidence_threshold = 0.9
        class_to_show = ['knife', 'scissors', 'fork']
        for *xyxy, conf, cls in results.xyxy[0]:
            class_index = int(cls)
            class_name = model.names[class_index]
            if  class_name in class_to_show:
                print(f' ################## DETECTED {img_filename} class_name {class_name}')
                x1, y1, x2, y2 = map(int, xyxy)
                xcenter = ((x1 + x2) // 2)
                ycenter = ((y1 + y2) // 2)
                xlarge = x2 - x1
                ylarge = y2 - y1
                xcenter, ycenter, xlarge, ylarge = normalize_yolo(xcenter, ycenter, xlarge, ylarge, width, height)
                print(xcenter, ycenter, xlarge, ylarge)
                # Desenha as caixas delimitadoras na imagem
                cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                # Adiciona o nome da classe e a confiança na imagem
                label = f'{class_name} {conf:.2f}'
                cv2.putText(img, label, (x1, (y1+5)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                # Salva a imagem com as caixas delimitadoras e os nomes das classes
                output_filename = os.path.join('dataset/archive_delimiters_view', filename)
                cv2.imwrite(output_filename, img)

        results.print()