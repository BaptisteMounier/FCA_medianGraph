from copy import copy
from graphviz import Graph, Digraph

class Lattice(object):
    '''
    classdocs
    '''


    def __init__(self, context):
        '''
        Constructor
        '''
        self.context = context
        self.nodes = set()
                    
    def getDirectChildren(self, filters_search):
        directChildren = set()
        for j in self.context.JExtended:
            if (self.context.getJPrimeExtended(j).issuperset(filters_search)) and not (self.context.getJPrimeExtended(j).issubset(filters_search)):
                directChildren_copy = copy(directChildren)
                alreadyHaveBetterChild = False
                for child in directChildren_copy:
                    if self.context.getJPrimeExtended(j).issubset(self.context.getJPrimeExtended(child)):
                        directChildren.discard(child)
                    elif self.context.getJPrimeExtended(j).issuperset(self.context.getJPrimeExtended(child)):
                        alreadyHaveBetterChild = True
                if not alreadyHaveBetterChild:
                    directChildren.add(j)
        return directChildren
    
    def generateGraph(self, targetDirectory):
 
        self.context.generateExtendedContext()
#         self.context.displayExtended()
         
        dot = Digraph(name = self.context.contextName, strict = True)
        dot.attr(rankdir='BT')
        #dot.attr('node', shape="point")
        
        for jExtended in self.context.JExtended:
            dot.node(str(jExtended))
#         
        for jExtended in self.context.JExtended:
            directChildren = self.getDirectChildren(self.context.getJPrimeExtended(jExtended))
            for directChild in directChildren:
                dot.edge(str(directChild), str(jExtended))
                    
        dot.render(targetDirectory+self.context.contextName+'.gv', view=False)