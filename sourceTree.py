from PyQt4 import QtGui, QtCore

class TreeItem(object):
    def __init__(self, data, parent = None, *args, **kwargs):
        super(TreeItem, self).__init__(*args, **kwargs)
        self.parentItem = parent
        self.childItems = []
        self.itemData = [data]

    def appendChild(self, child):
        self.childItems.append(child)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def parent(self):
        return self.parentItem


class SourceTree(QtCore.QAbstractItemModel):
    def __init__(self, sources, parent = None, *args, **kwargs):
        super(SourceTree, self).__init__(parent, *args, **kwargs)

        self.rootItem = TreeItem('Sources')
        self.setupModelData(sources, self.rootItem)

    def index(self, row, column, parent, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent = self.rootItem
        else:
            parent = parent.internalPointer()

        child = parent.child(row)
        if child:
            return self.createIndex(row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()
        return self.createIndex(parentItem.row(), 0, parentItem)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role= QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None

        if role != QtCore.Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.NoItemFlags

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.rootItem.data(section)

        return None


    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()
        return parentItem.childCount()


    def setupModelData(self, sources, root):
        if root == self.rootItem:
            self.rootItem = TreeItem('Sources')
        act_ti = {}
        act_ti['active'] = TreeItem('Active', self.rootItem)
        act_ti['inactive'] = TreeItem('Inactive', self.rootItem)
        self.rootItem.appendChild(act_ti['active'])
        self.rootItem.appendChild(act_ti['inactive'])

        project_periods = {}
        projects = {}

        for act in ['active', 'inactive']:
            project_periods[act] = {}
            projects[act] = {}

        for source in sources:
            if source['visible']:
                act = 'active'
            else:
                act = 'inactive'

            project = source['project']['id']
            project_period = source['project']['period']
            if project_period not in project_periods[act]:
                project_period_ti = TreeItem(project_period, act_ti[act])
                project_periods[act][project_period] = project_period_ti
                act_ti[act].appendChild(project_period_ti)
            else:
                project_period_ti = project_periods[act][project_period]


            if project not in projects[act]:
                project_ti = TreeItem(project, project_period_ti)
                projects[act][project] = project_ti
                project_period_ti.appendChild(project_ti)
            else:
                project_ti = projects[act][project]

            source_ti = TreeItem(source['ephem'].name, project_ti)
            project_ti.appendChild(source_ti)
