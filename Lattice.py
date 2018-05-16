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
    
    def generate_graph(self, target_directory, differences = None):
 
        extended = self.context.generate_extended_context()
         
        dot = Digraph(name = extended.context_name, strict = True)
        dot.attr(rankdir='BT')
        #dot.attr('node', shape="point")
        
        for j in extended.J:
            if not differences:
                dot.node(str(j), shape='circle')
            else:
                if j in differences:
                    dot.node(str(j), shape='circle')
                else:
                    dot.node(str(j), shape='doublecircle')
            
#         
        for j in extended.J:
            directs_infs = extended.get_directs_infs(extended.get_J_prime(j))
            for direct_inf in directs_infs:
                dot.edge(str(direct_inf), str(j))
                    
        dot.render(target_directory + extended.context_name + '.gv', view=False)