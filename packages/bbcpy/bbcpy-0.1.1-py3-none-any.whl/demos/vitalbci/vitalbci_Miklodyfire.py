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

for scoring in [None, 'roc_auc']:
    for i, fname in enumerate(subdir_list):
        fname = fname[0][0]
        subjname = fname.split('_')[0]
        fullfile = '/home/bbci/data/bbciMat/' + fname + '/imag_arrow' + subjname + '.mat'  # _250Hz option
        ival = ivals[i].astype(int)
        band = bands[i]
        nCSP = nCSPs[i][0]
        classi = [str(classes[i][0][0][0][0]), str(classes[i][0][0][1][0])]
        if band[0] < 13:
            cvresultsTheta[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, band / 2, classi, nCSP,
                                                                         scoring=scoring, estimator=estimator,
                                                                         excllev=excllev)
            cvresultsAlpha[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, band, classi, nCSP,
                                                                         scoring=scoring, estimator=estimator,
                                                                         excllev=excllev)
            if band[1] > 22.5:
                bandmax = 45
            else:
                bandmax = 2 * band[1]
            cvresultsBeta[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, [band[0] * 2, bandmax], classi,
                                                                        nCSP, scoring=scoring, estimator=estimator,
                                                                        excllev=excllev)
            cvresultsBroad[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, [band[0], bandmax], classi,
                                                                         nCSP, scoring=scoring, estimator=estimator,
                                                                         excllev=excllev)
        if band[0] >= 13:
            cvresultsTheta[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, band / 4, classi, nCSP,
                                                                         scoring=scoring, estimator=estimator,
                                                                         excllev=excllev)
            cvresultsAlpha[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, band / 2, classi, nCSP,
                                                                         scoring=scoring, estimator=estimator,
                                                                         excllev=excllev)
            cvresultsBeta[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, band, classi, nCSP,
                                                                        scoring=scoring, estimator=estimator,
                                                                        excllev=excllev)
            cvresultsBroad[i] = vitalbci_funcs.load_and_clfy_Miklodyfire(fullfile, ival, band * [0.5, 1], classi, nCSP,
                                                                         scoring=scoring, estimator=estimator,
                                                                         excllev=excllev)
        maxres = np.max([np.max(np.mean(cvresultsAlpha[i], axis=1)), np.max(np.mean(cvresultsBeta[i], axis=1)),
                         np.max(np.mean(cvresultsTheta[i], axis=1)), np.max(np.mean(cvresultsBroad[i], axis=1))])
        print('Subject finished, maximum accuracy was %2.1f%% while original was %2.1f%%' % (100 * maxres,
                                                                                             performance['acc_c'][0][
                                                                                                 i]))

    np.savez('/home/bbci/data/results/studies/vitalbci_season1/bbcpy_cv_results_Miklodyfire_%s_%s_excl_%s_lesschans' % (
        estimator, exclstr, str(scoring)),
             cvresultsAlpha=cvresultsAlpha, cvresultsBeta=cvresultsBeta, cvresultsTheta=cvresultsTheta,
             cvresultsBroad=cvresultsBroad)
