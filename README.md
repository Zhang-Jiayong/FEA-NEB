# FEA-NEB
Free-end adaptive nudged elastic band method for locating transition states in minimum energy path calculation



platform: 

    1) Ubuntu 12.04/14.04

    2) python 2.7.x, with the package 'numpy' installed

    3) LAMMPS 15May15, with the package 'python' installed, 
                       dynamic library that can be called within python scropt
		       other packages that are necessary to your simulation

usage:

    1) replace the file 'fix_neb.cpp' with the original one when compiling LAMMPS
       (the free-end algorithm is implemented in this file)

    2) run the script 'FEANEB.XXX.py' with necessary parameters from the bash terminal
       (a bash script named 'lmprun.sh' is given in the example)

input of FEANEB.XXX.py

    1) integer, nProc,    the number of processers (also the number of images) used in the simulation

    2) string,  pDir,     the path of necessary files with exactly the following names:
                          confInitial.restart        -  restart file of the starting state of the transition process
		          configuration.final.need   -  configuration of the ending state of the transition process

    3) string,  EXEC1,	  LAMMPS executable file used in the first level of the recursion

    4) string,  inFile1,  LAMMPS input file used in the first level of the recursion

    5) string,  EXEC2,    LAMMPS executable file used in the following level of the recursions

    6) string,  inFile2,  LAMMPS input file used in the following level of the recursions

    7) integer, nLevel,   number of levels of the recursions

    8) float,   ftol1,    force tolerance in the first level of the recursion

    9) float,   ftol2,    force tolerance in the final level of the recursion

    10) float,   etol,    energy tolerance: 
                          if the energy difference between the highest energy image and its two neighbours is below this
			  value, no further refinement of the elastic band is performed.

    11) string, varName,  name of optional variable when calling LAMMPS

    12) string, varValue, value of optional variable when calling LAMMPS

output:

    a serious of directories named as 

    e.g. 'pDir_res1to3_e0.03' 
    
    indicating that the calculation in the directory is restarted from the 1st to the 3rd configuration in the former level, and the force tolerance in the current level is 0.03


