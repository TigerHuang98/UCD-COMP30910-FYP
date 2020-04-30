import numpy as np

import DrawPlotCore

DrawPlotCore.drawPlot('data/dgemmIntelMKLserver1Archive/merged_result/mergedClean', np.arange(16384, 36865, 1024),
                      [1, 2, 3, 4, 6, 8, 12, 16, 24, 48], 48, False)
