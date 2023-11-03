import boto3
import csv
import os

with open('vc_aws_credentials.csv', 'r') as file:
  next(file)
  reader = csv.reader(file)

  for line in reader:
    access_key_id = line[0]
    secret_acess_key = line[1]

client = boto3.client('rekognition', region_name='us-east-1', 
                      aws_access_key_id=access_key_id, aws_secret_access_key=secret_acess_key)

# Caminho para a pasta com as imagens
foulder = r'C:\\Users\\gabya\Documents\\IC - Redes Sociais\\VC - AWS\\2º turno'

# Lista de nomes de arquivos na pasta
img_files = os.listdir(foulder)

# Lista para armazenar os resultados
results = []

# Para cada arquivo na pasta, chame a API Rekognition para detectar rótulos
for file_ in img_files:
  foulder_file = os.path.join(foulder, file_)

  # Chama a API Rekognition para detectar rótulos no arquivo
  with open(foulder_file, 'rb') as image_file:
    response = client.detect_labels(Image={'Bytes': image_file.read()})

  # Extrai os rótulos associados ao arquivo
  labels = [{'Nome': label['Name'], 'Confiança': label['Confidence']} for label in response['Labels']]

  # Adiciona os resultados à lista
  results.append({'Nome do Arquivo': file_, 'Rótulos': labels})

# Escreve os resultados em um arquivo CSV
with open('results_3.csv', 'w', newline='') as csvfile:
  names = ['Nome do Arquivo', 'Rótulos']
  writer = csv.DictWriter(csvfile, fieldnames=names)
  writer.writeheader()
  for result in results:
    writer.writerow(result)