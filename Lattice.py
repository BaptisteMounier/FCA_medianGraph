from graphviz import Graph, Digraph
import graphviz
import re

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
    
    def generate_graph(self, target_directory, add_name = '', differences = None):
 
        extended = self.context.generate_extended_context()
#         extended.display()
         
        dot = Digraph(name = extended.context_name, strict = True)
        dot.attr(rankdir='BT')
        #dot.attr('node', shape="point")
        
#         for j in extended.J:
#             if not differences:
#                 dot.node(str(j), shape='circle')
#             else:
#                 if j in differences:
#                     dot.node(str(j), shape='circle')
#                 else:
#                     dot.node(str(j), shape='doublecircle')
        
        for j in extended.J:
            if re.match(r"e([0-9]*)", j):
                dot.node(str(j), shape='circle')
            else:
                dot.node(str(j), shape='doublecircle')
            
#         
        for j in extended.J:
            directs_infs = extended.get_directs_infs(extended.get_J_prime(j))
            for direct_inf in directs_infs:
                dot.edge(str(direct_inf), str(j))
        
        target = target_directory / (extended.context_name + add_name)
        output_formats = {'pdf', 'svg', 'gv'}
        for output_format in output_formats:
            dot.format = output_format
            dot.render(target)