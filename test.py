
import pandas as pd
import numpy as np
import datetime

df = pd.read_excel('data/Bolsonaro + Lula - Validado.xlsx')


# ## Tratando coluna de duração

def day_for_flaot(x):
  if(isinstance(x, datetime.datetime)):
    x = float(f"{x.day}.{x.month}")
  print(x)
  return x

df['Duracao'] = df['Duracao'].apply(day_for_flaot)

# ## Observando primeiro quartil antes e depois do filtro de porcentagem

data = pd.read_csv('data/GoogleVision.csv')
data = data.loc[data['ID'].isin(df['ID'])] # Filtrando post que estão no dataset do tiktok
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

# ## Montando dataset com colunas em dummy

new_data = []
for id in data_test['ID'].unique():
  row = {'ID': id}
  for classe in data_test.loc[data_test['ID'] == id]['Class'].values:
    row[classe] = 1
  new_data.append(row)

new_data = pd.DataFrame(new_data)
new_data.fillna(0, inplace=True)
new_data

# ## Pegando quantidade de classes mais presentes nos dados

qtn_class = data_test.groupby('Class').size().reset_index(name='Total').sort_values('Total')
qtn_class

qtn = 50

qtn_class.tail(qtn)

new_data = new_data[np.append(qtn_class['Class'].tail(qtn).values, 'ID')]
new_data

# ## Verificando quantas classes ficam por post

def verify(data: pd.DataFrame, lista):
  if len(lista) == 1:
    return data.loc[data[lista[0]] == 0]
  return verify(data.loc[data[lista[0]] == 0], lista[1: ])

verify(new_data, qtn_class.tail(qtn)["Class"].values)

# # Fazendo merge dos dados com base no ID

data_final = new_data.merge(df, on='ID', how='outer')
data_final.columns

# # Filtrando colunas para os dados

df.columns

columns =  np.append(qtn_class['Class'].tail(qtn).values, [
  'ID', 
  #'DataColeta', 
  'Perfil', 
  #'DataPost', 
  'DiaDaSemana',
  #'Plays',                 Colunas que podem causar vazamento das informações
  #'Comentarios', 
  #'Compart.', 
  'Texto', 
  #'LinkFoto',
  #'LinkVideo',             Links não são pertinentes
  #'LinkPost', 
  'Duracao', 
  'Duração Classificada',
  #'Retórica Aristotélica', 
  #'Dispositivo Retórico', 
  #'Tipo de conteúdo',      Classificações manual
  #'Abordagem', 
  #'Tonalidade', 
  #'Main character', 
  'Texto / Hashtag',
  'Curtidas', 
  ])


# ## Salvando resultado final

data_final = data_final[columns]
data_final

data_final.sort_values('ID', inplace=True)
data_final.set_index('ID')
data_final['Duracao'] = pd.to_numeric(data_final['Duracao'], errors='coerce', downcast='signed')
#data_final.to_excel('data/dfGoogle.xlsx')


print(pd.get_dummies(data_final, columns='DiaDaSemana'))


