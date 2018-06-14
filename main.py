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
#         context_extended = engine.transform_to_extended_context(context)
        latice_context = Lattice(engine, context)
        latice_context.generate_graph(graph_directory)
#         context.display()
#         context.export_txt_for_conex(export_directory)
#         latice_context = Lattice(engine, context_extended)
#         latice_context.generate_graph(graph_directory, add_name = '_ext', extended = True)
        
#         context.display()
#         context.export_txt_for_conex(export_directory)
        
        median_context = engine.transform_to_median_context(context)
        lattice_median_context = Lattice(engine, median_context)
        lattice_median_context.generate_graph(graph_directory, differences = context.J)
        
        print('-'*25)

    # Check option's command
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default='validation', help="Context file name")
    args = parser.parse_args()
#     args.file = 'priss2013-table01'
#     args.file = 'cla_v5'

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