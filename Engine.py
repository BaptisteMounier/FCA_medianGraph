import csv
from copy import copy, deepcopy

from Context import Context
from Lattice import Lattice

class Engine(object):
    '''
    classdocs
    '''


    def __init__(self, graph_directory):
        '''
        Constructor
        '''
        self.graph_directory = graph_directory
        
    def import_context_from_file(self, file):
        """Import context values from a file.
        
        Read line by line the file to create J, M and I sets.
        Keyword arguments:
        file_path -- the file path
        
        """
        
#         print('Generate the context \'' + file.stem + '\' from \'' + str(file) + '\'')
        context = Context(file.stem)
        
        with file.open() as csv_file:
            lecteur = csv.reader(csv_file, delimiter='\t', quotechar='|')
            
            M_list = next(lecteur)
            for m in M_list:
                context.add_m(m)
            
            l = 1
            for line in lecteur:
                c = 0
                j = 'o'+str(l)
                context.add_j(j)
                for colonne in line:
                    if (colonne != '') and (colonne != '0'):
                        context.add_i(j, M_list[c])
                    c += 1
                l += 1
                
        return context
    
    def transform_to_standard_context(self, context):
        """Create standard context from current."""
        
#         print('Generate the standard context of \''+context.context_name+'\'')
        if context.mode == Context.standard:
            return context
        standard_context = Context(context.context_name)
        standard_context.J = copy(context.get_irreductibles_infs(False))
        standard_context.M = copy(context.get_irreductibles_sups(False))
        for i in context.I:
            if (i[0] in standard_context.J) and (i[1] in standard_context.M):
                standard_context.add_i(i[0], i[1])
        standard_context.mode = Context.standard
        return standard_context
        
    def transform_to_extended_context(self, context):
        """Generate the extended version of current context
        
        It'll create one j for each node on the graph
        
        """
        
#         print('Generate the extended context of \''+context.context_name+'\'')
        if context.mode == Context.extended:
            return context
        
        extended_context = Context(context.context_name)
        extended_context.J.update(context.J)
        extended_context.M.update(context.M)
        extended_context.I.update(context.I)
        
#         print('Debug - extended - start')
#         extended_context.display()
        
        extended_context.extend_j()
#         print('Debug - extended - j')
#         extended_context.display()
        extended_context.extend_m()
#         print('Debug - extended - m')
#         extended_context.display()
        extended_context.mode = Context.extended
        
        return extended_context
        
        
    def transform_to_distributive_context(self, context):
        """Generate distributive context from current
        
        Can add relations I(j,m) but can't destroy one
        
        """
                
#         print('Generate the distributive context \''+context.context_name+'_d\' of the context \''+context.context_name+'\'')
        if context.mode == Context.distributive:
            return context
        
        distributive_context = Context(context.context_name+'_d')
        distributive_context.J = copy(context.J)
        for j in distributive_context.J:
            j_prime = context.get_j_prime(j)
            j_filters = set()
            X = set()
            for k in distributive_context.J:
                i_prime = context.get_j_prime(k)
                if j_prime >= i_prime:
                    j_filters.add(k)
                else:
                    X.add(k)
            mj = 'm_'+j
            distributive_context.add_m(mj)
            for x in X:
                distributive_context.add_i(x, mj)
                
        return distributive_context
    
    def step_transform_to_median_context(self, context, atoms):
        
        global_context = Context(context.context_name)
        
        # For each first filters
        for atom in atoms:
              
            # Create a new working context
            filter_context = Context(context.context_name+'_' + atom)
            for m in context.get_j_prime(atom):
                filter_context.M.add(m)
                for j in context.get_m_prime(m):
                    if j != atom:
                        filter_context.add_j(j)
                        filter_context.add_i(j,m)
                      
            # Generate the distributive first filter context
            distributive_filter_context = self.transform_to_distributive_context(filter_context)
            
            if not len(distributive_filter_context.I):
                for j in distributive_filter_context.J:
                        m_label = 'c'+str(atom)
                        distributive_filter_context.add_m(m_label)
                        distributive_filter_context.add_i(j, m_label)
              
            # Fusion with previous distributive first filter context (no merge node atm)
            global_context.J.update(distributive_filter_context.J)
            # Add first filter if not exist
            # TODO: utile ?
            if not atom in global_context.J:
                global_context.add_j(atom)
                # If no attribute, create new one
                if not len(distributive_filter_context.M):
                    new_name_m = 'a'+str(global_context.name_next_variable)
                    global_context.add_m(new_name_m)
                    global_context.add_i(atom, new_name_m)
                    global_context.name_next_variable += 1
            # Add all M with a new name
            for m in distributive_filter_context.M:
                new_name_m = 'a'+str(global_context.name_next_variable)
                global_context.add_m(new_name_m)
                for i in distributive_filter_context.I:
                    if i[1] == m:
                        global_context.add_i(i[0], new_name_m)
                global_context.add_i(atom, new_name_m)
                global_context.name_next_variable += 1
                
        return global_context
    
    def transform_to_median_context(self, context):
