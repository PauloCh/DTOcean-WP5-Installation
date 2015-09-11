# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is the second and last part of the selection step in the WP5 methodology.
It contains functions to make the compatibility check between the characteristics
of port/vessel, port/equipment and vessel/equipment, returning only the feasible
and compatible solutions of vessels and equipments to perform the operations
sequence of the logistic phase.

BETA VERSION DETAILS: up to date, the functionalities explained previously have
not been implemented, this module should suffer major changes for the beta version
"""

from ..logistics.phase.classes import VE_solutions


def compatibility_ve(install, log_phase):
    """This function is currently limited to the selection of the first two
    feasible solutions for the installation logistic phase in analisys.

    Parameters
    ----------
    install : dict
     not used
    log_phase : class
     class of the logistic phase under consideration for assessment, contains
     data refered to the feasible vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    sol : dict
     A dict of panda dataframes with unique feasible solutions
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     equipments within each vessel and equipment combinations dataframes
    """
    ves = {}
    ves_sol = {}
    eq = {}
    eq_sol = {}
    nr_sol = 0

    for seq in range(len(log_phase.op_ve)):
        for combi in range(len(log_phase.op_ve[seq].ve_combination)):

            for nr_ves in range(len(log_phase.op_ve[seq].ve_combination[combi]['vessel'])):

                ves_quant = log_phase.op_ve[seq].ve_combination[combi]['vessel'][nr_ves][0]  # Quantity of vessels in the solution
                ves_class = log_phase.op_ve[seq].ve_combination[combi]['vessel'][nr_ves][1]

                ves_index = ves_class.panda.index

                for a in range(len(ves_index)):

                  ves[a] = ves_class.panda.ix[ves_index[a]]

                ves_sol[nr_ves] = {'quantity': ves_quant,
                                   'Series': ves}

            for nr_eq in range(len(log_phase.op_ve[seq].ve_combination[combi]['equipment'])):

                eq_quant = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][0]  # Quantity of vessels in the solution
                eq_class = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1]

                eq_index = eq_class.panda.index

                for a in range(len(eq_index)):

                  eq[a] = eq_class.panda.ix[eq_index[a]]

                eq_sol[nr_eq] = {'quantity': eq_quant,
                                 'Series': eq}

        nr_sol = nr_sol

        for a in range(nr_ves):
            for b in range(len(ves_sol[a]['Series'])):
                for c in range(nr_eq):
                    for d in range(len(eq_sol[c]['Series'])):

                        sol = VE_solutions(nr_sol)

                        sol.sol_ves[a] = ves_sol[a]['Series'][b]

                        log_phase.op_ve[seq].sol[nr_sol] = sol


#    log_phase.op_ve[1].sol[0] = VE_solutions(0)
#    log_phase.op_ve[1].sol[1] = VE_solutions(1)
#
#    pd_ves0 = log_phase.op_ve[1].ve_combination[0]['vessel'][0][1].panda
#    pd_ves0_index = pd_ves0.index
#
#    pd_ves1 = log_phase.op_ve[1].ve_combination[0]['vessel'][1][1].panda
#    pd_ves1_index = pd_ves1.index
#
#    pd_eq = log_phase.op_ve[1].ve_combination[0]['equipment'][0][1].panda
#    pd_eq_index = pd_eq.index
#
#    log_phase.op_ve[1].sol[0].sol_ves[0] = pd_ves0.ix[pd_ves0_index[0]]
#    log_phase.op_ve[1].sol[0].sol_ves[1] = pd_ves1.ix[pd_ves1_index[0]]
#    log_phase.op_ve[1].sol[0].sol_eq[0] = pd_eq.ix[pd_eq_index[0]]
#
#    log_phase.op_ve[1].sol[1].sol_ves[0] = pd_ves0.ix[pd_ves0_index[1]]
#    log_phase.op_ve[1].sol[1].sol_ves[1] = pd_ves1.ix[pd_ves1_index[1]]
#    log_phase.op_ve[1].sol[1].sol_eq[0] = pd_eq.ix[pd_eq_index[0]]
#
#    sol = {}
#    sol[0] = log_phase.op_ve[1].sol[0]
#    sol[1] = log_phase.op_ve[1].sol[1]

    return sol, log_phase


def compatibility_ve_om(install, log_phase):
    """This function is currently limited to the selection of the first two
    feasible solutions for the O&M logistic phase in analisys.

    Parameters
    ----------
    install : dict
     not used
    log_phase : class
     class of the logistic phase under consideration for assessment, contains
     data refered to the feasible vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    sol : dict
     A dict of panda dataframes with unique feasible solutions
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     equipments within each vessel and equipment combinations dataframes
    """

    log_phase.op_ve[0].sol[0] = VE_solutions(0)
    log_phase.op_ve[0].sol[1] = VE_solutions(1)

    pd_ves0 = log_phase.op_ve[0].ve_combination[0]['vessel'][0][1].panda
    pd_ves0_index = pd_ves0.index

    pd_ves1 = log_phase.op_ve[0].ve_combination[1]['vessel'][0][1].panda
    pd_ves1_index = pd_ves1.index

    log_phase.op_ve[0].sol[0].sol_ves[0] = pd_ves0.ix[pd_ves0_index[0]]

    log_phase.op_ve[0].sol[1].sol_ves[0] = pd_ves1.ix[pd_ves1_index[1]]

    sol = {}
    sol[0] = log_phase.op_ve[0].sol[0]
    sol[1] = log_phase.op_ve[0].sol[1]

    return sol, log_phase

#    for seq in log_phase.op_ve.keys():
#        for combi in log_phase.op_ve[seq].ve_combination.keys():
#
# log_phase.op_ve[seq].ve_combination[combi]['vessel']
           # log_phase.op_ve[seq].ve_combination[combi]['equipment']
#
#            for nr_ves in range(len(log_phase.op_ve[seq].ve_combination[combi]['vessel'])):
#                pd_ves = log_phase.op_ve[seq].ve_combination[combi]['vessel'][nr_ves][1].panda
#                pd_ves_index = pd_ves.index
#
#                for nr_ves in range(len(pd_ves_index))
#
#                log_phase.op_ve[seq].sol[0] =
#
#            for nr_eq in log_phase.op_ve[seq].ve_combination[combi]['equipment'].keys():
#                pd_eq = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1].panda
#                pd_eq_index = pd_eq.index
#
##                for ves in len(pd_index):
##
##                    sol[0] =
##
##                    log_phase.op_ve[seq].ve_combination[combi].sol[ves] = VE_solutions(ves)
##
##                    log_phase.op_ve[seq].ve_combination[combi].sol[ves].sol_ve[ = pd.ix[pd_index[ves]]
##
##                    sol[0] = {'sol_ve': 0: panda
##                                        1: panda
##                              'sol_eq': 0: panda}
##
#                pass



#    def compatibility_ve (install, log_phase):
#
#    req_e = install['requirement'][0]
#    for typ in range(len(req_e)):
#        e_key_req = req_e.keys()[typ]
#
#        for seq in range(len(log_phase.op_ve)):
#            for combi in range(len(log_phase.op_ve[seq].ve_combination)):
#                for nr_eq in range(len(log_phase.op_ve[seq].ve_combination[combi]['equipment'])):
#
#                    e_key_phase = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1].id
#
#                    if e_key_phase == e_key_req:
#
#                        for req in range(len(req_e[e_key_req][nr_eq])/3):
#                            e_para = req_e[e_key_req][nr_eq][0]
#                            e_meth = req_e[e_key_req][nr_eq][1]
#                            e_val = req_e[e_key_req][nr_eq][2]
#
#                            if e_meth == 'sup':
#                                pd = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1].panda
#                                eq = pd[pd[e_para] >= e_val]
#    return eq
