# -*- coding: utf-8 -*-
"""
@author: WavEC Offshore Renewables
email: boris.teillant@wavec.org; paulo@wavec.org

This module governs the definition of the logistic phases. The functions included
are responsible to initialize and characterize the logistic phases both of the
installation and O&M modules. The functions return a class of each logistic phase
characterized in terms of operations sequence and vessel & equipment combination.

BETA VERSION NOTES: In this version, only two logistic phases were characterized,
one related to Moorings and Foundation Installation: Driven Pile, and another
related to Operation and Maintenance: Offshore Inspection.
"""

from .classes import LogPhase, DefPhase

from .e_export import initialize_e_export_phase
from .e_array import initialize_e_array_phase
from .e_cp import initialize_e_cp_phase

from .Driven import initialize_drive_phase
from .Gravity import initialize_gravity_phase

from .M_Drag import initialize_m_drag_phase
from .M_Direct import initialize_m_direct_phase
from .M_Suction import initialize_m_suction_phase

from .devices import initialize_devices_phase


def logPhase_install_init(log_op, vessels, equipments, user_inputs, electrical_outputs, MF_outputs):
    """This function initializes and characterizes all logistic phases associated
    with the installation module. The first step uses LogPhase class to initialize
    each class with a key ID and description, the second step uses the DefPhase
    class to characterize each phase with a set of operation sequences and vessel
    and equipment combinations.
    Explanation of the key ID numbering system implemented:
     1st digit: 1 = Installation;
                9 = O&M
     2nd digit: 0 = Electrical infrastructure;
                1 = Moorings and foundations;
                2 = Wave and Tidal devices;
     3rd digit: component/sub-system type - differ depending on the logistic phase
     4th digit: method (level 1) - differ depending on the logistic phase
     5th digit: sub-method (level 2) - differ depending on the logistic phase

    Parameters
    ----------
    log_op : dict
     dictionnary containing all classes defining the individual logistic operations
    vessels : DataFrame
     Panda table containing the vessel database
    equipments : DataFrame
     Panda table containing the equipment database

    Returns
    -------
    logPhase_install : dict
     dictionnary containing all classes defining the logistic phases for installation
    """

    # 1st Level - Initialize the logistic phases through LogPhase classes

    logPhase_install = {
                        'E_export': initialize_e_export_phase(log_op, vessels, equipments, electrical_outputs)
                        , 'E_array': initialize_e_array_phase(log_op, vessels, equipments, electrical_outputs)
                        , 'E_cp': initialize_e_cp_phase(log_op, vessels, equipments, electrical_outputs)

                        , 'Driven': initialize_drive_phase(log_op, vessels, equipments)
                        , 'Gravity': initialize_gravity_phase(log_op, vessels, equipments, MF_outputs)
                        , 'M_Drag': initialize_m_drag_phase(log_op, vessels, equipments)
                        , 'M_Direct': initialize_m_direct_phase(log_op, vessels, equipments, MF_outputs)
                        , 'M_Suction': initialize_m_suction_phase(log_op, vessels, equipments)

                        , 'Devices': initialize_devices_phase(log_op, vessels, equipments, user_inputs)
                        }

    return logPhase_install