#         print('Generate the context with distributive first filters \'' + context.context_name+'_df\' from the context \'' + context.context_name+'\'')
        if context.mode == Context.median:
            return context
        
        global_context = self.transform_to_standard_context(context)
        atoms = global_context.get_atoms()
#         global_context_copy = deepcopy(global_context)
        ext_global_context = self.transform_to_extended_context(global_context)
        
        step = 0
        median = False
        
        while not median:
            
            previous_global_context = deepcopy(global_context)
            
            median = True
            atoms_contexts = self.extract_atoms_contexts(ext_global_context, atoms)
            for atom_context in atoms_contexts:
#                 print('test median')
                if not self.context_is_distributive(atom_context):
                    median = False
            if not median:
            
                step += 1
                
                global_context = self.step_transform_to_median_context(previous_global_context, atoms)
                ext_global_context = self.transform_to_extended_context(global_context)
                
                lattice = Lattice(self, ext_global_context)
                lattice.generate_graph(self.graph_directory, '_distri' + str(step), extended = True)
        
                merge_ended = False
                countLoop = 0
                while not merge_ended:
                    countLoop += 1
#                     print('Debug - median', step, countLoop)
                    
                    merge_ended = True
                    ext_global_context_copy = deepcopy(ext_global_context)
                    for concept in ext_global_context_copy.J:
                         
                        count = 0
                        for atom in atoms:
                            if ext_global_context.get_j_prime(atom).issuperset(ext_global_context.get_j_prime(concept)):
                                count += 1
                            if count > 1:
                                break
                         
                        if count > 1:
                            concept_prime = ext_global_context.get_j_prime(concept)
                            sups = ext_global_context.get_directs_j_sups(concept_prime)
#                             sups.difference_update(global_context_copy.J)
                            if len(sups) > 1:
                                      
                                # Check if e's sups are mergable    
                                sups_mergables = set()
                                concept_second = ext_global_context.get_j_second(concept)
                                modification = True
                                while modification: #len(sups) > 0:
                                    modification = False    
                                    sups.difference_update(sups_mergables)
                                    sups_mergables = set()
                                    atoms_source = set()
                                    for sup in sups:
                                        if sup in ext_global_context.J.difference(global_context.J):
                                            sup_seconds = ext_global_context.get_j_second(sup)
                                            sup_seconds.discard(sup)
                                            sup_edits = sup_seconds.difference(concept_second)
                                            sup_edits_prime = set()
                                            for sup_edit in sup_edits:
                                                sup_edits_prime.update(ext_global_context.get_j_prime(sup_edit))
                                            mergeable = True
                                            for atom_source in atoms_source:
                                                atom_prime = ext_global_context.get_j_prime(atom_source)
                                                for sup_second in sup_edits:
                                                    if atom_prime.issuperset(ext_global_context.get_j_prime(sup_second)):
                                                        mergeable = False
                                                        break
                                            if mergeable:
                                                for atom in atoms:
                                                    atom_prime = ext_global_context.get_j_prime(atom)
                                                    for sup_second in sup_edits:
                                                        if atom_prime.issuperset(ext_global_context.get_j_prime(sup_second)):
                                                            atoms_source.add(atom)
                                                            break
                                                sups_mergables.add(sup)
                                                modification = True
