import csv
from copy import copy, deepcopy
from pathlib import Path

from Lattice import Lattice

class Context(object):
    """
    classdocs
    """


    def __init__(self, context_name, debug_graph_folder):
        """Constructor."""
        
        self.context_name = context_name
        self.J = set()
        self.M = set()
        self.I = set()
        self.debug_graph_folder = debug_graph_folder
        self.debug = True
        self.name_next_variable = 1
        
    def generate_context_fom_file(self, file):
        """Import context values from a file.
        
        Read line by line the file to create J, M and I sets.
        Keyword arguments:
        file_path -- the file path
        
        """
        
        print('Generate the context \''+self.context_name+'\' from the file \''+file.stem+'\'')
        with file.open() as csv_file:
            lecteur = csv.reader(csv_file, delimiter='\t', quotechar='|')
            M_list = next(lecteur)
            self.M = set(M_list)
            
            l = 1
            for line in lecteur:
                c = 0
                object_of_line = 'o'+str(l)
                self.J.add(object_of_line)
                for colonne in line:
                    if (colonne != '') and (colonne != '0'):
                        self.I.add((object_of_line, M_list[c]))
                    c += 1
                l += 1
                
    def generate_standard_context(self):
        """Create standard context from current."""
        
        print('Generate the standard context of \''+self.context_name+'\'')
        standard_context = Context(self.context_name, self.debug_graph_folder)
        standard_context.J = copy(self.get_irreductible_J())
        standard_context.M = copy(self.get_irreductible_M())
        for i in self.I:
            if (i[0] in standard_context.J) and (i[1] in standard_context.M):
                standard_context.I.add((i[0],i[1]))
        return standard_context
    
    def step_distributive_context_on_first_filters(self, first_filters):
        
        global_context = Context(self.context_name, self.debug_graph_folder)
        
        # For each first filters
        for first_filter in first_filters:
              
            # Create a new working context
            filter_context = Context(self.context_name+'_'+first_filter, self.debug_graph_folder)
            for m in self.get_J_prime(first_filter):
                filter_context.M.add(m)
                for j in self.get_M_prime(m):
                    if j != first_filter:
                        filter_context.J.add(j)
                        filter_context.I.add((j,m))
                      
            # Generate the distributive first filter context
            distributive_filter_context = filter_context.generate_distributive_context()
            distributive_filter_context.display()
            
            if not len(distributive_filter_context.I):
                for j in distributive_filter_context.J:
                        m_label = 'c'+str(first_filter)
                        distributive_filter_context.M.add(m_label)
                        distributive_filter_context.I.add((j, m_label))
              
            # Fusion with previous distributive first filter context (no merge node atm)
            global_context.J.update(distributive_filter_context.J)
            # Add first filter if not exist
            if not first_filter in global_context.J:
                global_context.J.add(first_filter)
                # If no attribute, create new one
                if not len(distributive_filter_context.M):
                    new_name_m = 'a'+str(global_context.name_next_variable)
                    global_context.M.add(new_name_m)
                    global_context.I.add((first_filter, new_name_m))
                    global_context.name_next_variable += 1
            # Add all M with a new name
            for m in distributive_filter_context.M:
                new_name_m = 'a'+str(global_context.name_next_variable)
                global_context.M.add(new_name_m)
                for i in distributive_filter_context.I:
                    if i[1] == m:
                        global_context.I.add((i[0], new_name_m))
                global_context.I.add((first_filter, new_name_m))
                global_context.name_next_variable += 1
                
            global_context.display()
                
        return global_context
        
    def generate_distributive_context_on_first_filters(self):
        """Create first filters distributivity context from current."""
        
        print('Generate the context with distributive first filters \''+self.context_name+'_df\' from the context \''+self.context_name+'\'')
        # Section about cla2018 method
        
        first_filters = self.get_first_filters()
        ext = self.generate_extended_context()
        
        finish = False
        step = 1
        previous_global_context = deepcopy(self)
        while not finish:
            
            global_context = previous_global_context.step_distributive_context_on_first_filters(first_filters)
            
            ext_previous_global_context = previous_global_context.generate_extended_context()
            ext_global_context = global_context.generate_extended_context()
            if len(ext_previous_global_context.J) == len(ext_global_context.J):
                finish = True
            lattice = Lattice(global_context)
            lattice.generate_graph(self.debug_graph_folder, '_distri'+str(step))
            previous_global_context = deepcopy(global_context)
            step += 1
            global_context.display()
            lattice = Lattice(global_context)
            lattice.generate_graph(self.debug_graph_folder, '_preMerge')
        
        global_context.context_name += '_df'
        merge_ended = False
        countLoop = 1
        while not merge_ended:
            merge_ended = True
            ext_context_copy = deepcopy(ext_global_context)
            for concept in ext_context_copy.J:
                 
                count = 0
                for first_filter in first_filters:
                    if ext_context_copy.get_J_prime(first_filter).issuperset(ext_context_copy.get_J_prime(concept)):
                        count += 1
                    if count > 1:
                        break
                 
                if count > 1:
                    sups = ext_context_copy.get_directs_sups(ext_context_copy.get_J_prime(concept))
                    sups.difference_update(global_context.J)
                     
                    if len(sups) > 1:
                              
                        # Check if e's sups are mergable
                        sups_mergables = set()
                        for sup in sups:
                            if sup in ext_context_copy.J.difference(ext.J):
                                sups_mergables.add(sup)
                                 
                        if len(sups_mergables) > 1:
                             
                            sups_unions = set()
                            sups_second_union = set()
                            sups_second_inter = copy(ext_context_copy.J)
                            label = 'n'
                             
                            for sup in sups_mergables:
                                sups_unions.update(ext_context_copy.get_J_prime(sup))
                                second = ext_context_copy.get_J_second(sup)
                                sups_second_union.update(second)
                                sups_second_inter.intersection_update(second)
                                 
                            for sups_union in sups_unions:
                                label += '_'+sups_union
                             
                            for sup_second in sups_second_union:
                                for sups_union in sups_unions:
                                    ext_global_context.I.add((sup_second, sups_union))
                                     
                            ext_global_context.M.add(label)
                            for sup_second in sups_second_inter:
                                ext_global_context.I.add((sup_second, label))
                             
                            merge_ended = False
                            break
                             
            standard = ext_global_context.generate_standard_context()
            ext_global_context = standard.generate_extended_context()
            if not merge_ended:
                lattice = Lattice(standard)
                lattice.generate_graph(self.debug_graph_folder, '_merge' + str(countLoop))
                countLoop += 1
            standard.context_name += '_df'
            
        return standard
    
    def generate_distributive_context(self):
        """Generate distributive context from current
        
        Can add relations I(j,m) but can't destroy one
        
        """
                
        print('Generate the distributive context \''+self.context_name+'_d\' of the context \''+self.context_name+'\'')
        
        distributive_context = Context(self.context_name+'_d', self.debug_graph_folder)
        distributive_context.J = copy(self.J)
        for j in distributive_context.J:
            j_prime = self.get_J_prime(j)
            j_filters = set()
            X = set()
            for i in distributive_context.J:
                i_prime = self.get_J_prime(i)
                if j_prime >= i_prime:
                    j_filters.add(i)
                else:
                    X.add(i)
            mj = 'm_'+j
            distributive_context.M.add(mj)
            for x in X:
                distributive_context.I.add((x,mj))
                
        return distributive_context
    
    def generate_extended_context(self):
        """Generate the extended version of current context
        
        It'll create one j for each node on the graph
        
        """
        
        print('Generate the extended context of \''+self.context_name+'\'')
        
        extended = Context(self.context_name, self.debug_graph_folder)
        extended.J.update(self.J)
        extended.M.update(self.M)
        extended.I.update(self.I)
        
        already_exists = False
        for j in extended.J:
            if extended.get_J_prime(j) == extended.M:
                already_exists = True
        if not already_exists:
            j_bot = 'eBot'
            extended.J.add(j_bot)
            for m in extended.M:
                extended.I.add((j_bot, m))
                            
        already_exists = False
        for j in extended.J:
            have_filter = False
            for i in extended.I:
                if j == i[0]:
                    have_filter = True
                    break
            if not have_filter:
                already_exists = True
                break
        if not already_exists:
            j_top = 'eTop'
            extended.J.add(j_top)
        
        indice = 1
        modification = True
        while modification:
            modification = False
            extended_copy = deepcopy(extended)
            for j in extended_copy.J:
                j_prime = extended_copy.get_J_prime(j)
                for i in extended_copy.J:
                    i_prime = extended_copy.get_J_prime(i)
                    already_exists = False
                    if j != i:
                        intersection_ji = j_prime & i_prime
                        for k in extended.J:
                                if intersection_ji == extended.get_J_prime(k):
                                    already_exists = True
                                    break
                        if not already_exists:
                            modification = True
