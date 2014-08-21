import ephem
import numpy as np
from math import pi
from astropy import units as u
from astropy import coordinates as coord
import matplotlib.pylab as pl
import os

apex = ephem.Observer()
apex.lat = '-23:00:20.8'
apex.lon = '-67:45:33.0'
apex.elevation = 5105

f9301 = '/home/lindroos/jobb/apex/P94/cats/o-094.f-9301-2014.cat'
f9328 = '/home/lindroos/jobb/apex/P94/cats/o-094.f-9328-2014.cat'
apex1 = '/home/lindroos/jobb/apex/P94/cats/APEX-1'
apex2 = '/home/lindroos/jobb/apex/P94/cats/APEX-2'

today = ephem.now().datetime().strftime('%Y/%m/%d')+' '

def readCat(filename):
    catfile = open(filename, 'r')
    projnum = os.path.basename(filename).split('.')[1].split('-')[1]
    objs = []

    for row in catfile:
        if row.find('!') >= 0:
            row = row[:row.find('!')]
            if row == '':
                continue
        try:
            name = row.split()[0]
            epoch = row.split()[2]
            srctxt = '{0},f,{1},{2},0,2000'.format('_'.join([str(projnum),name]), row.split()[3], row.split()[4])
            objs.append(ephem.readdb(srctxt))
        except IndexError:
            pass

#     objs[0].compute(apex)
    return objs
        

def getElevation(time, obj, date=today, obs=apex):
    elevation = time.copy()
    it = np.nditer(time, flags=['f_index'])
    while not it.finished:
        h = int(it[0])
        m = int((it[0]-h)*60)
        s = ((it[0]-h)*60-m)*60
        obs.date = date + ' ' + '{0}:{1}:{2}'.format(h,m,s)
        obj.compute(obs)
        elevation[it.index] = obj.alt*180/pi
        it.iternext()
    return elevation


def getElevations(time, objs, date=today, obs=apex):
    elevations = []
    for obj in objs:
        elevation = time.copy()
        it = np.nditer(time, flags=['f_index'])
        while not it.finished:
            h = int(it[0])
            m = int((it[0]-h)*60)
            s = ((it[0]-h)*60-m)*60
            obs.date = date + ' ' + '{0}:{1}:{2}'.format(h,m,s)
            obj.compute(obs)
            elevation[it.index] = obj.alt*180/pi
            it.iternext()
        elevations.append(elevation)
    return elevations

def getSunDistance(time, objs, date=today, obs=apex):
    sundists = []
    sun = ephem.Sun()
    for obj in objs:
        separation = time.copy()
        it = np.nditer(time, flags=['f_index'])
        while not it.finished:
            h = int(it[0])
            m = int((it[0]-h)*60)
            s = ((it[0]-h)*60-m)*60
            obs.date = date + ' ' + '{0}:{1}:{2}'.format(h,m,s)
            obj.compute(obs)
            sun.compute(obs)
            separation[it.index] = ephem.separation(obj, sun)*180./pi
            it.iternext()
        sundists.append(separation)
    return sundists

def plotRecieverSundist(receiver):
    objs = []
    objs.append(ephem.Sun())
    apex1cats = [os.path.join(receiver, f) for f in os.listdir(receiver)]
    for cat in apex1cats:
        objs.extend(readCat(cat))
    pl.ion()
    pl.clf()
    eles = getSunDistance(time, objs)
    for (obj, ele) in zip(objs,eles):
        pl.plot(time, ele, label=obj.name)
        pl.text(time[np.argmax(ele)], np.max(ele)+0.1, obj.name, horizontalalignment='center')
    pl.axis([0, 24, -1, 91])
    pl.xlabel('UT [h]')
    pl.ylabel('Sun distance [deg]')

def plotReciever(receiver):
    objs = []
    objs.append(ephem.Sun())
    apex1cats = [os.path.join(receiver, f) for f in os.listdir(receiver)]
    for cat in apex1cats:
        objs.extend(readCat(cat))
    pl.ion()
    pl.clf()
    eles = getElevation(time, objs)
    for (obj, ele) in zip(objs,eles):
        pl.plot(time, ele, label=obj.name)
        pl.text(time[np.argmax(ele)], np.max(ele)+0.1, obj.name, horizontalalignment='center')
    pl.plot(time, 0*time+30, 'r')
    pl.axis([0, 24, -1, 91])
    pl.xlabel('UT [h]')
    pl.ylabel('Altitude [deg]')

if __name__ == '__main__':
    time = np.linspace(0,24,1000)

    pl.figure(1)
    plotReciever(apex1)
    pl.title('APEX-1')
    pl.savefig('APEX-1.pdf')
    pl.figure(3)
    plotRecieverSundist(apex1)
    pl.title('APEX-1 sun distance')
    pl.figure(2)
    plotReciever(apex2)
    pl.title('APEX-2')
    pl.savefig('APEX-2.pdf')
#     pl.figure(3)
#     plotReciever(apex3)
#     pl.title('APEX-3')
#     pl.figure(1)
#     plotReciever(apex1)


# k

