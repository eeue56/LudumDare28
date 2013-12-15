#!/usr/bin/python2

from __future__ import division

# PyQT4 imports
from PyQt4 import QtGui, QtCore, QtOpenGL
from PyQt4.QtOpenGL import QGLWidget
# PyOpenGL imports
import OpenGL.GL as gl
import OpenGL.arrays.vbo as glvbo

from random import choice, randint

from nigeludum.world import World
from nigeludum.misc import *

from nigeludum.world_objects import Player, Wall, Bomb, OldGrumper
from nigeludum.levels import Level, LevelController


class GLPlotWidget(QGLWidget):

    def __init__(self, width, height, world, *args):
        QGLWidget.__init__(self, *args)
        self.width = width
        self.height = height
        self.world = world
 
    def initializeGL(self):
        """Initialize OpenGL, VBOs, upload data on the GPU, etc.
        """
        # background color
        gl.glClearColor(0,0,0,0)
        gl.glViewport(0, 0, self.width, self.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()

    def paintGL(self):
        """Paint the scene.
        """
        # clear the buffer
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)

        self.world.draw()
        
    def resizeGL(self, width, height):
        """Called upon window resizing: reinitialize the viewport.
        """
        # update the window size    
        self.width, self.height = width, height
        # paint within the whole window
        gl.glViewport(0, 0, self.width, self.height)
        # set orthographic projection (2D only)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        # the window corner OpenGL coordinates are the same as the world height and width
        gl.glOrtho(0, self.world.width, 0, self.world.height, -1, 1)

 
if __name__ == '__main__':
    # import numpy for generating random data points
    import sys

 
    # define a QT window with an OpenGL widget inside it
    class TestWindow(QtGui.QMainWindow):
        def __init__(self):
            super(TestWindow, self).__init__()
            # initialize the GL widget
            self.player = Player(50, 50, COLOURS['white'], DIRECTIONS['up'])

            level1 = Level(COLOURS['black'], {DIRECTIONS['left'] : 0}, 100, 100)
            level = Level(COLOURS['grey'], {DIRECTIONS['right'] : 1}, 100, 100)

            for x in (DIRECTIONS['up'], DIRECTIONS['right'], DIRECTIONS['left'], DIRECTIONS['down']):
                level.add_object(Wall(100, 100, 5, gaps=range(20, 40), facing=x))
                level1.add_object(Wall(100, 100, 2, gaps=range(40, 60), facing=x))
            level.add_object(Bomb(20, 20, facing=DIRECTIONS['still']))


            levels = {
                0:level,
                1:level1
            }

            level.add_object(OldGrumper(70, 70, color=COLOURS['white'],facing=DIRECTIONS['still']))

            level_controller = LevelController(level, levels)

            self.world = World(self.player, level_controller)

            self.widget = GLPlotWidget(100, 100, self.world)
            self.keys = set()

            self.widget.setGeometry(0, 0, self.widget.width, self.widget.height)
            self.setCentralWidget(self.widget)
            self.show()

            self.paint_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.paint_timer, QtCore.SIGNAL("timeout()"), self.widget.updateGL)
            
            self.button_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.button_timer, QtCore.SIGNAL("timeout()"), self.check)

            self.tick_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.tick_timer, QtCore.SIGNAL("timeout()"), self.world.tick)

            self.clean_timer = QtCore.QTimer()
            QtCore.QObject.connect(self.clean_timer, QtCore.SIGNAL("timeout()"), self.world.clean_up)


            QtCore.QMetaObject.connectSlotsByName(self)
            
            self.paint_timer.start(30)
            self.button_timer.start(25)
            self.tick_timer.start(25)
            self.clean_timer.start(200)


            self.resize(600, 400)

            self._need_to_place = False

        def keyPressEvent(self, event):
            if event.key() == QtCore.Qt.Key_Space:
                self._need_to_place = True

            self.keys.add(event.key())

        def keyReleaseEvent(self, event):
            try:
                self.keys.remove(event.key())
            except:
                pass

        def check(self):
            face_movement = DIRECTIONS['still']

            for key in self.keys:  

                if key == QtCore.Qt.Key_A:
                    face_movement += DIRECTIONS['left']
                elif key == QtCore.Qt.Key_D:
                    face_movement += DIRECTIONS['right']
                elif key == QtCore.Qt.Key_W:
                    face_movement += DIRECTIONS['up']
                elif key == QtCore.Qt.Key_S:
                    face_movement += DIRECTIONS['down']

                if self._need_to_place and key == QtCore.Qt.Key_Space:
                    self._need_to_place = False
                    self.world.player.place_bomb(self.world)

            self.world.player.facing = face_movement
 
    # create the QT App and window
    app = QtGui.QApplication(sys.argv)
    window = TestWindow()
    window.show()
    app.exec_()