#                             if j < i:
#                                 j_extended = 'e('+str(j)+str(i)+')'
#                             else:
#                                 j_extended = 'e('+str(i)+str(j)+')'
                            j_extended = 'e'+str(indice)
                            extended.J.add(j_extended)
                            indice += 1
                            for intersection in intersection_ji:
                                extended.I.add((j_extended, intersection))
                            
#         modification = True
#         while modification:
#             modification = False
#             j_extended = copy(extended.J)
#             for j in j_extended:
#                 if j not in self.J:
#                     j_prime = extended.get_J_prime(j)
#                     infs = extended.get_directs_infs(j_prime)
#                     if infs:
#                         min = 'z'
#                         max = 'A'
#                         for inf in infs:
#                             if inf < min:
#                                 min = inf
#                             if inf > max:
#                                 max = inf
#                         new_name = 'e('+str(min)+str(max)+')'
#                         if new_name != j:
#                             modification = True
#                             extended.J.discard(j)
#                             extended.J.add(new_name)
#                             i_extended = copy(extended.I)
#                             for i in i_extended:
#                                 if i[0] == j:
#                                     extended.I.discard(i)
#                                     extended.I.add((new_name, i[1]))
            
        return extended
                
    def get_J_prime(self, j):
        """Return j' set for a given j"""
        j_prime = set()
        for i in self.I:
            if i[0] == j:
                j_prime.add(i[1])
        return j_prime
                
    def get_M_prime(self, m):
        """Return m' set for a given m"""
        m_prime = set()
        for i in self.I:
            if i[1] == m:
                m_prime.add(i[0])
        return m_prime
                
    def get_J_second(self, j):
        """Return j'' set for a given j"""
        j_second = copy(self.J)
        j_prime = self.get_J_prime(j)
        for m in j_prime:
            j_second &= self.get_M_prime(m)
        return j_second
                
    def get_M_second(self, m):
        """Return m'' set for a given m"""
        m_second = copy(self.M)
        m_prime = self.get_M_prime(m)
        for j in m_prime:
            m_second &= self.get_J_prime(j)
        return m_second
    
    def get_irreductible_J(self):
        """Return all irreductible j"""
        irreductibles_objects = set()
        for j in self.J:
            intersection = copy(self.M)
            already_equivalent = False
            bot = True
            j_prime = self.get_J_prime(j)
            j_second = self.get_J_second(j)
            for k in j_second:
                k_prime = self.get_J_prime(k)
                if j_prime != k_prime:
                    intersection &= k_prime
                    bot = False
            for object_v in irreductibles_objects:
                if j_prime == self.get_J_prime(object_v):
                    already_equivalent =True
                    break
            if ((j_prime != intersection) or bot) and not already_equivalent:
                irreductibles_objects.add(j)
        return irreductibles_objects
    
    def get_irreductible_M(self):
        """Return all irreductible m"""
        irreductibles_attributes = set()
        for m in self.M:
            intersection = copy(self.J)
            already_equivalent = False
            top = True
            m_prime = self.get_M_prime(m)
            m_second = self.get_M_second(m)
            for k in m_second:
                kPrime = self.get_M_prime(k)
                if m_prime != kPrime:
                    intersection &= kPrime
                    top = False
            for attribute in irreductibles_attributes:
                if m_prime == self.get_M_prime(attribute):
                    already_equivalent = True
                    break
            if ((m_prime != intersection) or top) and not already_equivalent:
                irreductibles_attributes.add(m)
        return irreductibles_attributes
    
    def get_first_filters(self):
        """Return all first filters"""
        first_filters = set()
        for j in self.J:
            primary = True
            j_prime = self.get_J_prime(j)
            for k in self.J:
                if j != k:
                    k_prime = self.get_J_prime(k)
                    if j_prime <= k_prime:
                        primary = False
                        break
            if primary:
                first_filters.add(j)
        return first_filters
    
    def get_directs_infs(self, searched_filters):
        """Return directs infs of given j'"""
        direct_infs = set()
        for j in self.J:
            j_prime = self.get_J_prime(j)
            if j_prime > searched_filters:
                direct_infs_copy = copy(direct_infs)
                already_have_better_inf = False
                for inf in direct_infs_copy:
                    inf_prime = self.get_J_prime(inf)
                    if j_prime < inf_prime:
                        direct_infs.discard(inf)
                    elif j_prime > inf_prime:
                        already_have_better_inf = True
                        break
                if not already_have_better_inf:
                    direct_infs.add(j)
        return direct_infs
    
    def get_directs_sups(self, searched_filters):
        """Return directs sups of given j'"""
        direct_sups = set()
        for j in self.J:
            j_prime = self.get_J_prime(j)
            if j_prime < searched_filters:
                direct_sups_copy = copy(direct_sups)
                already_have_better_sup = False
                for sup in direct_sups_copy:
                    sup_prime = self.get_J_prime(sup)
                    if j_prime > sup_prime:
                        direct_sups.discard(sup)
                    elif j_prime < sup_prime:
                        already_have_better_sup = True
                if not already_have_better_sup:
                    direct_sups.add(j)
        return direct_sups
    
    def display(self):
        """Display the current context in the console"""
        print('-'*15)
        print(self.context_name)
        print('-'*5)
        matrix = self.to_string()
        print(matrix)
        print('-'*15)
        
    def to_string(self):
        """Return the matrix of the context"""
        result = ''
        for m in sorted(self.M):
            result += str(m)+'\t'
        result += '\n'
        for j in sorted(self.J):
            for m in sorted(self.M):
                if m in self.get_J_prime(j):
                    result += 'x'
                result += '\t'
            result += str(j)+'\n'
        return result
    
    def switch_debug(self, debug):
        self.debug = debug
        
    def export_json_for_latviz(self):
        """Export context in json forma for LatViz using"""
        print('Not yet implemented')
        
    def export_txt_for_conex(self, directory):
        """Export context in txt forma for LatViz using"""
        file = directory / 'conexp' / (self.context_name+'.txt')
        with file.open('w') as f:
        
            s = ''
            first = True
            for m in sorted(self.M):
                if not first:
                    s+= '\t'
                first = False
                s += m
            s += '\n\n'
            for j in sorted(self.J):
                first = True
                for m in sorted(self.M):
                    if not first:
                        s += '\t'
                    if m in self.get_J_prime(j):
                        s += '1'
                    else:
                        s += '0'
                    first = False
                s += '\n'
            f.write(s)