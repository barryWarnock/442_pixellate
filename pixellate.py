from PIL.Image import open
from sys import argv
from pix_opengl import init_opengl, set_texture, draw
import time
import pymp
import numpy

pymp.config.nested = True

image = open(argv[1])

columns = int(argv[2])
rows = int(argv[3])

width, height = image.size
frames = 1

chunkWidth  = int(width/columns)
chunkHeight = int(height/rows)

init_opengl(width, height)
set_texture(image)

for i in range(frames):
    count = pymp.shared.array((columns, rows), dtype='uint8')
    avgs  = pymp.shared.list([[[0,0,0] for j in range(rows)] for i in range(columns)])#list comprehension is pretty neat
    with pymp.Parallel(columns) as column:
        with pymp.Parallel(rows) as row:
            chunkStartX = column.thread_num * chunkWidth
            chunkStartY = row.thread_num * chunkHeight
            for x in range(chunkStartX, chunkStartX+chunkWidth):
                for y in range(chunkStartY, chunkStartY+chunkHeight):
                                count[column.thread_num,row.thread_num] += 1
                                pixel = image.getpixel((x,y))
                                avgs[column.thread_num][row.thread_num][0] += pixel[0]
                                avgs[column.thread_num][row.thread_num][1] += pixel[1]
                                avgs[column.thread_num][row.thread_num][2] += pixel[2]

    for x in range(columns):
        for y in range(rows):
            avgs[x][y][0] = avgs[x][y]/count[x,y][0]
            avgs[x][y][0] = avgs[x][y]/count[x,y][0]
            avgs[x][y][0] = avgs[x][y]/count[x,y][0]
            print(avgs[x][y],end="")
        print()
    
    draw()
    time.sleep(1)
