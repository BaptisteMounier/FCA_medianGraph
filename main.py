# -*- coding: utf-8 -*-
import argparse
import os

from Context import Context
from Lattice import Lattice

if __name__=="__main__":
    
    def analyse(contextFileName, contextFilePath, graphDirectory):
        print('-'*25)
        print('Analysis of \''+contextFileName+'\'')
        
        context = Context(contextFileName, graphDirectory)
        context.generateContextFomFile(contextFilePath)
        context.display()
        
        sContext = context.generateStandardContext()
        sContext.display()
        slattice = Lattice(sContext)
        slattice.generateGraph(graphDirectory)
        
        dfContext = sContext.generateDistributiveContextOnFirstFilters()
        dfContext.display()
        dfGlobalLattice = Lattice(dfContext)
        dfGlobalLattice.generateGraph(targetDirectory)
        
#         dGlobalContext = sContext.generateDistributiveContext()
#         dGlobalContext.display()
#         dGlobalLattice = Lattice(dGlobalContext)
#         dGlobalLattice.generateGraph(targetDirectory)
        
#         sdfContext = dfContext.generateStandardContext()
#         sdfContext.display()
#         sdfLattice = Lattice(sdfContext)
#         sdfLattice.generateGraph(targetDirectory)
        
        print('-'*25)

    # Check option's command
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default='validation', help="Context file name")
    args = parser.parse_args()
    args.file = 'clav2'
    
    if args.file == 'validation':
        for filename in os.listdir('data/'+args.file+'/'):
            if filename.endswith(".txt"):
                targetDirectory = 'data/validation/graph/'
                contextFilePath = 'data/validation/' + filename
                (name,ext) = os.path.splitext(filename)
                analyse(name, contextFilePath, targetDirectory)
    else:
        targetDirectory = 'data/graph/'
        contextFilePath = 'data/' + args.file + '.txt'
        analyse(args.file, contextFilePath, targetDirectory)