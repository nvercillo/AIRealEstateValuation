import pandas as pd

data = pd.read_csv('/Users/jakobzerbs/Documents/GitHub/AIRealEstateValuation/dataset_pt1.csv')

data[['bedNum','Dens']] = data['bedNum'].str.split('+',expand=True)
data.Dens.fillna(value=0, inplace=True)

data.to_csv('/Users/jakobzerbs/Documents/GitHub/AIRealEstateValuation/dataset_pt2.csv')

