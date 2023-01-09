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

SERVER = '192.168.1.60'
HEADER = 10000
PORT = 5000
# SERVER = '192.168.1.63'
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'
ADDR = (SERVER, PORT)