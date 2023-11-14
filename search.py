import os
import json
import copy
import time
import base64
import struct
import random
import traceback
from bitarray import bitarray
from datetime import datetime
from itertools import combinations
from tcl_helper import get_scores, run_tcl, build_rtl, create_files

POP_N = 30                          # number of individuals in population
BST_N = 17                          # number of best individuals to select
CLD_N = 10                          # number of children to make
GEN_N = 100                         # max number of generations allowed
REP_N = 3                           # max number of consecutive generations with the same score
REP_E = 0.001                       # epsilon threshold such that two floating scores are considered equal
MUT_P = 0.07                        # probability of mutation
MAX_PROC = 5                        # max number of processes to run
random.seed(17)

COMBINATION_SEL = 0                 # switch to select combination type: 0 numerical, 1 linear, 2 binary
SELECTOR_SEL = 0                    # switch to select selector type: 0 tournament, 1 roulette
MUTATOR_SEL = 1                     # switch to select mutator type: 0 general, 1 binary

VAR_N = 39                          # number of variables per individual
VAR_D = ['full_adder',              # domain of each variable
         'full_adder_I',
         'full_adder_II',
         'full_adder_III'] + ['full_adder_'+str(i) for i in range(1,29)]
BIT_W = 5                           # number of possible variables bit width (e.g. 32 possible = 5 bits) 
INP_W = 8                           # input number bit width

TCL_DEBUG = False                   # set to true if you want TCL script output
EVL_DEBUG = False                   # set to true if you want evolution debug output

OUT_FILE = '8x8_runs.txt'           # output file name

score_proc = []

def assert_const():
    """Asserts that constant parameters for evolutionary algorithm are valid.

        Args:
            None

        Returns:
            None
    """
    if(BST_N == 0 or POP_N == 0):
        print("Constants ERROR, zero population or best individuals in constants (POP_N,BST_N)!")
        exit()
    if(BST_N > POP_N):
        print("Constants ERROR, best individuals more than population in constants (POP_N,BST_N)!")
        exit()
    if(CLD_N > BST_N*(BST_N-1)):
        print("Constants ERROR, new children more than what can be produced, BST_N*(BST_N-1) is max (BST_N,CLD_N)!")
        exit()
    return

class individual:

    def __init__(self, initial_vals):
        """Initializes an individual object.

        Args:
            self (individual): self
            initial_score (int): precalculated score for this individual
            initial_vals (list of ints): initial values for the variables

        Returns:
            None
        """
        if(initial_vals == None):
            self.rand_init()
        else:
            self.vars = initial_vals
        self.score = 100000
        self.mse = -1
        self.util = -1
        self.time = -1
        self.power = -1
        return
    
    def rand_init(self):
        """Initializes an individual's variables to random values.

        Args:
            self (individual): self

        Returns:
            None
        """
        self.vars = []
        for i in range(VAR_N):
            self.vars.append(random.randint(0,len(VAR_D)-1))
        return

    def name(self):
        """Returns an individual's name based on it's variable values.

        Args:
            self (individual): self

        Returns:
            name(str): the individual's name
        """
        name = ''
        for var in self.vars[:-1]:
            name += str(var) + '.'
        name += str(self.vars[-1])
        return name

    def short_name(self):
        """Returns an individual's hex name based on it's variable values.

        Args:
            self (individual): self

        Returns:
            number(str): the individual's hex name
        """
        number = self.number()
        return hex(number)[2:]

    def shorter_name(self):
        """Returns an individual's base 64 name based on it's variable values.

        Args:
            self (individual): self

        Returns:
            number(str): the individual's b64 name
        """
        number = self.number()
        num_bytes = number.to_bytes(length=25, byteorder='big')
        enc_bytes = base64.b64encode(num_bytes)
        return str(enc_bytes)[2:-1]

    def number(self):
        """Returns an individual's hash number based on it's variable values.

        Args:
            self (individual): self

        Returns:
            hash(int): the individual's hash
        """
        binary = ''
        for var in self.vars:
            binary += get_binary(var)
        hash = int(binary, base=2)
        return hash

    def report(self):
        """Returns a string reporting the individual's performance in simulation.

        Args:
            self (individual): self

        Returns:
            print_out(str): the individual's report
        """
        print_out = 'MSE = ' + str(self.mse) + '\n'
        print_out += 'util = '+ str(self.util[0]) + ' LUTs, ' + str(self.util[1]) + ' registers\n'
        print_out += 'timing = (WNS) '+ str(self.time[0]) + 'ns, (WHS) ' + str(self.time[1]) + 'ns, (WPWS) ' + str(self.time[2]) + 'ns\n'
        print_out += 'power = '+ str(self.power) + 'W\n'
        return print_out

    def __str__(self):
        """Returns the individual's string descriptor.

        Args:
            self (individual): self

        Returns:
            print_out (str): object as str
        """
        print_out = "Individual " + self.name() + '\n'
        print_out += 'Score = ' + str(self.score) + '\n'
        print_out += 'Report:\n' + self.report()
        return print_out 

