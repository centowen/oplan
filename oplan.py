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
from PyQt4 import QtGui
from sources import SourceDB

def main():
    app = QtGui.QApplication(sys.argv)
    periods = []
    periods.append({'file': '/home/lindroos/jobb/apex/P94/APEX-P94-PB.csv' ,
        'name': 'P94'})
    periods.append({'file': '/home/lindroos/jobb/apex/P93/APEX-P93.csv' ,
        'name': 'P93'})
    sources = SourceDB(periods)
    mainWindow = ApplicationWindow(sources)
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

