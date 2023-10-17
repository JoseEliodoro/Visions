import pandas as pd
import os
from create_file_id import create_file_id
from typing import List
import google_vision
import aws_vision

def MAIN(data_entry: pd.DataFrame, path: str, vision: int) -> None:
  
  for i in range(len(data_entry)):
    """ 
    new_data = pd.DataFrame([], columns=['ID', 'Class', 'Percent','Subclass',])
    print('oi') 
    """
    if (vision == 1):
      new_data = google_vision.load_labels(path_image=data_entry.iloc[i]['File'], fileID=data_entry.iloc[i]['ID'])
      if not os.path.isfile(path):
        data = pd.DataFrame([], columns=['ID', 'Class', 'Percent','Subclass',])
      else:
        data = pd.read_csv(path)
      data = pd.concat(([data, new_data]))
      data.set_index(['ID'], inplace=True)
      data[["Class", "Percent", "Subclass"]].to_csv(path)
    elif (vision == 2):
      aws_vision.load_labels('s', 'dfa')
      
def createFileVision(
  perfis: List[str],
  path_turnos: List[str],
  vision: int =1,
  path_vision: str='Vision.csv',
  ) -> None:
  """ 
    vision: 1 for google or 2 for amazon
    path: path file vision in csv
  """
  create_file_id(
    perfis= perfis,
    path_turnos= path_turnos
  )
  if vision == 1:
    if not os.path.isfile(path_vision):
      data = pd.DataFrame([], columns=['ID', 'Class', 'Percent','Subclass',])
    else:
      data = pd.read_csv(path_vision)
  elif vision == 2:
    if not os.path.isfile(path_vision):
      data = pd.DataFrame([], columns=['ID', 'Class', 'Percent','Subclass',])
    else:
      data = pd.read_csv(path_vision)
      
  
  data_file_id = pd.read_csv('data/File-id.csv')
  
  data_entry = data_file_id.loc[~data_file_id['ID'].isin(data['ID'])]
  k = 50
  print(data_entry)
  for d in range(k, len(data_entry)+50, k):
    print(f'Faltam {d-k, d, len(data_entry)-d} arquivos')
    MAIN(data_entry[d-k: d], path=path_vision, vision=vision)

createFileVision(
  vision=1,
  path_vision='data/GoogleVision.csv',
  perfis= ['@lulaoficial', '@bolsonaromessiasjair'],
  path_turnos= ['2º turno', '1º turno - Lula', '1º turno - Bolsonaro'],
)
