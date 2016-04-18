# -*- coding: gb18030 -*-
# 第一行的声明，使得在脚本中可以出现中文
#! /user/bin/python
# -*- coding: UTF-8 -*-
#################################################################################################### 
# Example: calling this script in bash
# nProc=9
# pDir=tesst
# EXEC1='/home/zhangjiayong/software/lammps-15May15/lmp_15May15'
# inFile1=neb.lmp
# EXEC2='/home/zhangjiayong/software/lammps-15May15/lmp_15May15_freeEnd_paper'
# inFile2=neb2.lmp
# nLevel=4
# ftol1=0.1
# ftol2=0.003
# etol=0.002
# python FEANEB.py ${nProc} ${pDir} \
#                  ${EXEC1} ${inFile1} ${EXEC2} ${inFile2} \
#                  ${nLevel} ${ftol1} ${ftol2} ${etol}     \
#                  metal Cu
####################################################################################################
#
# FEANEB.py nProc pDir EXEC1 inFile1  EXEC2 inFile2 nLevel ftol1 ftol2 etol
import os
import sys
import string
narg=len(sys.argv[1:])
if narg<10:  print "not enough args"; exit()
#----------------------------------
nProc   =  long(sys.argv[1])
pDir    =       sys.argv[2]
EXEC1   =       sys.argv[3]
inFile1 =       sys.argv[4]
EXEC2   =       sys.argv[5]
inFile2 =       sys.argv[6]
nLevel  =  long(sys.argv[7])
ftol1   = float(sys.argv[8])
ftol2   = float(sys.argv[9])
etol    = float(sys.argv[10])
#----------------------------------
print "######################################################"
print "# nProc   = %d"    %(nProc  )
print "# pDir    = %s"    %(pDir   )
print "# EXEC1   = %s"    %(EXEC1  )
print "# inFile1 = %s"    %(inFile1)
print "# EXEC2   = %s"    %(EXEC2  )
print "# inFile2 = %s"    %(inFile2)
print "# nLevel  = %d"    %(nLevel )
print "# ftol1   = %f"    %(ftol1  )
print "# ftol2   = %f"    %(ftol2  )
print "# etol    = %f"    %(etol   )
#--------------------------------------------------------------------
parAll = ' '
if narg>10:
    if narg%2:
        print "additional parameters are not in pair! please check ..."
        exit()
    pars = [' ']
    for i in range(11,narg,2):
        pars += [sys.argv[i] + ' ' + sys.argv[i+1]]
    parAll = ' -var '.join(item for item in pars) 
    print "# " + parAll
print "######################################################"

def onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps):
    print '######################################################'
    print '# newDir: %s' % (newDir,)
    print '# pDir: %s'   % (pDir,)
    print '# iLevel: %d' % (iLevel,)
    print '# iTrial: %d' % (iTrial,)
    print '# nStep: %d'  % (nStep,)
    print '# resStart: %d' % (resStart,)
    print '# resEnd: %d' % (resEnd,)
    for i in range(len(steps)):
        print '# steps[%d]: %d' % (i,steps[i])
    print '######################################################'
    exit()

def executeCheck(cmd):
    print cmd
    status = os.system(cmd)
    if status: 
        print '%s : encontoured some error!!!' %(cmd,)
    return status


import math
import numpy as np

newDir = pDir
#---------------- FEA-NEB --------------
q=pow(ftol2/ftol1,1.0/(nLevel-1))
ftols = np.zeros([nLevel])
for i in range(nLevel):
    ftols[i]=ftol1*pow(q,i)
    print 'ftol[%d] = %.3f' % (i, ftols[i])
steps = np.zeros([nLevel])

CIK='Last'
CIK=string.lower(CIK) # all none last
iLevel = -1
iTrial = 0
nTrial = 1

