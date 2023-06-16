import csv
from openpyxl import Workbook

def csv_to_xlsx(csv_file, xlsx_file):
    wb = Workbook()
    ws = wb.active

    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ws.append(row)

    wb.save(xlsx_file)

csv_to_xlsx('table.csv', 'table.xlsx')
