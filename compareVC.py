import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



def test(dataGoogle: pd.DataFrame, dataAmazon: pd.DataFrame, filter: float):
  #dataGoogle = pd.read_csv('GoogleVision.csv')
  #dataAmazon = pd.read_csv('rekognition/result_not_duplicates.csv') 
  #dataAmazon.rename(columns={"porcentagem": "Percent", "Nome": "Class"}, inplace=True)
  dfGoogle = dataGoogle.loc[dataGoogle['Subclass'] != 'text']

  #print(f"""Quantidade de classes únicas da Google: {len(dataGoogle['Class'].unique())} 
  #  'Qtn sem textos' {len(dfGoogle['Class'].unique())} """) 
  #print(f"Quantidade de classes únicas da Amazon: {len(dataAmazon['Class'].unique())}") 
    
  qtnClassGoogle = dfGoogle.groupby(['Class']).size().reset_index(name='Total').sort_values('Total', ascending=False).head(20)
  qtnClassAmazon = dataAmazon.groupby(['Class']).size().reset_index(name='Total').sort_values('Total', ascending=False).head(20)
  
  #print(qtnClassGoogle)
  #print(qtnClassAmazon)
  plt.style.use('fivethirtyeight')
  figBarGoogle, axGoogle = plt.subplots(figsize=(22, 10))
  axGoogle.set(xlabel="QTN. item", ylabel="Class", title='Gráfico das 20 maiores classes do Google')
  axGoogle.barh(qtnClassGoogle['Class'], qtnClassGoogle['Total'])
  axGoogle.axvline(qtnClassGoogle['Total'].mean(), ls='dotted', color='r')
  figBarGoogle.savefig(f'img/Googlebar_{filter}.jpg')
  
  figBarAmazon, axAmazon = plt.subplots(figsize=(22, 10))
  axAmazon.set(xlabel="QTN. item", ylabel="Class", title='Gráfico das 20 maiores classes da Amazon')
  axAmazon.barh(qtnClassAmazon['Class'], qtnClassAmazon['Total'])
  axAmazon.axvline(qtnClassAmazon['Total'].mean(), ls='dotted', color='r')
  figBarAmazon.savefig(f'img/Amazonbar_{filter}.jpg')
  
def testa(dataGoogle: pd.DataFrame, dataAmazon: pd.DataFrame, per: int=0):
  dataGoogle = dataGoogle.loc[dataGoogle['Percent'] >= per]
  dataAmazon = dataAmazon.loc[dataAmazon['Percent'] >= per]
  if per == 0:
    print("Sem filtro")
  else:
    print(f"Labels com Percent >= {per}")
  print(f"Descrição da Google e Amazon com filtro de {per*100}%")
  descGoogle = dataGoogle.describe()
  descGoogle.columns=['ID', 'Percent Google']
  descAmazon = dataAmazon.describe()
  descAmazon.columns=['ID', 'Percent Amazon']
  
  print(
    pd.concat([descGoogle['Percent Google'], descAmazon['Percent Amazon']], axis=1,),
  )
  groupGoogle = dataGoogle.groupby(['ID']).size().reset_index(name=f'Total Google {per*100}%')
  groupAmazon = dataAmazon.groupby(['ID']).size().reset_index(name=f'Total Amazon {per*100}%')
  
  
  descGroupAmazon = groupAmazon.describe()
  descGroupAmazon.columns=['ID', f'Total Amazon {per*100}%']
  
  
  print("Quantidade de labels por classe:")
  print(
    pd.concat(
      [groupGoogle[f'Total Google {per*100}%'].describe(), groupAmazon[f'Total Amazon {per*100}%'].describe()], 
      axis=1,
    ),
  )
  
  return dataGoogle, dataAmazon

dataGoogle = pd.read_csv('GoogleVision_not_repeat.csv')
dataAmazon = pd.read_csv('rekognition/result_not_duplicates_oficial.csv') 
dataAmazon.rename(columns={"porcentagem": "Percent", "Nome": "Class"}, inplace=True)
dataAmazon.Percent = dataAmazon['Percent']/100

for per in [.9, .8, .7, 0]:
  google, amazon = testa(dataGoogle, dataAmazon, per)
  test(google, amazon, filter=per*100)
