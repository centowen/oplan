import matplotlib as mpl
import matplotlib.pylab as pl
from PyQt4 import QtCore, QtGui
from VisibilityPlotCanvas import VisibilityPlotCanvas

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        print('in ApplicationWindow.__init__(self)')
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle('Visibilty plotter.')

        self.fileMenu = QtGui.QMenu('&File', self)
        self.fileMenu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL+QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.fileMenu)

        self.main_widget = QtGui.QWidget(self)
        self.l = QtGui.QVBoxLayout(self.main_widget)
        self.vp = VisibilityPlotCanvas(self, width=5, height=4, dpi=100)

        print('Adding VisibilityPlot to QVBoxLayout')
        self.l.addWidget(self.vp)
        print('Added VisibilityPlot to QVBoxLayout')
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)
        self.setLayout(self.l)

#         self.statusBar().showMessage('APEX-1')
        print('done ApplicationWindow.__init__(self)')

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()
