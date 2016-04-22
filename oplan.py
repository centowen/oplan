#!/usr/bin/python
import sys

import matplotlib as mpl
import matplotlib.pylab as pl
import os

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

import numpy as np
from math import pi
from ApplicationWindow import ApplicationWindow
from PyQt4 import QtGui, QtCore
from sources import readSources
from sourceKeeper import SourceKeeper
from sourceTree import SourceTree

def main():
    app = QtGui.QApplication(sys.argv)
    projectperiods = []
    projectperiods.append({'file': 'sthml_course.csv' ,
        'name': 'sthml'})
#     projectperiods.append({'file': '/home/lindroos/jobb/apex/P94/APEX-P94-PB.csv' ,
#         'name': 'P94'})
#     projectperiods.append({'file': '/home/lindroos/jobb/apex/P93/APEX-P93.csv' ,
#         'name': 'P93'})
#     sources = SourceDB(periods)
    sources = readSources(projectperiods)


    sourceTree = SourceTree(sources)

    sourceKeeper = SourceKeeper(sources, np.linspace(0,24,100), sourceTree)
    sourceKeeper.update()

    mainWindow = ApplicationWindow(sources, sourceTree, sourceKeeper)
    updateTimer = QtCore.QTimer()
    updateTimer.timeout.connect(mainWindow.update)
    updateTimer.start(500)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

