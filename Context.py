import csv
from copy import copy, deepcopy
from Lattice import Lattice

class Context(object):
    '''
    classdocs
    '''


    def __init__(self, contextName):
        '''
        Constructor
        '''
        self.contextName = contextName
        self.J = set()
        self.M = set()
        self.I = set()
        self.JExtended = set()
        self.IExtended = set()
        
    def generateContextFomFile(self, filePath):
        print('Generate the context \''+self.contextName+'\' from the file \''+filePath+'\'')
        with open(filePath, newline='') as csvfile:
            lecteur = csv.reader(csvfile, delimiter='\t', quotechar='|')
            MList = next(lecteur)
            self.M = set(MList)
            
            l = 0
            for line in lecteur:
                c = 0
                for colonne in line:
                    objectOfLine = 'o'+str(l)
                    self.J.add(objectOfLine)
                    if colonne == '1':
                        self.I.add((objectOfLine, MList[c]))
                    c += 1
                l += 1
                
    def generateStandardContext(self):
        print('Generate the standard context \''+self.contextName+'_s\' of the context \''+self.contextName+'\'')
        standardContext = Context(self.contextName+'_s')
        standardContext.J = self.getIrreductibleJ()
        standardContext.M = self.getIrreductibleM()
        for i in self.I:
            if (i[0] in standardContext.J) and (i[1] in standardContext.M):
                standardContext.I.add((i[0],i[1]))
        return standardContext
        
    def generateDistributiveContextOnFirstFilters(self):
        
        print('Not yet totally implemented')
        # Section about cla2018 method
        
        firstFilters = self.getPrimaryFilters()
        globalContext = Context(self.contextName+'_df')
         
        # For each first filters
        for firstFilter in firstFilters:
              
            # Create a new working context
            filterContext = Context(self.contextName+'_'+firstFilter)
            for m in self.getJPrime(firstFilter):
                filterContext.M.add(m)
                for j in self.getMPrime(m):
                    if j != firstFilter:
                        filterContext.J.add(j)
                        filterContext.I.add((j,m))
                          
            filterContext.display() # Display the context in console
                      
            # Generate the distributive first filter context
            distributiveFilterContext = filterContext.generateDistributiveContextv2()
              
            # Display to see step
            distributiveFilterContext.display() # Display the context in console
#             lattice = Lattice(distributiveFilterContext)
#             lattice.generateGraph('data/graph/')
              
            # Fusion with previous distributive first filter context (no merge node atm)
            globalContext.J.update(distributiveFilterContext.J)
            globalContext.M.update(distributiveFilterContext.M)
            globalContext.I.update(distributiveFilterContext.I)
            if not firstFilter in globalContext.J:
                globalContext.J.add(firstFilter)
            for m in distributiveFilterContext.M:
                globalContext.I.add((firstFilter, m))
                  
            # Display step
            globalContext.display() # Display the context in console
             
        # Merge node if we can
        globalContext.display()
        globalContext.generateExtendedContext()
        globalContext_copy = deepcopy(globalContext)
           
        addedElement = globalContext_copy.JExtended.difference(globalContext_copy.J)
        for e in addedElement:
            count = 0
            commonToMultipleFirstFilters = False
               
            # Search if e is present in at least two first filters lattice
            for firstFilter in firstFilters:
#                 print(firstFilter,globalContext_copy.getJPrimeExtended(firstFilter))
#                 print(e,globalContext_copy.getJPrimeExtended(e))
                if globalContext_copy.getJPrimeExtended(firstFilter).issuperset(globalContext_copy.getJPrimeExtended(e)):
                    count += 1
                if count > 1:
                    commonToMultipleFirstFilters = True
                    break
                   
            if commonToMultipleFirstFilters:
                parents = globalContext.getDirectParents(globalContext.getJPrimeExtended(e))
                globalContext.displayExtended()
                print('parents',e,parents)
                if len(parents) > 1:
                       
                    # Check if e's parents are mergable
                    parentsMergables = set()
                    for parent in parents:
                        if parent in globalContext_copy.JExtended.difference(globalContext_copy.J):
                            parentsMergables.add(parent)
                    
                    # Then merge its
                    if bool(parentsMergables):
                        
                        # misc
                        newName = 'merged_('
                        
                        # Get intersections of parents
                        parentsIntersections = globalContext.M
                        for parent in parentsMergables:
                            newName += str(parent)
                            parentsIntersections = parentsIntersections.intersection(globalContext.getJPrimeExtended(parent))
                            print('parentIntersections',parentsIntersections)
                            print('maxiDistributiveContext.getJPrimeExtended(parent)', parent,globalContext.getJPrimeExtended(parent))
                            
                        newName += ')'
                        
                        # Delete olds parents from contexte
                        IExtended_copy = copy(globalContext.IExtended)
                        JExtended_copy = copy(globalContext.JExtended)
                        for i in IExtended_copy:
                            if i[0] in parents:
                                globalContext.IExtended.discard(i)
                        for j in JExtended_copy:
                            if j in parents:
                                globalContext.JExtended.discard(j)
                                
                        # Add a new and unique parent
                        globalContext.JExtended.add(newName)
                        for intersection in parentsIntersections:
                            globalContext.IExtended.add((newName, intersection))
