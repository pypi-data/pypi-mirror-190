import matplotlib.pyplot as plt
import numpy as np
import bbcpy
import scipy.io as sio
from vitalbci_funcs import *
import glob
from scipy.stats import ranksums

vp_fb_parameters = sio.loadmat('C:/data/results/studies/vitalbci_season1/vp_fb_parameters.mat')
classes = vp_fb_parameters['classes']
bands = vp_fb_parameters['band']
bandinds = bands[:, 0] >= 13

performance = sio.loadmat('C:/data/results/studies/vitalbci_season1/performance.mat')

lwfresults = glob.glob('C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_lwf*None_lesschan*.npz')
lwfresults_roc = glob.glob('C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_lwf*roc_auc_lesschan'
                           '*.npz')
scmresults = glob.glob('C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_scm*None_lesschan*.npz')
scmresults_roc = glob.glob('C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_scm*roc_auc_lesschan'
                           '*.npz')
lwfexclparams = [x[x.find('_excl') - 2:x.find('_excl')] for x in lwfresults]
scmexclparams = [x[x.find('_excl') - 2:x.find('_excl')] for x in scmresults]

lwfresults_data = []
for i in range(len(lwfresults)):
    lwfresults_data.append(np.load(lwfresults[i], allow_pickle=True))

lwfresults_roc_data = []
for i in range(len(lwfresults)):
    lwfresults_roc_data.append(np.load(lwfresults_roc[i], allow_pickle=True))

scmresults_data = []
for i in range(len(scmresults)):
    scmresults_data.append(np.load(scmresults[i], allow_pickle=True))

scmresults_roc_data = []
for i in range(len(scmresults)):
    scmresults_roc_data.append(np.load(scmresults_roc[i], allow_pickle=True))

# for key in data.files:
#    globals()[key] = data.get(key)
# data.close()

dataset = bbcpy.load.eeg.dataset('C:/data/results/studies/vitalbci_season1/bbcpy_datsnip.npy')

bestexcl = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][scmresults_data[0].files[0]]), 8), int)
bestest = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][scmresults_data[0].files[0]]), 8), int)
best = np.zeros((len(scmresults_data[0].files), len(scmresults_data[0][scmresults_data[0].files[0]]), 8))
for ifile, file in enumerate(scmresults_data[0].files):
    for isubj in range(len(scmresults_data[0][file])):
        othersubj = np.arange(len(scmresults_data[0][file]))
        othersubj = othersubj[othersubj != isubj]
        res = np.zeros((len(scmresults_data), 2, *scmresults_data[0][file].shape))
        for iexcl in range(len(scmresults_data)):
            res[iexcl, 0] = scmresults_data[iexcl][file]
            res[iexcl, 1] = lwfresults_data[iexcl][file]
        bestest_tmp = res[:, :, othersubj].mean(axis=2).mean(axis=3).argmax(axis=1)
        bestexcl[ifile, isubj] = res[:, :, othersubj].mean(axis=2).mean(axis=3).max(axis=1).argmax(axis=0)
        bestest[ifile, isubj] = bestest_tmp[bestexcl[ifile, isubj], range(len(bestexcl[ifile, isubj]))]
        best[ifile, isubj] = res[bestexcl[ifile, isubj], bestest[ifile, isubj], [isubj] * len(bestexcl[ifile, isubj]),
                                 range(len(bestexcl[ifile, isubj]))].mean(axis=-1)

plt.figure()
plt.boxplot(best[bandinds*1,np.arange(80)])
ranksums(best[bandinds*1, np.arange(80), 1], best[bandinds*1, np.arange(80), 3])
plt.figure()
plt.scatter(best[bandinds*1, np.arange(80), 1], best[bandinds*1, np.arange(80), 3])
plt.plot([0.5, 1], [0.5, 1])

bestexcl_roc = np.zeros((len(scmresults_roc_data[0].files), len(scmresults_roc_data[0][file]), 8), int)
bestest_roc = np.zeros((len(scmresults_roc_data[0].files), len(scmresults_roc_data[0][file]), 8), int)
best_roc = np.zeros((len(scmresults_roc_data[0].files), len(scmresults_roc_data[0][file]), 8))
for ifile, file in enumerate(scmresults_roc_data[0].files):
    for isubj in range(len(scmresults_roc_data[0][file])):
        othersubj = np.arange(len(scmresults_roc_data[0][file]))
        othersubj = othersubj[othersubj != isubj]
        res = np.zeros((len(scmresults_roc_data), 2, *scmresults_roc_data[0][file].shape))
        for iexcl in range(len(scmresults_roc_data)):
            res[iexcl, 0] = scmresults_roc_data[iexcl][file]
            res[iexcl, 1] = lwfresults_roc_data[iexcl][file]
        bestest_tmp = res[:, :, othersubj].mean(axis=2).mean(axis=3).argmax(axis=1)
        bestexcl_roc[ifile, isubj] = res[:, :, othersubj].mean(axis=2).mean(axis=3).max(axis=1).argmax(axis=0)
        bestest_roc[ifile, isubj] = bestest_tmp[bestexcl_roc[ifile, isubj], range(len(bestexcl_roc[ifile, isubj]))]
        best_roc[ifile, isubj] = res[bestexcl_roc[ifile, isubj], bestest_roc[ifile, isubj],
                                     [isubj] * len(bestexcl_roc[ifile, isubj]),
                                     range(len(bestexcl_roc[ifile, isubj]))].mean(axis=-1)

plt.figure()
plt.boxplot(best_roc[bandinds*1,np.arange(80)])
ranksums(best_roc[bandinds*1, np.arange(80), 1], best_roc[bandinds*1, np.arange(80), 3])