#                                          
                                    if len(sups_mergables) > 1:
                                         
                                        sups_unions = set()
                                        sups_second_union = set()
                                        sups_second_inter = copy(ext_global_context.J)
    #                                     print('Debug, POWER')
    #                                     ext_global_context.display()
    #                                     print('Debug, sups_mergables', sups_mergables)
                                        
                                        for sup in sups_mergables:
                                            sup_prime = ext_global_context.get_j_prime(sup)
                                            sups_unions.update(sup_prime)
    #                                         print('Union', sup, sup_prime, sups_unions)
                                            second = ext_global_context.get_j_second(sup)
                                            sups_second_union.update(second)
    #                                         print('Second Union', sup, second, sups_second_union)
                                            sups_second_inter.intersection_update(second)
    #                                         print('Second Inter', sup, second, sups_second_inter)
                                             
    #                                     for sups_union in sorted(sups_unions):
    #                                         label += '_'+sups_union
                                            
                                        for sup_second in sups_second_union:
                                            for sups_union in sups_unions:
                                                ext_global_context.add_i(sup_second, sups_union)
    #                                         print('In loop, old', sup_second, sups_unions)
                                                 
                                        label = ext_global_context.new_m_id('n')
                                        ext_global_context.add_m(label)
                                        for sup_second in sups_second_inter:
                                            ext_global_context.add_i(sup_second, label)
    #                                     print('In loop, new', sups_second_inter, label)
    #                                     ext_global_context.display()
                                        merge_ended = False
                                        break
                                
                            elif len(sups) < 2:
                                infs = ext_global_context.get_directs_j_infs(concept_prime)
                                if len(infs) == 1:
                                    counter = 0
                                    for inf in infs:
                                        counter += 1
                                        assert counter < 2
                                        inf_prime = ext_global_context.get_j_prime(inf)
                                        for inf_m in inf_prime:
                                            ext_global_context.add_i(concept, inf_m)
                                    merge_ended = False
                                    break
                                    
                                    
                    global_context = self.transform_to_standard_context(ext_global_context)
#                     global_context.context_name = 'debug_std'+str(countLoop)
#                     global_context.display()
                    ext_global_context = self.transform_to_extended_context(global_context)
#                     ext_global_context.context_name = 'debug_ext'+str(countLoop)
#                     ext_global_context.display()
                    if not merge_ended:
                        lattice = Lattice(self, ext_global_context)
                        lattice.generate_graph(self.graph_directory, '_distri' + str(step) + '_merge' + str(countLoop))
               
        previous_global_context.context_name += '_median'
        previous_global_context.mode = Context.median
        return previous_global_context
    
    def context_is_distributive(self, context):
        if context.mode == Context.extended:
            ext = context
            std = self.transform_to_standard_context(ext)
        elif context.mode == Context.standard:
            std = context
            ext = self.transform_to_extended_context(std)
        elif context.mode == Context.median:
            return True
        else:
            std = self.transform_to_standard_context(context)
            ext = self.transform_to_extended_context(context)
            arrow = {}
            
        for j in std.J:
            j_prime = ext.get_j_prime(j)
            direct_infs = ext.get_directs_j_infs(j_prime)
            count = 0
            relation_down_arrow = set()
            for inf in direct_infs:
                if inf == 'jBot':
                    inf_prime = std.M
                else:
                    inf_prime = ext.get_j_prime(inf).intersection(std.M)
                relation_down_arrow.update(inf_prime.difference(j_prime))
            for m in relation_down_arrow:
                count += 1
                if count > 1:
                    return False
                if not (j, m) in arrow.keys():
                    arrow[(j, m)] = 'down'
                elif arrow[(j, m)] == 'up':
                    arrow[(j, m)] = 'double'
                elif arrow[(j, m)] != 'double':
                    assert 'This relation ' + arrow[(j, m)] + ' can\'t exist.'
            if count == 0:
                return False
        
        for m in std.M:
            m_prime = ext.get_m_prime(m)
            direct_infs = ext.get_directs_m_infs(m_prime)
            count = 0
            relation_up_arrow = set()
            for inf in direct_infs:
                if inf == 'mBot':
                    inf_prime = std.J
                else:
                    inf_prime = ext.get_m_prime(inf).intersection(std.J)
                tmp = inf_prime.difference(m_prime)
                relation_up_arrow.update(tmp)
            for j in relation_up_arrow:
                count += 1
                if count > 1:
                    return False
                if not (j, m) in arrow.keys():
                    arrow[(j, m)] = 'up'
                elif arrow[(j, m)] == 'down':
                    arrow[(j, m)] = 'double'
                elif arrow[(j, m)] != 'double':
                    assert 'This relation ' + str(arrow[(j, m)]) + ' can\'t exist.'
            if count == 0:
                return False
            
        for j in std.J:
            count = 0
            for m in std.M:
                if (j, m) in arrow.keys():
                    if arrow[(j, m)] != 'double':
                        return False
        
        context.mode = Context.median
        return True
    
    def extract_atoms_contexts(self, context, atoms):
        
        list_contexts = set()
        
        std = self.transform_to_standard_context(context)
        # For each first filters
        for atom in atoms:
              
            # Create a new working context
            atom_context = Context(std.context_name+'_' + atom)
            for m in std.get_j_prime(atom):
                atom_context.add_m(m)
                for j in std.get_m_prime(m):
                    atom_context.add_j(j)
                    atom_context.add_i(j,m)
            list_contexts.add(atom_context)
                        
        return list_contexts