from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

glConf = {}

# courtesy of tutorial: https://noobtuts.com/python/opengl-introduction
def draw_rect(x, y, width, height):
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


ID = None    
#this article helped me understand textures https://www.gamedev.net/resources/_/technical/opengl/opengl-texture-mapping-an-introduction-r947
def set_texture(image):
    global ID
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glPixelStorei(GL_UNPACK_ROW_LENGTH, 0);
    glPixelStorei(GL_UNPACK_SKIP_PIXELS, 0);
    glPixelStorei(GL_UNPACK_SKIP_ROWS, 0);
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, glConf["width"], glConf["height"], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glBindTexture(GL_TEXTURE_2D, ID)


def texture_as_image():
    global ID
    #GL_TEXTURE_2D,     0, GL_RGB, GL_UNSIGNED_BYTE
    #target       , level,  
    return glReadPixels(0,0, glConf["width"], glConf["height"], GL_RGB, GL_UNSIGNED_BYTE)


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
    refresh2d(glConf["width"], glConf["height"])

    glColor3f(0.0, 0.0, 1.0)
    draw_rect(0,0,glConf["width"], glConf["height"])
    
    glutSwapBuffers()                                  # important for double buffering


UNIFORM_LOCATIONS = {}
#this code helped me understand defining shaders in python: http://pyopengl.sourceforge.net/context/tutorials/shader_1.html 
def build_shader(columns, rows):
    VERTEX_SHADER = shaders.compileShader("""#version 120
        void main() {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }""", GL_VERTEX_SHADER)

    with open("frag_shader.glsl") as frag_shader:
        FRAGMENT_SHADER = shaders.compileShader(frag_shader.read() % (columns*rows), GL_FRAGMENT_SHADER)
        shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        shaders.glUseProgram(shader)
        global UNIFORM_LOCATIONS
        UNIFORM_LOCATIONS = {
            'width': glGetUniformLocation(shader, 'width'),
            'height': glGetUniformLocation(shader, 'height'),
            'columns': glGetUniformLocation(shader, 'columns'),
            'rows': glGetUniformLocation(shader, 'rows'),
            'averages': glGetUniformLocation(shader, 'averages'),
        }


def init_shader_sizes(width, height, columns, rows):
    glUniform1i(UNIFORM_LOCATIONS['width'], width)
    glUniform1i(UNIFORM_LOCATIONS['height'],height)
    glUniform1i(UNIFORM_LOCATIONS['columns'], columns)
    glUniform1i(UNIFORM_LOCATIONS['rows'], rows)


def set_averages(averages):
    averages1d = sum(averages, [])
    glUniform3fv( 
        UNIFORM_LOCATIONS['averages'],
        len(averages1d),
        averages1d)


def init_opengl(width, height):
    glConf["width"] = width
    glConf["height"] = height
    glutInit()                                             # initialize glut
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(glConf["width"], glConf["width"])                      # set window size
    glutInitWindowPosition(0, 0)                           # set window position
    glConf["window"] = glutCreateWindow("blockify")              # create window with title
    glEnable(GL_TEXTURE_2D)
    draw();draw()

