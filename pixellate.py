from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
#from OpenGL.arrays import vbo
#from OpenGLContext.arrays import *
from OpenGL.GL import shaders

from PIL.Image import open
from sys import argv

image = open(argv[1])

window = 0                                             # glut window number
width, height = image.size                               # window size

# courtesy of tutorial: https://noobtuts.com/python/opengl-introduction
def draw_rect(x, y, width, height):
    width, height = width/4, height/4
    glBegin(GL_QUADS)
    # start drawing a rectangle
    glTexCoord2f(0,0)
    glVertex2f(x, y)                                   # bottom left point

    glTexCoord2f(1,0)
    glVertex2f(x + width, y)                           # bottom right point

    glTexCoord2f(1,1)
    glVertex2f(x + width, y + height)                  # top right point

    glTexCoord2f(0,1)
    glVertex2f(x, y + height)                          # top left point
    glEnd()

#this article helped me understand textures https://www.gamedev.net/resources/_/technical/opengl/opengl-texture-mapping-an-introduction-r947
def set_texture():    
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, width, height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGBX", 0, -1)
    )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glBindTexture(GL_TEXTURE_2D, ID)

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def draw():                                            # ondraw is called all the time
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # clear the screen
    glLoadIdentity()                                   # reset position
    refresh2d(width, height)

    glColor3f(0.0, 0.0, 1.0)
    draw_rect(0,0,width, height)
    
    glutSwapBuffers()                                  # important for double buffering

#this code helped me understand defining shaders in python: http://pyopengl.sourceforge.net/context/tutorials/shader_1.html 
def build_shader():
    VERTEX_SHADER = shaders.compileShader("""#version 120
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }""", GL_VERTEX_SHADER)
    FRAGMENT_SHADER = shaders.compileShader("""#version 120
        void main() {
            gl_FragColor = vec4( 0.8, .5, 0, 1 );
        }""", GL_FRAGMENT_SHADER)
    shaders.glUseProgram(shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER))

# initialization
glutInit()                                             # initialize glut
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
glutInitWindowSize(width, height)                      # set window size
glutInitWindowPosition(0, 0)                           # set window position
window = glutCreateWindow("blockify")              # create window with title
glutDisplayFunc(draw)                                  # set draw function callback
glutIdleFunc(draw)                                     # draw all the time
glEnable(GL_TEXTURE_2D)
set_texture()
build_shader()
glutMainLoop()      
