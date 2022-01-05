import csv
import json
import time

csvfile = open('metadata.csv', 'r')
jsonfile = open('metadata.json', 'w')

def read_csv():
    csv_rows = []
    reader = csv.DictReader(csvfile)
    title = reader.fieldnames

    no_of_chars=0
    for t in title:
        if t.split('_')[0]=="character":
            no_of_chars= no_of_chars+1

    for row in reader:
        modif_row=[{title[i]:row[title[i]] for i in range(no_of_chars+1,len(title))}]
        modif_time=time.strftime('%H:%M:%S', time.gmtime(int(row[title[0]])))
        modif_row[0].update({title[0]:modif_time})

        character_name = []
        for i in range(1,no_of_chars):
            if row[title[i]]=="1":
                character_name.append(title[i].split('_')[1])
        modif_row[0].update({"Character": character_name})
        csv_rows.extend(modif_row)

    write_json(csv_rows)

def write_json(data):
    jsonfile.write(json.dumps(data, sort_keys=False, indent=4))

read_csv()
