# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the interphase relation between the different
logistic phases during installation. The inputs from the user and other DTOcean
packages build up unique projects which require specific installation sequences.
The functions in this module return the installation sequence required based on
some pre-defined cases (type of foundations, type of moorings, type of device,
type of electrical infranstrucutres).

BETA VERSION NOTES: the methodology was defined and implemented, should not
suffer major changes on the next version of the code. However the content (the
installation sequences) will be updated.
"""

import numpy
from transit_algorithm import transit_algorithm
from Logistics.installation.select_port import distance


def sched_dev(log_phase, user_inputs, hydrodynamic_outputs):
    """install_plan receives upstream data providing information to build the
    project case, based on this info the function returns a dictionary containing
    a specific installation sequence, using the following methodology:
        - the first key of the dict contains a list of the logistic phases which
        can start independently of others being finished.
        - the second key contains a information of the logistic interphase
         dependency from the logistic phases contained in the first key.
        - the third key contains a information of the logistic interphase
         dependency from the logistic phases contained in the second key.
        - etc...

    Parameters
    ----------
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user.
    wp3_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3.
    wp4_outputs : DataFrame
     panda table containing all required inputs to WP5 coming from WP4.

    Returns
    -------
    install_seq : dict
     dictionnary containing a list of the logistic phases required to conduct
     the installation of the project plus information about the interphase
     relation and sequence.
    """

    # check the transportation method
    # (1st branch in the decision making tree)
    if log_phase.op_ve[seq].description == 'On-deck transportation':
        # check the device assembly strategy
        # (2nd and FINAL branch in the decision making tree)
        assemb_method = user_inputs['device']['assembly strategy [-]'].ix[0]
        if assemb_method == '([A,B,C,D])':
            # calculate the number of devices
            nb_dev = len(hydrodynamic_outputs['device [-]'])
            elem_area = [0]*nb_dev
            elem_mass = [0]*nb_dev
            for dev in range(nb_dev): # loop over the number of devices
                # calculate the area and dry mass of all elements
                elem_area[dev] = user_inputs['device']['length [m]'].ix[0]*user_inputs['device']['width [m]'].ix[0] # [m^2]
                elem_mass[dev] = user_inputs['device']['dry mass [kg]'].ix[0]/1000 # [ton]
                
            nb_elem_port = nb_dev # initialise the number of elements to be transported that are initially at port
            nb_journey = 0 # initialise the number of vessel journeys
            nb_el_journey = [] # initialise the list of number of elements per journey
            while nb_elem_port > 0:
                # extract the panda series of the tranporting vessel
                # assumption: the first vessel is always the transporting vessel 
                sol_pd_series = log_phase.op_ve[seq].sol[ind_sol]['VEs'][0][2]
                # extract the deck area and cargo
                deck_area = sol_pd_series.ix['Deck space [m^2]']
                deck_cargo = sol_pd_series.ix['Max. cargo [t]']
                # determine the cumulative vector of element areas and dry masses
                elem_area_accum = list(numpy.cumsum(elem_area))
                elem_mass_accum = list(numpy.cumsum(elem_mass))
                # determine the maximum number of elements that can fit on-deck due to max deck area or max deck cargo limitations
                nb_dev_area = indices(elem_area_accum, lambda x: x>deck_area)
                if not nb_dev_area:
                    nb_dev_area = len(elem_area_accum)
                else:
                    nb_dev_area = min(nb_dev_area)
                nb_dev_mass = indices(elem_mass_accum, lambda x: x>deck_cargo)
                if not nb_dev_mass:
                    nb_dev_mass = len(elem_mass_accum)
                else:
                    nb_dev_mass = min(nb_dev_mass)
                nb_el_journey.append(min([nb_dev_area,nb_dev_mass]))
                # update the number of elements remaining at port and their areas/masses lists
                if nb_el_journey[nb_journey] == nb_elem_port:
                    nb_elem_port = 0
                elif nb_el_journey[nb_journey] == 0:
                    # error that means not a single element can fit!
                    print 'not a single device can fit in the deck!' 
                else:
                    nb_elem_port = nb_elem_port - nb_el_journey[nb_journey]
                    elem_area = elem_area[nb_el_journey[-1]:]
                    elem_mass = elem_mass[nb_el_journey[-1]:]
                # update the number of vessel journeys
                nb_journey = nb_journey + 1
                
                ind_el = 0
            for jour in range(nb_journey):
                # number of operation sequence in the preparation phase
                nb_op_prep = len(log_phase.op_ve[seq].op_seq_prep)                            
                # determine the duration of the logistic phase preparation before departure of the vessel(s)
                for op_prep in range(nb_op_prep): # loop over the nb of onshore logistic operations
                    log_op_prep = log_phase.op_ve[seq].op_seq_prep[op_prep]
                    # discriminate between the time assessment methods
                    if log_op_prep.time_value: # direct value
                        op_dur_prep.append(log_op_prep.time_value)
                    elif log_op_prep.time_function: # function
                        # type of function
                        if log_op_prep.time_function == "transit_algorithm":
                            port_pd = log_phase.op_ve[seq].sol[ind_sol]['port']
                            UTM_port = [port_pd.ix['UTM x [m]'],
                                        port_pd.ix['UTM y [m]'],
                                        port_pd.ix['UTM zone [-]']]
                            site = user_inputs['site']
                            UTM_site = [site['x coord [m]'].ix[0],
                                        site['y coord [m]'].ix[0],
                                        site['zone [-]'].ix[0]]
                            port_2_site_dist = transit_algorithm(UTM_port, UTM_site)
                            nb_ves_type = range(len(log_phase.op_ve[seq].sol[ind_sol]['VEs']))
                            # loop over the nb of vessel types                                        
                            for vt in nb_ves_type:
                                ves_speed[vt] = log_phase.op_ve[seq].sol[ind_sol]['VEs'][vt][2].ix['Transit speed [m/s]']
                            ves_slow = 3.6*min(ves_speed) # [km/h]
                            port_2_site_time = port_2_site_dist/ves_slow
                            # append transit time to the preparation time
                            op_dur_prep.append(port_2_site_time)
                        elif log_op_prep.time_function == "distance":
                            dist_tot = 0
                            dist_el = []
                            for el in range(nb_el_journey[jour]):
                                UTM_el_i = [hydrodynamic_outputs['x coord [m]'].ix[el],
                                            hydrodynamic_outputs['y coord [m]'].ix[el],
                                            hydrodynamic_outputs['zone [-]'].ix[el]]
                                UTM_el_f = [hydrodynamic_outputs['x coord [m]'].ix[el+1],
                                            hydrodynamic_outputs['y coord [m]'].ix[el+1],
                                            hydrodynamic_outputs['zone [-]'].ix[el+1]]
                                dist_el[el] = distance(UTM_el_i,UTM_el_f)
                                dist_tot = dist_tot + dist_el[el]  
                            
                    elif log_op_prep.time_other:
                        if log_op_prep.time_other == "vesselDB['Mob time [h]']":
                            mob_time = 0
                            op_dur_prep.append(mob_time)  
                        elif log_op_prep.time_other == "device['assembly duration [h]']":
                            assemb_time = 0
                            op_dur_prep.append(assemb_time)  
                        elif log_op_prep.time_other == "device['connect duration [h]']":
                            dev_connect_time = 0
                            op_dur_prep.append(dev_connect_time)  
                        elif log_op_prep.time_other == "device['disconnect duration [h]']":
                            dev_disconnect_time = 0
                            op_dur_prep.append(dev_disconnect_time)
                            
                ind_el = ind_el + nb_el_journey[jour]
                # determine the sea duration
                
            # add demobilisation time to finalise the logistic phase

#                    elif assemb_method == '([A,B,C],D)':

    return install_seq, instal_order

# see = selectSeq(end_user_inputs, WP3_outputs, WP4_outputs)
