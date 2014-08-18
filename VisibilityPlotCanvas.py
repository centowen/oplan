import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from VisibilityPlotter import getElevation
import ephem
import os
from PyQt4 import QtCore, QtGui
from math import pi
from readProjects import readProjects

class VisibilityPlotCanvas(FigureCanvas):


    def __init__(self, parent=None, sources=None, width=5, height=4, dpi=100, *args, **kwargs):
        self.frontend = 'SHFI-2'
        self.min_separation = 50
        self.min_grade = 2.0
        self.begin_shift = 17.
        self.end_shift = 18+4
        self.select_proj = None
        self.sources = sources

        print('in VisibilityPlot.__init__(self, ...)')
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(VisibilityPlotCanvas, self).__init__(self.fig)
        self.setParent(parent)

        self.compute_initial_figure()
        self.compute_coordinates()
        self.update_figure()
        print('done with VisibilityPlot.__init__(self, ...)')

        FigureCanvas.setSizePolicy(self,
                QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        print('start plotting')
        x = np.linspace(0,2*pi, 1000)
        self.axes.plot(x, np.sin(x))
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('sin(x)')
        self.axes.patch.set_facecolor('white')
        print('done plotting')

    def compute_coordinates(self):
        self.objs = []
        self.objs.append(ephem.Sun())
        for project in readProjects('/home/lindroos/jobb/apex/P94/APEX-P94-PB.csv'):
            if self.frontend.lower() in project['frontend']:
                filename = '/home/lindroos/jobb/apex/P94/ephems/o-'+project['id'].lower()+'-2014.edb'
                if filename[-10] == 'a' and not os.access(filename, os.F_OK):
                    f = list(filename)
                    f[-10] = 'b'
                    filename = ''.join(f)
                if filename[-10] == 'b' and not os.access(filename, os.F_OK):
                    f = list(filename)
                    f[-10] = 'a'
                    filename = ''.join(f)

                if (float(project['grade']) < self.min_grade 
                    and (self.select_proj is None or project['id'] in self.select_proj) 
                    and os.access(filename, os.F_OK)):


                    catfile = open(filename)
                    projobjs = []
                    for line in catfile:
                        obj = ephem.readdb(line)
                        obj.name = project['id'][6:]+'_'+obj.name
                        obj.compute(ephem.now())
                        for oldobj in projobjs:
                            if ephem.separation(oldobj, obj)*180./pi < self.min_separation:
                                oldobj.name = project['id'][6:]+'_multi'
                                obj = None
                                break
                        if obj is not None:
                            projobjs.append(obj)
                    self.objs.extend(projobjs)

        self.time = np.linspace(0,24,1000)
        self.eles = getElevation(self.time, self.objs)

    def update_figure(self):
        self.compute_coordinates()
        self.axes.clear()
        for (obj, ele) in zip(self.sources.objs, self.sources.eles):
            self.axes.plot(self.time, ele, label=obj.name, color='#888888')
#             pl.text(time[np.argmax(ele)], np.max(ele)+0.1, obj.name, horizontalalignment='center')
        self.axes.plot(self.time, 0*self.time+30, 'r')
#         self.axes.plot(self.time, 0*self.time+60, 'c')
#         self.axes.plot(self.time, 0*self.time+70, 'b')
        self.axes.plot(self.time, 0*self.time+80, 'b')
#         pl.plot([BEGIN_SHIFT, BEGIN_SHIFT], [-1,91], 'k--')
#         pl.plot([END_SHIFT, END_SHIFT], [-1,91], 'k--')
        self.axes.axis([0, 24, -1, 91])
        self.axes.set_xlabel('UT [h]')
        self.axes.set_ylabel('Altitude [deg]')
        self.fig.patch.set_facecolor('white')

        

