import matplotlib.pyplot as plt
import numpy as np
import bbcpy
import scipy.io as sio
from vitalbci_funcs import *
import glob
from scipy.stats import ranksums

vp_fb_parameters = sio.loadmat('C:/data/results/studies/vitalbci_season1/vp_fb_parameters.mat')
classes = vp_fb_parameters['classes']

performance = sio.loadmat('C:/data/results/studies/vitalbci_season1/performance.mat')

lwfresults = glob.glob(
    'C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_fb_lwf_*_excl_lesschans.npz')
scmresults = glob.glob(
    'C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_fb_scm_*excl_lesschan*.npz')

lwfexclparams = [x[x.find('_excl') - 2:x.find('_excl')] for x in lwfresults]
scmexclparams = [x[x.find('_excl') - 2:x.find('_excl')] for x in scmresults]

lwfresults_data = []
for i in range(len(lwfresults)):
    lwfresults_data.append(np.load(lwfresults[i], allow_pickle=True))
scmresults_data = []
for i in range(len(scmresults)):
    scmresults_data.append(np.load(scmresults[i], allow_pickle=True))

dataset = bbcpy.load.eeg.dataset('C:/data/results/studies/vitalbci_season1/bbcpy_datsnip.npy')

bestexcl = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][scmresults_data[0].files[0]]), 6), int)
bestest = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][scmresults_data[0].files[0]]), 6), int)
best = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][scmresults_data[0].files[0]]), 6))
for ifile, file in enumerate(scmresults_data[0].files):
    for isubj in range(len(scmresults_data[0][file])):
        othersubj = np.arange(len(scmresults_data[0][file]))
        othersubj = othersubj[othersubj != isubj]
        res = np.zeros((len(scmresults_data), 2, *scmresults_data[0][file].shape))
        for iexcl in range(len(scmresults_data)):
            res[iexcl, 0] = scmresults_data[iexcl][file]
            res[iexcl, 1] = lwfresults_data[iexcl][file]
        bestest_tmp = res[:, :, :, :, 0][:, :, othersubj].mean(axis=2).argmax(axis=1)
        bestexcl[ifile, isubj] = res[:, :, :, :, 0][:, :, othersubj].mean(axis=2).max(axis=1).argmax(axis=0)
        bestest[ifile, isubj] = bestest_tmp[bestexcl[ifile, isubj], range(len(bestexcl[ifile, isubj]))]
        best[ifile, isubj] = res[bestexcl[ifile, isubj], bestest[ifile, isubj], [isubj] * len(bestexcl[ifile, isubj]),
                                 range(len(bestexcl[ifile, isubj])), 0]
plt.figure()
plt.boxplot(best[0])
ranksums(best[0, :, 1], best[0, :, 3])
plt.figure()
plt.scatter(best[0, :, 1], best[0, :, 3])
plt.plot([0.5, 1], [0.5, 1])

bestexcl_roc = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][file]), 6), int)
bestest_roc = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][file]), 6), int)
best_roc = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][file]), 6))
for ifile, file in enumerate(scmresults_data[0].files):
    for isubj in range(len(scmresults_data[0][file])):
        othersubj = np.arange(len(scmresults_data[0][file]))
        othersubj = othersubj[othersubj != isubj]
        res = np.zeros((len(scmresults_data), 2, *scmresults_data[0][file].shape))
        for iexcl in range(len(scmresults_data)):
            res[iexcl, 0] = scmresults_data[iexcl][file]
            res[iexcl, 1] = lwfresults_data[iexcl][file]
        bestest_tmp = res[:, :, :, :, 1][:, :, othersubj].mean(axis=2).argmax(axis=1)
        bestexcl_roc[ifile, isubj] = res[:, :, :, :, 1][:, :, othersubj].mean(axis=2).max(axis=1).argmax(axis=0)
        bestest_roc[ifile, isubj] = bestest_tmp[bestexcl_roc[ifile, isubj], range(len(bestexcl_roc[ifile, isubj]))]
        best_roc[ifile, isubj] = res[bestexcl[ifile, isubj], bestest_roc[ifile, isubj],
                                     [isubj] * len(bestexcl_roc[ifile, isubj]), range(len(bestexcl[ifile, isubj])), 0]
plt.figure()
plt.boxplot(best_roc[0])
ranksums(best_roc[0, :, 1], best_roc[0, :, 3])