#                             for child in globalContext_copy.getDirectChildren(globalContext_copy.getJPrimeExtended(parent)):
#                                 for parentsIntersection in parentsIntersections:
# #                                     if (parentsIntersection in globalContext.M) and (child in globalContext.J):
# #                                         globalContext.I.add((child, parentsIntersection))
#                                     globalContext.IExtended.add((e, parentsIntersection))

        globalContext.displayExtended()
            
        
        
        
        
#         for firstFilter in firstFilters:
#               
#             # Create a context for each first filter
#             filterContext = Context(self.contextName+'_'+firstFilter)
#             filterContext.J = copy(self.J)
#             for i in self.I:
#                 if i[1] in self.getJPrime(firstFilter):
#                     filterContext.I.add(i)
#                     filterContext.M.add(i[1])
#                       
#             # Convert the context into a standard one
#             filterStandardContext = filterContext.generateStandardContext()
#             filterStandardContext.display() # Display the context in console
#               
#             # Convert the context into a distributive one
#             filterDistributiveContext = filterStandardContext.generateDistributiveContext()
#             filterDistributiveContext.display() # Display the context in console
#               
#             # Create first filter graph file if needed
#             lattice = Lattice(filterDistributiveContext)
#             lattice.generateGraph('data/graph/')
#               
#             # Add the current first filter context to previous one
#             filterStandardDistributiveContext = filterDistributiveContext.generateStandardContext()
#             for j in globalContext.J:
#                 if j == firstFilter:
#                     for m in filterStandardDistributiveContext.M:
#                         globalContext.I.add((j,m))
#             for j in filterStandardDistributiveContext.J:
#                 if (j != firstFilter) and (j in firstFilters):
#                     for m in globalContext.M:
#                         if m not in filterStandardDistributiveContext.M:
#                             globalContext.I.add((j,m))
#             globalContext.J.update(filterStandardDistributiveContext.J)
#             globalContext.M.update(filterStandardDistributiveContext.M)
#             globalContext.I.update(filterStandardDistributiveContext.I)
#             globalContext.display() # Display the context in console
#           
#         # Merge concept if we can
#           
#         globalContext.generateExtendedContext()
#         globalContext_copy = deepcopy(globalContext)
#           
#         addedElement = globalContext_copy.JExtended.difference(globalContext_copy.J)
#         for e in addedElement:
#             count = 0
#             commonToTwoFirstFilters = False
#               
#             # Search if e is present in at least two first filters lattice
#             for firstFilter in firstFilters:
# #                 print(firstFilter,globalContext_copy.getJPrimeExtended(firstFilter))
# #                 print(e,globalContext_copy.getJPrimeExtended(e))
#                 if globalContext_copy.getJPrimeExtended(firstFilter).issuperset(globalContext_copy.getJPrimeExtended(e)):
#                     count += 1
#                 if count > 1:
#                     commonToTwoFirstFilters = True
#                     break
#                   
#             if commonToTwoFirstFilters:
#                 parents = globalContext.getDirectParents(globalContext.getJPrimeExtended(e))
#                 if len(parents) > 1:
#                       
#                     # Check if e's parents are mergable
#                     parentsMergable = True
#                     for parent in parents:
#                         if not parent in globalContext_copy.JExtended.difference(globalContext_copy.J):
#                             parentsMergable = False
#                               
#                       
#                     if parentsMergable:
#                         maxiDistributiveContext = self.generateDistributiveContext()
#                         maxiDistributiveContext.generateExtendedContext()
#                         parentsIntersections = maxiDistributiveContext.M
#                         for parent in parents:
#                             parentsIntersections = parentsIntersections.intersection(maxiDistributiveContext.getJPrimeExtended(parent))
#                           
#                         IExtended_copy = copy(globalContext.IExtended)
#                         for i in IExtended_copy:
#                             if i[0] in parents:
#                                 globalContext.IExtended.discard(i)
#                         for parent in parents:
#                             for parentsIntersection in parentsIntersections:
#                                 globalContext.IExtended.add((parent, parentsIntersection))
#                             for child in globalContext_copy.getDirectChildren(globalContext_copy.getJPrimeExtended(parent)):
#                                 for parentsIntersection in parentsIntersections:
# #                                     if (parentsIntersection in globalContext.M) and (child in globalContext.J):
# #                                         globalContext.I.add((child, parentsIntersection))
#                                     globalContext.IExtended.add((child, parentsIntersection))
                                      
        extended = Context(globalContext.contextName)
        extended.J = globalContext.JExtended
        extended.M = globalContext.M
        extended.I = globalContext.IExtended
        
        print('maintenant')
        extended.display()
        
        return extended
        
        # Upgrade to merge nodes
        
        
    def generateDistributiveContext(self):
        print('Generate the distributive context \''+self.contextName+'_d\' of the context \''+self.contextName+'\'')
        distributiveContext = Context(self.contextName+'_d')
        distributiveContext.J = copy(self.J)
        for j in distributiveContext.J:
            jFilters = set()
            X = set()
            for i in distributiveContext.J:
                if self.getJPrime(j).issuperset(self.getJPrime(i)):
                    jFilters.add(i)
                else:
                    X.add(i)
            mj = 'm_'+str(j)
            distributiveContext.M.add(mj)
            for x in X:
                distributiveContext.I.add((x,mj))
        return distributiveContext
    
    def generateDistributiveContextv2(self):
        print('Generate the distributive context \''+self.contextName+'_d\' of the context \''+self.contextName+'\'')
        distributiveContext = Context(self.contextName+'_d')
        distributiveContext.J = copy(self.J)
        for j in distributiveContext.J:
            jFilters = set()
            X = set()
            for i in distributiveContext.J:
                if self.getJPrime(j).issuperset(self.getJPrime(i)):
                    jFilters.add(i)
                else:
                    X.add(i)
            mj = 'm_'+str(j)
            distributiveContext.M.add(mj)
            for x in X:
                distributiveContext.I.add((x,mj))
        return distributiveContext
    
    def generateExtendedContext(self):
        self.JExtended.update(self.J)
        self.IExtended.update(self.I)
        for j in self.J:
            for i in self.J:
                alreadyExists = False
                if j != i:
                    intersection_ji = self.getJPrime(j).intersection(self.getJPrime(i))
                    for k in self.JExtended:
                            if intersection_ji == self.getJPrimeExtended(k):
                                alreadyExists = True
                                break
                    if not alreadyExists:
                        if j < i:
                            jExtended = 'e'+str(j)+str(i)
                        else:
                            jExtended = 'e'+str(i)+str(j)
                        self.JExtended.add(jExtended)
                        for intersection in intersection_ji:
                            self.IExtended.add((jExtended, intersection))
                            
        alreadyExists = False
        for j in self.JExtended:
            if self.getJPrimeExtended(j) == self.M:
                alreadyExists = True
        if not alreadyExists:
            jBot = 'eBot'
            self.JExtended.add(jBot)
            for m in self.M:
                self.IExtended.add((jBot, m))
                            
        alreadyExists = False
        for j in self.JExtended:
            haveFilter = False
            for i in self.IExtended:
                if j == i[0]:
                    haveFilter = True
                    break
            if not haveFilter:
                alreadyExists = True
                break
        if not alreadyExists:
            jBot = 'eTop'
            self.JExtended.add(jBot)
        
        extended = Context(self.contextName)
        extended.J = self.JExtended
        extended.M = self.M
        extended.I = self.IExtended
        return extended
    # Unused
