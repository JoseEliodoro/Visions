import pandas as pd

data = pd.read_csv('data/GoogleVision02.csv')
#data = pd.read_csv('data/AmazonVision.csv')

dataID = data.groupby('ID').size().reset_index(
  name='Total'
).sort_values('Total', ascending=False)

def counts_values(data: pd.DataFrame) -> int:
  total = 0
  for x in range(data['Total'].min(), data['Total'].max()):
    count = data.loc[data["Total"] == x].count().Total
    #print(f'IDs com o valor {x}: {count}')
    total += count
  return total

def test(percent: float, data: pd.DataFrame) -> pd.DataFrame:
  new_data = data.loc[data['Percent'] > percent]
  new_dataID = new_data.groupby('ID').size().reset_index(
    name='Total'
  ).sort_values('Total', ascending=False)

  result = new_dataID['Total'].describe().reset_index(name=f"{percent*100}% total")
  result.drop('index', inplace=True, axis=1)
  
  return result

result = dataID['Total'].describe().reset_index(name='base total')
re = pd.concat([
  result,
  test(.80, data), 
  test(.75, data), 
  test(.73, data),
  test(.70 , data), 
  test(.65 , data), 
  test(.6 , data), 
], axis=1)

print(dataID)

data_80 = data.loc[data['Percent'] > .8]

print(re)
print(
  data_80.groupby('ID').size().reset_index(
  name='Total'
  ).sort_values('Total', ascending=False)
)

print(
  data.loc[data['Subclass'] != 'text']
  .groupby('Class').size().reset_index(name='Total')
  .sort_values('Total', ascending=False).head(10)
)
print(data[data['Class'] == 'Person'])