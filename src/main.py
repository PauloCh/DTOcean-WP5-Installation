"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

main.py is the main file of the WP5 module within the suite of design tools
developped under the EU FP7 DTOcean project. main.py provides an estimation of
the predicted performance of feasible maritime infrastructure solutions
that can carry out marine operations pertaining to the installation of
wave and tidal energy arrays.

main.py can be described in five core sub-modules:
0- Loading input data
1- Initialising the logistic classes
2- Defining the installation plan
3- Selecting the installation port
4- Performing the assessment of all logistic phases sequencially, following
   six steps:
    (i) characterizartion of logistic requirements
    (ii) selection of the maritime infrastructure
    (iii) schedule assessment of the logistic phase
    (iv) cost assessment of the logistic phase
    (v) risk assessment of the logistic phase
    (vi) environmental impact assessment of the logistic phase

Parameters
----------
vessels(DataFrame): Panda table containing the vessel database

equipments (DataFrame): Panda table containing the equipment database

ports (DataFrame): Panda table containing the ports database

user_inputs (dict): dictionnary containing all required inputs to WP5 coming from WP1/end-user:
     'device' (Dataframe): inputs required from the device
     'metocean' (Dataframe): metocean data

hydrodynamic_outputs (dict): dictionnary containing all required inputs to WP5 coming from WP2
     'units' (DataFrame): number of devices
     'position' (DataFrame): UTM position of the devices

electrical_outputs (dict): dictionnary containing all required inputs to WP5 coming from WP3
     'layout' (DataFrame): to be specified

M&F_outputs (DataFrame): containing foundation data required for each device

O&M_outputs (dict):  dictionnary containing all required inputs to WP5 coming from WP6
     'LogPhase1' (DataFrame): All inputs required for LpM1 logistic phase as defined by WP6

Returns
-------

install (dict): dictionnary compiling all key results obtained from the assessment of the logistic phases for installation
    'plan' (dict): installation sequence of the required logistic phases
    'port' (DataFrame): port data related to the selected installation port
    'requirement' (tuple): minimum requirements returned from the feasibility functions
    'eq_select' (dict): list of equipments satisfying the minimum requirements
    've_select' (dict): list of vessels satisfying the minimum requirements
    'combi_select' (dict): list of solutions passing the compatibility check
    'schedule' (dict): list of parameters with data about time
    'cost'  (dict): vessel equiment and port cost
    'risk': to be defined
    'envir': to be defined
    'status': to be defined


Examples
--------
>>> WP5()


See also: ...

                       DTOcean project
                    http://www.dtocean.eu

                   WavEC Offshore Renewables
                    http://www.wavec.org/en


"""

from os import path

from wp5.load import load_vessel_data, load_equipment_data, load_port_data
from wp5.load.wp_bom import load_user_inputs, load_hydrodynamic_outputs
from wp5.load.wp_bom import load_electrical_outputs, load_MF_outputs
from wp5.load.wp_bom import load_OM_outputs
from wp5.logistics.operations import logOp_init
from wp5.logistics.phase import logPhase_install_init
from wp5.installation import planning, select_port
from wp5.feasibility.glob import glob_feas
from wp5.selection.select_ve import select_e, select_v
from wp5.selection.match import compatibility_ve
from wp5.performance.schedule.schedule import sched
from wp5.performance.economic.eco import cost

# # Set directory paths for loading inputs (@Tecanalia)
mod_path = path.dirname(path.realpath(__file__))


def database_file(file):
    """shortcut function to load files from the database folder
    """
    fpath = path.join('databases', '{0}'.format(file))
    db_path = path.join(mod_path, fpath)
    return db_path


#def run():
"""
Loading required inputs and database into panda dataframes
"""
vessels = load_vessel_data(database_file("logisticsDB_vessel_python.xlsx"))
equipments = load_equipment_data(database_file("logisticsDB_equipment_python.xlsx"))
ports = load_port_data(database_file("logisticsDB_ports_python.xlsx"))

user_inputs = load_user_inputs(database_file("inputs_user.xlsx"))
hydrodynamic_outputs = load_hydrodynamic_outputs(database_file("ouputs_hydrodynamic.xlsx"))
electrical_outputs = load_electrical_outputs(database_file("ouputs_electrical.xlsx"))
MF_outputs = load_MF_outputs(database_file("outputs_MF.xlsx"))
OM_outputs = load_OM_outputs(database_file("outputs_OM.xlsx"))

"""
 Initialise logistic operations and logistic phases
"""
#logOp = logOp_init()
#
#logPhase_install = logPhase_install_init(logOp, vessels, equipments)
##logPhase_OM = logPhase_OM_init(logOp, vessels, equipments)
#
#"""
# Determine the adequate installation logistic phase plan
#"""
#install_plan = planning.install_plan(user_inputs, electrical_outputs, M&F_outputs)
#
## DUMMY-TO BE ERASED, install plan is constrained to F_driven because
## we just have the F_driven characterized for now
#install_plan = {0: ['F_driven']}
#
## Select the most appropriate base installation port
#install_port = select_port.install_port(user_inputs, electrical_outputs, M&F_outputs, ports)
#
## Incremental assessment of all logistic phase forming the the installation process
#install = {'plan': install_plan,
#           'port': install_port,
#           'requirement': {},
#           'eq_select': {},
#           've_select': {},
#           'combi_select': {},
#           'schedule': {},
#           'cost': {},
#           'risk': {},
#           'envir': {},
#           'status': "pending"}
#
#if install['status'] == "pending":
#    # loop over the number of layers of the installation plan
#    for x in range(len(install['plan'])):
#        for y in range(len(install['plan'][x])):
#            # extract the LogPhase ID to be evaluated from the installation plan
#            log_phase_id = install['plan'][x][y]
#            log_phase = logPhase_install[log_phase_id]
#            # characterize the logistic requirements
#            install['requirement'] = glob_feas(log_phase, log_phase_id,
#                                               user_inputs, hydrodynamic_outputs,
#                                               electrical_outputs, M&F_outputs)
#
#            # selection of the maritime infrastructure
#            install['eq_select'], log_phase = select_e(install, log_phase)
#            install['ve_select'], log_phase = select_v(install, log_phase)
#
#            # matching requirements for combinations of port/vessel(s)/equipment
#            # install['combi_select'] = compatibility_vp(install, log_phase)
#            install['combi_select'], log_phase = compatibility_ve(install, log_phase)
#
#            # schedule assessment of the different operation sequence
#            install['schedule'], log_phase = sched(x, install, log_phase, user_inputs, hydrodynamic_outputs, electrical_outputs, M&F_outputs)
#
#            # cost assessment of the different operation sequenc
#            install['cost'], log_phase = cost(install, log_phase)
#
#            # TO DO -> risk and enviromental impact

#
#if __name__ == "__main__":
#    run()
