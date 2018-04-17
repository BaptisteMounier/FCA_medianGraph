# -*- coding: utf-8 -*-
import argparse
import os

from Context import Context
from Lattice import Lattice

if __name__=="__main__":
    
    def analyse(contextFileName, contextFilePath, graphDirectory):
        print('-'*25)
        print('Analysis of \''+contextFileName+'\'')
        
        context = Context(contextFileName)
        context.generateContextFomFile(contextFilePath)
        #context.display()
        
        sContext = context.generateStandardContext()
        sContext.display()
        slattice = Lattice(sContext)
        slattice.generateGraph(graphDirectory)
        
        dfContext = sContext.generateDistributiveContextOnFirstFilters()
        #dfContext.display()
        
        sdfContext = dfContext.generateStandardContext()
        sdfContext.display()
        sdfLattice = Lattice(sdfContext)
        sdfLattice.generateGraph(targetDirectory)
        
#         dContext = sContext.generateDistributiveContext()
#         dContext.display()
#          
#         sdContext = dContext.generateStandardContext()
#         sdContext.display()
#         sdlattice = Lattice(sdContext)
#         sdlattice.generateGraph(graphDirectory)
        print('-'*25)

    # Check option's command
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default='validation', help="Context file name")
    args = parser.parse_args()
    #args.file = 'cla'
    args.file = 'crown'
    #args.file = 'clav2'
    #args.file = 'divisors'
    #args.file = 'priss2013-table01'
    #args.file = 'n5'
    
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