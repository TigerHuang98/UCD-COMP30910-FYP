import numpy as np

import DrawPlotCore

DrawPlotCore.drawPlot('data/dgemmOpenBLASserver2Archive/merged_result/mergedClean', np.arange(27648, 40961, 1024),
                      [1, 2, 4, 11, 22, 44], 44, False)
