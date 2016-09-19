EXEC=/home/zhangjiayong/software/lammps-15May15/lmp_15May15
nProc=`cat /proc/cpuinfo|grep processor|wc -l`

echo "fix   _001 boundary setforce 0 0 0" > extraSetting.lmp_mod
mpirun -n ${nProc} $EXEC        \
       -in SDP_calc.lmp         \
       -var metal Cu            \
       -var nStep 11710         \
       -var iReplica 6          \
       -var extraK   1          \
       -var etol     0          \
       -var ftol     0          \
       -var miniStep 20         \
       -log log.SDP.lammps

