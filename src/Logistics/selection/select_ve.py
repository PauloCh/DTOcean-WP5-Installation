# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the first part of the selection step in the WP5
methodology. It contains functions to match the requirements computed in the
feasibility functions, with the parameters of vessels and equipments imported
in the load functions.

BETA VERSION NOTES: These functions are mature and should not suffer many
changes from the current version to the following beta version.
"""

def select_e (install, log_phase):
    """select_e function selects the equipments that satisfy the minimum
    requirements calculated in the feasibility functions. The current method to
    achieve this is erasing the unfeasible equipments from the panda dataframes
    included in the ve_combination objects.

    Parameters
    ----------
    install : dict
     among other data contains the feasibility requirements of equipments
    log_phase : class
     class of the logistic phase under consideration for assessment, contains
     data refered to the vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    eq : dict
     A dict of panda dataframes with all the feasibile equipments
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     equipments within each vessel and equipment combinations dataframes
    """

    req_e = install['requirement'][0]
    #Initialize an empty dic with the name of the equip to be evaluated
    eq = dict.fromkeys(req_e.keys())

    for typ in range(len(req_e)):
        e_key_req = req_e.keys()[typ]

        for seq in range(len(log_phase.op_ve)):

            # print 'seq='
            # print seq

            LEN_combi = len(log_phase.op_ve[seq].ve_combination)
            combi = 0
            while combi < LEN_combi:

                # print 'combi='
                # print combi

                LEN_nr_eq = len(log_phase.op_ve[seq].ve_combination[combi]['equipment'])
                nr_eq = 0
                while nr_eq < LEN_nr_eq:

                    # print 'nr_eq='
                    # print nr_eq

                    e_key_phase = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1].id
                    e_pd = log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1].panda

                    if e_key_phase == e_key_req:

                        for req in range(len(req_e[e_key_req])):
                            e_para = req_e[e_key_req][req][0]
                            e_meth = req_e[e_key_req][req][1]
                            e_val = req_e[e_key_req][req][2]

                            if e_meth == 'sup':
                                e_pd = e_pd[e_pd[e_para] >= e_val]
                            # elif e_meth == 'inf':
                            #     e_pd = e_pd[e_pd[e_para] <= e_val]
                            # elif e_meth == 'equal':
                            #     e_pd = e_pd[e_pd[e_para] == e_val]


                        # e_sol = e_pd
                        # Check if no vessel is feasible within the req for this particular ve_combination
                        # if e_sol.empty:
                        if len(e_pd.index)==0:
                            del log_phase.op_ve[seq].ve_combination[combi]   # If so, force the combination to be 0
                            for ind_comb in range(combi,LEN_combi-1):
                                log_phase.op_ve[seq].ve_combination[ind_comb] = log_phase.op_ve[seq].ve_combination[ind_comb+1]
                                del log_phase.op_ve[seq].ve_combination[ind_comb+1]
                            LEN_combi = len(log_phase.op_ve[seq].ve_combination)
                            nr_eq = LEN_nr_eq
                            if combi==LEN_combi-1:
                                combi=combi+1
                            break
                        else:
                            eq[e_key_req] = e_pd
                            log_phase.op_ve[seq].ve_combination[combi]['equipment'][nr_eq][1].panda = e_pd
                            nr_eq = nr_eq + 1

                    else:
                        if nr_eq==LEN_nr_eq-1:
                            combi = combi + 1
                        nr_eq = nr_eq + 1

                combi = combi + 1


    return eq, log_phase


def select_v (install, log_phase):
    """select_v function selects the vessels that satisfy the minimum requirements
    calculated in the feasibility functions. The current method to do this is
    erasing the unfeasible vessels from the panda dataframes included in the
    ve_combination objects

    Parameters
    ----------
    install : dict
     among other data contains the feasibility requirements of vessels
    log_phase : class
     contains data refered to the vessel and equipment combinations specific of
     each operation sequence of the logistic phase

    Returns
    -------
    eq : dict
     A dict of panda dataframes with all the feasibile vessels
    log_phase : class
     An updated version of the log_phase argument containing only the feasible
     vessels within each vessel and equipment combinations dataframes
    """

    import matplotlib.pyplot as plt

    # load the vessel requirements inside a short named variable
    req_v = install['requirement'][1]

    # Initialize an empty dic with the name of the vessels to be evaluated
    ves = dict.fromkeys(req_v.keys())

    for typ in range(len(req_v)):   # loop over the vessel types in requirements
        v_key_req = req_v.keys()[typ]

        for seq in range(len(log_phase.op_ve)): # loop over the number of strategies (op_ve) of the logistic phase in study

            LEN_combi = len(log_phase.op_ve[seq].ve_combination)
            combi = 0
            while combi < LEN_combi: # loop over the number of combinations inside the strategy

                LEN_nr_ves = len(log_phase.op_ve[seq].ve_combination[combi]['vessel'])
                nr_ves = 0
                while nr_ves < LEN_nr_ves: # loop over the number of vessels inside the combination

                    v_key_phase = log_phase.op_ve[seq].ve_combination[combi]['vessel'][nr_ves][1].id
                    v_pd = log_phase.op_ve[seq].ve_combination[combi]['vessel'][nr_ves][1].panda

                    if v_key_phase == v_key_req:

                       for req in range(len(req_v[v_key_req])):
                           v_para = req_v[v_key_req][req][0]
                           v_meth = req_v[v_key_req][req][1]
                           v_val = req_v[v_key_req][req][2]

                           if v_meth == 'sup':
                               v_pd = v_pd[v_pd[v_para] >= v_val]
                           # elif v_meth == 'inf':
                           #     v_pd = v_pd[v_pd[v_para] <= v_val]
                           # elif v_meth == 'equal':
                           #     v_pd = v_pd[v_pd[v_para] == v_val]

                       # v_sol = v_pd
                       # Check if no vessel is feasible within the req for this particular ve_combination
                       # if v_sol.empty:
                       if len(v_pd.index)==0:
                            del log_phase.op_ve[seq].ve_combination[combi]   # If so, force the combination to be 0
                            for ind_comb in range(combi,LEN_combi-1):
                                log_phase.op_ve[seq].ve_combination[ind_comb] = log_phase.op_ve[seq].ve_combination[ind_comb+1]
                                del log_phase.op_ve[seq].ve_combination[ind_comb+1]
                            LEN_combi = len(log_phase.op_ve[seq].ve_combination)
                            nr_ves = LEN_nr_ves
                            if combi==LEN_combi-1:
                                combi=combi+1
                            break

                       else:
                            ves[v_key_req] = v_pd
                            log_phase.op_ve[seq].ve_combination[combi]['vessel'][nr_ves][1].panda = v_pd
                            nr_ves = nr_ves + 1

                    else:
                        if nr_ves==LEN_nr_ves-1:
                            combi = combi + 1
                        nr_ves = nr_ves + 1

                combi = combi + 1




    return ves, log_phase