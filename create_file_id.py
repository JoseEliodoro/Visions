import os
import pandas as pd
from typing import List

def load_data(path: str, extension: str) -> List[str] : 
  """ extension: '.jpg' or '.mp4' or '.jpeg' """
  data = list(filter(
    lambda item: item.find(extension) >= 0,
    [ path+'/'+item for item in os.listdir(path)],
  ))
  
  return data

def filterPerfis(perfis: List[str], lista):
  new_lista = []
  for perfil in perfis:
    new_lista.extend(list(filter(
      lambda item: item.find(perfil) >= 0,
      lista
    )))
  return new_lista

def extractID(file: str, perfil: str, exetension: str, paths=[]) -> str:
  file = file.replace(perfil, '')
  file = file.replace(exetension, '')
  for path in paths:
    file = file.replace(path+'/', '')
  return file

def create_file_id(perfis: List[str], path_turnos: List[str]):
  
  files : List[str]= []
  for turno in path_turnos:
    files.extend(load_data(turno, '.jpg'))
  files = filterPerfis(perfis, files)

  data = []
  for file in files:
    if (perfis[0] in file):
      data.append({'File': file, 'ID':extractID(file, perfis[0], '.jpg', path_turnos)})
    elif (perfis[1] in file):
      data.append({'File': file, 'ID':extractID(file, perfis[1], '.jpg', path_turnos),})

  data = pd.DataFrame(data)
  data.set_index(['ID'], inplace=True)
  data[['File']].to_csv('data/File-id.csv')