import numpy as np

import DrawPlotCore

DrawPlotCore.drawPlot('data/dgemmIntelMKLserver2Archive/merged_result/mergedClean', np.arange(27648, 38913, 1024),
                      [1, 2, 4, 11, 22, 44], 44, False)
