# AxC-8bit-Multiplier-Research

In this repository we publish the code used to run the Genetic Algorithm experiments for our paper:<br>
**Design space exploration of partial product reduction stage on 8x8 approximate multipliers**<br>
Published at [ieeexplore](https://ieeexplore.ieee.org/abstract/document/10497018). Presented at the 7th PAnhellenic Conference on Electronics and Telecommunications (PACET 2024).

Repository Authors:
- Ioannis Rizos
- Georgios Papatheodorou

**For any questions please create an Issue within this repository.**<br>
**There is a more advanced version of this pipeline [here](https://github.com/jrizxos/Approximate-Reduced-Complexity-Wallace-Multipliers).**

---

## Study Results

Using the code in this repository we succeeded in reducing the area of the wallace multiplier, by adding approximation, by 46% (E and F in figure below).
We also achieve a far more accurate result (still approximate) at 74% of the original area (G and H). More information in our paper.<br>
![bar graph](images/bar_graph.png)<br>

---

## Requirements

To run our code you need [Python](https://www.python.org/downloads/) installed with the [bitarray](https://pypi.org/project/bitarray/) library.
For VHDL simulation, synthesis and implementation we use [Xilinx Vivado](https://www.xilinx.com/support/university/vivado.html), it needs to be installed in your system.
We tested this program with **Python 3.10.12** and **Vivado v2021.1.1 (64-bit)** on **Ubuntu 22.04.2 LTS**.

---

## File Structure

```
├── 8x8_runs.txt                     	(search.py text output file)
├── highscores.json                  	(database for archived individuals)
├── search.py                        	(**main** search program)
├── tcl_helper.py                    	(helper functions for use of Vivado)
├── utilities.py                     	(some utilities to handle the study of produced data)
└── tcl_work_dir                     	(work directory for simulation, synthesis and implementation)
	├── constraints                  	(Vivado project constraints)
	│   └── Constraints_1.xdc
	├── main.tcl                     	(main script run by Vivado to conduct simulation-synthesis-implementation)
	├── tb                           	(VHDL testbench directory)
	│   ├── main_tb.vhd
	│   └── tb_wallace_test.vhd
	├── tcl_out                      	(Vivado report output directory)
	├── temp                         	(temporary Vivado project generation directory, safe to delete contents)
	└── vhdl                         	(Multiplier VHDL code directory)
    	├── axc_wallace.vhd
    	├── ...
    	└── wallace.vhd
```

---

## Code Usage

The main entry point for this program is **search.py**. Invoking this program is done with
```
> python search.py
```
in the root directory. This will start the GA which will do 1000 search runs by default.
While running the program will display some progress information in the console and at
the same time store critical run results in 8x8_runs.txt. Any individuals evaluated with
Vivado are stored inside *highscores.json*. Vivado will generate files inside the folders
*tcl_work_dir/tcl_out* and *tcl_work_dir/temp* during runtime. Any files inside *temp*
can safely be deleted after the program finishes running. Files inside *tcl_out* could
contain useful information that is not stored in *highscores.json*, specifically files
with *_out.rpt* suffix. The rest of *tcl_work_dir* contains files for running Vivado and
our VHDL code for the 8x8 Multiplier.

Some utilities for inspecting the results generated by search are included in **utilities.py**.
There is no command line interface for them, they need to be called from python code. Also
**search.py** contains the **run_static()** method which allows the user to evaluate some
specific individuals without running the genetic algorithm.

---

## Code Diagram

![code diagram](images/program_diagram.png)

---

## Code Configuration

- Inside **search.py** the following program parameters may be set:
  - **MAX_PROC**: sets the number of maximum parallel Vivado processes called by search.
  - **random.seed()**: set a seed in order to get the same results each time.
  - **TCL_DEBUG**: (True/False) whether or not to print debug info from Vivado commands.
  - **EVL_DEBUG**: (True/False) whether or not to print debug info from this program.
  - **OUT_FILE**: name for the output file.
- Inside **search.py** the following genetic algorithm parameters may be set:
  - **POP_N**: number of individuals in the population.
  - **BST_N**: number of best individuals to select.
  - **CLD_N**: number of children to make each generation.
  - **GEN_N**: max number of generations allowed per run.
  - **REP_N**: max number of consecutive generations with the same score.
  - **REP_E**: epsilon threshold such that two floating scores are considered equal.
  - **MUT_P**: probability of mutation.
  - **COMBINATION_SEL**: switch to select combination type: 0 numerical, 1 linear, 2 binary.
  - **SELECTOR_SEL**: switch to select selector type: 0 tournament, 1 roulette.
  - **MUTATOR_SEL**: switch to select mutator type: 0 general, 1 binary.
  - **VAR_N**: number of variables per individual.
  - **VAR_D**: domain of each variable.
  - **BIT_W**: number of possible variables bit width (e.g. length of VAR_D 32 : BIT_W = 5 bits).
  - **INP_W**: input number bit width (used only for MSE calculation).
 - Inside **tcl_work_dir/main.tcl** the following Vivado parameters may be set:
   - **set_param general.maxThreads**: maximum threads used by Vivado (tip: set to number of logical processors on your system).
   - **create_project -part**: ⚠️***Very important***⚠️ You might want to change the part identifier to an FPGA part for which you own the license,
 	Vivado will refuse to synthesise otherwise. The rest of the parameters for create_project are generated automatically during runtime.
   - **launch_simulation, launch_runs, wait_on_run, launch_runs, open_run, report_utilization, report_timing_summary, report_power**: are all called with a **-quiet** argument, remove it if you need to debug one of these commands.
- More constraints for Vivado can be added in **tcl_work_dir/constraints/Constraints_1.xdc**. Currently only contains a clock constraint.

---

## The individual Class

GA's are centered around a population of individuals, to implement that we created a class
called individual. An individual for this program is essentially the high level description for
an approximate multiplier. It's fields are:
- **vars**: (list of ints) the values for each variable
- **score**: (float) score calculated from fitness function
- **mse**: (float) mean squared error produced by this multiplier
- **util**: (\[int, int\]) Lut and Reg utilization by this multiplier
- **time**: (\[float, float, float\]) timing report in nS: WNS, WHS, WPWS of this multiplier
- **power**: (float) dynamic power consumption in Watts for this multiplier

An individual is initialized by invoking:

```
indy = individual(vars) # where vars is the list of initial values for each variable
#or
indy = individual(None) # the individual will have randomized initial values for each variable
```

All other values are initialized to -1. They are set to the correct values when

```
run_individual(indy)
```

is called. To evaluate your own individual/s we recommend using:

```
indx = individual(varsx)
# ...
indy = individual(varsy)
IUT = [indx, ..., indy]
run_static(IUT)
```

This will evaluate them and store their values in *highscores.js* from where they will be loaded
for any subsequent evaluations.

Once an individual is created and evaluated you can use:

```
indy.number()    	   # for a base 10 unique number for this multiplier
indy.name()      	   # for a base 10 name for this multiplier, based on the unique number
indy.short_name()	   # for the base 16 representation of the unique number
indy.shorter_name()  # for the base 64 representation of the unique number
indy.report()    	   # a string reporting the evaluation values (MSE, utilization, timing, power) for this multiplier
str(indy)        	   # the str representation, including name, score and the report above
```

---

## Fitness Fucntion

The fitness function used for our GA is <br>
![fitness function](images/fitness_function.png) <br>
It includes the MSE as a general measure of accuracy and LUTs, as reported by Vivado, as a *relatively*
general measure of area.
For a more specific application a designer might want to change this function.
To simply change the formula above with a different one, altering the *formula()* function within **search.py**
will suffice. To change the measure of accuracy you can use the *MSE()* function within **search.py** (you
might also want to refactor its name). Currently this program does not allow any further modularity without
a big refactorization of the code.

## VHDL code of individuals

During evaluation Vivado is used to run a behavioural simulation, synthesize and implement the
multiplier, all in order to fill in the MSE, utilization, timing, power values. To do this we
enlist the help of the methods inside *tcl_helper.py*. This file will help you if you want to
generate and study the VHDL code for a multiplier. The following code will create the necessary
files in a folder named with the short_name under the *tcl_work_dir/temp* directory:

```
indy = individual(vars)                                	# create an individual
name = indy.short_name()                               	# get its name
create_files(name)                                     	# create vivado project files
build_rtl(name, [VAR_D[i] for i in indy.vars])         	# create vhdl files
# ^ here the values of the individual's variables need to be translated to normal AFA names
```

Furthermore you can use the methods below to conduct an evaluation of your individual (even
though we recommend using *run_static* from **search.py** as mentioned before):

```
p = run_tcl(name, TCL_DEBUG)  # runs Vivado evaluation for this individual
indy_out = get_scores(name)   # parses evaluation output from Vivado output files
# ^ indy_out has the values that need to be inserted into the fields of the individual
```

---

## Included results

This repository has the *highscores.js* file. In this database file we include the individuals
we evaluated during our study of the 8x8 approximate multiplier. Currently the file addresses each
multiplier using its short_name (base 16). You can load and store the information using:

```
highscore_entries = load_entries()
store_entries(highscore_entries)
```

*highscore_entries* is a dict from which you can load any included individual using its short_name
as key. For statistical analysis we include a method to create a Pandas Dataframe in **utilities.py**:

```
highscores = load_entries()
dt = get_dataframe(highscores)
```

In case you would like to further inspect or create an individual yourself you can do so with a list
of values for its variables. If instead of a list of values you possess the name in base16 or base64
**utilities.py** has methods for converting in between the different formats:

```
indy_vals = [1. 2, ... , 39]
indy_16 = convert_16_to_vals(indy_vals)
indy_64 = convert_64_to_vals(indy_vals)
indy_16 == convert_64_to_16(indy_64) 	   # True
indy_64 == convert_16_to_64(indy_16) 	   # True
```

Finally **utilities.py** contains methods for experimenting with the multiplication table created by an
approximate multiplier. The approximate multiplier has errors in some cases so we need to map each possible
result in order to test the multiplier. Using the *"_out.rpt"* files generated by Vivado in the
*tcl_work_dir/tcl_out* directory you can get the multiplication table for an individual:

```
a = 42
b = 7
table = create_ax_mult(out_file)   # creates the multiplication table with the _out.rpt file as input
get_ax_mult(a, b, table)       	   # gives you the axb result from this approximate multiplication table
```

---

## Known Problems

- Binary combination and mutation might not work if the domain of variables is not of length equal to a power of two.
