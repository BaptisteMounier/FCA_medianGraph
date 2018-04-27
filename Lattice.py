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
 
        extended = self.context.generateExtendedContext()
#         extended.display()
         
        dot = Digraph(name = extended.contextName, strict = True)
        dot.attr(rankdir='BT')
        #dot.attr('node', shape="point")
        
        for j in extended.J:
            dot.node(str(j))
#         
        for j in extended.J:
            directsInfs = extended.getDirectsInfs(extended.getJPrime(j))
            for directInf in directsInfs:
                dot.edge(str(directInf), str(j))
                    
        dot.render(targetDirectory+extended.contextName+'.gv', view=False)