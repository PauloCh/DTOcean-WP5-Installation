# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module is responsible for the selection of ports for both the installation
and O&M logistic activities. 

BETA VERSION NOTES: This current version is limited to the feasibility functions 
of two logistic phases (one for the installation module and one for the O&M), 
this will be upgraded for the beta version due to october.
"""

from transit_algorithm import transit_algorithm
from geopy.distance import great_circle
import utm
import math


def distance(UTM_ini, UTM_fin):
    """
    distance returns the calculated distance (in kms) between two points
    defined in the UTM coordinate system
    """

    UTM_ini_x = UTM_ini[0]
    UTM_ini_y = UTM_ini[1]
    UTM_ini_zone = UTM_ini[2]

    UTM_fin_x = UTM_fin[0]
    UTM_fin_y = UTM_fin[1]
    UTM_fin_zone = UTM_fin[2]

    [LAT_INI, LONG_INI] = utm.to_latlon(UTM_ini_x, UTM_ini_y, int(UTM_ini_zone[0:2]), str(UTM_ini_zone[3]))  # to get dd.dd from utm
    [LAT_FIN, LONG_FIN] = utm.to_latlon(UTM_fin_x, UTM_fin_y, int(UTM_fin_zone[0:2]), str(UTM_fin_zone[3]))  # to get dd.dd from utm

    point_i = (LAT_INI, LONG_INI)
    point_f = (LAT_FIN, LONG_FIN)

    distance = great_circle(point_i, point_f).kilometers # gives you a distance (in kms) between two coordinate in dd.dd

    return distance




def install_port(user_inputs, hydrodynamic_outputs, electrical_outputs, MF_outputs, ports):
    """install_port function selects the home port used by all logistic phases
    during installation. This selection is based on a 2 step process: 
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.  
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.

    Parameters
    ----------
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user
    electrical_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3
    MF_outputs : DataFrame
     panda table containing all required inputs to WP5 coming from WP4
    port_data : DataFrame
     panda table containing the ports database     

    Returns
    -------
    port : dict
     dictionnary containing the results port_listof the port selection
    """    
    # initialisation
    # port = {'Terminal load bearing [t/m^2]': 0,
    #         'Terminal area [m2]': 0,
    #         'Port list satisfying the minimum requirements': 0,
    #         'Distance port-site': 0,
    #         'Selected base port for installation': 0}
    # # calculate loading and projected area of foundations/anchors
    # load = []
    # area = []
    # if user_inputs['device']['type [-]'].ix[0] == "seabed fixed":
    #     for x in range(MF_outputs['quantity'].ix[0]):
    #         key1 = "diameter foundation " + str(x) + " [m]"
    #         key2 = "length foundation " + str(x) + " [m]"
    #         key3 = "weight foundation " + str(x) + " [kg]"
    #         load[len(load):] = [MF_outputs[key1].ix[0] * MF_outputs[key2].ix[0] / MF_outputs[key3].ix[0]]
    #         area[len(area):] = [MF_outputs[key1].ix[0] * MF_outputs[key2].ix[0]]
    #
    # # terminal load bearing minimum requirement
    # port['Terminal load bearing [t/m^2]'] = max(user_inputs['device']['length [m]'].ix[0] * user_inputs['device']['width [m]'].ix[0] / user_inputs['device']['dry mass [kg]'].ix[0],
    #                                                max(load))
    # port_list = port_data[ port_data['Terminal load bearing [t/m^2]'] >= port['Terminal load bearing [t/m^2]'] ]
    #
    # port['Terminal area [m^2]'] = max(user_inputs['device']['length [m]'].ix[0] * user_inputs['device']['width [m]'].ix[0], sum(area))
    # port_list = port_list[ port_list['Terminal area [m^2]'] >= port['Terminal area [m^2]'] ]
    #
    # port['Port list satisfying the minimum requirements'] = port_list

    # Distance ports-site calculation to be implemented once the transit distance algorithm is available
    # by making use of the grid coordinate position of the site and the ports



    index_dev = 0  # USING POSITION OF FIRST DEVICE!!!
    site_coords_x = hydrodynamic_outputs['x coord [m]'][index_dev]
    site_coords_y = hydrodynamic_outputs['y coord [m]'][index_dev]
    site_coords_zone = hydrodynamic_outputs['zone [-]'][index_dev]
    site_coords = [site_coords_x, site_coords_y, site_coords_zone]
    dist_to_port_vec = []
    for ind_port in range(len(ports)):
        port_coords_x = ports['UTM x [m]'][ind_port]
        port_coords_y = ports['UTM y [m]'][ind_port]
        port_coords_zone = ports['UTM zone [-]'][ind_port]
        port_coords = [port_coords_x, port_coords_y, port_coords_zone]

        if math.isnan(port_coords_x):
            continue
        # dist_to_port_i = transit_algorithm(site_coords, port_coords)
        dist_to_port_i = distance(site_coords, port_coords)  # simplification just for testing
        dist_to_port_vec.append(dist_to_port_i)
        min_dist_to_port = min(dist_to_port_vec)
        if min_dist_to_port == dist_to_port_i:
            port_choice_index = ind_port

    # Nearest port selection to be modified by making use of port['Distance port-site'] will be implemented
    ports['Selected base port for installation'] = ports.ix[port_choice_index]

    return ports, ports.ix[port_choice_index], port_choice_index





def OM_port(wp6_outputs, port_data):
    """OM_port function selects the home port used by all logistic phases
    required by the O&M module. This selection is based on a 2 step process: 
        1 - the port feasibility functions from all logistic phases are taken
        into account, and the unfeasible ports are erased from the panda dataframes.  
        2 - the closest port to the project site is choosen from the feasbile
        list of ports.

    Parameters
    ----------
    user_inputs : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user
    electrical_outputs : dict
     dictionnary containing all required inputs to WP5 coming from WP3
    MF_outputs : DataFrame
     panda table containing all required inputs to WP5 coming from WP4
    port_data : DataFrame
     panda table containing the ports database     

    Returns
    -------
    port : dict
     dictionnary containing the results of the port selection
    """       
    # initialisation
    port = {'Terminal Load Bearing [t/m^2]': 0,
            'Terminal area [m2]': 0,
            'Port list satisfying the minimum requirements': 0,
            'Distance port-site': 0,
            'Selected base port for installation': 0}

    # Calculate loading and projeted area of Spare Parts

    # Input collection
    lenght_SP = wp6_outputs['LogPhase1']['Length_SP [m]'].ix[0]
    width_SP = wp6_outputs['LogPhase1']['Width_SP [m]'].ix[0]
    height_SP = wp6_outputs['LogPhase1']['Height_SP [m]'].ix[0]
    total_mass_SP = wp6_outputs['LogPhase1']['Total_Mass_SP [t]'].ix[0]
    indiv_mass_SP = wp6_outputs['LogPhase1']['Indiv_Mass_SP [t]'].ix[0]

    # Feasibility functions
    SP_area = float(lenght_SP) * float(width_SP)
    SP_loading = float(total_mass_SP) / float(SP_area)

    # terminal load bearing minimum requirement
    port_list = port_data[port_data['Terminal area [m^2]'] >= SP_area]
    port_list = port_list[port_list['Terminal Load Bearing [t/m^2]'] >= SP_loading]

    port['Port list satisfying the minimum requirements'] = port_list

    # Distance ports-site calculation
    # to be implemented once the transit distance algorithm is available
    # by making use of the grid coordinate position of the site and the ports

    # Nearest port selection
    # to be modified by making use of port['Distance port-site'] will be
    # implemented

    port['Selected base port for installation'] = port_list.ix[0]

    return port
