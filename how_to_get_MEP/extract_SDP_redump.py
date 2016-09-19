# -*- coding: gb18030 -*-   
# 第一行的声明，使得在脚本中可以出现中文

import os
import string


fin=open('log.SDP.lammps','r')
fout=open('log.data.lammps','w')

data=[];
keyMini=0; key=0; 
lastStep=-1
for eachLine in fin:
    eachLine = eachLine.strip()
    if len(eachLine)==0:
        continue
    # minimize 命令之后才开始统计，之前的不管
    if keyMini==0:
        if eachLine[0:8]=='minimize':
            numarr = eachLine.split();
            if not(numarr[-1].isdigit()):
                continue
            if numarr[-1]!='0' and numarr[-1]!='1':
                keyMini=1
        continue

    # 行首 Step 为统计开始字符，行首 Loop 为统计结束字符
    if key==0 and eachLine[0:4]=='Step':
        key=1
        continue
    elif key==1:
        if eachLine[0:4]=='Loop':
            key = 0
            # 遇到Loop, 同时把 keyMini 置零，则表示只读取 minimize 对应的模块
            keyMini = 0
            continue
        elif eachLine[0:7]=='WARNING':
            continue
        elif eachLine[0:7]=='ERROR':
            key=0
            continue

    # "转存"数据
    if key==1:
        
        numarr = eachLine.split();
        currentStep = string.atoi(numarr[0])
        if currentStep<=lastStep:
            continue
        #else:
            #print lastStep, currentStep
        fout.write(eachLine+'\n')
        arr = []
        for numstr in numarr:
            arr += [string.atof(numstr),]
        data += [arr,]
        lastStep=currentStep
    #else:
        #fout.write(eachLine[0:4]+" key==0\n")
    
fin.close()
fout.close()

# 检查最后一行是否完整
if len(data[-1])<len(data[0]):
    del data[-1]

import numpy as np
import matplotlib.pyplot as plt
dat = np.array(data)
mn = dat.shape; m = mn[0]; n = mn[1]

step=dat[:,0]
disp_diff=dat[:,1]
PE=dat[:,2]
disp=np.zeros((m,1),np.float64)
for i in range(m):
    if i==0:
        continue
    disp[i]=disp[i-1]+disp_diff[i]

# plot rdist-PotEng 
fig = plt.figure(); 
plt.plot(disp,PE,'-r')
plt.xlabel('rdist')
plt.ylabel('PE')
#show()
plt.savefig('SDP.png', transparent=True)
plt.close(fig)

# plot step-PotEng 
fig = plt.figure(); 
plt.plot(step,disp,'-r')
plt.xlabel('step')
plt.ylabel('disp')
#show()
plt.savefig('SDP_disp.png', transparent=True)
plt.close(fig)

# plot step-PotEng 
fig = plt.figure(); 
plt.plot(step,PE,'-r')
plt.xlabel('step')
plt.ylabel('PE')
#show()
plt.savefig('SDP_PE.png', transparent=True)
plt.close(fig)

print "succeed!" + "\n" + "press any key to continue ..."
raw_input()