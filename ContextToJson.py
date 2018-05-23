import json

class ContextToJson(object):
    '''
    classdocs
    '''

    def __init__(self, context):
        '''
        Constructor
        '''
        self.context = context
        self.data = []
        
    def export(self):
        print('Not yet implemented')
        
        header = {}
        nodes = {}
        arcs = {}
        
        extended = self.context.generate_extended_context()
        for j in extended.J:
            node = []
            
            