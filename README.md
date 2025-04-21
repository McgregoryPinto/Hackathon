
# Hackathon
Entrega final - AI for devs

## Aluno
Nome: Mcgregory D F R Pinto
Matricula: rm357350

## link github:
https://github.com/McgregoryPinto/Hackathon

## Instruções de Configuração

Para configurar o projeto, você precisa clonar o repositório YOLOv5 e instalar suas dependências. Execute os seguintes comandos:

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```
## Instruções para Baixar o Dataset

Para baixar o dataset do Kaggle, siga as instruções abaixo:

1. Acesse o link do dataset: [Knife, Scissors, and Cutter Detection Dataset](https://www.kaggle.com/datasets/feliparus/knife-scissors-and-cutter-detection-dataset/data)
2. Baixe os arquivos do dataset.
3. Coloque os arquivos no diretório `dataset` dentro do projeto.

4. Ao descompactar, as imagens estarão no diretório `dataset/archive`.

## Preparação do Dataset para YOLOv5

Para que o YOLOv5 funcione corretamente, as imagens precisam ter marcadores específicos para o treinamento. Siga os passos abaixo para preparar o dataset:

1. Execute o arquivo [`prepare_dataset.py`](./prepare_dataset.py) com o comando `python3 prepare_dataset.py` para preparar os dados.
2. Em seguida, execute o arquivo [`cp_files.py`](./cp_files.py) com o comando `python3 cp_files.py` para copiar os arquivos necessários.

Após esses passos, o modelo estará pronto para ser treinado localmente.

## Treinamento do Modelo

Para treinar o modelo, execute o arquivo `model_train.py` com o seguinte comando:

```bash
python3 model_train.py
```

## Teste com Webcam
## Interface Gráfica para Execução de Scripts

Para facilitar a execução dos scripts de detecção, você pode usar a interface gráfica disponível no arquivo `script_executor.py`. Esta interface permite selecionar qual script executar e se deseja usar um arquivo de vídeo ou a webcam.

Para usar a interface gráfica, execute o seguinte comando:

```bash
python script_executor.py
```

Certifique-se de ter todas as dependências instaladas conforme especificado no arquivo `requirements.txt`.


Para testar o modelo usando a sua webcam, você pode executar um dos seguintes arquivos:

1. Para usar o modelo treinado localmente, execute o arquivo [`pred_local_captura_webcam.py`](./pred_local_captura_webcam.py):

```bash
add-gui-and-update-requirements
python3 pred_local_captura_webcam.py [<caminho_do_video>]  # O parâmetro <caminho_do_video> é opcional. Se não for informado, a webcam será usada.

```

2. Para usar o modelo treinado da própria YOLO, execute o arquivo [`pred_yolo_captura_webcam.py`](./pred_yolo_captura_webcam.py):

```bash
python3 pred_yolo_captura_webcam.py [<caminho_do_video>]  # O parâmetro <caminho_do_video> é opcional. Se não for informado, a webcam será usada.
```


## Interface Gráfica para Execução de Scripts

Para facilitar a execução dos scripts de detecção, você pode usar a interface gráfica disponível no arquivo `script_executor.py`. Esta interface permite selecionar qual script executar e se deseja usar um arquivo de vídeo ou a webcam.

Para usar a interface gráfica, execute o seguinte comando:

```bash
python3 script_executor.py
```
## TO DO
Implementar na AWS 