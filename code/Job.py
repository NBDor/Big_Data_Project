from Population import Population

class Job:
    """
    A class that represents a single task
    used to set population and GA paramaters,
    and run the evolution process
    ...

    Attributes
    ----------
    population_size : int
        desired number of chromosomes in population
        
    pop_select : float
        percent of population fittest selection
    
    pop_cross : float
        percent of population to be generated
        through selected parents crossover
    
    pop_mut : float
        probablitity of mutation 
        in the generated offspring generation
    
    pop_elite : float
        percent of fittest parents
        to be inserted into next generation
     
    cross_function : method
        crossover function for generated population
        
    mut_function : method
        mutation function for generated population
        
    adjacency_matrix: ndarray
        distance matrix of vertices
    """
        
    def __init__(self,
                 population_size,
                 pop_select,
                 pop_cross, 
                 pop_mut,   
                 pop_elite,
                 cross_function, 
                 mut_function,   
                 adjacency_matrix= None):
        
        self.pop_size = population_size
        self.pop_select = pop_select
        self.pop_cross = pop_cross
        self.pop_mut = pop_mut
        self.pop_elite = pop_elite
        self.cross_func = cross_function
        self.mut_func = mut_function
        self.adj_mat = adjacency_matrix
        
        self.history = None
        self.population = Population(self.pop_size,self.adj_mat)
        self.population.set_params(self.pop_select,
                                   self.pop_cross,
                                   self.pop_mut,
                                   self.pop_elite,
                                   self.cross_func,
                                   self.mut_func)
    
    def generate_population(self):
        """
        generate initial population
        """
              
        self.population.generate()
        return self

            
    def get_history(self):
        """
        returns last run results
        """
        
        return self.history   
    
    def get_optimum(self):
        """
        return optimal chromosome found in population
        and its fitness
        """
        
        c = self.population.get_best_chromosome()
        f = self.population.get_best_fitness()
        
        return c,f    
    
    def run(self,generations,verbose= False):
        """
        Run GA for specified iteration
        """
        
        self.history=[]
        p = self.population
        
        while True:
            if p.get_generation()>generations:
                break
        
            p.evolve()    
            if verbose:
                if not p.get_generation()%100:
                    print(f'gen {p.get_generation()}: path length:',p.get_best_fitness())
            self.history.append(p.get_best_fitness())     
        return self
    