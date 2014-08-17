import csv

def readProjects(filename = 'APEX-P94-PB.csv'):
    projlistfile = open(filename)
    projlistreader = csv.reader(projlistfile)

    projects = []
    for row in projlistreader:
        project = {}
        project['id'] = row[0]
        project['frontend'] = [f.lower() for f in row[3].split('/')]
        project['PI'] = row[1]
        project['grade'] = row[11]
        project['title'] = row[2]
        project['pwv'] = row[13].split('/')
        projects.append(project)
    return projects

