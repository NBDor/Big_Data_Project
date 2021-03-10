import numpy as np
from random import sample

class Population:
    """
    A class used to represent a population of chromosomes
    each chromosome represents a possible path
    ...

    Attributes
    ----------
    population_size : int
        desired number of chromosomes in population
        
    population : list of chromosomes
        possible paths in current generation
        
    parents : list of chromosomes
        parent generation
        
    chromosome_len : int
        number of unique vertices in path
        
    adjacency_matrix: ndarray
        distance matrix of vertices
        
    generation: int
        current generation number
    """
    
    def __init__(self, pop_size, adj_mat):
        self.population_size = pop_size
        self.population = []
        self.parents = []
        self.generation = 0
        self.chromosome_len = adj_mat.shape[0]
        self.adjacency_matrix = adj_mat
        
        self.base = np.array([i+1 for i in range(self.chromosome_len)])
        
        
    def set_params(self,
                   pop_select,
                   pop_cross,
                   pop_mut,
                   pop_elite,
                   cross_func,
                   mut_func):
        """
        set population parameters and functions
        """
        
        self.pop_select = pop_select
        self.pop_cross = pop_cross
        self.pop_mut = pop_mut
        self.pop_elite = pop_elite
        self.crossover_func = cross_func
        self.mutation_func = mut_func
    
          
    def compute_fitness(self, chromosome):
        """
        compute chromosome fitness  
        """
        
        path_len = 0
        
        for i in range(self.chromosome_len-1):
            path_len+= self.adjacency_matrix[chromosome[i]-1][chromosome[i+1]-1]
            
        path_len+= self.adjacency_matrix[chromosome[i+1]-1][chromosome[0]-1]
        return path_len

    
    def get_best_fitness(self):
        """
        return best fitness in population
        """
        if len(self.population)==0:
            return -1
        
        c = min(self.population, key=self.compute_fitness)
        return self.compute_fitness(c)

    
    def get_best_chromosome(self):
        """
        return best chromosome in population
        """
        if len(self.population)==0:
            return []
        
        c = min(self.population, key=self.compute_fitness)
        return c
    
    
    def add_chromosome(self, chromosome):
        """
        add chromosome to population
        """
        
        self.population.append(chromosome)
    
    
    def generate(self):
        """
        generate population
        """
        
        self.kill()
        
        for i in range(self.population_size):
            c = self.base.copy()
            np.random.shuffle(c)
            self.add_chromosome(c)
    
    
    def kill(self):
        """
        kill current population
        """
        
        self.population = []
        self.parents = []
        self.generation = 0
            
            
    def get_population(self):
        """
        return population
        """
        
        return self.population
    

    def get_parent_population(self):
        """
        return parent population
        """
        
        return self.parents
    
    
    def get_generation(self):
        """
        return current generation number
        """
        
        return self.generation
    
    
    def size(self):
        """
        get current size of population
        """
        
        return len(self.population)
    
    
    def max_size(self):
        """
        get max size of population
        """
        
        return self.population_size
    
    
    def pool(self, other_pop):
        """
        combine current population with another
        select best chromosomes from each
        """
        
        p1 = np.copy(self.get_population)
        p2 = np.copy(other_pop.get_population)
        
        p1 = sorted(p1, key=self.compute_fitness)
        p1 = sorted(p2, key=self.compute_fitness)

        self.kill()
        
        j1=j2=0
        
        for i in range(self.population_size):
            if self.compute_fitness(po1[j1])<self.compute_fitness(po2[j2]):
                self.population[i] = p1[j1]
                j1+=1
            else:
                self.population[i] = p2[j2]
                j2+=1
        
        
    def selection(self):
        """
        Roulette Wheel Selection
        Select parents to be used in later crossover
        """
        
        probability = np.empty(self.size())
        sum_of_fitness = 0 
        sum_of_probabilities = 0
        self.parents = []

        for c in self.population:
            sum_of_fitness+= self.compute_fitness(c)

        for i,c in enumerate(self.population):
            sum_of_probabilities = probability[i] = sum_of_probabilities + self.compute_fitness(c)/sum_of_fitness

        while len(self.parents) < (self.max_size()*self.pop_select) :
            rand = np.random.random()
            for i,c in enumerate(self.population):
                if rand > probability[i] and rand < probability[i+1]:
                    self.parents.append(c)
                    break

                    
    def crossover(self):
        """
        Generate offpsring through parent crossover
        """
        
        new_population =[]

        while len(new_population) < (self.max_size()*self.pop_cross):
            p1,p2 = sample(self.parents,2)
            new_population.extend(self.crossover_func(p1,p2,self.chromosome_len))
            
        self.parents = self.population
        self.population = new_population
        
    
    def mutate(self):          
        """
        Introduce low chance of mutation in current population
        Used to maintain genetic diversity, prevents local minima convergence
        """
        
        for c in self.population:
            rand = np.random.random()
            if rand < self.pop_mut:
                self.mutation_func(c,self.chromosome_len)

                
    def insert_elite(self):
        """
        Retain elite chromosomes from parent generation
        Ensures fitness monotonicity 
        """
        
        elite_pop = []
        pop = sorted(self.parents, key=self.compute_fitness)

        i=0
        while len(elite_pop) < (self.max_size()*self.pop_elite):
            elite_pop.append(pop[i])
            i+=1

        self.population.extend(elite_pop)
        
        
    def evolve(self):
        """
        generate next generation population
        """
        
        self.selection()
        self.crossover()
        self.mutate()
        self.insert_elite()
        self.generation+=1
        