NORMAL_MULT = individual([0 for i in range(VAR_N)])
_norm = []
for i in range(2**INP_W):
    for j in range(2**INP_W):
        _norm.append(i*j)

###############################################################################################################################
################################################ Watch out this is arbitrary ! ################################################
NORMAL_OUT = (_norm, [77, 41], [2.969, 0.123, 2.225], 0.653)
###############################################################################################################################
###############################################################################################################################

def MSE(L1, L2):
    """Calculates the mean squared error in between two lists.

        Args:
            L1 (list of mubers): list 1
            L2 (list of mubers): list 2

        Returns:
            mse (float): mean squared error
    """
    mse = 0
    if(len(L1) != len(L2)):
        print('MSE ERROR, lists of different length')
        exit()
    for i,j in zip(L1, L2):
        error = i - j
        mse += error*error
    return mse/len(L1)

def run_individual(A:individual):
    """Runs simulation and synthesis for an individual A.
    Adds it to score_proc list.

        Args:
            A (individual): an individual

        Returns:
            None
    """
    global score_proc, TCL_DEBUG

    name = A.short_name()
    if(not name in highscore_entries):                      # check if already ran
        if(TCL_DEBUG):
            print('creating files for ', name)
        create_files(name)                                  # create the files
        if(TCL_DEBUG):
            print('creating RTL for ', name)
        build_rtl(name, [VAR_D[i] for i in A.vars])         # edit rtl
        if(TCL_DEBUG):
            print('running ', name)
        p = run_tcl(name, TCL_DEBUG)                        # run individual
        score_proc.append(p)                                # add to process list
    return

def formula(mse, lut, reg, wns):
    """Score formula for an individual. Subject to change

        Args:
            mse (int): mse for formula
            lut (int): lut for formula
            reg (int): reg for formula
            wns (float): wns for formula

        Returns:
            score (float): score calculated from formula
    """
    score = mse/1500 + lut*100/3 
    return score

def score(A:individual):
    """Calculates the score for an individual A.

        Args:
            A (individual): an individual

        Returns:
            None
    """
    name = A.short_name()
    if(name in highscore_entries):                                                                  # if individual already in database
        existing = highscore_entries[name]                                                          # load it
        A.mse = existing.mse                                                                        # copy the values
        A.util = existing.util
        A.time = existing.time
        A.power = existing.power
        score = formula(A.mse, A.util[0], A.util[1], A.time[0])                                     # recalculate score (incase formula has changed since last access)
        A.score = existing.score = score
    else:                                                                                           # else calculate values from simulation files
        norm_out = NORMAL_OUT[0]
        A_out = get_scores(name)
        mse = MSE(norm_out, A_out[0])
        A.mse = mse
        A.util = A_out[1]
        A.time = A_out[2]
        A.power = A_out[3]
        score = formula(A.mse, A.util[0], A.util[1], A.time[0])
        A.score = score
        highscore_entries[name] = A                                                                 # and add to the database
    return

