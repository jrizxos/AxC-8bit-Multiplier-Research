import os
import shutil
#from search import MSE, NORMAL_OUT
from subprocess import Popen, DEVNULL

TOP_DIR = 'tcl_work_dir'
CON_DIR = 'constraints'
TEMP_DIR = 'temp'
SRC_DIR = 'vhdl'
SIM_DIR = 'tb'
OUT_DIR = 'tcl_out'
MAIN_SCR = 'main.tcl'
MAIN_TB = 'main_tb.vhd'
MAIN_RTL = 'axc_wallace.vhd'
CWD = os.getcwd()

# maps adder name with variable index
ADDER_MAP = ['fa1002', 'fa1003', 'fa1004', 'fa1005', 'fa1006', 'fa1007', 'fa1008', 'fa1009', 'fa1010', 'fa1011', 'fa1012', 'fa1105', 'fa1106', 'fa1107', 'fa1108', 'fa1109', 'fa2003', 'fa2004', 'fa2005', 'fa2006', 'fa2007', 'fa2008', 'fa2009', 'fa2010', 'fa2011', 'fa2012', 'fa2107', 'fa3004', 'fa3006', 'fa3007', 'fa3008', 'fa3009', 'fa3010', 'fa3012', 'fa4005', 'fa4008', 'fa4009', 'fa4010', 'fa4011']  #['fa12','fa13','fa14','fa23','fa34','fa35','fa36']

def check_files(name):
    sim_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_out.rpt')
    util_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_syn_util.rpt')
    time_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_time.rpt')
    power_dir = os.path.join(TOP_DIR, OUT_DIR, name+'_power.rpt')
    if os.path.exists(sim_dir) and os.path.exists(util_dir) and os.path.exists(time_dir) and os.path.exists(power_dir):
        return True
    return False

def create_files(name):
    """Creates files for vivado simulation and sythesis. Edits the simulation file for output directory.
    Edits the main TCL script for project name, import directories and output directories

        Args:
            name (str): the name of the individual, which is going to be simulated and syhtesized 

        Returns:
            new_dir (str): path to the temporary directory created
    """
    # copy files
    new_dir = os.path.join(TOP_DIR, TEMP_DIR, name)     # temporary dir path
    if os.path.exists(new_dir):                         # if it exists erase
        shutil.rmtree(new_dir)
    os.mkdir(new_dir)                                   # create temporary dir
    get_dir = os.path.join(CWD, TOP_DIR, SRC_DIR)       # get vhdl files from here
    src_dir = os.path.join(CWD, new_dir, SRC_DIR)       # put vhdl files here
    shutil.copytree(get_dir, src_dir)                   # copy files
    get_dir = os.path.join(CWD, TOP_DIR, SIM_DIR)       # get simulation files from here
    sim_dir = os.path.join(CWD, new_dir, SIM_DIR)       # put simulation files from here
    shutil.copytree(get_dir, sim_dir)                   # copy files
    get_dir = os.path.join(CWD, TOP_DIR, MAIN_SCR)      # get tcl script from here
    put_dir = os.path.join(CWD, new_dir)                # put tcl script from here
    shutil.copy(get_dir, put_dir)                       # copy files

    # edit main tcl script
    scr_dir = os.path.join(put_dir, MAIN_SCR)           
    with open(scr_dir, 'r') as file:
        data = file.readlines()
        file.close()
    prj_dir = os.path.join(CWD, put_dir, 'xil_project')
    con_dir = os.path.join(CWD, TOP_DIR, CON_DIR)
    out_dir = os.path.join(CWD, TOP_DIR, OUT_DIR) 
    for i,line in enumerate(data):
        if(line.startswith('create_project')):
            data[i] = 'create_project ' + name + ' ' + prj_dir + ' -part xczu9eg-ffvb1156-2-e -force\n'
            continue
        elif(line.startswith('add_files <src_dir>')):
            data[i] = 'add_files ' + src_dir + '\n'
            continue
        elif(line.startswith('import_files -fileset constrs_1')):
            data[i] = 'import_files -fileset constrs_1 -force -norecurse ' + con_dir +'\n'
            continue
        elif(line.startswith('add_files -fileset sim_1')):
            data[i] = 'add_files -fileset sim_1 ' + sim_dir + '\n'
            continue
        elif(line.startswith('report_utilization')):
            data[i] = 'report_utilization -file ' + out_dir + '/' + name + '_syn_util.rpt -quiet\n'
            continue
        elif(line.startswith('report_timing_summary')):
            data[i] = 'report_timing_summary -delay_type min_max -report_unconstrained -check_timing_verbose -max_paths 10 -input_pins -routable_nets -file ' + out_dir + '/' + name + '_time.rpt -quiet\n'
            continue
        elif(line.startswith('report_power')):
            data[i] = 'report_power -file ' + out_dir + '/' + name + '_power.rpt -quiet\n'
            continue
    with open(scr_dir, 'w') as file:
        file.writelines( data )
        file.close()

    # edit simulation output
    tb_dir = os.path.join(sim_dir, MAIN_TB)
    with open(tb_dir, 'r') as file:
        data = file.readlines()
        file.close()
    for i,line in enumerate(data):
        if(line.startswith('	  file outfile     	: text open write_mode is')):
            data[i] = '	  file outfile     	: text open write_mode is \"' + out_dir + '/' + name + '_out.rpt' + '\"; \n'
            break
    with open(tb_dir, 'w') as file:
        file.writelines( data )
        file.close()

    return new_dir

