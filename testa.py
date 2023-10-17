import pandas as pd
import os 
""" data = pd.read_csv('data/GoogleVision.csv')
print(len(data['ID'].unique())) """
def load(perfil):
  return list(
  filter(
    lambda item: item.find(perfil) >= 0, 
    os.listdir('1º turno - Lula')
  ))
  
""" print('perfil lula', len(load('@lula')))
print('perfil bolsononaro', len(load('@bolso')))
data = pd.read_csv(data/'File-id.csv')
print(data)
print(data.groupby('ID').size().reset_index(name='Total').sort_values('ID', ascending=False)) """
dataAmazon:pd.DataFrame = pd.read_csv('data/AmazonVision.csv')

dataGoogle:pd.DataFrame = pd.read_csv('data/GoogleVision.csv')
dataGoogle.sort_values(['Class', 'Percent'], ascending=False, inplace=True)
dataGoogle.drop_duplicates(subset=['ID', 'Class'], inplace=True)

print(f"Quantidade de classes Amazon: {len(dataAmazon['Nome'].unique())}")
print(f"Quantidade de classes Google: {len(dataGoogle['Class'].unique())}")
print(
  dataGoogle.groupby(['Class', 'Subclass']).size().reset_index(
    name='Total'
  ).sort_values('Total', ascending=False).head(10)
)

print()

dataTest = dataGoogle.groupby(
  ['ID', 'Class'],
  ).size().reset_index(
  name='Total',
).sort_values(['ID', 'Total'], ascending=False)

dataGoogle.sort_values('ID', inplace=True)
""" 
print(dataTest.loc[dataTest['Total'] > 1])
test = dataGoogle
test.sort_values(['Class', 'Percent'], ascending=False ,inplace=True)

print(test[
  test['ID'] == 7157357899440803077]
)
test = test.drop_duplicates(subset=['ID', 'Class'], keep='first')
print(test[
  test['ID'] == 7157357899440803077]
)

dataTest = test.groupby(
  ['ID', 'Class'],
  ).size().reset_index(
  name='Total',
).sort_values('Total', ascending=False)

print(dataTest)
"""
#print(dataGoogle[dataGoogle['ID'] == 7157357899440803077].sort_values(['Class', 'Percent']))
#print(dataGoogle[dataGoogle['ID'] == 7157357899440803077])