def wait_runs():
    """Waits for all processes in score_proc to finish.

        Args:
            None

        Returns:
            None
    """
    global score_proc
    if(len(score_proc)>0):
        print('Waiting for',len(score_proc), 'runs...')
    while(len(score_proc) > 0):                                 # wait for all subprocesses to finish
        proc = score_proc.pop()
        proc.wait(timeout=900)
    return

def run_population(population):
    """Runs the simulation for all individuals in input population.

        Args:
            population (list of individuals): the individuals to run

        Returns:
            None
    """
    marked = []
    for indiv in population:
        if(indiv.short_name() not in marked):                           # skip any duplicates
            run_individual(indiv)                                       # launches one subprocess for each individual in group
            marked.append(indiv.short_name())
            wait_runs()
    # since while above proceeds only if last group has finished we don't need to wait again
    for indiv in population:                                            # update scores of all individuals in population
        score(indiv)
    store_entries(highscore_entries)                                    # store calculated socres
    return

def run_population_parallel(population):
    """Runs the simulation for all individuals in input population in parallel.

        Args:
            population (list of individuals): the individuals to run

        Returns:
            None
    """
    completed = 0
    marked = []
    while(completed < len(population)):                                 # run individuals  !! SLOW !!
        i = 0
        running = 0
        while(running < MAX_PROC):                                      # slices list in groups of MAX_PROC individuals
            j = i+completed                                             # index of current individual in population
            if(j >= len(population)):                                   # if out of bounds we are done
                break
            if(population[j].short_name() not in marked):                     # skip any duplicates
                run_individual(population[j])                           # launches one subprocess for each individual in group
                marked.append(population[j].short_name())
                running +=1
            i += 1
        wait_runs()                                                     # wait for all subprocesses in group to finish
        completed += MAX_PROC                                           # proceed with next group
    # since while above proceeds only if last group has finished we don't need to wait again
    for indiv in population:                                            # update scores of all individuals in population
        score(indiv)

    store_entries(highscore_entries)                                    # store calculated socres
    return

def tournament_selector(population):
    """Selects the best individuals from the population, based on tournament selection.

        Args:
            population (list of individuals): the population

        Returns:
            top (list of individual): selected individuals
    """
    top = []
    SAMPLES = int(POP_N/5)                                          # arbitrary, get a fifth of samples for each tournament
    for _ in range(BST_N):
        pop_sample = random.sample(population, SAMPLES)
        top.append(min(pop_sample, key=lambda x: x.score))
    top.sort(key=lambda x: x.score)                                 # sort top by score
    return top

def roulette_selector(population):
    """Selects the best individuals from the population, based on roulette selection.

        Args:
            population (list of individuals): the population

        Returns:
            top (list of individual): selected individuals
    """
    top = []
    scores = [indiv.score for indiv in population]                      # roulette can not be created with negative scores
    offset = min(scores)                                                # we need to find the minimum negative score
    if(offset > 0):                                                     # if offset is 0 we don't care
        offset = 0
    roulette = [population[0].score - offset]                           # create the roullete
    for i in range(1,len(population)):                                  # and increase everyone by abs(offset) to normalize
        roulette.append(population[i].score + roulette[i-1] - offset)
    for _ in range(BST_N):                                              # select individuals based on the roullete
        rand = random.uniform(0,roulette[-1])
        for j,score in enumerate(roulette):
            if(rand<=score):
                top.append(population[j])
                break
    top.sort(key=lambda x: x.score)                                     # sort top by score    
    return top

