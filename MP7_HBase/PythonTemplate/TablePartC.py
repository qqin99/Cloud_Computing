import happybase as hb
import csv

connection = hb.Connection('localhost')
connection.open()

table = connection.table('powers')

with open('input.csv') as csvInputFile:
    reader = csv.reader(csvInputFile, delimiter=',')
    for row in reader:
        table.put(row[0], {'personal:hero': row[1],
                           'personal:power': row[2],
                           'professional:name': row[3],
                           'professional:xp': row[4],
                           'custom:color':row[5]})

