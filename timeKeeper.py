import VisibilityPlotter

class SourceKeeper(object):
    """ Ensures that all time dependent variables are updated."""
    
    def __init__(self, sources, time, *args, **kwargs):
        """ constructor
        
        Keyword arguments:
        sources -- list of sources
        time -- Array of times to calculate time dependent variables
        """
        super(SourceKeeper, self).__init__(*args, **kwargs)
        self.sources = sources
        self.time = time

    def setPlotTimeRange(self, time):
        """ Set range for calculation of visibility plots.
        
        Keyword arguments:
        time -- Array of times to calculate time dependent variables
        """
        self.time = time

    def update(self):
        """Update all time dependent data."""
        for source in self.sources:
            if source['visible']:
                source['elevation'] = VisibilityPlotter.getElevation(self.time, source['ephem'])
            else:
                source['elevation'] = None

