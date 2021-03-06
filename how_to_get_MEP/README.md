How to get the MEP/SDP

    After the transition state is captured, the MEP can be tracked by calculating the Steepest Descent Path (SDP) from the transition state.

    The script 'SDP_calc.lmp' can be used to get the SDP.

    It is easy to learn to use 'SDP_calc.lmp' if you are familiar to Lammps. Just see the bash script 'lmprun.sh'

    I would to say something about how this script works:

    The initial state is the transition state or a neighbor of it, and the 'sd' minimizor is adopted to drive the configuration to move along the SDP.

    Every 20 steps, the potential energy of the configuration is recorded, and the distance between the current configuration and the former configuration is recorded.

    so the recorded data is in the following style:

    global coordinate | recorded distance | recorded energy
    #--------------------------------
     0          0        100.0
     0.1        0.1       99.9
     0.21       0.11      99.8
     0.30       0.09      99.7   

    the recorded data is:

    1) the distance between neighboring points on the SDP

    2) the potential energy on these points

    However, these data is 'hidden' in the log-file, and it is a annoying work to pick these data up manually.

    So I provide a python script 'extract_SDP_redump.py' to do this job.

    put the 'log.SDP.lammps' and 'extract_SDP_redump.py' in the same folder, and double-click the 'extract_SDP_redump.py', and the data will be extracted automatically.

How to get the 'whole' MEP/SDP

    From the calculated transiton state, we can only get one side of the MEP, that's to say, tha portion from the transiton state to the reactant/initial-state OR the product/final-state.

    That's is because the calculated transition state is slightly away from the real transition state and is is on one side of the ridge of the Potential Energy Surface (PES).

    The strategy to get the whole MEP is rather straight-forward:

    In the last level of recursion in the FEA-NEB calculation, the two neighbors of the transition state is certainly on two different sides of the ridge of the PES.

    Starting from these two replicas, two halves of the MEP can be calculated, and some more work is needed to join them together, and it is easy.

Good Luck!