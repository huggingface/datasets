import csv
with open('/home/mariama/Documents/SocialBiasFrames_v2/SBFv2.dev.csv') as f:
    data = csv.DictReader(f)
    for row in data:
        print(row.keys())
        for key in row:
            print(key +'==>'+ row[key])
        break