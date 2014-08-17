from readProjects import readProjects
import os
import ephem
from visplot import getElevation
import numpy as np
from matplotlib import pylab as pl
from math import pi

frontend = 'SHFI-2'
# frontend = 'SHFI-2'
# frontend = 'LABOCCA'
# frontend = 'ArTeMiS (GTO)'
MIN_SEPARATION = 50
MIN_GRADE = 2.0
BEGIN_SHIFT = 17
END_SHIFT = 19+4

# SELECT_PROJ = ['094.F-9334A', '094.F-9335A']
# SELECT_PROJ = ['094.F-9318A']
SELECT_PROJ = ['094.F-9322A', '094.F-9304A']
# SELECT_PROJ = None

objs = []
objs.append(ephem.Sun())
for project in readProjects():
    if frontend.lower() in project['frontend']:
        filename = 'ephems/o-'+project['id'].lower()+'-2014.edb'
        if filename[-10] == 'a' and not os.access(filename, os.F_OK):
            f = list(filename)
            f[-10] = 'b'
            filename = ''.join(f)
        if filename[-10] == 'b' and not os.access(filename, os.F_OK):
            f = list(filename)
            f[-10] = 'a'
            filename = ''.join(f)

        if (float(project['grade']) < MIN_GRADE 
            and (SELECT_PROJ is None or project['id'] in SELECT_PROJ) 
            and os.access(filename, os.F_OK)):

            print(project['id'], project['grade'])

            catfile = open(filename)
            projobjs = []
            for line in catfile:
                obj = ephem.readdb(line)
                obj.name = project['id'][6:]+'_'+obj.name
                obj.compute(ephem.now())
                for oldobj in projobjs:
                    if ephem.separation(oldobj, obj)*180./pi < MIN_SEPARATION:
                        oldobj.name = project['id'][6:]+'_multi'
                        obj = None
                        break
                if obj is not None:
                    projobjs.append(obj)
            objs.extend(projobjs)

time = np.linspace(0,24,1000)
pl.ion()
pl.clf()
eles = getElevation(time, objs)
for (obj, ele) in zip(objs, eles):
    pl.plot(time, ele, label=obj.name)
    pl.text(time[np.argmax(ele)], np.max(ele)+0.1, obj.name, horizontalalignment='center')
pl.plot(time, 0*time+30, 'r')
pl.plot(time, 0*time+60, 'c')
pl.plot(time, 0*time+70, 'b')
pl.plot([BEGIN_SHIFT, BEGIN_SHIFT], [-1,91], 'k--')
pl.plot([END_SHIFT, END_SHIFT], [-1,91], 'k--')
pl.axis([0, 24, -1, 91])
pl.xlabel('UT [h]')
pl.ylabel('Altitude [deg]')
