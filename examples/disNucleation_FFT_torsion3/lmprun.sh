# written by zhangjiayong

nProc=9
pDir=N9
EXEC1='/home/zhangjiayong/software/lammps-15May15/lmp_15May15'
inFile1=neb.lmp
EXEC2='/home/zhangjiayong/software/lammps-15May15/lmp_15May15_freeEnd_paper'
inFile2=neb2.lmp
nLevel=4
ftol1=0.1
ftol2=0.003
etol=0.002
python FEANEB_v3.2_publish.py ${nProc} ${pDir} \
                 ${EXEC1} ${inFile1} ${EXEC2} ${inFile2} \
                 ${nLevel} ${ftol1} ${ftol2} ${etol}     \
                 metal Cu
