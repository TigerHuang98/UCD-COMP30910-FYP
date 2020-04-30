import numpy as np

import DrawPlotCore

DrawPlotCore.drawPlot('data/dgemmOpenBLASserver1Archive/merged_result/mergedClean', np.arange(16384, 35841, 1024),
                      [1, 2, 3, 4, 6, 8, 12, 16, 24, 48], 48, False)
