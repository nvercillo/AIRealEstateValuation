import pandas as pd

data = pd.read_excel('/Users/jakobzerbs/Documents/GitHub/AIRealEstateValuation/dataset_pt2.xlsx')

renamedType = data['Type'].replace({  'Co-Op Apt' : 'Co-op / Co-Ownership Apartment', 
                                                        'Co-Ownership Apt' : 'Co-op / Co-Ownership Apartment', 
                                                        'Att/Row/Twnhouse' : 'Townhouse', 
                                                        'Link' : 'Semi-Detached', 
                                                        'Condo Apt' : 'Condo Apartment', 
                                                        'Comm Element Condo' : 'Condo Apartment', 
                                                        'Semi-Det Condo' : 'Semi-Detached', 
                                                        'Duplex' : 'Semi-Detached', 
                                                        'Triplex' : 'Semi-Detached'})

data.insert(data.columns.get_loc('Type')+1, 'renamedType', renamedType)

data.to_excel('/Users/jakobzerbs/Documents/GitHub/AIRealEstateValuation/dataset_pt2.xlsx', index=False)