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

def load_WP1_BoM(file_path_device, file_path_metocean):
    """Imports WP1 data set into panda dataframes.

    :param file_path_device (str): the folder path of the device database
    :param file_path_metocean (str): the folder path of the metocean database
    :returns: A dict of panda dataframes
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path_device)
    metocean = pd.read_csv(file_path_metocean)
    # Collect data from a particular .xls tab
    device = excel.parse('device', header=0, index_col=0)
    # Splits the different dataset through different dict keys()
    WP1_BoM = {'device': device,
               'metocean': metocean
               }

    return WP1_BoM


def load_WP2_BoM(file_path):
    """Imports WP2 data set into panda dataframes.

    :param file_path (str): the folder path of the WP2 database
    :returns: A dict of panda dataframes
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    units = excel.parse('units', header=0, index_col=0)
    position = excel.parse('position', header=0, index_col=0)
    # Splits the different dataset through different dict keys()
    WP2_BoM = {'NumOFunits': units,
               'Position': position
               }

    return WP2_BoM


def load_WP3_BoM(file_path):
    """Imports WP3 data set into panda dataframes.

    :param file_path (str): the folder path of the WP3 database
    :returns: A dict of panda dataframes
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    layout = excel.parse('Sheet1', header=0, index_col=0)
    # Splits the different dataset through different dict keys()
    WP3_BoM = {'layout': layout,
               }

    return WP3_BoM


def load_WP4_BoM(file_path):
    """Imports WP4 data set into panda dataframes.

    :param file_path (str): the folder path of the WP4 database
    :returns: A panda dataframe
    """
    # Transform the .csv database into panda type
    WP4_BoM = pd.read_csv(file_path)

    return WP4_BoM


def load_WP6_BoM(file_path):
    """Imports WP6 data set into panda dataframes.

    :param file_path (str): the folder path of the WP6 database
    :returns: A dict of panda dataframes
    """
    # Transform the .xls database into panda type
    excel = pd.ExcelFile(file_path)
    # Collect data from a particular tab
    wp6inputs = excel.parse('Sheet1', header=0, index_col=0)
    # Splits the different dataset through different dict keys()
    WP6_BoM = {'LogPhase1': wp6inputs,
               }

    return WP6_BoM
