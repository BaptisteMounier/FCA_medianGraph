from copy import copy, deepcopy

class Context(object):
    '''
    classdocs
    '''
    
    custom = 'custom'
    standard = 'standard'
    extended = 'extended'
    distributive = 'extended'
    median = 'median'


    def __init__(self, context_name):
        '''
        Constructor
        '''
        
        self.context_name = context_name
        self.mode = Context.custom
        self.J = set()
        self.M = set()
        self.I = set()
        self.name_next_variable = 1
        
    def add_j(self, j):
        if j not in self.J:
            self.mode = Context.custom
            self.J.add(j)
        
    def add_m(self, m):
        if m not in self.M:
            self.mode = Context.custom
            self.M.add(m)
        
    def add_i(self, j, m):
        already_present = False
        for i in self.I:
            if i[0] == j:
                if i[1] == m:
                    already_present = True
        if not already_present:    
            self.add_j(j)
            self.add_m(m)
            self.I.add((j, m))
            self.mode = Context.custom
        
    def remove_j(self, j):
        if j in self.J:
            self.mode = Context.custom
            self.J.remove(j)
        
    def remove_m(self, m):
        if m in self.M:
            self.mode = Context.custom
            self.M.remove(m)
        
    def remove_i(self, j, m):
        for i in self.I:
            if i[0] == j:
                if i[1] == m:
                    self.mode = Context.custom
                    self.I.remove((j, m))
        
    def extend_j(self):
        
        self.mode = Context.custom
        
        # Check if the bot node exist in J, create it if not
        bot_already_exist = False
        for j in self.J:
            j_prime = self.get_j_prime(j)
            if j_prime == self.M:
                bot_already_exist = True
        if not bot_already_exist:
            bot = 'jBot'
            self.add_j(bot)
            for m in self.M:
                self.add_i(bot, m)
                
        # Check if the top node exist in J, create it if not
        top_already_exist = False
        for j in self.J:
            j_second = self.get_j_second(j)
            if not j_second:
                top_already_exist = True
            elif j_second == self.J:
                top_already_exist = True
        if not top_already_exist:
            top = 'jTop'
            for m in self.M:
                m_prime = self.get_m_prime(m)
                if m_prime == self.J:
                    self.add_i(top, m)
            self.add_j(top)
            
        # Extend all classics nodes
        modification = True
        while modification:
            modification = False
            J_copy = deepcopy(self.J)
            for j in J_copy:
                j_prime = self.get_j_prime(j)
                for k in J_copy:
                    k_prime = self.get_j_prime(k)
                    already_exists = False
                    if j != k:
                        intersection_jk = j_prime & k_prime
                        for l in self.J:
                            if intersection_jk == self.get_j_prime(l):
                                already_exists = True
                                break
                        if not already_exists:
                            modification = True
                            j_extended = 'e('+str(j)+str(k)+')'
                            self.add_j(j_extended)
                            for intersection in intersection_jk:
                                self.add_i(j_extended, intersection)
                                
        # Remane extended nodes
        modification = True
        while modification:
            modification = False
            J_copy = copy(self.J)
            for j in J_copy:
                if j not in self.J:
                    j_prime = self.get_j_prime(j)
                    infs = self.get_directs_j_infs(j_prime)
                    if infs:
                        min_label = 'z'
                        max_label = 'A'
                        for inf in infs:
                            if inf < min_label:
                                min_label = inf
                            if inf > max_label:
                                max_label = inf
                        new_name = 'e('+str(min_label)+str(max_label)+')'
                        if new_name != j:
                            modification = True
                            self.remove_j(j)
                            self.add_j(new_name)
                            I_copy = copy(self.I)
                            for i in I_copy:
                                if i[0] == j:
                                    self.remove_i(i[0], i[1])
                                    self.add_i(new_name, i[1])
        
    def extend_m(self):
        
        self.mode = Context.custom
        
        # Check if the top node exist in M, create it if not
        top_already_exist = False
        for m in self.M:
            m_prime = self.get_m_prime(m)
            if m_prime == self.J:
                top_already_exist = True
        if not top_already_exist:
            top = 'mTop'
            self.add_m(top)
            for j in self.J:
                self.add_i(j, top)
                
        # Check if the bot node exist in J, create it if not
        bot_already_exist = False
        for m in self.M:
            m_second = self.get_m_second(m)
            if not m_second:
                bot_already_exist = True
            elif m_second == self.M:
                bot_already_exist = True
        if not bot_already_exist:
            bot = 'MBot'
            for j in self.J:
                j_prime = self.get_j_prime(j)
                if j_prime == self.M:
                    self.add_i(j, bot)
            self.add_m(bot)
            
        # Extend all classics nodes
        modification = True
        while modification:
            modification = False
            M_copy = deepcopy(self.M)
            for m in M_copy:
                m_prime = self.get_m_prime(m)
                for k in M_copy:
                    k_prime = self.get_m_prime(k)
                    already_exists = False
                    if m != k:
                        intersection_mk = m_prime & k_prime
                        for l in self.M:
                            if intersection_mk == self.get_m_prime(l):
                                already_exists = True
                                break
                        if not already_exists:
                            modification = True
                            m_extended = 'e('+str(m)+str(k)+')'
                            self.add_m(m_extended)
                            for intersection in intersection_mk:
                                self.add_i(intersection, m_extended)
                                
        # Remane extended nodes
        modification = True
        while modification:
            modification = False
            M_copy = copy(self.M)
            for m in M_copy:
                if m not in self.M:
                    m_prime = self.get_m_prime(m)
                    infs = self.get_directs_m_infs(m_prime)
                    if infs:
                        min_label = 'z'
                        max_label = 'A'
                        for inf in infs:
                            if inf < min_label:
                                min_label = inf
                            if inf > max_label:
                                max_label = inf
                        new_name = 'e('+str(min_label)+str(max_label)+')'
                        if new_name != m:
                            modification = True
                            self.remove_m(m)
                            self.add_m(new_name)
                            I_copy = copy(self.I)
                            for i in I_copy:
                                if i[1] == m:
                                    self.remove_i(i[0], i[1])
                                    self.add_i(i[0], new_name)
            
    def get_j_prime(self, j):
        """Return j' set for a given j"""
        j_prime = set()
        for i in self.I:
            if i[0] == j:
                j_prime.add(i[1])
        return j_prime
        
    def get_m_prime(self, m):
        """Return m' set for a given m"""
        m_prime = set()
        for i in self.I:
            if i[1] == m:
                m_prime.add(i[0])
        return m_prime
        
    def get_j_second(self, j):
        """Return j'' set for a given j"""
        j_second = copy(self.J)
        j_prime = self.get_j_prime(j)
        for m in j_prime:
            j_second &= self.get_m_prime(m)
        return j_second
        
    def get_m_second(self, m):
        """Return m'' set for a given m"""
        m_second = copy(self.M)
        m_prime = self.get_m_prime(m)
        for j in m_prime:
            m_second &= self.get_j_prime(j)
        return m_second
        
    def get_atoms(self):
        """Return all atoms"""
        atoms = set()
        for j in self.J:
            primary = True
            j_prime = self.get_j_prime(j)
            for k in self.J:
                if j != k:
                    k_prime = self.get_j_prime(k)
                    if j_prime <= k_prime:
                        primary = False
                        break
            if primary:
                atoms.add(j)
        return atoms
        
    def get_irreductibles_infs(self, with_bot = True):
        """Return all irreductible j"""
        irreductibles_objects = set()
        for j in self.J:
            intersection = copy(self.M)
            already_equivalent = False
            bot = with_bot
            j_prime = self.get_j_prime(j)
            j_second = self.get_j_second(j)
            for k in j_second:
                k_prime = self.get_j_prime(k)
                if j_prime != k_prime:
                    intersection &= k_prime
                    bot = False
            for object_v in irreductibles_objects:
                if j_prime == self.get_j_prime(object_v):
                    already_equivalent = True
                    break
            if ((j_prime != intersection) or bot) and not already_equivalent:
                irreductibles_objects.add(j)
        return irreductibles_objects
        
    def get_irreductibles_sups(self, with_top = True):
        """Return all irreductible m"""
        irreductibles_attributes = set()
        for m in self.M:
            intersection = copy(self.J)
            already_equivalent = False
            top = with_top
            m_prime = self.get_m_prime(m)
            m_second = self.get_m_second(m)
            for k in m_second:
                kPrime = self.get_m_prime(k)
                if m_prime != kPrime:
                    intersection &= kPrime
                    top = False
            for attribute in irreductibles_attributes:
                if m_prime == self.get_m_prime(attribute):
                    already_equivalent = True
                    break
            if ((m_prime != intersection) or top) and not already_equivalent:
                irreductibles_attributes.add(m)
        return irreductibles_attributes
    
    def get_directs_j_infs(self, searched_filters):
        """Return directs infs of given j'"""
        direct_infs = set()
        for j in self.J:
            j_prime = self.get_j_prime(j)
            if j_prime > searched_filters:
                direct_infs_copy = copy(direct_infs)
                already_have_better_inf = False
                for inf in direct_infs_copy:
                    inf_prime = self.get_j_prime(inf)
                    if j_prime < inf_prime:
                        direct_infs.discard(inf)
                    elif j_prime > inf_prime:
                        already_have_better_inf = True
                        break
                if not already_have_better_inf:
                    direct_infs.add(j)
        return direct_infs
    
    def get_directs_j_sups(self, searched_filters):
        """Return directs sups of given j'"""
        direct_sups = set()
        for j in self.J:
            j_prime = self.get_j_prime(j)
            if j_prime < searched_filters:
                direct_sups_copy = copy(direct_sups)
                already_have_better_sup = False
                for sup in direct_sups_copy:
                    sup_prime = self.get_j_prime(sup)
                    if j_prime > sup_prime:
                        direct_sups.discard(sup)
                    elif j_prime < sup_prime:
                        already_have_better_sup = True
                if not already_have_better_sup:
                    direct_sups.add(j)
        return direct_sups
    
    def get_directs_m_infs(self, searched_ideals):
        """Return directs infs of given m'"""
        direct_infs = set()
        for m in self.M:
            m_prime = self.get_m_prime(m)
            if m_prime > searched_ideals:
                direct_infs_copy = copy(direct_infs)
                already_have_better_inf = False
                for inf in direct_infs_copy:
                    inf_prime = self.get_m_prime(inf)
                    if m_prime < inf_prime:
                        direct_infs.discard(inf)
                    elif m_prime > inf_prime:
                        already_have_better_inf = True
                        break
                if not already_have_better_inf:
                    direct_infs.add(m)
        return direct_infs
    
    def get_directs_m_sups(self, searched_filters):
        """Return directs sups of given m'"""
        direct_sups = set()
        for m in self.M:
            m_prime = self.get_m_prime(m)
            if m_prime < searched_filters:
                direct_sups_copy = copy(direct_sups)
                already_have_better_sup = False
                for sup in direct_sups_copy:
                    sup_prime = self.get_m_prime(sup)
                    if m_prime > sup_prime:
                        direct_sups.discard(sup)
                    elif m_prime < sup_prime:
                        already_have_better_sup = True
                if not already_have_better_sup:
                    direct_sups.add(m)
        return direct_sups
    
    def display(self):
        print('-'*15)
        print(self.context_name)
        print('-'*5)
        matrix = self.to_string()
        print(matrix)
#         print(self)
        print('-'*15)
        
    def to_string(self):
        """Return the matrix of the context"""
        result = ''
        for m in sorted(self.M):
            result += str(m)+'\t'
        result += '\n'
        for j in sorted(self.J):
            for m in sorted(self.M):
                if m in self.get_j_prime(j):
                    result += 'x'
                result += '\t'
            result += str(j)+'\n'
        return result
        
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
                    if m in self.get_j_prime(j):
                        s += '1'
                    else:
                        s += '0'
                    first = False
                s += '\n'
            f.write(s)