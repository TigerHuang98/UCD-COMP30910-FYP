import numpy as np

import DrawPlotCore

DrawPlotCore.drawPlot('data/fftFFTWserver2Archive/merged_result/mergedClean', np.arange(16384, 35841, 1024),
                      [1, 2, 4, 11, 22, 44], 44, True)
