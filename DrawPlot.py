import matplotlib.pyplot as plt
import numpy as np
import re

plt.style.use('seaborn-darkgrid')
dataDict = dict()
lines = open('data/dgemmOpenBLASserver1Archive/merged_result/mergedClean', 'r').readlines()
for line in lines:
    matchObj = re.match(
        r"N=(\d*), G=(\d*), T=(\d*), DummyTotalEnergy\(J\)=(\d+(?:\.\d+)?), Time\(s\)=(\d+(?:\.\d+)?), TotalEnergy\(J\)=(\d+(?:\.\d+)?), DynamicEnergy\(J\)=(\d+(?:\.\d+)?)",
        line.rstrip('\n'))
    if matchObj:
        dataDict[matchObj.group(1), matchObj.group(2), matchObj.group(3)] = float(matchObj.group(4)), float(
            matchObj.group(5)), float(matchObj.group(6)), float(matchObj.group(7))

colors = {1: '#1f77b4', 2: '#ff7f0e', 3: '#2ca02c', 4: '#d62728', 6: '#9467bd', 8: '#8c564b', 12: '#e377c2',
         16: '#7f7f7f', 24: '#bcbd22', 48: '#17becf'}

for N in np.arange(16384, 35841, 1024):
    fig, plot = plt.subplots(figsize=(16, 9))
    for G in 1, 2, 3, 4, 6, 8, 12, 16, 24, 48:
        xList=[]
        yList=[]
        tMax = 48 / G

        if tMax >= 12:
            tStep = 4
        elif tMax >= 6:
            tStep = 2
        else:
            tStep = 1

        for T in np.arange(tStep, tMax + 1, tStep):
            # print(str(N) + ',' + str(G) + ',' + str(T) + ','+str(dataDict[str(N),str(G),str(int(T))]))
            dataObj = dataDict.get((str(N), str(G), str(int(T))))
            if dataObj:
                plt.scatter(dataObj[1], dataObj[3], color=colors[G])
                xList.append(dataObj[1])
                yList.append(dataObj[3])
        plt.plot(xList, yList, color=colors[G], linewidth=2, alpha=0.6,label=G)
    plt.title("N=" + str(N))
    plot.set_xlabel('Time(s)')
    plot.set_ylabel('DynamicEnergy(J)')
    plt.legend()
    plt.show()
