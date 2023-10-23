import pandas as pd
import numpy as np

df= pd.read_excel('data/Bolsonaro + Lula - Validado.xlsx')
df = df[[
  'DataColeta', 
  'Perfil', 
  'DataPost', 
  'DiaDaSemana',
  'Plays', 
  'Curtidas', 
  'Comentarios', 
  'Compart.', 
  'Texto', 
  'LinkFoto',
  'LinkVideo', 
  'LinkPost', 
  'ID', 
  'Duracao', 
  'Duração Classificada',
  'Retórica Aristotélica', 
  'Dispositivo Retórico', 
  'Tipo de conteúdo',
  'Abordagem', 
  'Tonalidade', 
  'Main character', 
  'Texto / Hashtag'
]]

data = pd.read_csv('data/GoogleVision.csv')
data = data.loc[data['ID'].isin(df['ID'])]
data = data.loc[data['Subclass'] != 'text']
data_test = data.loc[data['Percent'] >= 0.74]

print('Dados anteriores')
print('Quantidade de IDs:', len(data['ID'].unique()))
print('Quantidade de de classes:', data['ID'].count())
print('Mediana:', data['Percent'].median())
print('Média:', data['Percent'].mean())
print('1º Quartil:', data['Percent'].quantile(.25))
print('-----------------------------')
print('Dados posteriores')
print('Quantidade de IDs:', len(data_test['ID'].unique()))
print('Quantidade de de classes:', data_test['ID'].count())
print('Mediana:', data_test['Percent'].median())
print('Média:', data_test['Percent'].mean())
print('1º Quartil:', data_test['Percent'].quantile(.25))

""" 
import nltk
from nltk.corpus import wordnet

# Baixe o WordNet (caso ainda não tenha sido baixado)
#nltk.download('wordnet')

def sao_sinonimos(palavra1, palavra2):
  sinonimos1 = set([lemma.name() for synset in wordnet.synsets(palavra1) for lemma in synset.lemmas()])
  sinonimos2 = set([lemma.name() for synset in wordnet.synsets(palavra2) for lemma in synset.lemmas()])
  print(sinonimos1)
  print(sinonimos2)
  return bool(sinonimos1.intersection(sinonimos2))

a = 'male'
b = 'man'
print(sao_sinonimos(a, b))
"""

#df.set_index('ID', inplace=True)
#print(data_test)
""" 
new_data = [
  {'ID': 65554, 'class2': 'j2', 'class3': 'j2'},
  {'ID': 8778, 'class3': 'k2'},
  {'ID': 87876, 'class2': 'l2', 'class3': 'l2'}
]
a = pd.DataFrame(new_data)
for id in data_test['ID'].unique():

  print(data_test.loc[data_test['ID'] == id]['Class'].unique())
  print(id) 
"""


new_data = []
for id in data_test['ID'].unique():
  row = {'ID': id}
  for classe in data_test.loc[data_test['ID'] == id]['Class'].values:
    row[classe] = 1
  new_data.append(row)

new_data = pd.DataFrame(new_data)
new_data.fillna(0, inplace=True)

ordenado = data_test.groupby('Class').size().reset_index(name='Total').sort_values('Total')
new_data = new_data[np.append(ordenado['Class'].tail(10).values, 'ID')]

testa = new_data.merge(df, on='ID', how='outer')
colunas = [
  'ID', 
  'DataPost', 
  'DataColeta', 
  'DiaDaSemana', 
  'Perfil', 
  'Texto', 
  'Duracao', 
  'Duração Classificada', 
  'Event', 
  'Tie', 
  'Chin', 
  'Smile', 
  'Hat',
  'Font', 
  'Forehead', 
  'Gesture', 
  'Joy', 
  'Person',
  'Curtidas',
]
#np.append(df.columns, ordenado['Class'].tail(10).values)
testa.sort_values('ID', inplace=True)
df.sort_values('ID', inplace=True)
testa.set_index('ID')
testa = testa[colunas]
df['Duracao'] = pd.to_numeric(df['Duracao'], errors='coerce', downcast='float')
testa['Duracao'] = df['Duracao']
#print(testa.info())

print(testa['Duracao'])
testa.to_csv('data/dfGoogle.csv')
testa.to_excel('data/dfGoogle.xlsx')
#df.merge(new_data, on='ID', how='outer')[colunas].to_csv('data/dfGoogle.csv')