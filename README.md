# AxC-8bit-Multiplier-Research

In this repository we publish the code used to run the Genetic Algorithm experiments for our paper:

---

# Requirements

To run our code you need [Python](https://www.python.org/downloads/) installed with the [bitarray](https://pypi.org/project/bitarray/) libary.
For VHDL simulation, synthesis and implementation we use [Xilinx Vivado](https://www.xilinx.com/support/university/vivado.html), it needs to be installed in your system.
We tested this program with **Python 3.10.12** and **Vivado v2021.1.1 (64-bit)** on **Ubuntu 22.04.2 LTS**.

---

## File Structure
```
├── 8x8_runs.txt                         (search.py text output file)<br>
├── highscores.json                      (database for archived individuals)<br>
├── search.py                            (**main** search program)<br>
├── tcl_helper.py                        (helper functions for use of Vivado)<br>
├── utilities.py                         (some utilites to handle the study of produced data)<br>
└── tcl_work_dir                         (work directory for simulation, synthesis and implementation)<br>
    ├── constraints                      (Vivado project constraints)<br>
    │   └── Constraints_1.xdc<br>
    ├── main.tcl                         (main script run by Vivado to conduct simulation-synthesis-implementation)<br>
    ├── tb                               (VHDL testbench directory)<br>
    │   ├── main_tb.vhd<br>
    │   └── tb_wallace_test.vhd<br>
    ├── tcl_out                          (Vivado report output directory)<br>
    ├── temp                             (temporary Vivado project generation directory, safe to delete contents)<br>
    └── vhdl                             (Multiplier VHDL code directory)<br>
        ├── axc_wallace.vhd<br>
        ├── ...<br>
        └── wallace.vhd<br>
```
---

## Code Usage

The main entry proint for this program is **search.py**. Invoking this program is done with 
```
> python search.py
```
in the root directory. This will start the GA which will do 1000 search runs by default.
While running the program will dispaly some progress infromation in the console and at
the same time store critical run results in 8x8_runs.txt. Any individuals evaluated with
Vivado are stored inside *highscores.json*. Vivado will generate files inside the folders
*tcl_work_dir/tcl_out* and *tcl_work_dir/temp* during runtime. Any files inside *temp*
can safely be deleted after the program finishes running. Files inside *tcl_out* could
contain usefull information that is not stored in *highscores.json*, specifically files
with *_out.rpt* suffix. The rest of *tcl_work_dir* contains files for running vivado and
our VHDL code for the 8x8 Multiplier.

---

## Code Configuration

- Inside **search.py** the following program parameters may be set:
  - **MAX_PROC**: sets the number of maximum parallel Vivado processes called by search.
  - **random.seed()**: set a seed in order to get the same results each time.
  - **TCL_DEBUG**: (True/False) whether or not to print debug info from Vivado commands.
  - **EVL_DEBUG**: (True/False) whether or not to print debug info from this program.
  - **OUT_FILE**: name for the output file.
- Inside **search.py** the following genetic algorithm parameters may be set:
  - **POP_N**: number of individuals in population.
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
  - **BIT_W**: number of possible variables bit width (e.g. legnth of VAR_D 32 : BIT_W = 5 bits).
  - **INP_W**: input number bit width (used only for MSE calculation).
 - Inside **tcl_work_dir/main.tcl** the following vivado parameters may be set:
   - **set_param general.maxThreads**: maxmum threads used by Vivado (tip: set to number of logical processors on your system).
   - **create_project -part**: ⚠️***Very important***⚠️ You might want to change the part identifier to an FPGA part for which you own the liscence,
     Vivado will refuse to synthesise otherwise. The rest of the prameters for create_project are generated automatically during runtime.
   - **launch_simulation, launch_runs, wait_on_run, launch_runs, open_run, report_utilization, report_timing_summary, report_power**: are all called with a **-quiet** argument, remove it if you need to debug one of these commands.
  
## Known Problems

*Binary combination and mutation might not work if the domain of variables is not of length equal to a power of two.
