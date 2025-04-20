import sys
from ultralytics import YOLO
import cv2
import numpy as np
import time
# retirei a parte de alarme sonoro, pois o codigo difere conforme o sistema operacional
#import pygame  # Descomente essa linha para Linux/Mac
# def setup_pygame():
#     """Inicializa o pygame e retorna o mixer configurado"""
#     pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
#     # Retorna que a inicialização foi feita com sucesso
#     return True

# def play_alarm_sound():
#     """Reproduz um som de alarme usando pygame"""
#     # Verifica se o pygame já foi inicializado
#     if not hasattr(play_alarm_sound, "initialized"):
#         play_alarm_sound.initialized = setup_pygame()
    
#     # Método 1: Usando pygame para gerar um beep
#     pygame.mixer.Sound(pygame.sndarray.make_sound(
#         np.array([4096 * np.sin(2.0 * np.pi * 440.0 * x / 44100) for x in range(0, 44100 // 2)]).astype(np.int16)
#     )).play()
#     #time.sleep(0.5)  # Espera um pouco para não sobrecarregar o sistema
# Carrega o modelo treinado
model = YOLO('yolo12x.pt')  # Substitua pelo caminho do seu modelo treinado YOLOv8

# Carrega os nomes das classes
model_names = model.names

import os

# Obtém o nome do arquivo de vídeo a partir dos argumentos da linha de comando
video_file = sys.argv[1] if len(sys.argv) > 1 else None

# Inicializa a captura de vídeo
if video_file:
    if os.path.exists(video_file):
        cap = cv2.VideoCapture(video_file)  # Usa o arquivo de vídeo fornecido
    else:
        print(f"Arquivo de vídeo {video_file} não encontrado. Usando webcam.")
        cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(0)  # Usa a webcam padrão se nenhum arquivo for fornecido

# Define a resolução desejada
largura = 640
altura = 480

# Define a largura e a altura da webcam
cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)

# Define o codec e cria o objeto VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para vídeos MP4
out = cv2.VideoWriter('pred_yolo_captura_webcam.mp4', fourcc, 20.0, (largura, altura))  # Nome do arquivo, codec, FPS e resolução

# Selecionamos as apenas as classes abaixo criar os frames e gerar alarmes
class_to_show = ['knife', 'scissors', 'fork']

# Variáveis para controle do alarme
alarme_ativo = False
ultimo_alarme = 0
intervalo_alarme = 2  # segundos entre alarmes para não sobrecarregar

# Contagem de frames para limitar a frequência do alarme sonoro
frame_count = 0
alarm_frame_interval = 20  # Tocar alarme a cada N frames quando objeto for detectado

# Fonte para o aviso de alarme
fonte = cv2.FONT_HERSHEY_SIMPLEX
espessura_fonte = 2

while(True):
    # Captura um frame da webcam
    ret, frame = cap.read()
    frame_count += 1
    
    if ret == True:
        # Cria uma cópia do frame original para eventual aplicação do efeito de alarme
        frame_original = frame.copy()
        
        # Flag para verificar se algum objeto perigoso foi detectado neste frame
        objeto_perigoso_detectado = False
        
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

                # Define um limiar de confiança (opcional)
                if confidence < 0.5:
                    continue

                # Obtém o índice da classe
                class_index = int(box.cls[0].item())
                class_name = model_names[class_index]
                
                if class_name in class_to_show:
                    objeto_perigoso_detectado = True
                    
                    # Desenha a caixa delimitadora e o rótulo na imagem com cor vermelha para destacar o perigo
                    label = f'{class_name} {confidence:.2f}'
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)  # Vermelho e mais espesso
                    cv2.putText(frame, label, (x1, y1 - 10), fonte, 0.7, (0, 0, 255), espessura_fonte)
        
        # Se um objeto perigoso foi detectado, ativa o sistema de alarme
        tempo_atual = time.time()
        if objeto_perigoso_detectado:
            # Atualiza o status do alarme
            alarme_ativo = True
            
            # ALARME VISUAL: Adiciona um overlay vermelho semitransparente
            overlay = frame.copy()
            cv2.rectangle(overlay, (0, 0), (largura, altura), (0, 0, 255), -1)  # Retângulo vermelho
            # Aplica o overlay com transparência
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            
            # Adiciona texto de alerta
            texto_alerta = "ALERTA! OBJETO PERIGOSO DETECTADO!"
            tamanho_texto = cv2.getTextSize(texto_alerta, fonte, 1, espessura_fonte)[0]
            posicao_x = (largura - tamanho_texto[0]) // 2  # Centraliza o texto
            cv2.putText(frame, texto_alerta, (posicao_x, 50), fonte, 1, (255, 255, 255), espessura_fonte)
            
            # # ALARME SONORO: Toca o som de alarme a cada N frames e respeitando o intervalo mínimo
            # if (tempo_atual - ultimo_alarme) > intervalo_alarme and frame_count % alarm_frame_interval == 0:
            #     play_alarm_sound()
            #     ultimo_alarme = tempo_atual
        else:
            alarme_ativo = False

        # Exibe o frame com as detecções
        cv2.imshow('YOLOv8 Detection', frame)

        # Grava o frame no arquivo de vídeo
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