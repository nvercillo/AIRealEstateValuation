import json
import csv


lines = "" 

rows = []
col_names = []
first = True
for i in range(1, 450):
    try:
        with open(f"../../Data/data{i}.txt", "r", encoding="utf8") as f:
            flines = f.readlines()
            for line in flines:
                lines += line
                
                data = json.loads(line)
                rows.append([data[k] for k in data])
                col_names = [k for k in data] 
        
        if len(rows) > 150:
            with open('../../Data/data.csv', 'a+', newline='') as csv_f:
                writer = csv.writer(csv_f)
                if first:
                    writer.writerows([col_names])
                    first = False

                writer.writerows(rows)
                rows = [] 
    except:
        print(f"page {i} failed")


with open('../../Data/data.csv', 'a+', newline='') as csv_f:
    writer = csv.writer(csv_f)
    if first:
        writer.writerows(col_names)
        first = False

    writer.writerows(rows)
    rows = [] 
    