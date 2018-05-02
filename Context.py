import csv
from copy import copy, deepcopy
from Lattice import Lattice

class Context(object):
    '''
    classdocs
    '''


    def __init__(self, contextName, debugGraphFolder = 'data/debug/'):
        '''
        Constructor
        '''
        self.contextName = contextName
        self.J = set()
        self.M = set()
        self.I = set()
        self.debugGraphFolder = debugGraphFolder
        
    def generateContextFomFile(self, filePath):
        print('Generate the context \''+self.contextName+'\' from the file \''+filePath+'\'')
        with open(filePath, newline='') as csvfile:
            lecteur = csv.reader(csvfile, delimiter='\t', quotechar='|')
            MList = next(lecteur)
            self.M = set(MList)
            
            l = 1
            for line in lecteur:
                c = 0
                objectOfLine = 'o'+str(l)
                self.J.add(objectOfLine)
                for colonne in line:
                    if colonne == '1':
                        self.I.add((objectOfLine, MList[c]))
                    c += 1
                l += 1
                
    def generateStandardContext(self):
        print('Generate the standard context of \''+self.contextName+'\'')
        standardContext = Context(self.contextName, self.debugGraphFolder)
        standardContext.J = copy(self.getIrreductibleJ())
        standardContext.M = copy(self.getIrreductibleM())
        for i in self.I:
            if (i[0] in standardContext.J) and (i[1] in standardContext.M):
                standardContext.I.add((i[0],i[1]))
        return standardContext
        
    def generateDistributiveContextOnFirstFilters(self):
        
        print('Generate the context with distributive first filters \''+self.contextName+'_df from the context \''+self.contextName+'\'')
        # Section about cla2018 method
        
        firstFilters = self.getPrimaryFilters()
        globalContext = Context(self.contextName+'_df', self.debugGraphFolder)
        nameNextVariable = ord('a')
        
        # For each first filters
        for firstFilter in firstFilters:
              
            # Create a new working context
            filterContext = Context(self.contextName+'_'+firstFilter, self.debugGraphFolder)
            for m in self.getJPrime(firstFilter):
                filterContext.M.add(m)
                for j in self.getMPrime(m):
                    if j != firstFilter:
                        filterContext.J.add(j)
                        filterContext.I.add((j,m))
                          
            # Display the context in console
            filterContext.display()
                      
            # Generate the distributive first filter context
#             standardFilterContext = filterContext.generateStandardContext()
            distributiveFilterContext, nameNextVariable = filterContext.generateDistributiveContext(nameNextVariable)
            
            # Display the context in console
            distributiveFilterContext.display()
            # Dsplay the lattice in folder
            lattice = Lattice(distributiveFilterContext)
            lattice.generateGraph(self.debugGraphFolder)
              
            # Fusion with previous distributive first filter context (no merge node atm)
            globalContext.J.update(distributiveFilterContext.J)
            globalContext.M.update(distributiveFilterContext.M)
            globalContext.I.update(distributiveFilterContext.I)
            if not firstFilter in globalContext.J:
                globalContext.J.add(firstFilter)
            for m in distributiveFilterContext.M:
                globalContext.I.add((firstFilter, m))
            
            # Display the context in console
            globalContext.display()
            
        preMerge = deepcopy(globalContext)
        preMerge.contextName += '_preMerge'
        lattice = Lattice(preMerge)
        lattice.generateGraph(self.debugGraphFolder)
#         globalContext.display()
    
        extContext = globalContext.generateExtendedContext()
        
        # Merge node if we can
        addedElement = extContext.J.difference(globalContext.J)
        for e in addedElement:
            count = 0
            commonToMultipleFirstFilters = False
                 
            # Search if e is present in at least two first filters lattice
            for firstFilter in firstFilters:
#                 print(firstFilter,extContext.getJPrime(firstFilter))
#                 print(e,extContext.getJPrime(e))
                if extContext.getJPrime(firstFilter).issuperset(extContext.getJPrime(e)):
                    count += 1
                if count > 1:
                    commonToMultipleFirstFilters = True
                    break
                  
            if commonToMultipleFirstFilters:
                sups = extContext.getDirectsSups(extContext.getJPrime(e))
