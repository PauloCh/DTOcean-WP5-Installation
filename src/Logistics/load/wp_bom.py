# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module imports the upstream data required to run WP5 package. Each function
contains the data sets of the different WPs. All data imported is translated to
panda dataframes.

BETA VERSION NOTES: the module also aims to provide a buffer between the
database source and WP5 package, so it becomes simple to shift from
the temporary .xlsx and .csv files to the final SQL solution.
"""

import pandas as pd

def load_user_inputs(file_path_device):
    """Imports WP1 data set into panda dataframes.

    Parameters
    ----------
    file_path_device : string
     the folder path of the device database

    Returns
    -------
    WP1_BoM : dict
     dictionnary containing all required inputs to WP5 coming from WP1/end-user
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path_device)

    # Collect data from a particular .xls tab
    site = excel.parse('site', header=0, index_col=0)
    metocean = excel.parse('metocean', header=0, index_col=0)
    device = excel.parse('device', header=0, index_col=0)
    sub_device = excel.parse('sub_device', header=0, index_col=0)
    landfall = excel.parse('landfall', header=0, index_col=0)

    # Splits the different dataset through different dict keys()
    user_inputs = {'site': site,
                   'metocean': metocean,
                   'device': device,
                   'sub_device': sub_device,
                   'landfall': landfall
                  }

    return user_inputs


def load_hydrodynamic_outputs(file_path):
    """Imports WP2 data set into panda dataframes.

    Parameters
    ----------
    file_path : string
     the folder path of the WP2 database

    Returns
    -------
    WP2_BoM : dict
     dictionnary containing all required inputs to WP5 coming from WP2
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    hydrodynamic_outputs = excel.parse('Units', header=0, index_col=0)

    return hydrodynamic_outputs


def load_electrical_outputs(file_path):
    """Imports WP3 data set into panda dataframes.

    Parameters
    ----------
    file_path : string
     the folder path of the WP3 database

    Returns
    -------
    WP3_BoM : dict
     dictionnary containing all required inputs to WP5 coming from WP3
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    collection_point = excel.parse('collection point', header=0, index_col=0)
    dynamic_cable = excel.parse('dynamic cable', header=0, index_col=0)
    static_cable = excel.parse('static cable', header=0, index_col=0)
    cable_route = excel.parse('cable route', header=0, index_col=0)
    connectors = excel.parse('connectors', header=0, index_col=0)
    external_protection = excel.parse('external protection', header=0, index_col=0)
    layout = excel.parse('layout', header=0, index_col=0)

    # Splits the different dataset through different dict keys()
    electrical_outputs = {'collection point': collection_point,
                          'dynamic cable': dynamic_cable,
                          'static cable': static_cable,
                          'cable route': cable_route,
                          'connectors': connectors,
                          'external protection': external_protection,
                          'layout': layout
                          }

    return electrical_outputs


def load_MF_outputs(file_path):
    """Imports WP4 data set into panda dataframes.

    Parameters
    ----------
    file_path : string
     the folder path of the WP4 database

    Returns
    -------
    WP4_BoM : Dataframe
     Dataframe containing all required inputs to WP5 coming from WP4
    """
    # Transform the .csv database into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    line = excel.parse('line', header=0, index_col=0)
    foundation = excel.parse('foundation', header=0, index_col=0)

    # Splits the different dataset through different dict keys()
    MF_outputs = {'line': line,
                  'foundation': foundation,
                  }

    return MF_outputs


def load_OM_outputs(file_path):
    """Imports WP6 data set into panda dataframes.

    Parameters
    ----------
    file_path : string
     the folder path of the WP6 database

    Returns
    -------
    WP6_BoM : Dataframe
     Dataframe containing all required inputs to WP5 coming from WP6
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path)

    # Collect data from a particular tab
    OM_outputs = excel.parse('OM', header=0, index_col=0)

    return OM_outputs
