import scipy.io as sio

import bbcpy.load.eeg
import vitalbci_funcs
import numpy as np

performance = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/performance.mat')
subdir_list = performance['subdir_list']
Nsubj = len(subdir_list)
datsnip = [dict] * Nsubj
for i, fname in enumerate(subdir_list):
    fname = fname[0][0]
    subjname = fname.split('_')[0]
    fullfile = '/home/bbci/data/bbciMat/' + fname + '/imag_arrow' + subjname + '_250Hz.mat'  # _250Hz option
    data = bbcpy.load.eeg.bbci_mat(fullfile, load_data=False)
    datsnip[i] = data.dataDict()

np.save('/home/bbci/data/results/studies/vitalbci_season1/bbcpy_datsnip', datsnip)
