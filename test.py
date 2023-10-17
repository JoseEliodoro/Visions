import pandas as pd

data = pd.read_csv('data/googleVision02.csv')

print(data.groupby(['ID', 'Class']).size().reset_index(name='Total').sort_values('Total', ascending=False))