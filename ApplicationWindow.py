import matplotlib as mpl
import matplotlib.pylab as pl
from PyQt4 import QtCore, QtGui
from VisibilityPlotCanvas import VisibilityPlotCanvas
from MainWindow_ui import Ui_MainWindow

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

#from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self, sources, sourceTree, sourceKeeper):
        print('in ApplicationWindow.__init__(self)')
        QtGui.QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.sourceKeeper = sourceKeeper
#         self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
#         self.setWindowTitle('Visibilty plotter.')

#         self.fileMenu = QtGui.QMenu('&File', self)
#         self.fileMenu.addAction('&Quit', self.fileQuit, QtCore.Qt.CTRL+QtCore.Qt.Key_Q)
#         self.menuBar().addMenu(self.fileMenu)

#         self.main_widget = QtGui.QWidget(self)
        self.l = QtGui.QVBoxLayout(self.ui.visPlotCanvas)
        self.vp = VisibilityPlotCanvas(self, width=5, height=4, 
                sources=sources, sourceKeeper=sourceKeeper, dpi=100)


        self.l.addWidget(self.vp)
        self.ui.sourceSelector.setModel(sourceTree)
        self.sourceKeeper.sourceSelector = self.ui.sourceSelector
        QtCore.QObject.connect(self.ui.sourceSelector.selectionModel(),
                QtCore.SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), 
                self.sourceKeeper.sourceSelected)
        QtCore.QObject.connect(self.ui.actionFlip_activity, 
                QtCore.SIGNAL(_fromUtf8("activated()")),
                self.sourceKeeper.swapSelected)

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

    def update(self):
        self.vp.update_figure()
# 
#     def fileQuit(self):
#         self.close()
# 
#     def closeEvent(self, ce):
#         self.fileQuit()
