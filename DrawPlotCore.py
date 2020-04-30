import matplotlib.pyplot as plt
import numpy as np
import re


def drawPlot(clean_data_file, n_range, g_set, t__up, step_by_step):
    plt.style.use('seaborn-darkgrid')
    dataDict = dict()
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

    colors = {1: '#1f77b4', 2: '#ff7f0e', 3: '#2ca02c', 4: '#d62728', 6: '#9467bd', 8: '#8c564b', 12: '#e377c2',
              16: '#7f7f7f', 24: '#bcbd22', 48: '#17becf', 11: '#e377c2', 22: '#bcbd22', 44: '#17becf'}

    step_by_step_threshold = 16
    if t__up == 48:
        non_step_by_step_threshold = 20
    else:
        non_step_by_step_threshold = 11

    for N in n_range:
        fig, plot = plt.subplots(figsize=(16, 9))
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

            if G == 1 and step_by_step:
                fitXList = []
                fitYList = []
                for T in np.arange(tStep, tMax + 1, tStep):
                    if T <= step_by_step_threshold:
                        fitdataObj = dataDict.get((str(N), str(G), str(int(T))))
                        fitXList.append(fitdataObj[1])
                        fitYList.append(fitdataObj[3])
                func = np.polyfit(fitXList, fitYList, 2)
                p1 = np.poly1d(func)
                print('N:' + str(N) + ',G:' + str(G) + str(p1))
                XSeries = np.arange(np.min(fitXList), np.max(fitXList))
                fitYValues = p1(XSeries)
                plt.plot(XSeries, fitYValues, ':', color=colors[G])

            if not step_by_step:  # dgemm
                if t__up == 48:  # server1
                    if G != 48:
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
                        if True:  # T <= step_by_step_threshold:
                            fitdataObj = dataDict.get((str(N), str(G), str(int(T))))
                            if fitdataObj:
                                fitXList.append(fitdataObj[1])
                                fitYList.append(fitdataObj[3])
                    func = np.polyfit(fitXList, fitYList, 2)
                    p1 = np.poly1d(func)
                    print('N:' + str(N) + ',G:' + str(G) + str(p1))
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
                    if T == tStep:
                        plt.scatter(dataObj[1], dataObj[3], color='black', s=3)
                    if step_by_step:
                        if T * G <= step_by_step_threshold < (T + tStep) * G:
                            plt.scatter(dataObj[1], dataObj[3], color='black', s=14, marker='*')
                    else:
                        if T * G <= non_step_by_step_threshold < (T + tStep) * G:
                            plt.scatter(dataObj[1], dataObj[3], color='black', s=14, marker='*')
            if True:
                plt.scatter(xList, yList, color=colors[G], label="g = " + str(G))
            # plt.plot(xList, yList, color=colors[G], linewidth=2, alpha=0.6, label=G)
        title_match_obj = re.match(r"data/([^/]*)Archive/.*", clean_data_file)
        if title_match_obj:
            title_prefix = title_match_obj.group(1) + ","
        else:
            title_prefix = ''
        plt.title(title_prefix + "N=" + str(N))
        plot.set_xlabel('Time(s)')
        plot.set_ylabel('DynamicEnergy(J)')
        plt.legend()
        plt.show()
