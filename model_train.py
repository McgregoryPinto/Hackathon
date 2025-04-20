from ultralytics import YOLO

# Carrega um modelo pré-treinado (YOLOv5s, YOLOv5m, etc.) ou cria um novo modelo
model = YOLO('yolov8n.yaml')  # Cria um novo modelo a partir de um arquivo YAML
#model = YOLO('yolo12x.pt')  # Carrega um modelo pré-treinado

# Treina o modelo com o seu dataset
results = model.train(data='config.yaml', epochs=100, imgsz=640)  # Substitua 'config.yaml' pelo caminho do seu arquivo de configuração

# Avalia o modelo no conjunto de validação
metrics = model.val()

# Exporta o modelo treinado para um formato que pode ser usado para inferência
model.export(format='torchscript')