def gene_combinator(A:individual, B:individual):
    """Combines individuals A and B, based on numerical combination method.
        Works like binary but selects entire variable values instead of bits

        Args:
            A (individual): first individual
            B (individual): second individual

        Returns:
            [C1,C2] (list of individuals): two new children
    """
    mask = []
    for i in range(VAR_N):
        mask.append(random.choice([True,False]))
    
    child_vars_1 = []
    child_vars_2 = []
    for i,choice in enumerate(mask):
        if choice:
            child_vars_1.append(A.vars[i])
            child_vars_2.append(B.vars[i])
        else:
            child_vars_1.append(B.vars[i])
            child_vars_2.append(A.vars[i])
    
    C1 = individual(child_vars_1)
    C2 = individual(child_vars_2)
    return [C1,C2]

def linear_combinator(A:individual, B:individual):
    """Combines individuals A and B, based on linear combination method.
        linearly combines A's and B's variables based on random weights.

        Args:
            A (individual): first individual
            B (individual): second individual

        Returns:
            [C1,C2] (list of individuals): two new children
    """
    frac = []
    for i in range(VAR_N):
        frac.append(random.uniform(0.,1.))
    
    child_vars_1 = []
    child_vars_2 = []
    for i,choice in enumerate(frac):
        child_vars_1.append(int(choice*A.vars[i] + (1-choice)*B.vars[i]))
        child_vars_2.append(int((1-choice)*A.vars[i] + choice*B.vars[i]))

    C1 = individual(child_vars_1)
    C2 = individual(child_vars_2)
    return [C1,C2]

def get_binary(a:int):
    """Creates a binary string of length BIT_W with the bits of a

        Args:
            a (int): a number to conver to binary

        Returns:
            bits (str): the bits of a
    """
    enc_bits = bitarray(endian='little')            # get a bitarray object
    enc_bytes = struct.pack('i', a)                 # get bytes of number
    enc_bits.frombytes(enc_bytes)                   # get bitarray from bytes
    return enc_bits[0:BIT_W].to01()[::-1]           # export bits as string, sliced down to BIT_W and reversed

def get_ints(s:str):
    """Returns a list of ints from a binary string.

        Args:
            s (str): a binary string of length BIT_W*k

        Returns:
            vars (list of ints): the ints that correspond to every BIT_W bits of input
    """
    vars = []
    for i in range(BIT_W, len(s)+1, BIT_W):         # for every BIT_W bits
        vars.append(int(s[i-BIT_W:i],base=2))       # put the int that corresponds to them in list
    return vars

def binary_combinator(A:individual, B:individual):
    """Combines individuals A and B, based on binary combination method.

        Args:
            A (individual): first individual
            B (individual): second individual

        Returns:
            [C1,C2] (list of individuals): two new children
    """
    A_bits = B_bits = ''
    for var_A,var_B in zip(A.vars, B.vars):
        A_bits += get_binary(var_A)
        B_bits += get_binary(var_B)

    mask = []
    for i in range(len(A_bits)):
        mask.append(random.choice([True,False]))

    child_bits_1 = ''
    child_bits_2 = ''
    for i,choice in enumerate(mask):
        if choice:
            child_bits_1 += A_bits[i]
            child_bits_2 += B_bits[i]
        else:
            child_bits_1 += B_bits[i]
            child_bits_2 += A_bits[i]
    
    C1 = individual(get_ints(child_bits_1))
    C2 = individual(get_ints(child_bits_2))

    return [C1,C2]

def mate(top):
    """Combines top individuals to produce a specified number of children.

        Args:
            top (list of individuals): individuals to be mate (expected sorted)

        Returns:
            children (list of individuals): new children generated
    """
    children = []
    comb = list(combinations([x for x in range(len(top))], 2))      # these are the total possible ways to combine the individuals of input
    skipped = []                                                    # list of skipped combinations
    for i in range(len(comb)):                                      # limit those to the total number of childern we asked for
        idx_A = comb[i][0]                                          # creating two children per loop
        idx_B = comb[i][1]
        if(top[idx_A].short_name() == top[idx_B].short_name()):     # if they are the same individuals skip this combination
            skipped.append(comb[i])
            continue
        C = combine(top[idx_A],top[idx_B])                          # combine the children
        children.append(C[0])                                       # and add them to the list
        children.append(C[1])
        if(len(children)>=CLD_N):
            break
    i = 0
    while(len(children)<CLD_N):                                     # still need more children ?                        
        idx_A = skipped[i][0]                                       # creating using the skipped combinations now
        children.append(top[idx_A])                                 # since in this combination the parents are the same
        children.append(top[idx_A])                                 # both children will be the same as the parent
        i += 1

    return children[:CLD_N]                                         # if the number of children is odd, ditch the last child