while 1:
    iLevel = iLevel + 1
    if iLevel==nLevel: break
    pDir = newDir
    #
    # -------- NEB calculation --------
    #
    if iLevel==0:
        # ---- start Step of FEA-NEB ----
        EXEC=EXEC1; inFile=inFile1
        newDir = '%s_e%.3f' % (pDir,ftols[0])
        if os.path.exists(newDir):
            print 'error: %s already exists!' % (newDir,)
            exit()
        os.system('mkdir ./%s' % (newDir,))
        os.system('mkdir ./%s/res' % (newDir,))
        os.system('cp ./%s/confFinal.restart    ./%s/res' % (pDir, newDir))
        os.system('cp ./%s/confInitial.restart  ./%s/res' % (pDir, newDir))
        os.system('cp ./%s/configuration.final.need ./%s' % (pDir, newDir))
        os.system('cp ./neb.lmp ./%s' % (newDir,))
        os.chdir('./%s' % (newDir,)); print os.getcwd()
        if (not cmp(CIK,'none')):  climbStep = 0
        if (not cmp(CIK,'last')):  climbStep = 0
        if (not cmp(CIK, 'all')):  climbStep = 400000
        cmd = \
        '''mpirun -n %d %s  \
         -partition %dx1    \
         -in %s   %s        \
         -var climbStep %d  \
         -var ftol %.3f''' % (nProc, EXEC, nProc, inFile, parAll, climbStep, ftols[0])
    else:
        # ---- following Steps of FEA-NEB ----
        EXEC=EXEC2; inFile=inFile2
        newDir = '%s_res%dto%d_e%.3f' % (pDir,resStart,resEnd,ftols[iLevel])
        if os.path.exists(newDir):
            print 'error: %s already exists!' % (newDir,)
            onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)
        os.system('mkdir ./%s' % (newDir,))
        os.system('mkdir ./%s/res' % (newDir,))
        if (resStart==1) and (resEnd==nProc):
            os.system('cp ./%s/*%d*.restart   ./%s/res' % (pDir,nStep,newDir))
        else:
            os.system('cp ./%s/%dto%d/*%d*.restart   ./%s/res' % (pDir,resStart,resEnd,nStep,newDir))
        os.system('cp ./neb2.lmp ./%s' % (newDir,))
        os.chdir('./%s' % (newDir,)); print os.getcwd()
        if (not cmp(CIK,'none')):  climbStep = 0
        if (not cmp(CIK,'last')):
            if iLevel==nLevel-1:
                climbStep = 400000
            else:
                climbStep = 0
        if (not cmp(CIK, 'all')):  climbStep = 400000
        cmd = \
        '''mpirun -n %d %s  \
         -partition %sx1    \
         -in %s   %s        \
         -var nStep %d      \
         -var climbStep %d  \
         -var ftol  %.3f''' % ((nProc, EXEC, nProc, inFile, parAll, nStep, climbStep, ftols[iLevel]))
    if executeCheck(cmd): onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)
    #
    # -------- plot the results --------
    #
    # cmd = 'python ../draw_engBarrier_LastLine_ubuntu.pyc';
    # if executeCheck(cmd): onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)
    #
    # -------- check the results --------
    #
    flog = './log.lammps'
    fin=open(flog,'r')
    lastLine=fin.readlines()[-1]
    numarr = lastLine.split()
    data = []
    for numstr in numarr:
        data += [string.atof(numstr),]
    dat = np.array(data)
    steps[iLevel] = dat[0]
    rdist = dat[9::2];
    energy = dat[10::2]; energy = energy - energy[0]
    maxPosi = np.argmax(energy)
    # ediff = energy[maxPosi]-min(energy[maxPosi-1], energy[maxPosi+1])
    maxPosi = maxPosi + 1;
    # ----------------------------------------
    if (maxPosi==1) or (maxPosi==nProc):
        if iLevel<=0:
            print 'the first recursion fails!!!'
            exit()
        # ---- if the highest energy appears at the end nodes
        # recalculate the current recursion with new end nodes
        # if necessary and possible
        # -- if still fails after some trials
        # recalculate the former level
        iTrial = iTrial + 1
        newDir = pDir
        iLevel = iLevel - 1
        if iTrial <= nTrial :
            if (maxPosi==1) and (resStart>1):
                resStart = resStart - 1
                #if resStart>1:    resStart = resStart - 1;
            elif (maxPosi==nProc) and (resEnd<nProc):
                resEnd = resEnd + 1
                #if resEnd<nProc:  resEnd = resEnd + 1
            else:
                print 'maximum energy at the end nodes: %s' % (newDir,)
                onExit(newDir,pDir,iLevel+1,iTrial,nStep,resStart,resEnd,steps)
            os.chdir('../%s' %(pDir,)); print os.getcwd()
            #
            # build restart files by interpolation
            #
            cmd = 'python ../build_NEB_restart.pyc %d %d %d %d' % (steps[iLevel], resStart, resEnd, nProc)
            if executeCheck(cmd): onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)
        elif iTrial <= nTrial+1:
            if (maxPosi==1) and (resStart>1):
                resStart = 1
            elif (maxPosi==nProc) and (resEnd<nProc):
                resEnd = nProc
            else:
                print 'maximum energy at the end nodes: %s' % (newDir,)
                onExit(newDir,pDir,iLevel+1,iTrial,nStep,resStart,resEnd,steps)
            os.chdir('../%s' %(pDir,)); print os.getcwd()
            #
            # build restart files by interpolation
            #
            cmd = 'python ../build_NEB_restart.pyc %d %d %d %d' % (steps[iLevel], resStart, resEnd, nProc)
            if executeCheck(cmd): onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)
        else:
            onExit(newDir,pDir,iLevel+1,iTrial,nStep,resStart,resEnd,steps)
    else:
        if iLevel==nLevel-1: break
        iTrial = 0
        ediff = energy[maxPosi-1]-min(energy[maxPosi-2], energy[maxPosi])
        if ediff<etol:
            # if the energy difference between the highest-energy node
            # and its two neigibors is less than the specified `etol`,
            # go straight to the last level
            resStart = 1
            resEnd = nProc
            nStep = steps[iLevel]
            iLevel = nLevel - 2
        else:
            #
            # execute the next recursion normally
            #
            resStart = maxPosi - 1
            resEnd = maxPosi + 1
            nStep = steps[iLevel] + 1
            #
            # build restart files by interpolation
            #
            cmd = 'python ../build_NEB_restart.pyc %d %d %d %d' % (steps[iLevel], resStart, resEnd, nProc)
            if executeCheck(cmd): onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)
    #
    # -------- back to the upper directory --------
    #
    os.chdir('..'); print os.getcwd()

onExit(newDir,pDir,iLevel,iTrial,nStep,resStart,resEnd,steps)

