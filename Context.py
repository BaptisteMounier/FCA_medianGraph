import csv
from copy import copy
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
        for firstFilter in firstFilters:
            filterContext = Context(self.contextName+'_'+firstFilter)
            filterContext.J = copy(self.J)
            for i in self.I:
                if i[1] in self.getJPrime(firstFilter):
                    filterContext.I.add(i)
                    filterContext.M.add(i[1])
            filterStandardContext = filterContext.generateStandardContext()
#             filterStandardContext.display()
            filterDistributiveContext = filterStandardContext.generateDistributiveContext()
            filterDistributiveContext.display()
            filterStandardDistributiveContext = filterDistributiveContext.generateStandardContext()
            for j in globalContext.J:
                if j == firstFilter:
                    for m in filterStandardDistributiveContext.M:
                        globalContext.I.add((j,m))
            for j in filterStandardDistributiveContext.J:
                if (j != firstFilter) and (j in firstFilters):
                    for m in globalContext.M:
                        globalContext.I.add((j,m))
            globalContext.J.update(filterStandardDistributiveContext.J)
            globalContext.M.update(filterStandardDistributiveContext.M)
            globalContext.I.update(filterStandardDistributiveContext.I)
            globalContext.display()
            lattice = Lattice(filterDistributiveContext)
            lattice.generateGraph('data/graph/')
            
        glattice = Lattice(globalContext)
        glattice.generateGraph('data/graph/')
        
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
                        jExtended = 'e'+str(j)+str(i)
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