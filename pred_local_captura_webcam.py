from ultralytics import YOLO
import cv2

# Carrega o modelo treinado
# model = YOLO('runs/train/exp/weights/best.pt')  # Substitua pelo caminho do seu modelo treinado
model = YOLO('runs/detect/train13/weights/best.torchscript')
# Carrega os nomes das classes
model_names = model.names

# Inicializa a webcam
cap = cv2.VideoCapture(0)  # 0 é o índice da webcam padrão

# Define a resolução desejada
largura = 640
altura = 480

# Define a largura e a altura da webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)

# Verifica se a webcam foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a webcam")
    exit()

# Define o codec e cria o objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para vídeos AVI
out = cv2.VideoWriter('pred_local_captura_webcam.mp4', fourcc, 20.0, (largura, altura))  # Nome do arquivo, codec, FPS e resolução
# selecionamos as apenas as classes abaixo criar os framaes e gerar alarmes
class_to_show = ['knife', 'scissors', 'fork']

# Verifica se o VideoWriter foi criado corretamente
if not out.isOpened():
    print("Erro ao criar o arquivo de vídeo")
    cap.release()
    exit()

while(True):
    # Captura um frame da webcam
    ret, frame = cap.read()

    if ret == True:
        # Realiza a detecção
        results = model.predict(frame)

        # Percorre os resultados
        for result in results:
            boxes = result.boxes  # Obtém as caixas delimitadoras
            for box in boxes:
                # Obtém as coordenadas da caixa delimitadora
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())

                # Obtém a confiança da detecção
                confidence = box.conf[0].item()

                # Obtém o índice da classe
                class_index = int(box.cls[0].item())
                class_name = model_names[class_index]
                if  class_name in class_to_show:
                    # Desenha a caixa delimitadora e o rótulo na imagem
                    label = f'{model.names[class_index]} {confidence:.2f}'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Exibe o frame com as detecções
        cv2.imshow('YOLOv8 Detection', frame)

        # Grava o frame no arquivo de vídeo
                # Testes antes de gravar o frame
        if frame is None:
            print("Erro: Frame está vazio")
        elif frame.shape != (480, 640, 3):
            print(f"Erro: Tamanho do frame incorreto: {frame.shape}")
        elif not out.isOpened():
            print("Erro: VideoWriter não está aberto")
        else:
            # Grava o frame no arquivo de vídeo
            print("Gravando frame...")
            out.write(frame)

        # Sai do loop se a tecla 'q' for pressionada
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Libera os recursos
cap.release()
out.release()
cv2.destroyAllWindows()
# EOF