def build_rtl(name, vars):
    """Builds the RTL description of the multiplier based on the vars passed as argument.

        Args:
            name (str): the name of the temporaty directory that contains the rtl files
            vars (list): specific adders to put at each location in the design

        Returns:
            None
    """
    # edit rtl file
    rtl_dir = os.path.join(CWD, TOP_DIR, TEMP_DIR, name, SRC_DIR, MAIN_RTL)
    with open(rtl_dir, 'r') as file:
        data = file.readlines()
        file.close()
    for i,line in enumerate(data):
        try:
            j = ADDER_MAP.index(line[0:len(ADDER_MAP[0])])
        except:
            continue
        ports = line.index(' port')
        colon = line.index(' : ')
        data[i] = line[0:colon+3] + str(vars[j]) + line[ports:]
    with open(rtl_dir, 'w') as file:
        file.writelines( data )
        file.close()
    return

def run_tcl(name, out):
    """Runs the TCL script in the temporaty directory given as argument.

        Args:
            name (str): the name of the temporaty directory that contains the scipt

        Returns:
            p (Popen): process created
    """
    command = 'vivado -mode tcl -source main.tcl -nojournal -nolog'
    work_dir = os.path.join(CWD, TOP_DIR, TEMP_DIR, name)
    stdout = None
    if(not out):
        stdout = DEVNULL
    p = Popen(command, cwd = work_dir, shell=True, stdout=stdout)
    return p

def get_scores(name):
    """Rreads Vivado report values for an individual with given name from the tcl_out directory.

        Args:
            name (str): the name of the individual in base16

        Returns:
            sim (list of ints): the multiplication table for this individual
            util (list of ints): [LUT utilization, REG utilization]
            time (list of floats): [WNS, WHS, WPWS]
            power (float): dynamic power consumption
    """
    score_dir = os.path.join(CWD, TOP_DIR, OUT_DIR)

    # read simulation output
    sim_dir = os.path.join(score_dir, name + '_out.rpt')
    with open(sim_dir, 'r') as file:
        data = file.readlines()
        file.close()
    sim = []
    for b in data:
        try:
            num = int(b.strip('\n'),base=2)
            sim.append(num)
        except:
            continue

    util = [0,0]
    time = [0,0,0]
    power = 0

    # read util report
    util_dir = os.path.join(score_dir, name + '_syn_util.rpt')
    with open(util_dir, 'r') as file:
        data = file.readlines()
        file.close()
    util = []
    for i,line in enumerate(data):
        if(line.startswith('| CLB LUTs')):
            space1 = line.index('|',1)+1
            space2 = line.index('|',space1)
            util.append(int(line[space1:space2]))
            continue
        elif(line.startswith('| CLB Registers ')):
            space1 = line.index('|',1)+1
            space2 = line.index('|',space1)
            util.append(int(line[space1:space2]))
            break

    # read time report
    time_dir = os.path.join(score_dir, name + '_time.rpt')
    with open(time_dir, 'r') as file:
        data = file.readlines()
        file.close()
    time = []
    for i,line in enumerate(data):
        if(line.startswith('| Design Timing Summary')):
            j = i+6
            line = data[j].strip()
            lst = [x for x in line.split(' ') if not x=='']
            time = [float(lst[0]), float(lst[4]), float(lst[8])]

    # read power report
    power_dir = os.path.join(score_dir, name + '_power.rpt')
    with open(power_dir, 'r') as file:
        data = file.readlines()
        file.close()
    for i,line in enumerate(data):
        if(line.startswith('| Total On-Chip Power (W)')):
            space1 = line.index('|',1)+1
            space2 = line.index('|',space1)
            power = float(line[space1:space2])

    return sim, util, time, power
