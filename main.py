# -*- coding: utf-8 -*-
import argparse
import os

from Context import Context
from Lattice import Lattice

if __name__=="__main__":
    
    def analyse(context_file_name, context_file_path, graph_directory):
        print('-'*25)
        print('Analysis of \''+context_file_name+'\'')
        
        context = Context(context_file_name, graph_directory)
        context.generate_context_fom_file(context_file_path)
        context.display()
        
        context_s = context.generate_standard_context()
        context_s.display()
        lattice_s = Lattice(context_s)
        lattice_s.generate_graph(graph_directory)
        tmp = context_s.generate_extended_context()
        
        Context_df = context_s.generate_distributive_context_on_first_filters()
        Context_df.display()
        global_lattice_df = Lattice(Context_df)
        global_lattice_df.generate_graph(target_directory, tmp.J)
        
        global_context_d, useless_here = context_s.generate_distributive_context()
        global_context_d.display()
        global_lattice_d = Lattice(global_context_d)
        global_lattice_d.generate_graph(target_directory)
        
#         context_s_df = Context_df.generate_standard_context()
#         context_s_df.display()
#         lattice_s_df = Lattice(context_s_df)
#         lattice_s_df.generate_graph(target_directory)
        
        print('-'*25)

    # Check option's command
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default='validation', help="Context file name")
    args = parser.parse_args()
    args.file = 'cla_v4'
    
    if args.file == 'validation':
        for filename in os.listdir('data/'+args.file+'/'):
            if filename.endswith(".txt"):
                target_directory = 'data/validation/graph/'
                context_file_path = 'data/validation/' + filename
                (name,ext) = os.path.splitext(filename)
                analyse(name, context_file_path, target_directory)
    else:
        target_directory = 'data/graph/'
        context_file_path = 'data/' + args.file + '.txt'
        analyse(args.file, context_file_path, target_directory)