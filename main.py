# -*- coding: utf-8 -*-
import argparse
from pathlib import Path

from Context import Context
from Lattice import Lattice

if __name__=="__main__":
    
    def analyse(file, graph_directory, export_directory):
        print('-'*25)
        print('Analysis of \''+file.stem+'\'')
        
        context = Context(file.stem, graph_directory)
        context.generate_context_fom_file(file)
        context.display()
        context.export_txt_for_conex(export_directory)
        
        context_s = context.generate_standard_context()
        lattice_s = Lattice(context_s)
        lattice_s.generate_graph(graph_directory)
        tmp = context_s.generate_extended_context()
        
        Context_df = context_s.generate_distributive_context_on_first_filters()
        global_lattice_df = Lattice(Context_df)
        global_lattice_df.generate_graph(graph_directory, differences = tmp.J)
        Context_df.export_txt_for_conex(export_directory)
        
#         global_context_d = context_s.generate_distributive_context()
#         global_lattice_d = Lattice(global_context_d)
#         global_lattice_d.generate_graph(graph_directory)
        
        print('-'*25)

    # Check option's command
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default='validation', help="Context file name")
    args = parser.parse_args()
#     args.file = 'priss2013-table01'
#     args.file = 'bandelt2000-table02'
#     args.file = 'cla_v4'
#     args.file = 'test'

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
        
#     for x in range(0,3):
#         test1 = set()
#         test1.add('a')
#         test1.add('b')
#         test1.add('c')
#         test1.add('d')
#         test1.add('e')
#         s = ''
#         for t in test1:
#             s += t
#         print(s)
#         print(test1)
#         
#     
#     test2 = set()
#     test2.add('b')
#     test2.add('d')
#     test2.add('c')
#     test2.add('a')
#     test2.add('e')
#     s = ''
#     for t in test2:
#         s += t
#     print(s)
#     print(test2)