def check_diversity(population):
    """Checks if population is diverse enough. That is it does not contain
        more than <thres> copies of the same individual. In this case
        thres = 1/3 of the population.

        Args:
            population (list of individuals): population to check

        Returns:
            diverse? (boolean): True if diverse, False if not
    """
    thres = int(POP_N/3)
    for i, ind_A in enumerate(population):
        repeats = 0
        for ind_B  in population[i+1:]:
            if(ind_A.short_name() == ind_B.short_name()):
                repeats += 1
                if(repeats > thres):
                    break
        if(repeats > thres):
            return True
    return False

def binary_mutation(A:individual):
    """Mutates individual A using binary mutation. Inveses one bit of A.

        Args:
            A (individual): individual to be mutated

        Returns:
            new_indiv (individual): mutated individual
    """
    A_bits = ''
    for var_A in A.vars:
        A_bits += get_binary(var_A)
    
    curr_idx = random.randrange(0,len(A_bits))                                              # select index of bit to mutate
    new_bit = '1' if A_bits[curr_idx]=='0' else '0'                                         # inverse that bit
    A_bits = A_bits[:curr_idx] + new_bit + A_bits[curr_idx+1:]
    new_indiv = individual(get_ints(A_bits))

    return new_indiv

def mutation(A:individual):
    """Mutates a variable of individual A replacing it with another value at random.

        Args:
            A (individual): individual to be mutated

        Returns:
            new_indiv (individual): mutated individual
    """
    curr_idx = random.randrange(0,VAR_N)                                                    # select index of gene/variable to mutate
    mut_gene = A.vars[curr_idx]                                                             # value of selected gene
    avail_genes = [0 if i==mut_gene else 1 for i in range(len(VAR_D))]                      # mask of genes, with a 0 at curr_idx
    new_gene = random.choices([i for i in range(len(VAR_D))], weights = avail_genes)[0]     # select a new value for this gene, previous not included
    new_vars = copy.deepcopy(A.vars)                                                        # replace the value
    new_vars[curr_idx] = new_gene                                                           # make new individual with new values
    new_indiv = individual(new_vars)
    return new_indiv

def create_init():
    """Creates an initial population of individuals.

        Args:
            None

        Returns:
            population (list of individuals): generated initial population
    """
    global EVL_DEBUG

    print('Creating initial population...')
    population = []
    for i in range(POP_N):                                          # initialize individuals and run them  !! SLOW !!
        population.append(individual(None))   

    t = time.time()

    run_population_parallel(population)

    t = time.time() - t
    print('(in',t,'seconds)')

    if(EVL_DEBUG):
        print('initial population:')
        for i in population:
            print(i.short_name())

    return population

