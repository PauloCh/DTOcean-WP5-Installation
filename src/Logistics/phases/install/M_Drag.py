from .classes import DefPhase, LogPhase


def initialize_m_drag_phase(log_op, vessels, equipments, MF_outputs):

    # save outputs required inside short named variables
    found_db = MF_outputs['foundation']
    drag_db = found_db[found_db['type [-]'] == 'drag-embedment anchor']

    # initialize logistic phase
    phase = LogPhase(113, "Installation of mooring systems with drag-embedment anchors")

    ''' Deploy drag-embedment anchor installation strategy'''

    # initialize strategy
    phase.op_ve[0] = DefPhase(1, 'Deploy drag-embedment anchor')

    # define vessel and equipment combinations suited for this strategy
    phase.op_ve[0].ve_combination[0] = {'vessel': [(1, vessels['AHTS'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    phase.op_ve[0].ve_combination[1] = {'vessel': [(1, vessels['Multicat'])],
                                        'equipment': [(1, equipments['rov'], 0)]}

    # define initial mobilization and onshore preparation tasks
    phase.op_ve[0].op_seq_prep = [log_op["Mob"],
                                  log_op["AssPort"],
                                  log_op["VessPrep"]]

    # iterate over the list of elements to be installed.
    # each element is associated with a customized operation sequence depending on it's characteristics
    for index, row in drag_db.iterrows():

        # initialize an empty operation sequence list for the 'index' element
        phase.op_ve[0].op_seq_sea[index] = []

        phase.op_ve[0].op_seq_sea[index].extend([ log_op["SeafloorEquipPrep"],
                                                  log_op["DragEmbed"],
                                                  log_op["PreLay"] ])

    # define final demobilization tasks
    phase.op_ve[0].op_seq_demob = [log_op["Demob"]]

    return phase
