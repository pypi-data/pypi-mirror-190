import os, sys

sys.path.append(os.getcwd())
import scipy.io as sio
import demos.vitalbci.vitalbci_funcs as vitalbci_funcs
import numpy as np

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'None':
            excllev = None
            exclstr = 'None'
        else:
            excllev = float(sys.argv[1])
            exclstr = '%i' % (excllev*10)
    else:
        excllev = 1.5
    if len(sys.argv) > 2:
        estimator = sys.argv[2]
    else:
        estimator = 'lwf'
    print(excllev)
    print(estimator)

vp_fb_parameters = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/vp_fb_parameters.mat')
performance = sio.loadmat('/home/bbci/data/results/studies/vitalbci_season1/performance.mat')
subdir_list = performance['subdir_list']
ivals = vp_fb_parameters['ival']
bands = vp_fb_parameters['band']
classes = vp_fb_parameters['classes']
nCSPs = vp_fb_parameters['nCSP']
Nsubj = len(subdir_list)
cvresultsAlpha = [None] * Nsubj
cvresultsBeta = [None] * Nsubj
cvresultsTheta = [None] * Nsubj
cvresultsBroad = [None] * Nsubj

for i, fname in enumerate(subdir_list):
    fname = fname[0][0]
    subjname = fname.split('_')[0]
    fullfile = '/home/bbci/data/bbciMat/' + fname + '/imag_arrow' + subjname + '.mat'  # _250Hz option
    fullfilefb = '/home/bbci/data/bbciMat/' + fname + '/imag_fbarrow' + subjname + '.mat'  # _250Hz option
    ival = ivals[i].astype(int)
    band = bands[i]
    nCSP = nCSPs[i][0]
    classi = [str(classes[i][0][0][0][0]), str(classes[i][0][0][1][0])]
    if band[0] < 13:
        cvresultsTheta[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, band / 2, classi, nCSP,
                                                                       estimator=estimator, excllev=excllev)
        cvresultsAlpha[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, band, classi, nCSP,
                                                                       estimator=estimator, excllev=excllev)
        if band[1] > 22.5:
            bandmax = 45
        else:
            bandmax = 2 * band[1]
        cvresultsBeta[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, [band[0] * 2, bandmax], classi,
                                                                      nCSP,  estimator=estimator, excllev=excllev)
        cvresultsBroad[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, [band[0], bandmax], classi,
                                                                       nCSP, estimator=estimator, excllev=excllev)
    if band[0] >= 13:
        cvresultsTheta[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, band / 4, classi, nCSP,
                                                                       estimator=estimator, excllev=excllev)
        cvresultsAlpha[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, band / 2, classi, nCSP,
                                                                       estimator=estimator, excllev=excllev)
        cvresultsBeta[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, band, classi, nCSP,
                                                                       estimator=estimator, excllev=excllev)
        cvresultsBroad[i] = vitalbci_funcs.load_and_clfy_Miklodyfirefb(fullfile, fullfilefb, ival, band * [0.5, 1], classi, nCSP,
                                                                       estimator=estimator, excllev=excllev)
    maxres = np.max([np.max(cvresultsAlpha[i][0]), np.max(cvresultsBeta[i][0]),
                     np.max(cvresultsTheta[i][0]), np.max(cvresultsBroad[i][0])])
    print('Subject finished, maximum accuracy was %2.1f%% while original was %2.1f%%' % (100 * maxres,
                                                                                         performance['acc_f'][0][
                                                                                             i]))

np.savez('/home/bbci/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_fb_%s_%s_excl_lesschans' % (
    estimator, exclstr),
         cvresultsAlpha=cvresultsAlpha, cvresultsBeta=cvresultsBeta, cvresultsTheta=cvresultsTheta,
         cvresultsBroad=cvresultsBroad)
