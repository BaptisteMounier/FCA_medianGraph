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
            directChildren = self.context.getDirectChildren(self.context.getJPrimeExtended(jExtended))
            for directChild in directChildren:
                dot.edge(str(directChild), str(jExtended))
                    
        dot.render(targetDirectory+self.context.contextName+'.gv', view=False)