def search(population):
    """Searches the search space and returns the best individual.

        Args:
            population (list of individuals): initial population for search

        Returns:
            solution (individual): best solution found
    """
    global EVL_DEBUG, MUT_P, GEN_N, REP_N

    print('\nSearching...')
    score_stats = []
    min_score = 1000000                                                     # max score of all generations
    best_indiv = None                                                       # best individual of all generations
    previous_min = min_score                                                # min score of all individuals in previous generation
    repeats = 0                                                             # number of repeats of the same score in consecutive generations
    generation = 1                                                          # number of generations processed

    while(generation<=GEN_N and repeats<REP_N):
        print('\nGeneration:', generation, '/', GEN_N)
        # Update Max Score
        current_min = 1000000                                               # max score of all individuals in this generation
        best_current = population[0]                                        # best individual for this generation
        for indiv in population:
            if(indiv.score < current_min):                                  # calculate max score for this generation
                current_min = indiv.score
                best_current = indiv
        if(current_min < min_score):                                        # update best of all generations
            min_score = current_min
            best_indiv = best_current
        
        # Selection
        top = select(population)                                            # select top individuals
        if(EVL_DEBUG):
            print('selected:')
            for i in top:
                print(i.short_name())

        # Combination
        children = mate(top)                                                # make new chidren
        run_population_parallel(children)                                            # find their scores
        if(EVL_DEBUG):
            print('new children:')
            for i in children:
                print(i.short_name())
        population += children                                              # add children to population

        # Mutation
        mutated = []
        old = []
        if(check_diversity(population)):                                    # if too many are the same, increase mutation probability
            MUT_P = 0.3
        for i,indiv in enumerate(population):                               # iterate for mutation
            if(random.random()<MUT_P):
                new_indiv = mutate(indiv)                                   # mutate individuals
                if(EVL_DEBUG):
                    print('mutated:', indiv.short_name(), '->', new_indiv.short_name())
                mutated.append(new_indiv)                                   # create new mutated individual
                old.append(i)
        run_population_parallel(mutated)                                             # find the new individuals' scores
        wait_runs()
        for i,new_indiv in zip(old,mutated):                                # swap new individuals with old ones
            population.pop(i)                                               # remove old one
            population.append(new_indiv)                                    # add new
            highscore_entries[new_indiv.short_name()] = new_indiv
        if(MUT_P == 0.3):                                                   # reset mutation probability if increased
            MUT_P = 0.07
        
        # New population
        population.sort(key=lambda x: x.score)                              # sort population top by score
        population = population[0:POP_N]                                    # keep best
        if(EVL_DEBUG):
            print('new population:')
            for i in population:
                print(i.short_name())

        # Evolution control
        generation += 1                                                     # increment generation counter
        if(abs(current_min - previous_min) <= REP_E):                       # count repeats
            repeats += 1
        else:
            repeats = 0
        previous_min = current_min                                          # update previous minimum
        score_stats.append(current_min)                                     # add current_min to evolution stats
        print('\tscore = ', current_min)

    return best_indiv, score_stats

def load_entries(FILE = 'highscores.json'):
    """Loads previously calculated scores and simulation values.

        Args:
            FILE (str): json filename of database

        Returns:
            highscore_entries (dict of individuals): loaded values and scores
    """
    highscore_entries = {}
    if(os.path.exists(os.path.join(os.getcwd(), FILE))):
        with open(FILE, 'r') as json_file:                              # load json db
            json_object = json.load(json_file)
            json_file.close()
            for id in json_object:                                      # for every object in db
                raw_entry = json_object[id]                             
                indiv = individual(raw_entry['solution'])               # make a new individual with those values
                indiv.score = raw_entry['score']
                indiv.mse = raw_entry['mse']
                indiv.util = raw_entry['util']
                indiv.time = raw_entry['time']
                indiv.power = raw_entry['power']
                highscore_entries[indiv.short_name()] = indiv                 # add it to dict
                #date = datetime.strptime(raw_entry['date'], '%Y-%m-%d %H:%M:%S.%f')
        json_file.close()    
    return highscore_entries

def store_entries(highscore_entries, FILE = 'highscores.json'):
    """Stores calculated scores and simulation values.

        Args:
            highscore_entries (dict of individuals): loaded values and scores
            FILE (str): json filename of database

        Returns:
            None
    """

    entr_dict = {}
    for name in highscore_entries:                          # for every calculated individual
        ent = highscore_entries[name]                       # add it to the entry dictionary
        entr_dict[name] = {'solution' : ent.vars, 
                           'score' : ent.score, 
                           'mse' : ent.mse,
                           'util' : ent.util, 
                           'time' : ent.time, 
                           'power' : ent.power}
    json_object = json.dumps(entr_dict, indent = 4)         # dump the entry dictionary into the json file
    with open(FILE, 'w') as json_file:
        json_file.write(json_object)
        json_file.close()
    return