#     def generateLattice(self):
#         print('Generate the lattice of the context \''+self.contextName+'\'')
#         lattice = Lattice(self.contextName)
#         for i in self.I:
#             lattice.injectTuple(i)
#         lattice.extendTuple()
#         return lattice
                
    def getJPrime(self, j):
        jPrime = set()
        for i in self.I:
            if i[0] == j:
                jPrime.add(i[1])
        return jPrime
                
    def getJPrimeExtended(self, j):
        jPrimeExtended = set()
        for i in self.IExtended:
            if i[0] == j:
                jPrimeExtended.add(i[1])
        return jPrimeExtended
                
    def getMPrime(self, m):
        mPrime = set()
        for i in self.I:
            if i[1] == m:
                mPrime.add(i[0])
        return mPrime
    
    def getIrreductibleJ(self):
        irreductiblesObjects = set()
        allAttributes = set()
        J_copy = copy(self.J)
        for j in J_copy:
            if j in self.J:
                for i in J_copy:
                    if (j != i) and self.getJPrime(j).issubset(self.getJPrime(i)) and self.getJPrime(j).issuperset(self.getJPrime(i)):
                        self.J.discard(i)
        for j in self.J:
            allAttributes.update(self.getJPrime(j))
        for j in self.J:
            if self.getJPrime(j) != allAttributes:
                irreductible = True
                for i in self.J:
                    if j != i:
                        for k in self.J:
                            if (j != k) and (i != k):
                                intersection_ik = self.getJPrime(i).intersection(self.getJPrime(k))
                                if(self.getJPrime(j) == intersection_ik):
                                    irreductible = False
                                    break
                        if not irreductible:
                            break
                if irreductible:
                    irreductiblesObjects.add(j)
        return irreductiblesObjects
    
    def getIrreductibleM(self):
        irreductiblesAttributes = set()
        allObjects = set()
        M_copy = copy(self.M)
        for m in M_copy:
            if m in self.M:
                for n in M_copy:
                    if (m != n) and self.getMPrime(m).issubset(self.getMPrime(n)) and self.getMPrime(m).issuperset(self.getMPrime(n)):
                        self.M.discard(n)
        for m in self.M:
            allObjects.update(self.getMPrime(m))
        for m in self.M:
            if self.getMPrime(m) != allObjects:
                irreductible = True
                for n in self.M:
                    if m != n:
                        for o in self.M:
                            if (m != o) and (n != o):
                                intersection_no = self.getMPrime(n).intersection(self.getMPrime(o))
                                if(self.getMPrime(m) == intersection_no):
                                    irreductible = False
                                    break
                        if not irreductible:
                            break
                if irreductible:
                    irreductiblesAttributes.add(m)
        return irreductiblesAttributes
    
    def getPrimaryFilters(self):
        self.generateExtendedContext()
        firstFilters = set()
        for j in self.JExtended:
            sourceCount = 0
            for i in self.JExtended:
                if j != i:
                    if self.getJPrimeExtended(j).issubset(self.getJPrimeExtended(i)):
                        sourceCount += 1
                    if sourceCount > 1:
                        break
            if sourceCount == 1:
                firstFilters.add(j)
        return firstFilters
    
    def getDirectChildren(self, filters_search):
        directChildren = set()
        for j in self.JExtended:
            if (self.getJPrimeExtended(j).issuperset(filters_search)) and not (self.getJPrimeExtended(j).issubset(filters_search)):
                directChildren_copy = copy(directChildren)
                alreadyHaveBetterChild = False
                for child in directChildren_copy:
                    if self.getJPrimeExtended(j).issubset(self.getJPrimeExtended(child)):
                        directChildren.discard(child)
                    elif self.getJPrimeExtended(j).issuperset(self.getJPrimeExtended(child)):
                        alreadyHaveBetterChild = True
                if not alreadyHaveBetterChild:
                    directChildren.add(j)
        return directChildren
    
    def getDirectParents(self, filters_search):
        directParents = set()
        for j in self.JExtended:
            if (self.getJPrimeExtended(j).issubset(filters_search)) and not (self.getJPrimeExtended(j).issuperset(filters_search)):
                directParents_copy = copy(directParents)
                alreadyHaveBetterParent = False
                for parent in directParents_copy:
                    if (self.getJPrimeExtended(j).issuperset(self.getJPrimeExtended(parent))) and not (self.getJPrimeExtended(j).issubset(self.getJPrimeExtended(parent))):
                        directParents.discard(parent)
                    elif self.getJPrimeExtended(j).issubset(self.getJPrimeExtended(parent)):
                        alreadyHaveBetterParent = True
                if not alreadyHaveBetterParent:
                    directParents.add(j)
        return directParents
    
    def display(self):
        print('-'*15)
        print(self.contextName)
        print('-'*5)
        matrix = ''
        for m in sorted(self.M):
            matrix += '\t'+str(m)
        matrix += '\n'
        for j in sorted(self.J):
            matrix += str(j)
            for m in sorted(self.M):
                matrix += '\t'
                if m in self.getJPrime(j):
                    matrix += 'x'
            matrix += '\n'
        print(matrix)
        print('-'*15)
    
    def displayExtended(self):
        print('-'*15)
        print(self.contextName+'ext')
        print('-'*5)
        matrix = ''
        for m in sorted(self.M):
            matrix += '\t'+str(m)
        matrix += '\n'
        for j in sorted(self.JExtended):
            matrix += str(j)
            for m in sorted(self.M):
                matrix += '\t'
                if m in self.getJPrimeExtended(j):
                    matrix += 'x'
            matrix += '\n'
        print(matrix)
        print('-'*15)
        
    def exportJsonForLatviz(self):
        print('Not yet implemented')