#                 extContext.display()
                print('parents',e,sups)
                if len(sups) > 1:
                         
                    # Check if e's sups are mergable
                    supsMergables = set()
                    for sup in sups:
                        if sup in extContext.J.difference(globalContext.J):
                            supsMergables.add(sup)
                      
                    # Then merge its
                    if bool(supsMergables):
                        
                        supsUnions = set()
                        for sup in supsMergables:
                            supsUnions = supsUnions.union(extContext.getJPrime(sup))
                            
#                         print('DEBUG_1:',e,parentsMergables,parentsUnions)
#                         extContext.display()
                        supsSecond = set()
                        for sup in supsMergables:
                            supsSecond.update(extContext.getJSecond(sup))
#                             print('DEBUG_2:',parent,parentsSecond)
                        for supSecond in supsSecond:
                            for supsUnion in supsUnions:
                                extContext.I.add((supSecond, supsUnion))                                
                                
        standard = extContext.generateStandardContext()
        extContext.display()
        standard.display()
        return standard
        
        
    def generateDistributiveContext(self, nameNextVariable = ord('a')):
        '''Generate the distributive context of the current contexte
        This can add relation I(j,m) but can't destroy one
        
        '''
                
        print('Generate the distributive context \''+self.contextName+'_d\' of the context \''+self.contextName+'\'')
        
        distributiveContext = Context(self.contextName+'_d', self.debugGraphFolder)
        distributiveContext.J = copy(self.J)
        for j in distributiveContext.J:
            jPrime = self.getJPrime(j)
            jFilters = set()
            X = set()
            for i in distributiveContext.J:
                iPrime = self.getJPrime(i)
                if jPrime >= iPrime:
                    jFilters.add(i)
                else:
                    X.add(i)
            mj = chr(nameNextVariable)
            nameNextVariable += 1
            distributiveContext.M.add(mj)
            for x in X:
                distributiveContext.I.add((x,mj))
                
        return distributiveContext, nameNextVariable
    
    def generateExtendedContext(self):
        
        print('Generate the extended context of \''+self.contextName+'\'')
        
        extended = Context(self.contextName, self.debugGraphFolder)
        extended.J.update(self.J)
        extended.M.update(self.M)
        extended.I.update(self.I)
        
        for j in self.J:
            jPrime = self.getJPrime(j)
            for i in self.J:
                iPrime = self.getJPrime(i)
                alreadyExists = False
                if j != i:
                    intersection_ji = jPrime & iPrime
                    for k in extended.J:
                            if intersection_ji == extended.getJPrime(k):
                                alreadyExists = True
                                break
                    if not alreadyExists:
                        if j < i:
                            jExtended = 'e('+str(j)+str(i)+')'
                        else:
                            jExtended = 'e('+str(i)+str(j)+')'
                        extended.J.add(jExtended)
                        for intersection in intersection_ji:
                            extended.I.add((jExtended, intersection))
                            
        alreadyExists = False
        for j in extended.J:
            if extended.getJPrime(j) == extended.M:
                alreadyExists = True
        if not alreadyExists:
            jBot = 'eBot'
            extended.J.add(jBot)
            for m in extended.M:
                extended.I.add((jBot, m))
                            
        alreadyExists = False
        for j in extended.J:
            haveFilter = False
            for i in extended.I:
                if j == i[0]:
                    haveFilter = True
                    break
            if not haveFilter:
                alreadyExists = True
                break
        if not alreadyExists:
            jBot = 'eTop'
            extended.J.add(jBot)
            
        return extended
                
    def getJPrime(self, j):
        jPrime = set()
        for i in self.I:
            if i[0] == j:
                jPrime.add(i[1])
        return jPrime
                
    def getMPrime(self, m):
        mPrime = set()
        for i in self.I:
            if i[1] == m:
                mPrime.add(i[0])
        return mPrime
                
    def getJSecond(self, j):
        jSecond = copy(self.J)
        jPrime = self.getJPrime(j)
        for m in jPrime:
            jSecond &= self.getMPrime(m)
        return jSecond
                
    def getMSecond(self, m):
        mSecond = copy(self.M)
        mPrime = self.getMPrime(m)
        for j in mPrime:
            mSecond &= self.getJPrime(j)
        return mSecond
    
    def getIrreductibleJ(self):
        irreductiblesObjects = set()
        for j in self.J:
            intersection = copy(self.M)
            alreadyEquivalent = False
            jPrime = self.getJPrime(j)
            jSecond = self.getJSecond(j)
            for k in jSecond:
                kPrime = self.getJPrime(k)
                if jPrime != kPrime:
                    intersection &= kPrime
            for object_v in irreductiblesObjects:
                if jPrime == self.getJPrime(object_v):
                    alreadyEquivalent =True
                    break
            if (jPrime != intersection) and not alreadyEquivalent:
                irreductiblesObjects.add(j)
        return irreductiblesObjects
    
    def getIrreductibleM(self):
        irreductiblesAttributes = set()
        for m in self.M:
            intersection = copy(self.J)
            alreadyEquivalent = False
            mPrime = self.getMPrime(m)
            mSecond = self.getMSecond(m)
            for k in mSecond:
                kPrime = self.getMPrime(k)
                if mPrime != kPrime:
                    intersection &= kPrime
            for attribute in irreductiblesAttributes:
                if mPrime == self.getMPrime(attribute):
                    alreadyEquivalent = True
                    break
            if (mPrime != intersection) and not alreadyEquivalent:
                irreductiblesAttributes.add(m)
        return irreductiblesAttributes
    
    def getPrimaryFilters(self):
        firstFilters = set()
        for j in self.J:
            primary = True
            jPrime = self.getJPrime(j)
            for k in self.J:
                if j != k:
                    kPrime = self.getJPrime(k)
                    if jPrime <= kPrime:
                        primary = False
                        break
            if primary:
                firstFilters.add(j)
        return firstFilters
    
    def getDirectsInfs(self, searchedFilters):
        directInfs = set()
        for j in self.J:
            jPrime = self.getJPrime(j)
            if jPrime > searchedFilters: #(self.getJPrime(j).issuperset(searchedFilters)) and not (self.getJPrime(j).issubset(searchedFilters)):
                directInfs_copy = copy(directInfs)
                alreadyHaveBetterInf = False
                for inf in directInfs_copy:
                    infPrime = self.getJPrime(inf)
                    if jPrime < infPrime: #self.getJPrime(j).issubset(self.getJPrime(child)):
                        directInfs.discard(inf)
                    elif jPrime > infPrime: #self.getJPrime(j).issuperset(self.getJPrime(child)):
                        alreadyHaveBetterInf = True
                        break
                if not alreadyHaveBetterInf:
                    directInfs.add(j)
        return directInfs
    
    def getDirectsSups(self, searchedFilters):
        directSups = set()
        for j in self.J:
            jPrime = self.getJPrime(j)
            if jPrime < searchedFilters: #(self.getJPrime(j).issubset(searchedFilters)) and not (self.getJPrime(j).issuperset(searchedFilters)):
                directSups_copy = copy(directSups)
                alreadyHaveBetterSup = False
                for sup in directSups_copy:
                    supPrime = self.getJPrime(sup)
                    if jPrime > supPrime: #(self.getJPrime(j).issuperset(self.getJPrime(parent))) and not (self.getJPrime(j).issubset(self.getJPrime(parent))):
                        directSups.discard(sup)
                    elif jPrime < supPrime: #self.getJPrime(j).issubset(self.getJPrime(parent)):
                        alreadyHaveBetterSup = True
                if not alreadyHaveBetterSup:
                    directSups.add(j)
        return directSups
    
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
        
    def exportJsonForLatviz(self):
        print('Not yet implemented')