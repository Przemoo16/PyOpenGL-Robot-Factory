import sys
from OpenGL.GLUT import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
import time

window_size = (1920, 1200)

gif_frame = 0

animate = 0
set_view = 1
light_on = 1
enable_light_settings = 0
enable_fog = 0

view_translation = np.array([0, 0, 0])
view_rotation = np.array([0, 0, 0])

rotation_robot1 = [0, 0, 0, 0]
rotation_robot2_1 = [0, 0, 0, 0, 0, 0]
rotation_robot2_2 = [0, 0, 0, 0, 0, 0]
rotation_robot3 = [0, 0, 0.5]
flag_rob1 = 1
flag_rob2_1 = 0
flag_rob2_2 = 0
flag_rob3 = 1

tasma_rot = [0, 0, 0, 0]

przes_szesc = []
przes_walec = []
przes_szesc_wal = []
przes_szesc_wal_last = []

num_szescian = 0
num_walec = 0
num_szesc_wal = 0
num_szesc_wal_last = 0

lightPos = [0.0, 30.0, 5.0, 1.0]
spotDir = [0.0, 0.0, -1.0]

initial_time = 0
final_time = 0
frame_count = 0
show_fps = 0
actual_FPS = 1
set_fps = 20

time_flag = 0

stop_szescian = 0
stop_walec = 0

lin = np.linspace(0, np.pi, num=10, endpoint=True)


def init():
    ambientLight = [0.3, 0.3, 0.3, 1.0]
    diffuseLight = [0.7, 0.7, 0.7, 1.0]
    specular = [1.0, 1.0, 1.0, 1.0]
    specref = [1.0, 1.0, 1.0, 1.0]

    glClearColor(0.3, 0.3, 0.8, 0.4)

    glEnable(GL_DEPTH_TEST)
    glFrontFace(GL_CCW)
    glEnable(GL_CULL_FACE)

    glEnable(GL_LIGHTING)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLight)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuseLight)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular)
    glEnable(GL_LIGHT0)

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specref)
    glMateriali(GL_FRONT, GL_SHININESS, 128)

    glColor3f(1.0, 1.0, 1.0)

    glEnable(GL_NORMALIZE)

    loadTexture()

    fogColor = [0.5, 0.5, 0.5, 1.0]

    glFogfv(GL_FOG_COLOR, fogColor)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogf(GL_FOG_DENSITY, 0.03)
    glFogf(GL_FOG_START, 10.0)
    glFogf(GL_FOG_END, 60.0)
    glHint(GL_FOG_HINT, GL_DONT_CARE)


