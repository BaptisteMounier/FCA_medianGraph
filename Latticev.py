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
        
#     def generateNodesV2(self):
#         print('Not yet implemented')
#         for j in self.context.JExtended:
#             newNode = Node(str(j))
#             for node in self.nodes:
#                 if newNode.filters.issubset(node.filters):
#                     newNode.addSubNode(node)
#                     node.addSupNode(newNode)
#                 elif newNode.filters.issuperset(node.filters):
#                     newNode.addSupNode(node)
#                     node.addSubNode(newNode)
#             self.nodes.add(newNode)
        
#     def generateNodes(self):
#         print('Not yet implemented')
#         for j in self.context.J:
#             newNode = Node(str(j))
#             newNode.addFilters(self.context.getJPrime(j))
# #             newNode.addIdeals({j})
#             directSubNodes = set()
#             directSupNodes = set()
#             alreadyExists = False
#             for node in self.nodes:
#                 if (newNode.filters.issubset(node.filters)) and (newNode.filters.issuperset(node.filters)):
#                     alreadyExists = True
#                 else:
#                     if (newNode.filters.issubset(node.filters)) and not (newNode.filters.issuperset(node.filters)):
#                         directSubNodes.add(node)
#                     elif (newNode.filters.issuperset(node.filters)) and not (newNode.filters.issubset(node.filters)):
#                         directSupNodes.add(node)
#             if not alreadyExists:
#                 self.nodes.add(newNode)
#                 directSubNode_copy = copy(directSubNodes)
#                 for node1 in directSubNode_copy:
#                     for node2 in directSubNode_copy:
#                         if node1 != node2:
#                             if node1.filters.issubset(node2.filters):
#                                 directSubNodes.discard(node2)
#                 directSupNode_copy = copy(directSupNodes)
#                 for node1 in directSupNode_copy:
#                     for node2 in directSupNode_copy:
#                         if node1 != node2:
#                             if node1.filters.issuperset(node2.filters):
#                                 directSupNodes.discard(node2)
#                     
#                 for node in directSubNodes:
#                     newNode.addSubNode(node)
#                     node.addSupNode(newNode)
#                     
#                 for node in directSupNodes:
#                     newNode.addSupNode(node)
#                     node.addSubNode(newNode)
#         
#         needBot = True
#         for node in self.nodes:
#             if not bool(node.subNodes):
#                 needBot = False
#         if not needBot:
#             bot = Node('bot')
#             for node in self.nodes:
#                 if not bool(node.subNodes):
#                     bot.addSupNode(node)
#                     node.addSubNode(bot)
#                 
#         needTop = True
#         for node in self.nodes:
#             if not bool(node.supNodes):
#                 needTop = False
#         if not needTop:
#             top = Node('top')
#             for node in self.nodes:
#                 if not bool(node.supNodes):
#                     top.addSubNode(node)
#                     node.addSupNode(top)
                    
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
#         
        self.context.generateExtendedContext()
        self.context.displayExtended()
         
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
                
#         JExtended_copy = copy(self.context.JExtended)
#         botestJExtended = set()
#         maxFiltersNumber = 0
#         for jExtended1 in JExtended_copy:
#             if len(self.context.getJPrimeExtended(jExtended1)) > maxFiltersNumber:
#                 botestJExtended.clear()
#                 maxFiltersNumber = len(jExtended1)
#                 botestJExtended.add(jExtended1)
#             elif len(self.context.getJPrimeExtended(jExtended1)) == max:
#                 botestJExtended.add(jExtended1)
#                 
#         for j in botestJExtended:
#             newNode = Node(str(j))
#             newNode.filters = self.context.getJPrimeExtended(j)
#             for node in self.nodes:
#                 if newNode.filters.issubset()
#         
#         levelMax = len(self.concepts['bottom'])
#         for level1 in range(levelMax, -1, -1):
#             for concept1 in self.conceptByLevel[level1]:
#                 for level2 in range(level1, -1, -1):
#                     for concept2 in self.conceptByLevel[level2]:
#                         if (concept1 != concept2) and (self.concepts[concept1].issuperset(self.concepts[concept2])):
#                             direct = True
#                             for level3 in range(level2, level1):
#                                 for concept3 in self.conceptByLevel[level3]:
#                                     if (concept1 != concept3) and (self.concepts[concept1].issuperset(self.concepts[concept3])):
#                                         if (concept2 != concept3) and (self.concepts[concept3].issuperset(self.concepts[concept2])):
#                                             direct = False
#                             if direct:
#                                 dot.edge(concept1, concept2)
        
        
        
#         for node in self.nodes:
#             for directSubNode in node.directSubNodes:
#                 dot.edge(directSubNode.n, node.n)
#             for directSupNode in node.directSupNodes:
#                 dot.edge(node.n, directSupNode.n)