import matplotlib.pyplot as plt
import numpy as np
import re
import copy


class dataPoint:
    def __init__(self, N, G, T, dynEnergy, time):
        self.N = float(N)
        self.G = float(G)
        self.T = float(T)
        self.dynEnergy = float(dynEnergy)
        self.time = float(time)


def isParetoFront(costs):
    results = np.ones(costs.shape[0], dtype=bool)
    for index, cost in enumerate(costs):
        results[index] = np.all(  # for all points
            np.any(costs[:index] > cost, axis=1)  # for any character
        ) \
                         and \
                         np.all(
                             np.any(costs[index + 1:] > cost, axis=1)
                         )
    return results


def drawPlot(clean_data_file, n_range, g_set, t__up, step_by_step):
    plt.style.use('seaborn-darkgrid')
    dataDict = dict()
    dataPointDict = dict()
    lines = open(clean_data_file, 'r').readlines()
    for line in lines:
        matchObj = re.match(
            r"N=(\d*), G=(\d*), T=(\d*), DummyTotalEnergy\(J\)=(\d+(?:\.\d+)?), Time\(s\)=(\d+(?:\.\d+)?), TotalEnergy\(J\)=(\d+(?:\.\d+)?), DynamicEnergy\(J\)=(\d+(?:\.\d+)?)",
            line.rstrip('\n'))
        if matchObj:
            if (matchObj.group(1), matchObj.group(2), matchObj.group(3)) in dataDict:
                print("Warning: over writing duplicate keys N=" + matchObj.group(1) + ", G=" + matchObj.group(
                    2) + ", T=" + matchObj.group(3))
            dataDict[matchObj.group(1), matchObj.group(2), matchObj.group(3)] = float(matchObj.group(4)), float(
                matchObj.group(5)), float(matchObj.group(6)), float(matchObj.group(7))
            if matchObj.group(1)in dataPointDict:
                dataPointDict[matchObj.group(1)].append(
                    dataPoint(matchObj.group(1), matchObj.group(2), matchObj.group(3), matchObj.group(7),
                              matchObj.group(5)))
            else:
                dataPointDict[matchObj.group(1)] = [
                    dataPoint(matchObj.group(1), matchObj.group(2), matchObj.group(3), matchObj.group(7),
                              matchObj.group(5))]

    colors = {1: '#1f77b4', 2: '#ff7f0e', 3: '#2ca02c', 4: '#d62728', 6: '#9467bd', 8: '#8c564b', 12: '#e377c2',
              16: '#7f7f7f', 24: '#bcbd22', 48: '#17becf', 11: '#e377c2', 22: '#bcbd22', 44: '#17becf'}

    step_by_step_threshold = 16
    if t__up == 48:
        non_step_by_step_threshold = 20
    else:
        non_step_by_step_threshold = 11

    for N in n_range:
        fig, plot = plt.subplots(figsize=(8, 6))
        total_fit_flag = False
        if total_fit_flag:
            fitXall = []
            fitYall = []

        G1xList = []
        G2xList = []
        G3pxList = []
        G1yList = []
        G2yList = []
        G3pyList = []

        NG1xList = []  #
        NG1yList = []  #




        dataPointList=dataPointDict[str(N)]
        costList=[]
        for point in dataPointList:
            costList.append([point.time,point.dynEnergy])
        paretoFrontResult=isParetoFront(np.array(costList))
        paretoFrontList=[]
        for index,point in enumerate(dataPointList):
            if paretoFrontResult[index]:
                paretoFrontList.append(copy.deepcopy(point))
        paretoFrontList.sort(key=lambda point:point.time)


        for G in g_set:
            xList = []
            yList = []
            tMax = t__up / G

            if step_by_step:
                tStep = 1
            else:
                if tMax >= 12:
                    tStep = 4
                elif tMax >= 6:
                    tStep = 2
                else:
                    tStep = 1

            if G == 1 and step_by_step and not total_fit_flag:
                fitXList = []
                fitYList = []
                for T in np.arange(tStep, tMax + 1, tStep):
                    if T <= step_by_step_threshold:
                        fitdataObj = dataDict.get((str(N), str(G), str(int(T))))
                        fitXList.append(fitdataObj[1])
                        fitYList.append(fitdataObj[3])
                func = np.polyfit(fitXList, fitYList,
                                  2)  # change the last parameter to 1 to get straight line for FFTIntelMKL
                p1 = np.poly1d(func)
                print('N:' + str(N) + ',G:' + str(G) + str(p1))
                XSeries = np.arange(np.min(fitXList), np.max(fitXList) + 1)
                fitYValues = p1(XSeries)
                plt.plot(XSeries, fitYValues, ':', color=colors[G])

            ##tmp
            if G != 1 and step_by_step:
                for T in np.arange(tStep, tMax + 1, tStep):
                    if T <= step_by_step_threshold:
                        fitdataObj = dataDict.get((str(N), str(G), str(int(T))))
                        if fitdataObj:
                            NG1xList.append(fitdataObj[1])
                            NG1yList.append(fitdataObj[3])
                        ##tmp

            if not step_by_step:  # dgemm
                if t__up == 48:  # server1
                    if G == 1:
                        fitXList1 = []
                        fitYList1 = []
                        fitXList2 = []
                        fitYList2 = []
                        for T in np.arange(tStep, tMax + 1, tStep):
                            fitdataObj = dataDict.get((str(N), str(G), str(int(T))))
                            if fitdataObj != None:
                                if G * T <= non_step_by_step_threshold:
                                    fitXList1.append(fitdataObj[1])
                                    fitYList1.append(fitdataObj[3])
                                else:
                                    fitXList2.append(fitdataObj[1])
                                    fitYList2.append(fitdataObj[3])

                        if len(fitXList1) != 0:
                            func1 = np.polyfit(fitXList1, fitYList1, 1)
                            p1 = np.poly1d(func1)
                            print('func 1:  N:' + str(N) + ',G:' + str(G) + str(p1))
                            XSeries1 = np.arange(np.min(fitXList1), np.max(fitXList1))
                            fitYValues1 = p1(XSeries1)
                            plt.plot(XSeries1, fitYValues1, '-.', color=colors[G])

                        if len(fitXList2) != 0:
                            func2 = np.polyfit(fitXList2, fitYList2, 1)
                            p2 = np.poly1d(func2)
                            print('func 2:  N:' + str(N) + ',G:' + str(G) + str(p2))
                            XSeries2 = np.arange(np.min(fitXList2), np.max(fitXList2))
                            fitYValues2 = p2(XSeries2)
                            plt.plot(XSeries2, fitYValues2, ':', color=colors[G])
                else:  # server 2
                    fitXList = []
                    fitYList = []
                    for T in np.arange(tStep, tMax + 1, tStep):
                        if G == 1:  # T <= step_by_step_threshold:
                            fitdataObj = dataDict.get((str(N), str(G), str(int(T))))
                        if fitdataObj:
                            fitXList.append(fitdataObj[1])
                            fitYList.append(fitdataObj[3])
                    if G == 1:
                        func = np.polyfit(fitXList, fitYList, 2)
                        p1 = np.poly1d(func)
                        print('N:' + str(N) + ',G:' + str(G) + str(p1).strip())
                    XSeries = np.arange(np.min(fitXList), np.max(fitXList))
                    fitYValues = p1(XSeries)
                    plt.plot(XSeries, fitYValues, ':', color=colors[G])

            for T in np.arange(tStep, tMax + 1, tStep):
                # print(str(N) + ',' + str(G) + ',' + str(T) + ','+str(dataDict[str(N),str(G),str(int(T))]))
                dataObj = dataDict.get((str(N), str(G), str(int(T))))
                if dataObj:
                    # plt.scatter(dataObj[1], dataObj[3], color=colors[G], label=G)
                    xList.append(dataObj[1])
                    yList.append(dataObj[3])
                    if G == 1:
                        G1xList.append(dataObj[1])
                        G1yList.append(dataObj[3])
                    if G == 2:
                        G2xList.append(dataObj[1])
                        G2yList.append(dataObj[3])
                    if G >= 3:
                        G3pxList.append(dataObj[1])
                        G3pyList.append(dataObj[3])
                    if total_fit_flag:
                        fitXall.append(dataObj[1])
                        fitYall.append(dataObj[3])
                    if T == tStep:
                        plt.scatter(dataObj[1], dataObj[3], color='black', s=3)
                    if step_by_step:
                        if T * G <= step_by_step_threshold < (T + tStep) * G:
                            plt.scatter(dataObj[1], dataObj[3], color='black', s=14, marker='*')
                    else:
                        if T * G <= non_step_by_step_threshold < (T + tStep) * G:
                            plt.scatter(dataObj[1], dataObj[3], color='black', s=14, marker='*')
            if False:
                plt.scatter(xList, yList, color=colors[G], label="g = " + str(G))
            # plt.plot(xList, yList, color=colors[G], linewidth=2, alpha=0.6, label=G)

        plt.scatter(G1xList, G1yList, color=colors[1], label="g = 1")
        plt.scatter(G2xList, G2yList, color=colors[2], label="g = 2")
        plt.scatter(G3pxList, G3pyList, color=colors[3], label="g >= 3")

        title_match_obj = re.match(r"data/([^/]*)Archive/.*", clean_data_file)
        if title_match_obj:
            title_prefix = title_match_obj.group(1) + ","
        else:
            title_prefix = ''
        plt.title(title_prefix + "N=" + str(N))
        plot.set_xlabel('Time(s)')
        plot.set_ylabel('DynamicEnergy(J)')
        if total_fit_flag:
            func = np.polyfit(fitXall, fitYall, 2)
            p1 = np.poly1d(func)
            XSeries = np.arange(np.min(fitXall), np.max(fitXall))
            fitYValues = p1(XSeries)
            plt.plot(XSeries, fitYValues)
            print("fit all" + str(p1))
        if step_by_step:
            func = np.polyfit(NG1xList, NG1yList, 1)
            p1 = np.poly1d(func)
            # print('N:' + str(N) + ',G:1++' + str(p1))
            XSeries = np.arange(np.min(fitXList), np.max(fitXList) + 1)
            fitYValues = p1(XSeries)
            # plt.plot(XSeries, fitYValues, ':', color=colors[G]) # uncomment this line for FFTIntelMKL


        paretoFrontX=[]
        paretoFrontY=[]

        print('pareto front for N='+str(N)+':')

        for point in paretoFrontList:
            paretoFrontX.append(point.time)
            paretoFrontY.append(point.dynEnergy)
            print('G='+str(point.G)+',T='+str(point.T)+',time='+str(point.time)+',dynEnergy='+str(point.dynEnergy))

        plt.scatter(paretoFrontX, paretoFrontY,marker='x', color='red')
        plt.plot(paretoFrontX,paretoFrontY,color='red')

        plt.legend()
        plt.show()