def display():

    global gif_frame

    global initial_time
    global final_time
    global frame_count
    global actual_FPS

    glPolygonMode(GL_BACK, GL_LINE)

    glMatrixMode(GL_MODELVIEW)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()

    # x y z
    if set_view == 1:  # GENERAL
        gluLookAt(0.0, 30.0, 18.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    elif set_view == 2:  # LEFT
        gluLookAt(-15.0, 15.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    elif set_view == 3:  # MID
        gluLookAt(0.0, 10.0, 5.0, 0.0, 0.0, -10.0, 0.0, 1.0, 0.0)
    elif set_view == 4:  # PIEC
        gluLookAt(15.0, 10.0, 0.0, 0.0, 0.0, 10.0, 0.0, 1.0, 0.0)
    elif set_view == 5:  # LAST
        gluLookAt(10.0, 15.0, -30.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    glScalef(0.5, 0.5, 0.5)

    glPushMatrix()

    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, spotDir)

    glTranslatef(lightPos[0], lightPos[1], lightPos[2])

    if enable_light_settings == 1:
        glPushAttrib(GL_LIGHTING_BIT)
        glDisable(GL_LIGHTING)
        szescian(1, 0)
        glPopAttrib()

    glPopMatrix()

    if show_fps == 1:
        drawText('FPS: ' + str(actual_FPS), 20, 20, window_size[0], window_size[1])

    scena(rotation_robot1, rotation_robot2_1, rotation_robot2_2, rotation_robot3)

    frame_count += 1
    final_time = time.time()
    if (final_time - initial_time > 0):
        actual_FPS = int(frame_count / (final_time - initial_time))
        # print('FPS:', actual_FPS)
        frame_count = 0
        initial_time = final_time

    if animate == 1:
        gif_frame += 1

    if gif_frame == 39:
        gif_frame = 0

    glutSwapBuffers()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(w) / float(h), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)


def createPopupMenus():

    select_views = glutCreateMenu(MenuSelect)
    glutAddMenuEntry("General", 0)
    glutAddMenuEntry("Left", 1)
    glutAddMenuEntry("Mid", 2)
    glutAddMenuEntry("Furnace", 3)
    glutAddMenuEntry("Behind", 4)

    start_stop = glutCreateMenu(MenuSelect)
    glutAddMenuEntry("Start animation", 5)
    glutAddMenuEntry("Stop animation", 6)

    select_light = glutCreateMenu(MenuSelect)
    glutAddMenuEntry("ON / OFF Light", 8)
    glutAddMenuEntry("ON / OFF Settings", 9)

    fog_settings = glutCreateMenu(MenuSelect)
    glutAddMenuEntry("ON / OFF Fog", 10)
    glutAddMenuEntry("LINEAR", 11)
    glutAddMenuEntry("EXP", 12)
    glutAddMenuEntry("EXP2", 13)

    fps_settings = glutCreateMenu(MenuSelect)
    glutAddMenuEntry("ON / OFF FPS", 14)
    glutAddMenuEntry("60 FPS", 15)
    glutAddMenuEntry("40 FPS", 16)
    glutAddMenuEntry("20 FPS", 17)

    mainMenu = glutCreateMenu(MenuSelect)
    glutAddSubMenu("START / STOP", start_stop)
    glutAddSubMenu("VIEWS", select_views)
    glutAddSubMenu("LIGHT", select_light)
    glutAddSubMenu("FOG", fog_settings)
    glutAddSubMenu("FPS", fps_settings)
    glutAddMenuEntry("EXIT", 7)

    glutAttachMenu(GLUT_RIGHT_BUTTON)


def MenuSelect(idCommand):

    global animate
    global set_view
    global enable_light_settings
    global light_on
    global enable_fog
    global show_fps
    global set_fps

    if idCommand == 0:
        set_view = 1
        return 0
    if idCommand == 1:
        set_view = 2
        return 0
    if idCommand == 2:
        set_view = 3
        return 0
    if idCommand == 3:
        set_view = 4
        return 0
    if idCommand == 4:
        set_view = 5
        return 0
    if idCommand == 5:
        animate = 1
        return 0
    if idCommand == 6:
        animate = 0
        return 0
    if idCommand == 7:
        sys.exit(0)
    if idCommand == 8:
        if light_on == 0:
            light_on = 1
            glEnable(GL_LIGHTING)
        elif light_on == 1:
            light_on = 0
            glDisable(GL_LIGHTING)
        return 0
    if idCommand == 9:
        if enable_light_settings == 0:
            enable_light_settings = 1
        elif enable_light_settings == 1:
            enable_light_settings = 0
        return 0
    if idCommand == 10:
        if enable_fog == 0:
            enable_fog = 1
            glEnable(GL_FOG)
        elif enable_fog == 1:
            enable_fog = 0
            glDisable(GL_FOG)
        return 0
    if idCommand == 11:
        glFogi(GL_FOG_MODE, GL_LINEAR)
        return 0
    if idCommand == 12:
        glFogi(GL_FOG_MODE, GL_EXP)
        return 0
    if idCommand == 13:
        glFogi(GL_FOG_MODE, GL_EXP2)
        return 0
    if idCommand == 14:
        if show_fps == 0:
            show_fps = 1
        elif show_fps == 1:
            show_fps = 0
        return 0
    if idCommand == 15:
        set_fps = 60
        return 0
    if idCommand == 16:
        set_fps = 40
        return 0
    if idCommand == 17:
        set_fps = 20
        return 0


def keyboard(key, x, y):
    if key == b'\x1b':
        sys.exit(0)
    elif key == b'w':
        if enable_light_settings == 1:
            view_rotation[0] -= 2
    elif key == b's':
        if enable_light_settings == 1:
            view_rotation[0] += 2
    elif key == b'a':
        if enable_light_settings == 1:
            view_rotation[1] -= 2
    elif key == b'd':
        if enable_light_settings == 1:
            view_rotation[1] += 2
    elif key == b'1':
        if enable_light_settings == 1:
            lightPos[0] += 1.0
    elif key == b'2':
        if enable_light_settings == 1:
            lightPos[0] -= 1.0
    elif key == b'3':
        if enable_light_settings == 1:
            lightPos[1] += 1.0
    elif key == b'4':
        if enable_light_settings == 1:
            lightPos[1] -= 1.0
    elif key == b'5':
        if enable_light_settings == 1:
            lightPos[2] += 1.0
    elif key == b'6':
        if enable_light_settings == 1:
            lightPos[2] -= 1.0


def mouse(button, state, x, y):
    if button == 3:
        view_translation[2] += 1
        glutPostRedisplay()
    if button == 4:
        view_translation[2] -= 1
        glutPostRedisplay()


def loadTexture():

    tex = glGenTextures(60)

    image1 = Image.open('./textures/metal.jpg')
    string_image1 = image1.convert("RGBA").tobytes("raw", "RGBA")
    width1, height1 = image1.size

    glBindTexture(GL_TEXTURE_2D, tex[0])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width1, height1,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image1)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image2 = Image.open('./textures/metal2.jpg')
    string_image2 = image2.convert("RGBA").tobytes("raw", "RGBA")
    width2, height2 = image2.size

    glBindTexture(GL_TEXTURE_2D, tex[1])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width2, height2,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image2)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image3 = Image.open('./textures/black.jpg')
    string_image3 = image3.convert("RGBA").tobytes("raw", "RGBA")
    width3, height3 = image3.size

    glBindTexture(GL_TEXTURE_2D, tex[2])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width3, height3,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image3)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image4 = Image.open('./textures/red.jpg')
    string_image4 = image4.convert("RGBA").tobytes("raw", "RGBA")
    width4, height4 = image4.size

    glBindTexture(GL_TEXTURE_2D, tex[3])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width4, height4,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image4)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image5 = Image.open('./textures/brown.jpg')
    string_image5 = image5.convert("RGBA").tobytes("raw", "RGBA")
    width5, height5 = image5.size

    glBindTexture(GL_TEXTURE_2D, tex[4])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width5, height5,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image5)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image6 = Image.open('./textures/brown2.jpg')
    string_image6 = image6.convert("RGBA").tobytes("raw", "RGBA")
    width6, height6 = image6.size

    glBindTexture(GL_TEXTURE_2D, tex[5])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width6, height6,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image6)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image7 = Image.open('./textures/floor.jpg')
    string_image7 = image7.convert("RGBA").tobytes("raw", "RGBA")
    width7, height7 = image7.size

    glBindTexture(GL_TEXTURE_2D, tex[6])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width7, height7,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image7)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image8 = Image.open('./textures/box.jpg')
    string_image8 = image8.convert("RGBA").tobytes("raw", "RGBA")
    width8, height8 = image8.size

    glBindTexture(GL_TEXTURE_2D, tex[7])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width8, height8,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image8)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image9 = Image.open('./textures/brick.jpg')
    string_image9 = image9.convert("RGBA").tobytes("raw", "RGBA")
    width9, height9 = image9.size

    glBindTexture(GL_TEXTURE_2D, tex[8])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width9, height9,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image9)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image10 = Image.open('./textures/belt.jpg')
    string_image10 = image10.convert("RGBA").tobytes("raw", "RGBA")
    width10, height10 = image10.size

    glBindTexture(GL_TEXTURE_2D, tex[9])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width10, height10,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image10)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image11 = Image.open('./textures/ice.jpg')
    string_image11 = image11.convert("RGBA").tobytes("raw", "RGBA")
    width11, height11 = image11.size

    glBindTexture(GL_TEXTURE_2D, tex[10])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width11, height11,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image11)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image12 = Image.open('./textures/glass.jpg')
    string_image12 = image12.convert("RGBA").tobytes("raw", "RGBA")
    width12, height12 = image12.size

    glBindTexture(GL_TEXTURE_2D, tex[11])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width12, height12,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image12)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image13 = Image.open('./textures/wood.jpg')
    string_image13 = image13.convert("RGBA").tobytes("raw", "RGBA")
    width13, height13 = image13.size

    glBindTexture(GL_TEXTURE_2D, tex[12])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width13, height13,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image13)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image14 = Image.open('./textures/window.jpg')
    string_image14 = image14.convert("RGBA").tobytes("raw", "RGBA")
    width14, height14 = image14.size

    glBindTexture(GL_TEXTURE_2D, tex[13])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width14, height14,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image14)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image15 = Image.open('./textures/ja_napis.png')
    string_image15 = image15.convert("RGBA").tobytes("raw", "RGBA")
    width15, height15 = image15.size

    glBindTexture(GL_TEXTURE_2D, tex[14])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width15, height15,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image15)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    for i in range(39):

        image = Image.open('./gif/giphy.gif-'+str(i)+'.gif')
        string_image = image.convert("RGBA").tobytes("raw", "RGBA")
        width, height = image.size

        glBindTexture(GL_TEXTURE_2D, tex[i+15])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, string_image)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    image54 = Image.open('./textures/tv.jpg')
    string_image54 = image54.convert("RGBA").tobytes("raw", "RGBA")
    width54, height54 = image54.size

    glBindTexture(GL_TEXTURE_2D, tex[54])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width54, height54,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, string_image54)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)

    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)


def get_normal_vector(v1, v2, v3):
    v = np.cross(v2-v1, v3-v1)
    n = np.sqrt(np.dot(v, v.conj()))
    if n:
        return v/n
    else:
        print(v1)
        print(v2)
        print(v3)
        print(v/n)
        sys.exit(-1)


