import csv

WIDTH    = 1280	
HEIGTH   = 720
FPS      = 60
TILESIZE = 64

MAP = [
    
]

with open('ourmap.csv', 'r') as file:
    csvReader = csv.reader(file)
    for row in csvReader:
        MAP.append(row)

MAPHEIGTH = len(MAP) * TILESIZE
MAPWIDTH = len(MAP[0]) * TILESIZE
print(MAPWIDTH, MAPHEIGTH)
print(MAP)