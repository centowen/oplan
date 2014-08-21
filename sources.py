from readProjects import readProjects
from VisibilityPlotter import getElevation
import ephem
import os
from math import pi
import numpy as np

class SourceDB(object):
    def __init__(self, projectperiods, ephemdirs = '', *args, **kwargs):
        super(SourceDB, self).__init__(*args, **kwargs)
        self.projectperiods = projectperiods
        self.computeSourceElevations()
#         self.ephemdirs = ephemdirs

    def computeSourceElevations(self, frontend = 'SHFI-1', min_grade=2.0, 
                                selected_projects =None, min_separation = 0.1):

        self.objs = []
        self.objs.append(ephem.Sun())

        # '/home/lindroos/jobb/apex/P94/APEX-P94-PB.csv'
        projects = []
        for projectperiod in self.projectperiods:
            periodprojects = readProjects(projectperiod['file'])
            for project in periodprojects:
                project['period'] = projectperiod['name']
            projects.extend(periodprojects)

        for project in projects:
            if frontend.lower() in project['frontend']:
                filename = '/home/lindroos/jobb/apex/'+project['period']+'/ephems/o-'+project['id'].lower()+'-2014.edb'
                if filename[-10] == 'a' and not os.access(filename, os.F_OK):
                    f = list(filename)
                    f[-10] = 'b'
                    filename = ''.join(f)
                if filename[-10] == 'b' and not os.access(filename, os.F_OK):
                    f = list(filename)
                    f[-10] = 'a'
                    filename = ''.join(f)

                if (float(project['grade']) < min_grade 
                    and (selected_projects is None or project['id'] in selected_projects) 
                    and os.access(filename, os.F_OK)):

                    projobjs = self.readEphemFile(project, filename, min_separation)
                    self.objs.extend(projobjs)

        self.time = np.linspace(0,24,1000)
        self.eles = getElevation(self.time, self.objs)


    def readEphemFile(self, project, filename, min_separation):
        catfile = open(filename)
        projobjs = []
        for line in catfile:
            obj = ephem.readdb(line)
            obj.name = project['id'][6:]+'_'+obj.name
            obj.compute(ephem.now())
            for oldobj in projobjs:
                if ephem.separation(oldobj, obj)*180./pi < min_separation:
                    oldobj.name = project['id'][6:]+'_multi'
                    obj = None
                    break
            if obj is not None:
                projobjs.append(obj)
        return projobjs

def readEphemFile(filename):
    catfile = open(filename)
    projobjs = []
    for line in catfile:
        obj = ephem.readdb(line)
        if obj is not None:
            projobjs.append(obj)
    return projobjs

def findFilename(project):
    filename = '/home/lindroos/jobb/apex/'+project['period']+'/ephems/o-'+project['id'].lower()+'-2014.edb'
    if os.access(filename, os.F_OK):
        return filename

    if filename[-10] == 'a' and not os.access(filename, os.F_OK):
        f = list(filename)
        f[-10] = 'b'
        filename = ''.join(f)
    if os.access(filename, os.F_OK):
        return filename

    if filename[-10] == 'b' and not os.access(filename, os.F_OK):
        f = list(filename)
        f[-10] = 'a'
        filename = ''.join(f)
    if os.access(filename, os.F_OK):
        return filename

    return None


def readSources(projectperiods):
    projects = []
    for projectperiod in projectperiods:
        periodprojects = readProjects(projectperiod['file'])
        for project in periodprojects:
            project['period'] = projectperiod['name']
        projects.extend(periodprojects)

    sources = []
    for project in projects:
        filename = findFilename(project)

        if filename is not None:
            ephems = readEphemFile(filename)
            
            for ephemObj in ephems:
                source = {}
                source['project'] = project
                source['ephem'] = ephemObj
                source['visible'] = False
                source['highlight'] = False
                sources.append(source)
    return sources
