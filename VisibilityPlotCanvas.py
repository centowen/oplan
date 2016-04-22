import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from VisibilityPlotter import getElevation
import ephem
import os
from PyQt4 import QtCore, QtGui
from math import pi
from readProjects import readProjects
import time as ti

class VisibilityPlotCanvas(FigureCanvas):


    def __init__(self, parent=None, sources=None, sourceKeeper = None,
                 width=5, height=4, dpi=100, *args, **kwargs):
#         self.frontend = 'SHFI-2'
#         self.min_separation = 50
#         self.min_grade = 2.0
        self.begin_shift = 17.
        self.end_shift = 18+4
        self.select_proj = None
        self.sources = sources
        self.sourceKeeper = sourceKeeper

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(VisibilityPlotCanvas, self).__init__(self.fig)
        self.setParent(parent)

#         self.compute_initial_figure()
#         self.compute_coordinates()
        self.update_figure()

        FigureCanvas.setSizePolicy(self,
                QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

#     def compute_initial_figure(self):
#         print('start plotting')
#         x = np.linspace(0,2*pi, 100)
#         self.axes.plot(x, np.sin(x))
#         self.axes.set_xlabel('x')
#         self.axes.set_ylabel('sin(x)')
#         self.axes.patch.set_facecolor('white')
#         print('done plotting')

#     def compute_coordinates(self):
#         self.objs = []
#         self.objs.append(ephem.Sun())
#         for project in readProjects('/home/lindroos/jobb/apex/P94/APEX-P94-PB.csv'):
#             if self.frontend.lower() in project['frontend']:
#                 filename = '/home/lindroos/jobb/apex/P94/ephems/o-'+project['id'].lower()+'-2014.edb'
#                 if filename[-10] == 'a' and not os.access(filename, os.F_OK):
#                     f = list(filename)
#                     f[-10] = 'b'
#                     filename = ''.join(f)
#                 if filename[-10] == 'b' and not os.access(filename, os.F_OK):
#                     f = list(filename)
#                     f[-10] = 'a'
#                     filename = ''.join(f)
# 
#                 if (float(project['grade']) < self.min_grade 
#                     and (self.select_proj is None or project['id'] in self.select_proj) 
#                     and os.access(filename, os.F_OK)):
# 
# 
#                     catfile = open(filename)
#                     projobjs = []
#                     for line in catfile:
#                         obj = ephem.readdb(line)
#                         obj.name = project['id'][6:]+'_'+obj.name
#                         obj.compute(ephem.now())
#                         for oldobj in projobjs:
#                             if ephem.separation(oldobj, obj)*180./pi < self.min_separation:
#                                 oldobj.name = project['id'][6:]+'_multi'
#                                 obj = None
#                                 break
#                         if obj is not None:
#                             projobjs.append(obj)
#                     self.objs.extend(projobjs)
# 
#         time = np.linspace(0,24,1000)
#         self.eles = getElevation(time, self.objs)

    def update_figure(self):
        time = self.sourceKeeper.time
        self.axes.clear()
        highlighted_sources = []
        bg_sources = []
        for source in self.sources:
            if source['elevation'] is not None and source['visible']:
                if source['highlight']:
                    highlighted_sources.append(source)
                else:
                    bg_sources.append(source)

        for source in bg_sources:
            self.axes.plot(time, source['elevation'], 
                            color='#AAAAAA')
        for source in highlighted_sources:
            self.axes.plot(time, source['elevation'], 
                            color='k')

        self.axes.plot(time, 0*time+30, 'r')
#         self.axes.plot(time, 0*time+60, 'c')
#         self.axes.plot(time, 0*time+70, 'b')
        self.axes.plot(time, 0*time+80, 'b')
#         pl.plot([BEGIN_SHIFT, BEGIN_SHIFT], [-1,91], 'k--')
#         pl.plot([END_SHIFT, END_SHIFT], [-1,91], 'k--')
        self.axes.axis([0, 24, -1, 91])
#         self.axes.set_xlabel('UT [h] {0}'.format(ti.clock()))
        self.axes.set_xlabel('UT [h]')
        self.axes.set_ylabel('Altitude [deg]')
        self.fig.patch.set_facecolor('white')
        self.draw()

        

