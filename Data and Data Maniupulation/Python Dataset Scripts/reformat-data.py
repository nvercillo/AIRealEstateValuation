import pandas as pd

data = pd.read_excel('/Users/jakobzerbs/Documents/GitHub/AIRealEstateValuation/dataset_pt2.xlsx')

data['squarefootage'] = data['sqarefootage']
data[['sqarefootage','sqarefootage1']] = data['sqarefootage'].str.split('-',expand=True)
mean_sqarefootage = (data['sqarefootage'].astype(int) + data['sqarefootage1'].astype(int) + 1) / 2
data.insert(data.columns.get_loc('sqarefootage')+1, 'mean_sqarefootage', mean_sqarefootage)
del data['sqarefootage']
del data['sqarefootage1']

data['Municipality District'] = data['Municipality District'].str[8:]

data.to_excel('/Users/jakobzerbs/Documents/GitHub/AIRealEstateValuation/dataset_pt3.xlsx', index=False)