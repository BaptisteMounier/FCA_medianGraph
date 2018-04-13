class Node(object):
    '''
    classdocs
    '''


    def __init__(self, n):
        '''
        Constructor
        '''
        self.n = n
        self.filters = set()
        self.ideals = set()
        self.directSubNodes = set()
        self.directSupNodes = set()
        
    def addFilters(self, filters):
        self.filters.update(filters)
        
    def addIdeals(self, ideals):
        self.ideals.update(ideals)
        
    def addSubNode(self, node):
        for directSubNode in self.directSubNodes:
            self.subNodes.add(node)
        
    def addSupNode(self, node):
        self.supNodes.add(node)
        
    def getClosestSubNodes(self, search):
        closestSubNodes = set()
        tmp = False
        for directSubNode in self.directSubNodes:
            closestSubNodes.update(directSubNode.getClosestSubNodes(search))
        if bool(closestSubNodes):
            closestSubNodes.add({self,})
        return closestSubNodes