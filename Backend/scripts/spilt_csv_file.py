""" THIS FILE WAS IMPORTED BY kelvintaywl ON GITHUB
SEE GIST AT https://gist.github.com/kelvintaywl/37dbfaea789707ec5f48
"""

import csv
import sys
import os

# example usage: python split.py example.csv 200
# above command would split the `example.csv` into smaller CSV files of 200 rows each (with header included)
# if example.csv has 401 rows for instance, this creates 3 files in same directory:
#   - `example_1.csv` (row 1 - 200)
#   - `example_2.csv` (row 201 - 400)
#   - `example_3.csv` (row 401)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
filename = sys.argv[1]

full_file_path = os.path.join(CURRENT_DIR, filename)
file_name = os.path.splitext(full_file_path)[0]

rows_per_csv = int(sys.argv[2]) if len(sys.argv) > 2 else 5000

with open(filename) as infile:
    reader = csv.DictReader(infile)
    header = reader.fieldnames
    rows = [row for row in reader]
    pages = []

    row_count = len(rows)
    start_index = 0
    # here, we slice the total rows into pages, each page having [row_per_csv] rows
    while start_index < row_count:
        pages.append(rows[start_index : start_index + rows_per_csv])
        start_index += rows_per_csv

    for i, page in enumerate(pages):
        with open("{}_{}.csv".format(file_name, i + 1), "w+") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=header)
            writer.writeheader()
            for row in page:
                writer.writerow(row)

        print("DONE splitting {} into {} files".format(filename, len(pages)))
