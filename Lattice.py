from graphviz import Graph, Digraph
import graphviz
import re

class Lattice(object):
    '''
    classdocs
    '''


    def __init__(self, engine, context):
        '''
        Constructor
        '''
        self.context = context
        self.nodes = set()
        self.engine = engine
    
    def generate_graph(self, target_directory, add_name = '', differences = None, extended = False):
 
        if extended:
            extended = self.context
        else:
            extended = self.engine.transform_to_extended_context(self.context)
         
        dot = Digraph(name = extended.context_name, strict = True)
        dot.attr(rankdir='BT')
        #dot.attr('node', shape="point")
        
        indice = 1
        for j in extended.J:
            if re.match(r"e.*", str(j)):
                label = 'e'+str(indice)
                indice += 1
            else:
                label = str(j)
            if not differences:
                dot.node(str(j), label, shape='circle')
            else:
                if j in differences:
                    dot.node(str(j), label, shape='circle')
                else:
                    dot.node(str(j), label, shape='doublecircle')
        
#         for j in extended.J:
#             if re.match(r"e([0-9]*)", j):
#                 dot.node(str(j), shape='circle')
#             else:
#                 dot.node(str(j), shape='doublecircle')
            
#         
        for j in extended.J:
            directs_infs = extended.get_directs_j_infs(extended.get_j_prime(j))
            for direct_inf in directs_infs:
                dot.edge(str(direct_inf), str(j))
        
        target = target_directory / (extended.context_name + add_name)
        output_formats = {'pdf', 'svg', 'gv'}
        for output_format in output_formats:
            dot.format = output_format
            dot.render(target)