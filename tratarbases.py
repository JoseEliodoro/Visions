import pandas as pd


def RepeatClassGoogle():
  google = pd.read_csv('GoogleVision.csv')
  print('Total de classes repitidas')
  test = lambda : print(google.groupby(['ID', 'Class']).size().reset_index(name='Total').sort_values('Total', ascending=False))
  test()
  google.sort_values(['Class', 'Percent'], ascending=False, inplace=True)
  google.drop_duplicates(['ID', 'Class'], inplace=True)
  google.set_index('ID', inplace=True)
  google.to_csv('GoogleVision_not_repeat.csv')
  test()
def oficialAmazon():
  amazon = pd.read_csv('rekognition/result_not_duplicates.csv')
  #amazon.rename(columns={"porcentagem": "Percent", "Nome": "Class"}, inplace=True)
  test = pd.to_numeric(amazon['ID'], errors='coerce')
  print(f"Qtn de elementos restantes: {len(amazon) - test.isna().sum()}")
  amazon = amazon[test.notna()]
  amazon.set_index('ID', inplace=True)
  amazon.to_csv('rekognition/result_not_duplicates_oficial.csv')

amazon = pd.read_csv('rekognition/result_not_duplicates_oficial.csv')
amazon.rename(columns={"porcentagem": "Percent", "Nome": "Class"}, inplace=True)
google = pd.read_csv('GoogleVision_not_repeat.csv')

print(amazon)
print(google)