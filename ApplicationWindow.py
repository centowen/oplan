import matplotlib as mpl
import matplotlib.pylab as pl
from PyQt4 import QtCore, QtGui
from VisibilityPlotCanvas import VisibilityPlotCanvas
from MainWindow_ui import Ui_MainWindow

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self, sources):
        print('in ApplicationWindow.__init__(self)')
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         self.setWindowTitle('Visibilty plotter.')

#         self.fileMenu = QtGui.QMenu('&File', self)
#         self.fileMenu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL+QtCore.Qt.Key_Q)
#         self.menuBar().addMenu(self.fileMenu)

        self.main_widget = QtGui.QWidget(self)
        self.l = QtGui.QVBoxLayout(self.ui.visPlotCanvas)
        self.vp = VisibilityPlotCanvas(self, width=5, height=4, sources=sources, dpi=100)
# 
        self.l.addWidget(self.vp)
        self.main_widget.setFocus()
        self.ui.visPlotCanvas = self.main_widget

#         table_header = ['Project', 'Source name', 'grade', 'frontend']
#         table_header = [ 'Source name']
#         self.ui.sourceListTable.verticalHeader().hide()
#         self.ui.sourceListTable.setColumnCount(len(table_header))
#         self.ui.sourceListTable.setHorizontalHeaderLabels(table_header)
#         self.ui.sourceListTable.setRowCount(len(sources.objs))
#         for i, obj in enumerate(sources.objs):
#             self.ui.sourceListTable.setItem(i, 0, QtGui.QTableWidgetItem(obj.name))
#             self.ui.sourceListTable.setItem(i, 1, QTableWidgetItem(obj.name))
#             self.ui.sourceListTable.setItem(i, 2, QTableWidgetItem(obj.name))
#             self.ui.sourceListTable.setItem(i, 3, QTableWidgetItem(obj.name))

#         self.visPlotCanvas.setLayout(self.l)
#         self.visPlotCanvas = self.main_widget

#         self.statusBar().showMessage('APEX-1')
        print('done ApplicationWindow.__init__(self)')
# 
#     def fileQuit(self):
#         self.close()
# 
#     def closeEvent(self, ce):
#         self.fileQuit()
