import scipy.io as sio
import vitalbci_funcs
import numpy as np

vp_fb_parameters = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/vp_fb_parameters.mat')
performance = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/performance.mat')
subdir_list = performance['subdir_list']
ivals = vp_fb_parameters['ival']
bands = vp_fb_parameters['band']
classes = vp_fb_parameters['classes']
Nsubj = len(subdir_list)
cvresultsBroader = [None] * Nsubj
epoCSPBroader = [None] * Nsubj
cvresultsBroader100 = [None] * Nsubj
epoCSPBroader100 = [None] * Nsubj
for i, fname in enumerate(subdir_list):
    fname = fname[0][0]
    subjname = fname.split('_')[0]
    fullfile = '/home/bbci/data/bbciMat/' + fname + '/imag_arrow' + subjname + '_250Hz.mat'  # _250Hz option
    ival = ivals[i].astype(int)
    band = bands[i]
    classi = [str(classes[i][0][0][0][0]), str(classes[i][0][0][1][0])]
    cvresultsBroader[i], epoCSPBroader[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, [4, 40], classi, PSDfreq=[0, 100])
    cvresultsBroader100[i], epoCSPBroader100[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, [4, 100], classi, PSDfreq=[0, 100])
    maxres = np.max([np.mean(cvresultsBroader[i]), np.mean(cvresultsBroader100[i])])
    print('Subject finished, maximum accuracy was %2.1f%% while original was %2.1f%%' % (100*maxres,
                                                                                     performance['acc_c'][0][i]))
BroaderWs = np.array([x.W for x in epoCSPBroader])
Broader100Ws = np.array([x.W for x in epoCSPBroader100])

BroaderAs = np.array([x.A for x in epoCSPBroader])
Broader100As = np.array([x.A for x in epoCSPBroader100])

Broaderscores = np.array([x.score for x in epoCSPBroader])
Broader100scores = np.array([x.score for x in epoCSPBroader100])

Broaderspecs = np.array([x.spec for x in epoCSPBroader])
Broader100specs = np.array([x.spec for x in epoCSPBroader100])

np.savez('/home/bbci/data/results/studies/vitalbci_season1/bbcpy_cv_results_broader', cvresultsBroader=cvresultsBroader,
         cvresultsBroader100=cvresultsBroader100, BroaderWs=BroaderWs, BroaderAs=BroaderAs, Broaderscores=Broaderscores,
         Broaderspecs=Broaderspecs, Broader100Ws=Broader100Ws, Broader100As=Broader100As,
         Broader100scores=Broader100scores, Broader100specs=Broader100specs)