def run_search(run_file, id):
    """A wrapper function for search. Creates an initial population, prints information on console,
        prints output in <run_file> and handles exceptions.

        Args:
            run_file (file): file handle to print output to
            id (any): id for this run

        Returns:
            None
    """
    global score_proc, combine, select, mutate, COMBINATION_SEL, SELECTOR_SEL, MUTATOR_SEL, TCL_DEBUG, EVL_DEBUG

    assert_const()                                                          # assert constants

    run_file.write('Run ' + str(id) + '#############################################################################\n')

    print('####################################################################################################################################')
    combine = gene_combinator                                               # set combinator
    if(COMBINATION_SEL == 1):
        combine = linear_combinator
    elif(COMBINATION_SEL == 2 ):
        combine = binary_combinator
    select = tournament_selector                                            # set selector
    if(SELECTOR_SEL == 1):
        select = roulette_selector
    mutate = binary_mutation
    if(MUTATOR_SEL == 1):
        mutate = mutation

    print('combinator:', combine.__name__, ', selector:', select.__name__, ', mutator:', mutate.__name__,'\n')

    population = create_init()
    try:
        solution, stats = search(population)                                # start searching
        print('\nSolution:')
        print(solution)

        run_file.write('\nSolution:' + str(solution) + '\n')

        print('Score evolution:')
        print(stats)

        run_file.write('\nScore evolution:' + str(stats) + '\n\n')
    except Exception as e:
        print(traceback.format_exc())
        print('Search failed:', str(e))
        run_file.write('\n' + traceback.format_exc())
        run_file.write('\nSearch failed:' + str(e) + '\n')
        for p in score_proc:
            p.kill()

    print('\n' + str(datetime.now()))
    print('####################################################################################################################################')
    return

def get_solutions(FILE = '8x8_runs.txt'):
    """Gets the solutions from the <run_search> generated output file.

        Args:
            FILE (file): file including the solutions from multiple runs

        Returns:
            solutions (list of str): the names of the idividuals that were in FILE in str form
            stats (list of list of float): the best scores recorded per generation per run
    """
    solutions = []
    stats = []
    if(os.path.exists(os.path.join(os.getcwd(), FILE))):
        with open(FILE, 'r') as sol_file:
            lines = sol_file.readlines()
            sol_file.close()
        for i in range(len(lines)):
            line = lines[i]
            if(line.startswith('Solution:Individual')):
                space = line.index(' ')
                name = line[space+1:].strip()
                solutions.append(name)
            if(line.startswith('Score evolution:')):
                list_str = line[line.index('[')+1 : line.index(']')].strip()
                stat = [float(x) for x in list_str.split(', ')]
                stats.append(stat)
    return solutions, stats

def run_static(IUT):
    """Runs specific individuals in IUT. This will evaluate the individuals in IUT and update the
        <highscore_entries> and highscores.json with their results. Nothing is returned.

        Args:
            IUT (list of individuals): individuals under testing

        Returns:
            None
    """
    global score_proc, VAR_D, VAR_N

    try:
        run_population_parallel(IUT)
        for i in IUT:
            print(i)
    except Exception as e:
        print(traceback.format_exc())
        print('Search failed:', str(e))
        for p in score_proc:
            p.kill()

    return

############################################## Main ###############################################
if __name__ == '__main__':
    
    highscore_entries = load_entries()

    print(datetime.now(),'\n')
    
    for i in range(1000):
        with open(OUT_FILE,'a') as run_file:
            run_search(run_file, i)
            run_file.close()
