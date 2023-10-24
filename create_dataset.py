
import pandas as pd
import numpy as np
import datetime

df = pd.read_excel('data/Bolsonaro + Lula - Validado.xlsx')


# ## Tratando coluna de duração

def day_for_flaot(x):
  if(isinstance(x, datetime.datetime)):
    x = float(f"{x.day}.{x.month}")
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
print('DataFrame contando todas as classes')
print(new_data)

# ## Pegando quantidade de classes mais presentes nos dados

qtn_class = data_test.groupby('Class').size().reset_index(name='Total').sort_values('Total')
print('Quantidade de frequência de cada classe')
print(qtn_class)

qtn = 10

print(f'{qtn} classes mais frequentes')
print(qtn_class.tail(qtn))

new_data = new_data[np.append(qtn_class['Class'].tail(qtn).values, 'ID')]
print('Novo dataframe com classes em dummy e ID')
print(new_data)

# ## Verificando quantas classes ficam por post

def verify(data: pd.DataFrame, lista):
  if len(lista) == 1:
    return data.loc[data[lista[0]] == 0]
  return verify(data.loc[data[lista[0]] == 0], lista[1: ])
print(f'Todos os valores que não possuem nenhuma frequência das {qtn} classes mais frequentes')
print(verify(new_data, qtn_class.tail(qtn)["Class"].values))

# # Fazendo merge dos dados com base no ID

data_final = new_data.merge(df, on='ID', how='outer')
print('Colunas do dataframe final')
print(data_final.columns)

# # Filtrando colunas para os dados
print('Colunas do dataset validado')
print(df.columns)

columns =  np.append(qtn_class['Class'].tail(qtn).values, [
  'ID', 
  #'DataColeta', 
  'Perfil', 
  #'DataPost', 
  'DiaDaSemana',
  #'Plays',                 Colunas que podem causar vazamento das informações
  #'Comentarios', 
  #'Compart.', 
  #'Texto',               Decidir o que fazer com essa coluna 
  #'LinkFoto',
  #'LinkVideo',             Links não são pertinentes
  #'LinkPost', 
  'Duracao', 
  #'Duração Classificada',
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
print('Dataframe final com o filtro das colunas que serão utilizandos')
print(data_final)


data_final['Duracao'] = pd.to_numeric(data_final['Duracao'], errors='coerce', downcast='signed')

data_final = pd.get_dummies(data_final, columns=['DiaDaSemana', 'Perfil'], prefix='', prefix_sep='', dtype='int',)
data_final.drop('lulaoficial', axis=1, inplace=True)
data_final.rename({'bolsonaromessiasjair': 'Perfil'}, axis=1, inplace=True)


""" 
OBS na coluna perfil os valores repesentam
1 == bolsonaromessiasjair
0 == lulaoficial 
"""

print('DataFrame final com o dummy nas colunas de DiaDaSemana e Perfil')
print(data_final)


data_final = pd.get_dummies(data_final, columns=['Texto / Hashtag'], prefix='', prefix_sep='', dtype='int')
print(data_final)
aux = data_final['Texto + Hashtag'].apply(lambda x: 1 if x==1 else 0).astype('int32')
aux = pd.DataFrame({"Texto":aux.values, "Hashtag":aux.values})
data_final['Texto'] = aux['Texto'] + data_final['Texto']
data_final['Hashtag'] = aux['Texto'] + data_final['Hashtag']
data_final.drop(['Texto + Hashtag', 'Nenhum'], inplace=True, axis=1)


print(data_final.columns.values)
data_final.sort_values('ID', inplace=True)
data_final.set_index('ID', inplace=True)

print(data_final.columns)

data_final.to_csv('data/dfGoogle.csv')
data_final.to_excel('data/dfGoogle.xlsx')