def robots_move(value):
    move_robot_1()
    move_robot_2_1()
    move_robot_2_2()
    move_robot_3()
    glutPostRedisplay()
    glutTimerFunc(1000//set_fps, robots_move, 0)


def move_robot_1():
    global flag_rob1
    global num_szescian
    global num_walec
    global przes_szesc
    global przes_walec

    if animate == 1:

        if flag_rob1 == 1:  # [180.0, 40.0, -120.0, -25.0]
            if rotation_robot1[0] != 180:
                rotation_robot1[0] += 5.0
            if rotation_robot1[1] != 40:
                rotation_robot1[1] += 5.0
            if rotation_robot1[2] != -120:
                rotation_robot1[2] -= 5.0
            if rotation_robot1[3] != -25:
                rotation_robot1[3] -= 5.0
            if rotation_robot1[0] == 180 and rotation_robot1[1] == 40 and rotation_robot1[2] == -120 and rotation_robot1[3] == -25:
                flag_rob1 = 2

        elif flag_rob1 == 2:  # [180.0, 40.0, -70.0, 40.0]
            if rotation_robot1[0] != 180:
                rotation_robot1[0] += 5.0
            if rotation_robot1[1] != 40:
                rotation_robot1[1] -= 5.0
            if rotation_robot1[2] != -70:
                rotation_robot1[2] += 5.0
            if rotation_robot1[3] != 40 and rotation_robot1[0] == 180 and rotation_robot1[1] == 40 and rotation_robot1[2] == -70:
                rotation_robot1[3] += 5.0
            if rotation_robot1[0] == 180 and rotation_robot1[1] == 40 and rotation_robot1[2] == -70 and rotation_robot1[3] == 40:
                flag_rob1 = 3

        elif flag_rob1 == 3:  # [180.0, 40.0, -120.0, -25.0]
            if rotation_robot1[0] != 180 and rotation_robot1[3] == -25:
                rotation_robot1[0] += 5.0
            if rotation_robot1[1] != 40 and rotation_robot1[3] == -25:
                rotation_robot1[1] += 5.0
            if rotation_robot1[2] != -120 and rotation_robot1[3] == -25:
                rotation_robot1[2] -= 5.0
            if rotation_robot1[3] != -25:
                rotation_robot1[3] -= 5.0
            if rotation_robot1[0] == 180 and rotation_robot1[1] == 40 and rotation_robot1[2] == -120 and rotation_robot1[3] == -25:
                flag_rob1 = 4

        elif flag_rob1 == 4:  # [0.0, 40.0, -30, 0.0]
            if rotation_robot1[0] != 0.0:
                rotation_robot1[0] -= 5.0
            if rotation_robot1[1] != 40.0:
                rotation_robot1[1] -= 5.0
            if rotation_robot1[2] != -30 and rotation_robot1[0] < 150.0:
                rotation_robot1[2] += 5.0
            if rotation_robot1[3] != 0.0:
                rotation_robot1[3] += 5.0
            if rotation_robot1[0] == 0 and rotation_robot1[1] == 40 and rotation_robot1[2] == -30 and rotation_robot1[3] == 0:
                flag_rob1 = 5

        elif flag_rob1 == 5 and (num_szescian < 1 and num_walec < 1):  # [-30, 40, -70, 30]
            if rotation_robot1[0] != -30:
                rotation_robot1[0] -= 5.0
            if rotation_robot1[1] != 40:
                rotation_robot1[1] += 5.0
            if rotation_robot1[2] != -70:
                rotation_robot1[2] -= 5.0
            if rotation_robot1[3] != 30:
                rotation_robot1[3] += 5.0
            if rotation_robot1[0] == -30 and rotation_robot1[1] == 40 and rotation_robot1[2] == -70 and rotation_robot1[3] == 30:
                przes_szesc.append(0)
                przes_walec.append(0)
                num_szescian += 1
                num_walec += 1
                flag_rob1 = 6

        elif flag_rob1 == 6:  # [0.0, 40.0, -30, 0.0]
            if rotation_robot1[0] != 0.0 and rotation_robot1[2] > -35:
                rotation_robot1[0] += 5.0
            if rotation_robot1[1] != 40.0:
                rotation_robot1[1] -= 5.0
            if rotation_robot1[2] != -30:
                rotation_robot1[2] += 5.0
            if rotation_robot1[3] != 0.0:
                rotation_robot1[3] -= 5.0
            if rotation_robot1[0] == 0 and rotation_robot1[1] == 40 and rotation_robot1[2] == -30 and rotation_robot1[3] == 0:
                flag_rob1 = 1


def move_robot_2_1():
    global flag_rob2_1
    global flag_rob2_2
    global num_walec
    global przes_walec
    global stop_walec

    if animate == 1:

        if flag_rob2_1 == 1:  # [-47.5, -70, 0, 35, 0, 15]
            if rotation_robot2_1[0] != -47.5:
                if rotation_robot2_1[0] > -45.0:
                    rotation_robot2_1[0] -= 5.0
                else:
                    rotation_robot2_1[0] -= 0.5
            if rotation_robot2_1[1] != -70 and rotation_robot2_1[3] > 20:
                rotation_robot2_1[1] -= 5.0
            if rotation_robot2_1[2] != 0:
                rotation_robot2_1[2] -= 5.0
            if rotation_robot2_1[3] != 35:
                rotation_robot2_1[3] += 5.0
            if rotation_robot2_1[4] != 0:
                rotation_robot2_1[4] -= 5.0
            if rotation_robot2_1[5] != 15 and rotation_robot2_1[0] == -47.5 and rotation_robot2_1[1] == -70 and rotation_robot2_1[2] == 0 and rotation_robot2_1[3] == 35 and rotation_robot2_1[4] == 0:
                rotation_robot2_1[5] += 5.0
            if rotation_robot2_1[0] == -47.5 and rotation_robot2_1[1] == -70 and rotation_robot2_1[2] == 0 and rotation_robot2_1[3] == 35 and rotation_robot2_1[4] == 0 and rotation_robot2_1[5] == 15:
                flag_rob2_1 = 2
                num_walec -= 1
                stop_walec = 0
                przes_walec.pop(0)

        if flag_rob2_1 == 2:
            if rotation_robot2_1[1] != -55:
                rotation_robot2_1[1] += 1.0
            if rotation_robot2_1[3] != 40:
                rotation_robot2_1[3] += 1.0
            if rotation_robot2_1[1] == -55 and rotation_robot2_1[3] == 40:
                flag_rob2_1 = 3

        if flag_rob2_1 == 3:  # [-81.5, -85.0, -0.5, 54, 0, 15]
            if rotation_robot2_1[0] != -81.5:
                rotation_robot2_1[0] += -2
            if rotation_robot2_1[1] != -85.0 and rotation_robot2_1[0] == -81.5 and flag_rob2_2 == 4:
                rotation_robot2_1[1] -= 2.0
            if rotation_robot2_1[2] != -0.5:
                rotation_robot2_1[2] -= 0.1
            if rotation_robot2_1[3] != 54 and rotation_robot2_1[0] == -81.5 and flag_rob2_2 == 4:
                rotation_robot2_1[3] += 2.0
            if rotation_robot2_1[4] != 0:
                rotation_robot2_1[4] -= 5.0
            if rotation_robot2_1[5] != 15:
                rotation_robot2_1[5] += 5.0
            if rotation_robot2_1[0] == -81.5 and rotation_robot2_1[1] == -85.0 and rotation_robot2_1[2] == -0.5 and rotation_robot2_1[3] == 54 and rotation_robot2_1[4] == 0 and rotation_robot2_1[5] == 15:
                flag_rob2_1 = 4

        if flag_rob2_1 == 4:
            if rotation_robot2_1[5] != 0.0:
                rotation_robot2_1[5] -= 2.5
            if rotation_robot2_1[5] == 0.0:
                flag_rob2_1 = 5

        if flag_rob2_1 == 5:  # [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            if rotation_robot2_1[0] != 0.0 and rotation_robot2_1[5] == 0.0:
                if rotation_robot2_1[0] < -1.5:
                    rotation_robot2_1[0] += 5.0
                else:
                    rotation_robot2_1[0] += 0.5
            if rotation_robot2_1[1] != 0.0:
                rotation_robot2_1[1] += 5.0
            if rotation_robot2_1[2] != 0.0:
                rotation_robot2_1[2] += 0.5
            if rotation_robot2_1[3] != 0.0:
                rotation_robot2_1[3] -= 6.0
            if rotation_robot2_1[4] != 0.0:
                rotation_robot2_1[4] -= 1.0
            if rotation_robot2_1[5] != 0.0:
                rotation_robot2_1[5] -= 2.5
            if rotation_robot2_1[0] == 0.0 and rotation_robot2_1[1] == 0.0 and rotation_robot2_1[2] == 0.0 and rotation_robot2_1[3] == 0.0 and rotation_robot2_1[4] == 0 and rotation_robot2_1[5] == 0.0:
                flag_rob2_1 = 0


def move_robot_2_2():
    global flag_rob2_1
    global flag_rob2_2
    global num_szescian
    global przes_szesc
    global num_szesc_wal
    global time_flag
    global stop_szescian

    if animate == 1:

        if flag_rob2_2 == 1:  # [50, -63, 0, 25, 0, 15]
            if rotation_robot2_2[0] != 50:
                rotation_robot2_2[0] += 5.0
            if rotation_robot2_2[1] != -63:
                rotation_robot2_2[1] -= 3.0
            if rotation_robot2_2[2] != 0:
                rotation_robot2_2[2] -= 5.0
            if rotation_robot2_2[3] != 25:
                rotation_robot2_2[3] += 5.0
            if rotation_robot2_2[4] != 0:
                rotation_robot2_2[4] -= 5.0
            if rotation_robot2_2[5] != 15 and rotation_robot2_2[0] == 50 and rotation_robot2_2[1] == -63 and rotation_robot2_2[2] == 0 and rotation_robot2_2[3] == 25 and rotation_robot2_2[4] == 0:
                rotation_robot2_2[5] += 5.0
            if rotation_robot2_2[0] == 50 and rotation_robot2_2[1] == -63 and rotation_robot2_2[2] == 0 and rotation_robot2_2[3] == 25 and rotation_robot2_2[4] == 0 and rotation_robot2_2[5] == 15:
                flag_rob2_2 = 2
                num_szescian -= 1
                stop_szescian = 0
                przes_szesc.pop(0)

        if flag_rob2_2 == 2:
            if rotation_robot2_2[1] != -55:
                rotation_robot2_2[1] += 1.0
            if rotation_robot2_2[3] != 30:
                rotation_robot2_2[3] += 1.0
            if rotation_robot2_2[1] == -55 and rotation_robot2_2[3] == 30:
                flag_rob2_2 = 3

        if flag_rob2_2 == 3:  # [88.5, -65.0, 0, 25.0, 0, 15.0]
            if rotation_robot2_2[0] != 88.5:
                rotation_robot2_2[0] += 3.5
            if rotation_robot2_2[1] != -65 and rotation_robot2_2[0] == 88.5:
                rotation_robot2_2[1] -= 1.0
            if rotation_robot2_2[2] != 0:
                rotation_robot2_2[2] -= 5.0
            if rotation_robot2_2[3] != 25 and rotation_robot2_2[0] == 88.5:
                rotation_robot2_2[3] -= 5.0
            if rotation_robot2_2[4] != 0:
                rotation_robot2_2[4] -= 5.0
            if rotation_robot2_2[5] != 15:
                rotation_robot2_2[5] += 5.0
            if rotation_robot2_2[0] == 88.5 and rotation_robot2_2[1] == -65 and rotation_robot2_2[2] == 0 and rotation_robot2_2[3] == 25 and rotation_robot2_2[4] == 0 and rotation_robot2_2[5] == 15:
                flag_rob2_2 = 4

        if flag_rob2_2 == 4 and (flag_rob2_1 == 5 or flag_rob2_1 == 0):
            if rotation_robot2_2[1] != -45:
                rotation_robot2_2[1] += 5.0
            if rotation_robot2_2[1] == -45:
                flag_rob2_2 = 5

        if flag_rob2_2 == 5:  # [-91.5, -108, 0.0, 53, 0, 15]
            if rotation_robot2_2[0] != -91.5:
                rotation_robot2_2[0] -= 10.0
            if rotation_robot2_2[1] != -108 and rotation_robot2_2[0] == -91.5:
                rotation_robot2_2[1] -= 9.0
            if rotation_robot2_2[2] != 0.0:
                rotation_robot2_2[2] -= 5.0
            if rotation_robot2_2[3] != 53 and rotation_robot2_2[0] == -91.5:
                rotation_robot2_2[3] += 4.0
            if rotation_robot2_2[4] != 0:
                rotation_robot2_2[4] -= 5.0
            if rotation_robot2_2[5] != 15:
                rotation_robot2_2[5] += 5.0
            if rotation_robot2_2[0] == -91.5 and rotation_robot2_2[1] == -108 and rotation_robot2_2[2] == 0 and rotation_robot2_2[3] == 53 and rotation_robot2_2[4] == 0 and rotation_robot2_2[5] == 15:
                if time_flag == 0:
                    glutTimerFunc(2000, freeze_glass, 0)
                    time_flag = 1

        if flag_rob2_2 == 6:
            if rotation_robot2_2[1] != -59.0:
                rotation_robot2_2[1] += 3.5
            if rotation_robot2_2[1] == -59.0:
                flag_rob2_2 = 7
                time_flag = 0

        if flag_rob2_2 == 7:  # [-246.5, -79.0, 0.0, 51.0, 0.0, 15]
            if rotation_robot2_2[0] != -246.5:
                rotation_robot2_2[0] -= 5.0
            if rotation_robot2_2[1] != -79.0 and rotation_robot2_2[0] == -246.5:
                rotation_robot2_2[1] -= 5.0
            if rotation_robot2_2[2] != 0.0:
                rotation_robot2_2[2] -= 5.0
            if rotation_robot2_2[3] != 51.0:
                rotation_robot2_2[3] -= 2.0
            if rotation_robot2_2[4] != 0:
                rotation_robot2_2[4] -= 5.0
            if rotation_robot2_2[5] != 15:
                rotation_robot2_2[5] += 5.0
            if rotation_robot2_2[0] == -246.5 and rotation_robot2_2[1] == -79.0 and rotation_robot2_2[2] == 0 and rotation_robot2_2[3] == 51.0 and rotation_robot2_2[4] == 0 and rotation_robot2_2[5] == 15:
                flag_rob2_2 = 8

        if flag_rob2_2 == 8:
            if rotation_robot2_2[5] != 0.0:
                rotation_robot2_2[5] -= 2.5
            if rotation_robot2_2[5] == 0.0:
                flag_rob2_2 = 9
                przes_szesc_wal.append(0)
                num_szesc_wal += 1

        if flag_rob2_2 == 9:
            if rotation_robot2_2[1] != -70:
                rotation_robot2_2[1] += 3.0
            if rotation_robot2_2[3] != 42:
                rotation_robot2_2[3] -= 3.0
            if rotation_robot2_2[1] == -70 and rotation_robot2_2[3] == 42:
                flag_rob2_2 = 10

        if flag_rob2_2 == 10:  # [-360.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            if rotation_robot2_2[0] != -360.0:
                if rotation_robot2_2[0] > -356.5:
                    rotation_robot2_2[0] -= 5.0
                else:
                    rotation_robot2_2[0] -= 0.5
            if rotation_robot2_2[1] != 0.0:
                rotation_robot2_2[1] += 5.0
            if rotation_robot2_2[2] != 0.0:
                rotation_robot2_2[2] -= 5.0
            if rotation_robot2_2[3] != 0.0:
                rotation_robot2_2[3] -= 7.0
            if rotation_robot2_2[4] != 0.0:
                rotation_robot2_2[4] -= 5.0
            if rotation_robot2_2[5] != 0.0:
                rotation_robot2_2[5] += 5.0
            if rotation_robot2_2[0] == -360.0 and rotation_robot2_2[1] == 0.0 and rotation_robot2_2[2] == 0.0 and rotation_robot2_2[3] == 0.0 and rotation_robot2_2[4] == 0.0 and rotation_robot2_2[5] == 0.0:
                flag_rob2_2 = 0
                rotation_robot2_2[0] = 0


def move_robot_3():

    global flag_rob3
    global przes_szesc_wal
    global num_szesc_wal
    global num_szesc_wal_last

    if animate == 1:

        if flag_rob3 == 1:  # [-171.5, 0, 2.5]
            if rotation_robot3[0] != -171.5:
                if rotation_robot3[0] > -170:
                    rotation_robot3[0] -= 5.0
                else:
                    rotation_robot3[0] -= 0.5
            if rotation_robot3[1] != 0.0:
                rotation_robot3[1] -= 6.0
            if round(rotation_robot3[2], 1) != 2.5:
                rotation_robot3[2] += 0.1

        if flag_rob3 == 2:
            if round(rotation_robot3[2], 1) != 1.4:
                rotation_robot3[2] -= 0.1
            if round(rotation_robot3[2], 1) == 1.4:
                flag_rob3 = 3
                num_szesc_wal -= 1
                przes_szesc_wal.pop(0)

        if flag_rob3 == 3:
            if round(rotation_robot3[2], 1) != 2.5:
                rotation_robot3[2] += 0.1
            if round(rotation_robot3[2], 1) == 2.5:
                flag_rob3 = 4

        if flag_rob3 == 4:  # [-0.5, 66.0, 2.5]
            if rotation_robot3[0] != -0.5:
                if rotation_robot3[0] < -1.5:
                    rotation_robot3[0] += 5.0
                else:
                    rotation_robot3[0] += 0.5
            if rotation_robot3[1] != 66.0:
                rotation_robot3[1] += 6.0
            if rotation_robot3[0] == -0.5 and rotation_robot3[1] == 66.0:
                flag_rob3 = 5

        if flag_rob3 == 5:
            if round(rotation_robot3[2], 1) != 1.4:
                rotation_robot3[2] -= 0.1
            if round(rotation_robot3[2], 1) == 1.4:
                flag_rob3 = 6
                przes_szesc_wal_last.append(0)
                num_szesc_wal_last += 1

        if flag_rob3 == 6:
            if round(rotation_robot3[2], 1) != 2.5:
                rotation_robot3[2] += 0.1
            if round(rotation_robot3[2], 1) == 2.5:
                flag_rob3 = 1


def freeze_glass(value):
    global flag_rob2_2
    flag_rob2_2 = 6


def drawText(value, x, y,  windowHeight, windowWidth, step=18):
    """Draw the given text at given 2D position in window."""
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    glPushMatrix()
    matrix = glGetDouble(GL_PROJECTION_MATRIX)

    glLoadIdentity()
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2i(x, y)
    lines = 0

    for character in value:
        if character == '\n':
            glRasterPos2i(x, y-(lines*18))
        else:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    glPopMatrix()
    glLoadMatrixd(matrix)  # should have un-decorated alias for this...

    glMatrixMode(GL_MODELVIEW)


def szescian(d, num_text):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glBegin(GL_QUADS)
    glNormal3d(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d, d, d)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d, d, d)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d, -d, d)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d, -d, d)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d, d, d)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(d, -d, d)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d, -d, -d)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d, d, -d)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(0, 1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d, d, d)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(d, d, -d)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d, d, -d)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-d, d, d)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(-1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-d, d, -d)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d, -d, -d)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d, -d, d)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-d, d, d)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(0, -1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-d, -d, d)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d, -d, -d)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d, -d, -d)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d, -d, d)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(0, 0, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d, -d, -d)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d, -d, -d)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d, d, -d)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d, d, -d)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def prostopadloscian(d1, d2, d3, num_text):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glBegin(GL_QUADS)
    glNormal3d(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d1, d2, d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d1, d2, d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d1, -d2, d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d1, -d2, d3)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d1, d2, d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(d1, -d2, d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d1, -d2, -d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d1, d2, -d3)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(0, 1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d1, d2, d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(d1, d2, -d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d1, d2, -d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-d1, d2, d3)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(-1, 0, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-d1, d2, -d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d1, -d2, -d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d1, -d2, d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(-d1, d2, d3)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(0, -1, 0)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(-d1, -d2, d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d1, -d2, -d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d1, -d2, -d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d1, -d2, d3)
    glEnd()

    glBegin(GL_QUADS)
    glNormal3d(0, 0, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d1, -d2, -d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d1, -d2, -d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d1, d2, -d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d1, d2, -d3)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def ekran_napis(d1, d2, d3, num_text):

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glBegin(GL_QUADS)
    glNormal3d(0, 0, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d1, -d2, -d3)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d1, -d2, -d3)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d1, d2, -d3)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d1, d2, -d3)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def ice_box(num_text1, num_text2):

    glPushMatrix()

    prostopadloscian(10, 5, 0.5, num_text1)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(14.5, 0.0, 10.5)
    prostopadloscian(15, 5, 0.5, num_text1)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(9.5, 0.0, 15.5)
    prostopadloscian(10, 5, 0.5, num_text1)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(14.5, 0.0, 10.5)
    prostopadloscian(15, 5, 0.5, num_text1)
    glRotatef(90.0, 1.0, .0, 0.0)
    glTranslatef(0.0, -10.0, 0.0)
    prostopadloscian(14, 10, 0.5, num_text2)

    glPopMatrix()


