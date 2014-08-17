#!/usr/bin/python
import sys

import matplotlib as mpl
import matplotlib.pylab as pl

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

import numpy as np
from math import pi
from ApplicationWindow import ApplicationWindow
from PyQt4 import QtGui

def main():
    app = QtGui.QApplication(sys.argv)
    mainWindow = ApplicationWindow()
    mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()

