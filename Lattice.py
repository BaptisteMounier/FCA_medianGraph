from graphviz import Graph, Digraph
from copy import copy

class Lattice:
    '''
    classdocs
    '''


    def __init__(self, latticeName):
        '''
        Constructor
        '''
        self.latticeName = latticeName
        self.concepts = {}
        self.conceptByLevel = {}
            
    def injectTuple(self, t):
        if t[0] in self.concepts:
            self.concepts.get(t[0]).add(t[1])
        else:
            s = set()
            s.add(t[1])
            self.concepts[t[0]] = s
            
    def extendTuple(self):
        
        allAttributes = set()
        for conceptKey in self.concepts:
            allAttributes.update(self.concepts[conceptKey])
            
        foundBot = False
        foundKeyBot = None
#         foundTop = False
#         foundKeyTop = None
        for conceptKey in self.concepts:
            if self.concepts[conceptKey] == allAttributes:
                foundBot = True
                foundKeyBot = conceptKey
#             if self.concepts[conceptKey] == {conceptKey}:
#                 foundTop = True
#                 foundKeyTop = conceptKey

        if foundBot:
            del self.concepts[foundKeyBot]
#         if foundTop:
#             del self.concepts[foundKeyTop]
        self.concepts['bottom'] = allAttributes
#         self.concepts['top'] = set()
        
        levelMax = len(self.concepts['bottom'])
        for level in range(levelMax, -1, -1):
            self.conceptByLevel[level] = set()
            for conceptKey in self.concepts:
                if len(self.concepts[conceptKey]) == level:
                    self.conceptByLevel[level].add(conceptKey)
            
        countNewConcept = 0
        concepts_copy = copy(self.concepts)
        for concept1 in concepts_copy:
            for concept2 in concepts_copy:
                intersection = concepts_copy[concept1].intersection(concepts_copy[concept2])
                alreadyExist = False
                for concept3 in self.concepts:
                    if intersection == self.concepts[concept3]:
                        alreadyExist = True
                if not alreadyExist:
                    countNewConcept += 1
                    conceptKey = 'newConcept'+str(countNewConcept)
                    self.concepts[conceptKey] = intersection
                    self.conceptByLevel[len(self.concepts[conceptKey])].add(conceptKey)
        
                    
#         for debug in self.conceptByLevel:
#             print('Level: ',debug,'\t',self.conceptByLevel[debug])
     
    def generateGraph(self, targetDirectory):
        
        dot = Digraph(name = self.latticeName, strict = True)
        dot.attr(rankdir='BT')
        #dot.attr('node', shape="point")
        
        levelMax = len(self.concepts['bottom'])
        for level1 in range(levelMax, -1, -1):
            for concept1 in self.conceptByLevel[level1]:
                for level2 in range(level1, -1, -1):
                    for concept2 in self.conceptByLevel[level2]:
                        if (concept1 != concept2) and (self.concepts[concept1].issuperset(self.concepts[concept2])):
                            direct = True
                            for level3 in range(level2, level1):
                                for concept3 in self.conceptByLevel[level3]:
                                    if (concept1 != concept3) and (self.concepts[concept1].issuperset(self.concepts[concept3])):
                                        if (concept2 != concept3) and (self.concepts[concept3].issuperset(self.concepts[concept2])):
                                            direct = False
                            if direct:
                                dot.edge(concept1, concept2)
        dot.render(targetDirectory+self.latticeName+'.gv', view=False)