def walec(h, r, num_text):

    obj = gluNewQuadric()

    gluQuadricTexture(obj, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glEnable(GL_TEXTURE_2D)

    gluCylinder(obj, r, r, h, 100, 1)

    glPushMatrix()
    glTranslatef(0.0, 0.0, h)
    gluDisk(obj, 0, r, 100, 1)
    glPopMatrix()

    glPushMatrix()
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluDisk(obj, 0, r, 100, 1)
    glPopMatrix()

    glDisable(GL_TEXTURE_2D)


def pol_ramie(r, d, h, num_text):

    obj = gluNewQuadric()

    gluQuadricTexture(obj, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glEnable(GL_TEXTURE_2D)

    glPushMatrix()

    glPushMatrix()
    glRotatef(180.0, 0.0, 1.0, 0.0)

    gluPartialDisk(obj, 0, r, 100, 1, 0, 180)
    glPopMatrix()

    glPushMatrix()
    glRotatef(180.0, 1.0, 0.0, 0.0)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, h)
    gluPartialDisk(obj, 0, r, 100, 1, 0, 180)
    glPopMatrix()

    glRotatef(180.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, -h)
    glBegin(GL_QUAD_STRIP)

    i = 0
    for angle in lin:
        u = lin[i] / np.pi
        x = r * np.sin(angle)
        y = r * np.cos(angle)
        glNormal3d(np.sin(angle), np.cos(angle), 0.0)
        glTexCoord2d(u, 1.0)
        glVertex3d(x, y, 0)
        glTexCoord2d(u, 0.0)
        glVertex3d(x, y, h)
        i += 1
    glEnd()
    glPopMatrix()

    glDisable(GL_TEXTURE_2D)


def ramie(r1, r2, d, h, num_text1, num_text2):

    pol_ramie(r1, d, h, num_text1)

    glPushMatrix()
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glTranslatef(-d, 0.0, -h)
    pol_ramie(r2, d, h, num_text1)
    glPopMatrix()

    glBindTexture(GL_TEXTURE_2D, num_text2)
    glEnable(GL_TEXTURE_2D)

    glBegin(GL_QUADS)

    n = get_normal_vector(np.array([0, r1, 0]), np.array([0, r1, h]), np.array([d, r2, h]))
    glNormal3d(n[0], n[1], n[2])
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, r1, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(0, r1, h)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d, r2, h)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d, r2, 0)

    n = get_normal_vector(np.array([d, -r2, 0]), np.array([d, -r2, h]), np.array([0, -r1, h]))
    glNormal3d(n[0], n[1], n[2])
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d, -r2, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(d, -r2, h)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(0, -r1, h)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(0, -r1, 0)

    glNormal3d(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, r1, h)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(0, -r1, h)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d, -r2, h)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d, r2, h)

    glNormal3d(0, 0, -1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(0, r1, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(d, r2, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(d, -r2, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(0, -r1, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)


def stozek(h, rs, rb, num_text):

    obj = gluNewQuadric()

    gluQuadricTexture(obj, GL_TRUE)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glEnable(GL_TEXTURE_2D)

    glPushMatrix()

    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluCylinder(obj, rs, rb, h, 100, 1)

    glPushMatrix()
    glTranslatef(0.0, 0.0, h)
    gluDisk(obj, 0, rb, 100, 1)
    glPopMatrix()

    glPushMatrix()
    glRotatef(180.0, 1.0, 0.0, 0.0)
    gluDisk(obj, 0, rs, 100, 1)
    glPopMatrix()

    glPopMatrix()

    glDisable(GL_TEXTURE_2D)


def pol_chwyt(r, d, h):

    glPushMatrix()
    ramie(r, r, d, h)
    glTranslate(d, 0.0, 0.0)
    glRotatef(45, 0.0, 0.0, 1.0)
    ramie(r, r, d, h)
    glPopMatrix()


def piec():

    glPushMatrix()

    prostopadloscian(8.0, 5.0, 1.0, 9)
    glTranslatef(0.0, 0.0, 0.1)
    prostopadloscian(3.0, 2.0, 1.0, 8)

    glPopMatrix()


def tunel():

    glPushMatrix()

    prostopadloscian(8.0, 5.0, 4.0, 9)
    glTranslatef(0.0, 0.0, 0.1)
    prostopadloscian(3.0, 2.0, 4.0, 3)

    glPopMatrix()


def polka(num_text):
    glPushMatrix()
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(-8.0, 49.0, 0.0)
    glPushMatrix()
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, 5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, 5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, 5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, 5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, -25.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, -5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, -5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glTranslatef(0.0, 0.0, -5.0)
    prostopadloscian(8.0, 1.0, 1.0, num_text)
    glPopMatrix()
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.1, -5.0)
    prostopadloscian(20.0, 1.0, 0.5, num_text)
    glTranslatef(0.0, 0.0, 5.0)
    prostopadloscian(20.0, 1.0, 0.5, num_text)
    glTranslatef(0.0, 0.0, 5.0)
    prostopadloscian(20.0, 1.0, 0.5, num_text)
    glPopMatrix()


def window():

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 10.0, 30.0)
    prostopadloscian(10.1, 4.1, 0.2, 1)
    glTranslatef(0.0, 0.0, -0.1)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    prostopadloscian(10.0, 4.0, 0.2, 14)
    glPopMatrix()


def powierzchnia(d1, d2, num_text):

    glPushMatrix()

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, num_text)

    glBegin(GL_QUADS)
    glNormal3d(0, 0, 1)
    glTexCoord2f(0.0, 0.0)
    glVertex3d(d1, d2, 0)
    glTexCoord2f(1.0, 0.0)
    glVertex3d(-d1, d2, 0)
    glTexCoord2f(1.0, 1.0)
    glVertex3d(-d1, -d2, 0)
    glTexCoord2f(0.0, 1.0)
    glVertex3d(d1, -d2, 0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

    glPopMatrix()


def tasma(fig):

    global tasma_rot
    global przes_szesc
    global przes_walec
    global przes_szesc_wal_last
    global num_szesc_wal_last
    global flag_rob2_1
    global flag_rob2_2
    global flag_rob3
    global stop_szescian
    global stop_walec

    if fig == 'szescian':
        k = 0
        if animate == 1:
            if stop_szescian == 0:
                tasma_rot[k] -= 10.0
        else:
            tasma_rot[k] = 0.0
    if fig == 'walec':
        k = 1
        if animate == 1:
            if stop_walec == 0:
                tasma_rot[k] -= 10.0
        else:
            tasma_rot[k] = 0.0
    if fig == 'szesc_wal':
        k = 2
        if flag_rob3 != 2:
            if animate == 1:
                tasma_rot[k] -= 10.0
        else:
            tasma_rot[k] = 0
    if fig == 'szesc_wal_last':
        k = 3
        if animate == 1:
            tasma_rot[k] -= 10.0

    glPushMatrix()

    ramie(1, 1, 30, 5, 10, 10)
    glTranslatef(0.0, 0.0, -1.5)
    glPushMatrix()
    glRotatef(tasma_rot[k], 0.0, 0.0, 1.0)
    walec(8, 0.5, 1)
    glPopMatrix()
    glTranslatef(30.0, 0.0, 0.0)
    glPushMatrix()
    glRotatef(tasma_rot[k], 0.0, 0.0, 1.0)
    walec(8, 0.5, 1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-15.0, 0.0, 0.5)
    prostopadloscian(15.7, 1.0, 0.3, 3)
    glRotatef(90.0, 0.0, 0.0, 1.0)
    glTranslatef(-3.0, -14.7, -0.05)
    prostopadloscian(4, 1.0, 0.3, 3)
    glTranslatef(0.0, 29.4, -0.1)
    prostopadloscian(4, 1.0, 0.3, 3)
    glPopMatrix()

    glTranslatef(0.0, 0.0, 6.5)

    glPushMatrix()
    glTranslatef(-15.0, 0.0, 1.0)
    prostopadloscian(15.7, 1.0, 0.3, 3)
    glRotatef(90.0, 0.0, 0.0, 1.0)
    glTranslatef(-3.0, -14.7, 0.1)
    prostopadloscian(4, 1.0, 0.3, 3)
    glTranslatef(0.0, 29.4, 0)
    prostopadloscian(4, 1.0, 0.3, 3)
    glPopMatrix()

    for i in range(0, num_szescian):
        if przes_szesc[i] <= 23.0:
            if animate == 1:
                przes_szesc[i] += 0.2
        else:
            if flag_rob2_2 == 0:
                flag_rob2_2 = 1
            stop_szescian = 1
        if fig == 'szescian':
            glPushMatrix()
            glTranslatef(przes_szesc[i], 0.0, 0.0)
            glTranslatef(-25.0, 2.0, -14.0)
            glRotatef(-35.0, 0.0, 1.0, 0.0)
            glTranslatef(-0.7, 0.0, 0.0)
            szescian(0.9, 8)
            glPopMatrix()

    for i in range(0, num_walec):
        if przes_walec[i] <= 23.0:
            if animate == 1:
                przes_walec[i] += 0.2
        else:
            if flag_rob2_1 == 0 and flag_rob2_2 == 1:
                flag_rob2_1 = 1
            stop_walec = 1
        if fig == 'walec':
            glPushMatrix()
            glTranslatef(przes_walec[i], 0.0, 0.0)
            glTranslatef(-25.0, 2.0, 7.0)
            glRotatef(35.0, 0.0, 1.0, 0.0)
            glTranslatef(-1.6, 0.0, 0.25)
            walec(2.6, 1.0, 8)
            glPopMatrix()

    for i in range(0, num_szesc_wal):
        if przes_szesc_wal[i] <= 25.0:
            if animate == 1:
                przes_szesc_wal[i] += 0.2
        else:
            if flag_rob3 == 1:
                flag_rob3 = 2
        if fig == 'szesc_wal':
            glPushMatrix()
            glTranslatef(przes_szesc_wal[i], 0.0, 0.0)
            glTranslatef(-29.0, 2.0, -3.0)
            glRotatef(31.0, 0.0, 1.0, 0.0)
            glTranslatef(0.3, 0.0, -0.3)
            szescian(0.9, 12)
            walec(3.0, 0.8, 12)
            glPopMatrix()

    for i in range(0, num_szesc_wal_last):
        if przes_szesc_wal_last[i] <= 27.0:
            if animate == 1:
                przes_szesc_wal_last[i] += 0.2
        else:
            przes_szesc_wal_last.pop(0)
            num_szesc_wal_last -= 1
        if fig == 'szesc_wal_last':
            glPushMatrix()
            glTranslatef(przes_szesc_wal_last[i], 0.0, 0.0)
            glTranslatef(-29.0, 2.0, -3.0)
            glTranslatef(0.3, 0.0, -0.3)
            szescian(0.9, 12)
            walec(3.0, 0.8, 12)
            glPopMatrix()

    glPopMatrix()


def robot1(d1, d2, d3, d4, fig):

    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    walec(0.5, 1.0, 1)
    glTranslatef(0.0, 0.0, 0.5)
    glRotatef(d1, 0.0, 0.0, 1.0)
    walec(1.5, 0.5, 1)
    glTranslatef(0.0, 0.0, 1.5)
    walec(1.5, 0.3, 1)
    glTranslatef(0.0, 0.0, 1.5)
    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(d2, 0.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, -0.5)
    walec(1.0, 0.3, 1)
    glTranslatef(0.0, 0.0, -0.3)
    glRotatef(90, 0.0, 0.0, 1.0)
    ramie(0.5, 0.5, 3, 0.3, 3, 6)
    glTranslatef(0.0, 0.0, 1.3)
    ramie(0.5, 0.5, 3, 0.3, 3, 6)
    glTranslatef(3.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, -0.3)
    glRotatef(d3, 0.0, 0.0, 1.0)
    ramie(0.5, 0.5, 3, 0.3, 3, 6)
    glTranslatef(0.0, 0.0, -0.7)
    ramie(0.5, 0.5, 3, 0.3, 3, 6)
    glTranslatef(3.0, 0.0, 0.3)
    glRotatef(d4, 0.0, 0.0, 1.0)
    walec(0.4, 0.2, 1)
    ramie(0.3, 0.3, 1, 0.2, 3, 6)
    glTranslatef(0.0, 0.0, 0.2)
    ramie(0.3, 0.3, 1, 0.2, 3, 6)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 0.5)
    stozek(0.3, 0.05, 0.1, 4)
    if flag_rob1 == 3 or flag_rob1 == 4 or flag_rob1 == 5:
        if fig == 'szescian':
            glPushMatrix()
            glTranslatef(0.0, 0.0, 0.3)
            szescian(0.3, 8)
            glPopMatrix()
        if fig == 'walec':
            glPushMatrix()
            glRotatef(90.0, 1.0, 0.0, 0.0)
            glTranslatef(0.0, 0.3, -0.5)
            walec(1.0, 0.3, 8)
            glPopMatrix()
    glPopMatrix()


def robot2(d1, d2, d3, d4, d5, d6, fig):

    glPushMatrix()

    glRotatef(-90.0, 1.0, 0.0, 0.0)
    stozek(0.5, 0.3, 0.5, 2)
    glRotatef(d1, 0.0, 0.0, 1.0)
    walec(0.5, 0.3, 1)
    glTranslatef(0.0, 0.0, 0.7)
    stozek(0.2, 0.2, 0.3, 2)
    glTranslatef(0.0, 0.0, -0.35)
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-45+d2, 0.0, 0.0, 1.0)
    walec(0.8, 0.3, 1)
    glTranslatef(0.0, 0.0, 1.0)
    stozek(0.2, 0.2, 0.3, 2)
    glTranslatef(0.0, 0.0, -0.5)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    walec(0.5, 0.3, 1)
    glTranslatef(0.0, 0.0, 0.7)
    stozek(0.2, 0.2, 0.3, 2)
    glRotatef(d3, 0.0, 0.0, 1.0)
    walec(2.5, 0.2, 1)
    glTranslatef(0.0, 0.0, 2.5)
    glRotatef(180, 0.0, 1.0, 0.0)
    stozek(0.2, 0.2, 0.3, 2)
    glRotatef(180, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, 0.2)
    walec(0.5, 0.3, 1)
    glRotatef(90, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.5, -0.4)
    walec(0.8, 0.3, 1)
    glTranslatef(0.0, 0.0, 1.0)
    stozek(0.2, 0.2, 0.3, 2)
    glTranslatef(0.0, 0.0, -1.8)
    glRotatef(45+d4, 0.0, 0.0, 1.0)
    walec(0.8, 0.3, 1)
    glRotatef(180, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 0.2)
    stozek(0.2, 0.2, 0.3, 2)
    glRotatef(180, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 0.0, 0.6)
    glRotatef(90, 1.0, 0.0, 0.0)
    walec(0.5, 0.3, 1)
    glTranslatef(0.0, 0.0, 0.7)
    stozek(0.2, 0.2, 0.3, 2)
    glRotatef(d5, 0.0, 0.0, 1.0)
    walec(2.0, 0.2, 1)
    glTranslatef(0.0, 0.0, 2.3)
    stozek(0.3, 0.1, 0.2, 2)

    glPushMatrix()

    glRotatef(90, 0.0, 0.0, 1.0)
    glRotatef(90, 1.0, 0.0, 0.0)
    glTranslatef(0.15, -0.15, 0.0)
    glRotatef(45, 0.0, 0.0, 1.0)
    ramie(0.05, 0.05, 0.3, 0.01, 3, 3)
    glTranslatef(0.3, 0.0, 0.0)
    glRotatef(15+d6, 0.0, 0.0, 1.0)
    ramie(0.05, 0.05, 0.3, 0.01, 3, 3)
    glTranslate(0.3, 0.0, 0.0)
    glRotatef(45, 0.0, 0.0, 1.0)
    ramie(0.05, 0.05, 0.3, 0.01, 3, 3)

    glPopMatrix()

    glPushMatrix()

    glRotatef(-90, 0.0, 0.0, 1.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    glTranslatef(0.15, 0.15, 0.0)
    glRotatef(-45, 0.0, 0.0, 1.0)
    ramie(0.05, 0.05, 0.3, 0.01, 3, 3)
    glTranslatef(0.3, 0.0, 0.0)
    glRotatef(-15-d6, 0.0, 0.0, 1.0)
    ramie(0.05, 0.05, 0.3, 0.01, 3, 3)
    glTranslate(0.3, 0.0, 0.0)
    glRotatef(-45, 0.0, 0.0, 1.0)
    ramie(0.05, 0.05, 0.3, 0.01, 3, 3)

    glPopMatrix()

    if flag_rob2_2 == 6 or flag_rob2_2 == 7 or flag_rob2_2 == 8:
        num_text = 12
    else:
        num_text = 8

    if flag_rob2_2 == 2 or flag_rob2_2 == 3 or flag_rob2_2 == 4 or flag_rob2_2 == 5 or flag_rob2_2 == 6 or flag_rob2_2 == 7 or flag_rob2_2 == 8:
        if fig == 'szescian':
            glPushMatrix()
            glRotatef(90, 0.0, 1.0, 0.0)
            glTranslate(-0.6, 0.0, -0.2)
            glRotatef(-55, 0.0, 1.0, 0.0)
            glRotatef(5, 1.0, 0.0, 0.0)
            glTranslate(0.0, 0.0, -0.03)
            szescian(0.28, num_text)
            if flag_rob2_1 == 4 or flag_rob2_1 == 5 or flag_rob2_1 == 0:
                walec(0.8, 0.28, num_text)
            glPopMatrix()

    if flag_rob2_1 == 2 or flag_rob2_1 == 3:
        if fig == 'walec':
            glPushMatrix()
            glRotatef(90, 0.0, 1.0, 0.0)
            glTranslate(-0.38, 0.0, -0.15)
            glRotatef(-15, 1.0, 0.0, 0.0)
            glRotatef(-55, 0.0, 1.0, 0.0)
            walec(0.8, 0.28, num_text)
            glPopMatrix()

    glPopMatrix()


def robot3(d1, d2, d3):

    glPushMatrix()

    walec(0.2, 2.0, 4)
    glTranslatef(0.0, 0.0, 0.2)
    walec(5.0, 1.0, 4)
    glTranslatef(0.0, 0.0, 5.7)
    stozek(0.7, 0.5, 1.0, 4)
    glRotatef(d1, 0.0, 0.0, 1.0)
    ramie(0.5, 0.5, 3.0, 0.3, 5, 5)
    glTranslatef(3.0, 0.0, 0.3)
    glRotatef(d2, 0.0, 0.0, 1.0)
    walec(0.5, 0.5, 1)
    glTranslatef(0.0, 0.0, 0.5)
    ramie(0.5, 0.5, 2.0, 3.0, 5, 5)
    glTranslatef(2.0, 0.0, 0.3)
    glTranslatef(0.0, 0.0, -3.3+d3)
    walec(3.0, 0.2, 4)
    stozek(0.2, 0.2, 0.1, 2)

    if flag_rob3 == 3 or flag_rob3 == 4 or flag_rob3 == 5:

        glRotatef(90.0, 1.0, 0.0, 0.0)
        glRotatef(-66.0, 0.0, 1.0, 0.0)
        glTranslatef(0.0, -0.6, -0.8)
        szescian(0.5, 12)
        walec(1.7, 0.4, 12)

    glPopMatrix()


def scena(rob1, rob2_1, rob2_2, rob3):

    glRotatef(-90.0, 1.0, 0.0, 0.0)

    glPushMatrix()
    glTranslatef(0.0, 10.0, 0.0)
    powierzchnia(30, 40, 7)
    glPopMatrix()

    glPushMatrix()
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(30.0, 10.0, -30.0)
    powierzchnia(30, 40, 7)
    glPopMatrix()

    glPushMatrix()
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    glTranslatef(30.0, -10.0, -30.0)
    powierzchnia(30, 40, 7)
    glPopMatrix()

    glPushMatrix()
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(90.0, 0.0, 0.0, 1.0)
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, -30.0, -50.0)
    powierzchnia(30, 30, 7)
    glPopMatrix()

    glPushMatrix()
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glRotatef(-90.0, 0.0, 0.0, 1.0)
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 30.0, -30.0)
    glRotatef(180.0, 0.0, 0.0, 1.0)
    powierzchnia(30, 30, 7)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.0, 10.0, 60.0)
    glRotatef(180.0, 1.0, 0.0, 0.0)
    powierzchnia(30, 40, 7)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-8.0, -20.0, 0.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glScalef(1.5, 1.5, 1.5)
    robot1(rob1[0], rob1[1], rob1[2], rob1[3], 'szescian')
    glPopMatrix()

    glPushMatrix()
    glTranslatef(8.0, -20.0, 0.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glScalef(1.5, 1.5, 1.5)
    robot1(-rob1[0], rob1[1], rob1[2], rob1[3], 'walec')
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10.0, 8.5, 0.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 1.0, 0.0)
    glScalef(2.0, 2.0, 2.0)
    robot2(rob2_1[0], rob2_1[1], rob2_1[2], rob2_1[3], rob2_1[4], rob2_1[5], 'walec')
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-10.0, 6.0, 0.0)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 1.0, 0.0)
    glScalef(2.0, 2.0, 2.0)
    robot2(rob2_2[0], rob2_2[1], rob2_2[2], rob2_2[3], rob2_2[4], rob2_2[5], 'szescian')
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5.0, 27.0, 0.0)
    robot3(rob3[0], rob3[1], rob3[2])
    glPopMatrix()

    glPushMatrix()
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glTranslatef(-8.0, -5.0, -29.0)
    piec()
    glTranslatef(16.0, 0.0, 0.0)
    piec()
    glPopMatrix()

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(2.0, 3.5, 15.0)
    glScale(0.6, 0.5, 0.6)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    tasma('szescian')
    glPopMatrix()

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(-5.0, 3.5, 15.0)
    glScale(0.6, 0.5, 0.6)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    tasma('walec')
    glPopMatrix()

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(-1.6, 3.5, -10.0)
    glScale(0.6, 0.5, 0.6)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    tasma('szesc_wal')
    glPopMatrix()

    glPushMatrix()
    glScale(0.3, 0.3, 0.3)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(-70.0, 5.0, -5.0)
    ice_box(1, 11)
    glPopMatrix()

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(8.0, 3.5, -30.5)
    glScale(0.6, 0.5, 0.6)
    tasma('szesc_wal_last')
    glPopMatrix()

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glRotatef(-90.0, 0.0, 1.0, 0.0)
    glTranslatef(-29.0, 5.0, -26.0)
    tunel()
    glRotatef(90.0, 0.0, 0.0, 1.0)
    glRotatef(180.0, 0.0, 1.0, 0.0)
    glTranslatef(-5.0, 0.0, -4.0)
    pol_ramie(8.0, 10.0, 8.0, 9)
    glPopMatrix()

    polka(13)

    glPushMatrix()
    glRotatef(90.0, 0.0, 0.0, 1.0)
    glTranslatef(0.0, -20.0, 0.0)
    polka(13)
    glPopMatrix()

    window()

    glPushMatrix()
    glRotatef(90.0, 1.0, 0.0, 0.0)
    glTranslatef(0.0, 18.0, 30.0)
    glRotatef(180, 0.0, 0.0, 1.0)
    glRotatef(-25.0, 0.0, 0.0, 1.0)
    ekran_napis(8.0, 3.0, 0.3, 15)
    glPopMatrix()

    glPushMatrix()
    glRotatef(25.0, 0.0, 0.0, 1.0)
    glTranslatef(20.0, -5.0, 0.0)
    prostopadloscian(0.5, 1.0, 2.0, 55)
    glTranslatef(0.0, 0.0, 4.0)
    prostopadloscian(0.5, 6.0, 2.0, 55)
    glRotatef(-90.0, 1.0, 0.0, 0.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glTranslatef(0.0, 0.0, -0.45)
    ekran_napis(6.0, 2.0, 0.1, gif_frame+16)
    glPopMatrix()


def main():
    glutInit(sys.argv)
    glutInitWindowSize(window_size[0], window_size[1])
    glutInitWindowPosition(300, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGBA)
    glutCreateWindow('OpenGL Project')
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutReshapeFunc(reshape)
    createPopupMenus()
    glutTimerFunc(1000//set_fps, robots_move, 0)
    init()
    glutMainLoop()


main()
