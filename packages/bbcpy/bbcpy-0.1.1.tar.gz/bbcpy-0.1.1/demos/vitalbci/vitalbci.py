import scipy.io as sio
import vitalbci_funcs
import numpy as np

vp_fb_parameters = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/vp_fb_parameters.mat')
performance = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/performance.mat')
subdir_list = performance['subdir_list']
ivals = vp_fb_parameters['ival']
bands = vp_fb_parameters['band']
classes = vp_fb_parameters['classes']
# ival = [580, 4470]
# band = np.array([15, 23]) / 2
# band = [7.5, 40]
Nsubj = len(subdir_list)
cvresultsAlpha = [None] * Nsubj
epoCSPAlpha = [None] * Nsubj
cvresultsBeta = [None] * Nsubj
epoCSPBeta = [None] * Nsubj
cvresultsTheta = [None] * Nsubj
epoCSPTheta = [None] * Nsubj
cvresultsBroad = [None] * Nsubj
epoCSPBroad = [None] * Nsubj

for i, fname in enumerate(subdir_list):
    fname = fname[0][0]
    subjname = fname.split('_')[0]
    fullfile = '/home/bbci/data/bbciMat/' + fname + '/imag_arrow' + subjname + '.mat'  # _250Hz option
    ival = ivals[i].astype(int)
    band = bands[i]
    classi = [str(classes[i][0][0][0][0]), str(classes[i][0][0][1][0])]
    if band[0] < 13:
        cvresultsTheta[i], epoCSPTheta[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, band / 2, classi)
        cvresultsAlpha[i], epoCSPAlpha[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, band, classi)
        if band[1] > 22.5:
            bandmax = 45
        else:
            bandmax = 2 * band[1]
        cvresultsBeta[i], epoCSPBeta[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, [band[0] * 2, bandmax], classi)
        cvresultsBroad[i], epoCSPBroad[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, [band[0], bandmax], classi)
    if band[0] >= 13:
        cvresultsTheta[i], epoCSPTheta[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, band / 4, classi)
        cvresultsAlpha[i], epoCSPAlpha[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, band / 2, classi)
        cvresultsBeta[i], epoCSPBeta[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, band, classi)
        cvresultsBroad[i], epoCSPBroad[i] = vitalbci_funcs.load_and_clfy(fullfile, ival, band * [0.5, 1], classi)
    maxres = np.max([np.mean(cvresultsAlpha[i]), np.mean(cvresultsBeta[i]), np.mean(cvresultsTheta[i]),
                     np.mean(cvresultsBroad[i])])
    print('Subject finished, maximum accuracy was %2.1f%% while original was %2.1f%%' % (100*maxres,
                                                                                     performance['acc_c'][0][i]))
AlphaWs = np.array([x.W for x in epoCSPAlpha])
BetaWs = np.array([x.W for x in epoCSPBeta])
ThetaWs = np.array([x.W for x in epoCSPTheta])
BroadWs = np.array([x.W for x in epoCSPBroad])
AlphaAs = np.array([x.A for x in epoCSPAlpha])
BetaAs = np.array([x.A for x in epoCSPBeta])
ThetaAs = np.array([x.A for x in epoCSPTheta])
BroadAs = np.array([x.A for x in epoCSPBroad])
Alphascores = np.array([x.score for x in epoCSPAlpha])
Betascores = np.array([x.score for x in epoCSPBeta])
Thetascores = np.array([x.score for x in epoCSPTheta])
Broadscores = np.array([x.score for x in epoCSPBroad])
Alphaspecs = np.array([x.spec for x in epoCSPAlpha])
Betaspecs = np.array([x.spec for x in epoCSPBeta])
Thetaspecs = np.array([x.spec for x in epoCSPTheta])
Broadspecs = np.array([x.spec for x in epoCSPBroad])

np.savez('/home/bbci/data/results/studies/vitalbci_season1/bbcpy_cv_results', cvresultsAlpha=cvresultsAlpha,
         cvresultsBeta=cvresultsBeta, cvresultsTheta=cvresultsTheta, cvresultsBroad=cvresultsBroad,
         AlphaWs=AlphaWs, AlphaAs=AlphaAs, Alphascores=Alphascores, Alphaspecs=Alphaspecs,
         BetaWs=BetaWs, BetaAs=BetaAs, Betascores=Betascores, Betaspecs=Betaspecs,
         ThetaWs=ThetaWs, ThetaAs=ThetaAs, Thetascores=Thetascores,Thetaspecs=Thetaspecs,
         BroadWs=BroadWs, BroadAs=BroadAs, Broadscores=Broadscores, Broadspecs=Broadspecs)
