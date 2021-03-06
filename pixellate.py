from PIL.Image import open
from PIL import Image
from sys import argv
from pix_opengl import init_opengl, set_texture, draw, build_shader, init_shader_sizes, set_averages, texture_as_image
import time
import pymp
import numpy
from concurrent.futures import *
import imageio

pymp.config.nested = True

image = open(argv[1])
outName = argv[2]
frame = None
columns = int(argv[3])
rows = int(argv[4])

width, height = image.size

chunkWidth  = int(width/columns)
chunkHeight = int(height/rows)

def do_chunk(column, row):
    global frame
    chunkStartX = column * chunkWidth
    chunkStartY = row * chunkHeight
    count = 0
    average = [0,0,0]
    
    for x in range(chunkStartX, chunkStartX+chunkWidth):
        for y in range(chunkStartY, chunkStartY+chunkHeight):
            count += 1
            pixel = frame.getpixel((x,y))
            average[0] += pixel[0]
            average[1] += pixel[1]
            average[2] += pixel[2]
    return (column, row), [int(average[i]/count) for i in range(3)]


def do_rows(column, rows):
    with ThreadPoolExecutor(max_workers=rows) as executor:
        rowThreads = []
        for row in range(rows):
            rowThreads.append(executor.submit(do_chunk, column, row))

        rowValues = [0 for i in range(rows)]
        for rowThread in rowThreads:
            coordinate, average = rowThread.result()
            rowValues[coordinate[1]] = average
        
        return column, rowValues
        

def average_image(columns, rows):
    with ThreadPoolExecutor(max_workers=columns) as executor:
        columnThreads = []
        for column in range(columns):
            columnThreads.append(executor.submit(do_rows, column, rows))

        columnValues = [0 for i in range(columns)]
        for columnThread in columnThreads:
            coordinate, rowsValues = columnThread.result()
            columnValues[coordinate] = rowsValues

        return columnValues


init_opengl(width, height)
build_shader(columns, rows)
init_shader_sizes(width, height, columns, rows)
draw()
try:
    newFrames = []
    while True:
        frame = image.convert("RGB")
        set_texture(frame)

        set_averages(average_image(columns, rows))
        draw()
        newFrames.append(Image.frombytes("RGB", (width, height), texture_as_image()).transpose(Image.FLIP_TOP_BOTTOM))


        image.seek(image.tell()+1)
except EOFError:
    imageio.mimsave(outName, [numpy.array(frame) for frame in newFrames])        
