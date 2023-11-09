# AxC-8bit-Multiplier-Research

In this repository we publish the code used to run the Genetic Algorithm experiments for our paper:

---

# Requirements

To run our code you need [Python](https://www.python.org/downloads/) installed with the [bitarray](https://pypi.org/project/bitarray/) libary.
For VHDL simulation, synthesis and implementation we use [Xilinx Vivado](https://www.xilinx.com/support/university/vivado.html), it needs to be installed in your system.
We tested this program with **Python 3.10.12** and **Vivado v2021.1.1 (64-bit)** on **Ubuntu 22.04.2 LTS**.

---

## File Structure

├── 8x8_runs.txt                         (search.py text output file)
├── highscores.json                      (database for archived individuals)
├── search.py                            (**main** search program)
├── tcl_helper.py                        (helper functions for use of Vivado)
├── utilities.py                         (some utilites to handle the study of produced data)
└── tcl_work_dir                         (work directory for simulation, synthesis and implementation)
    ├── constraints                      (Vivado project constraints)
    │   └── Constraints_1.xdc
    ├── main.tcl                         (main script run by Vivado to conduct simulation-synthesis-implementation)
    ├── tb                               (VHDL testbench directory)
    │   ├── main_tb.vhd
    │   └── tb_wallace_test.vhd
    ├── tcl_out                          (Vivado report output directory)
    ├── temp                             (temporary Vivado project generation directory, safe to delete contents)
    └── vhdl                             (Multiplier VHDL code directory)
        ├── axc_wallace.vhd
        ├── ...
        └── wallace.vhd

---

## Code Usage

The main entry proint for this project is **search.py**. Invoking this program with 

> python search.py

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

## Known Problems
