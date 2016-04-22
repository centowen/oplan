import VisibilityPlotter
from PyQt4 import QtCore

class SourceKeeper(object):
    """ Ensures that all time dependent variables are updated."""
    
    def __init__(self, sources, time, sourceTree, *args, **kwargs):
        """ constructor
        
        Keyword arguments:
        sources -- list of sources
        time -- Array of times to calculate time dependent variables
        """
        super(SourceKeeper, self).__init__(*args, **kwargs)
        self.sources = sources
        self.time = time
        self.sourceTree = sourceTree

    def setPlotTimeRange(self, time):
        """ Set range for calculation of visibility plots.
        
        Keyword arguments:
        time -- Array of times to calculate time dependent variables
        """
        self.time = time

    def update(self, sources = None):
        """Update all time dependent data."""
        if sources is None:
            sources = self.sources
        for source in sources:
            if source['visible']:
                source['elevation'] = VisibilityPlotter.getElevation(self.time, source['ephem'])
            else:
                source['elevation'] = None

    @QtCore.pyqtSlot("QItemSelection, QItemSelection")
    def sourceSelected(self, selected, deselected):
        self.selected_sources = self.findSelectedSource(selected)
        for source in self.findSelectedSource(deselected):
            source['highlight'] = False
        for source in self.selected_sources:
            source['highlight'] = True

    @QtCore.pyqtSlot(result=bool)
    def swapSelected(self):
        try:
            needUpdate = []
            for source in self.selected_sources:
                source['visible'] = not source['visible']
                if source['visible'] and source['elevation'] is None:
                    needUpdate.append(source)
            self.update(needUpdate)

        except AttributeError:
            return True
        self.sourceTree.setupModelData(self.sources, self.sourceTree.rootItem)
        self.sourceSelector.reset()
        return True




    def findSelectedSource(self, selected):
        selected_sources = []
        for i in selected:
            treeItems = []
            treeItem = self.sourceTree.index(i.top(), 0, i.parent())
            sourceName = self.sourceTree.data(treeItem)

# Generate list of all levels, 
# should be activity, period, project and source in that order.
            treeItems.append(treeItem)
            while self.sourceTree.parent(treeItem) != QtCore.QModelIndex():
                treeItem = self.sourceTree.parent(treeItem)
                treeItems.append(treeItem)

            selectionRules = [lambda s, value: True,
                              lambda s, value: s['project']['period'] == value,
                              lambda s, value: s['project']['id'] == value,
                              lambda s, value: s['ephem'].name == value]
#             selectionRules = [lambda s, value: value == 'Active' and s['visible'],
#                               lambda s, value: s['project']['period'] == value,
#                               lambda s, value: s['project']['id'] == value,
#                               lambda s, value: s['ephem'].name == value]

            selectionRules = selectionRules[:len(treeItems)]

            for source in self.sources:
                for selectionRule, treeItem in zip(selectionRules, treeItems[::-1]):
                    if not selectionRule(source, str(self.sourceTree.data(treeItem))):
                        source = None
                        break

                if source is not None:
                    selected_sources.append(source)


        return selected_sources


