# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

from Lattice import Lattice
from Engine import Engine

if __name__=="__main__":
    
    def analyse(file, graph_directory, export_directory):
        print('-'*25)
        print('Analysis of \''+file.stem+'\'')
        
        print(file)
        
        engine = Engine(graph_directory)
        context = engine.import_context_from_file(file)
        context.display()
        lat2 = Lattice(engine, context)
        lat2.generate_graph(graph_directory, extended = True)
        std = engine.transform_to_standard_context(context)
        std.context_name += '_std'
        std.display()
        lat3 = Lattice(engine, std)
        lat3.generate_graph(graph_directory)
        ext = engine.transform_to_extended_context(std)
        ext.context_name += '_ext'
        ext.display()
        lat = Lattice(engine, ext)
        lat.generate_graph(graph_directory, extended = True)
#         ext = engine.transform_to_extended_context(context)
#         lat = Lattice(engine, ext)
#         lat.generate_graph(graph_directory, extended = True)
#         median = engine.transform_to_median_context(context)
#         lat = Lattice(engine, median)
#         lat.generate_graph(graph_directory)
        
        print('-'*25)

    # Check option's command
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default='validation', help="Context file name")
    args = parser.parse_args()
#     args.file = 'priss2013-table01'
    args.file = 'tmp3'

    data_dir = Path('data')
    graph_target_directory = Path('data/graph/')
    export_target_directory = Path('data/export/')
    
    if args.file == 'validation':
        for file in data_dir.glob('*.txt'):
            analyse(file, graph_target_directory, export_target_directory)
    else:
        for file in data_dir.glob('*.txt'):
            if file.stem == args.file:
                analyse(file, graph_target_directory, export_target_directory)