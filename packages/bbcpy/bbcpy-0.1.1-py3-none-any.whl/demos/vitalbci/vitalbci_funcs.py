import bbcpy
from bbcpy.pipeline import make_pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as lda
import numpy as np
from sklearn.model_selection import cross_val_score, KFold, train_test_split
from sklearn import clone
from sklearn.metrics import roc_auc_score
from matplotlib import pyplot as plt
from matplotlib import patches


def load_and_clfy(fname, ival, band, classes, PSDfreq=[1, 40], cvSplits=5):
    print('Starting subj: ' + fname)
    print('band= %2.1f to %2.1fHz' % (band[0], band[1]))
    print('ival= %i to %ims' % (ival[0], ival[1]))
    print('classes= %s' % classes)

    data = bbcpy.load.eeg.bbci_mat(fname)
    data = data['~E*']  # exclude EMG and EOG
    # classinds = [np.where(data.mrk.className==classes[0]), np.where(data.mrk.className==classes[1])]
    data.mrk = data.mrk.select_classes(classes)
    cv = KFold(n_splits=cvSplits)

    epo = data.lfilter(band).epochs(ival)

    vary = bbcpy.functions.base.ImportFunc(np.var, axis=2)
    logy = bbcpy.functions.base.ImportFunc(np.log)
    spec = bbcpy.functions.spectral.PSD(freq_range=PSDfreq, nperseg=data.fs)

    CSPpipeline = make_pipeline(bbcpy.functions.spatial.CSP, vary, logy, lda())
    cvresult = cross_val_score(CSPpipeline, epo, data.mrk.y, cv=cv)

    bbcpy.functions.spatial.CSP.n_cmps = 8
    X_train, X_test, y_train, y_test = train_test_split(epo, epo.y, test_size=1 / cvSplits, random_state=0)
    epoCSP = clone(bbcpy.functions.spatial.CSP)
    epoCSP.fit(X_train, y_train)
    features = logy(vary(epoCSP.transform(X_train)))
    features_test = logy(vary(epoCSP.transform(X_test)))
    epoCSP.score = list([])
    # plt.figure()
    Nfeatures = features.shape[1]
    for i in range(Nfeatures):
        feature = features[:, i][:, np.newaxis]
        clf = lda().fit(feature, y_train)
        feature_test = features_test[:, i][:, np.newaxis]
        epoCSP.score.append(clf.score(feature_test, y_test))
        # plt.subplot(2, Nfeatures, i + 1)
        # bbcpy.visual.scalp.map(data, epoCSP.A[:, i], clim='sym', colorbar=False)
        # plt.title('Cmp  %i acc=%2.1f%%' % (i, 100 * epoCSP.score[i]))
        # sbpl2 = plt.subplot(2, Nfeatures, i + 1 + Nfeatures)
        # plt.plot(Pxx.t, Pxx[:, i, :].T)
        # bandrect = patches.Rectangle((band[0], Pxx.min()), np.diff(band), np.diff([Pxx.min(), Pxx.max()]),
        #                             facecolor='g')
        # sbpl2.add_patch(bandrect)

    epoCSP.score = np.array(epoCSP.score)
    epoCSP.spec = (spec(epoCSP.transform(data.epochs(ival))).classmean())

    print('band= %2.1f to %2.1fHz' % (band[0], band[1]))
    print(np.array2string(cvresult * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresult.mean() * 100))
    return cvresult, epoCSP


def load_and_clfy_Miklodyfire(fname, ival, band, classes, nCSP, cvSplits=5, scoring=None, excllev=1.4, estimator='scm'):
    print('Starting subj: ' + fname)
    print('band= %2.1f to %2.1fHz' % (band[0], band[1]))
    print('ival= %i to %ims' % (ival[0], ival[1]))
    print('classes= %s' % classes)

    data = bbcpy.load.eeg.data(fname)
    # data = data['~E*'] #exclude EMG and EOG
    data = data[['~E*', '~Fp*', '~AF*', '~FAF*', '~*9', '~*10', '~O*', '~I*', '~PO7', '~PO8']]
    # classinds = [np.where(data.mrk.className==classes[0]), np.where(data.mrk.className==classes[1])]
    data.mrk = data.mrk.select_classes(classes)
    cv = KFold(n_splits=cvSplits)

    epo = data.lfilter(band).epochs(ival)

    vary = bbcpy.functions.base.ImportFunc(np.var, axis=2)
    logy = bbcpy.functions.base.ImportFunc(np.log)

    CSPpipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=nCSP), vary, logy, lda())
    cvresultCSP = cross_val_score(CSPpipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    CSPpipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=nCSP, excllev=excllev, estimator=estimator), vary,
                                logy, lda())
    cvresultCSP2 = cross_val_score(CSPpipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    pipeline = make_pipeline(bbcpy.functions.classifiers.Wishart(excllev=excllev, estimator=estimator))
    cvresultwish = cross_val_score(pipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    pipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=nCSP, excllev=excllev),
                             bbcpy.functions.classifiers.Wishart(excllev=excllev, estimator=estimator))
    cvresultCSPwish = cross_val_score(pipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire(excllev=excllev, n_cmps=nCSP, estimator=estimator))
    cvresultMfire = cross_val_score(pipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire(excllev=excllev, n_cmps=2, estimator=estimator))
    cvresultMfire_2 = cross_val_score(pipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    pipeline = make_pipeline(
        bbcpy.functions.classifiers.Miklodyfire2(excllev=excllev, n_cmps=nCSP, estimator=estimator))
    cvresultMfire2_1 = cross_val_score(pipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire2(excllev=excllev, n_cmps=2, estimator=estimator))
    cvresultMfire2_2 = cross_val_score(pipeline, epo, data.mrk.y, cv=cv, scoring=scoring)

    print('band= %2.1f to %2.1fHz' % (band[0], band[1]))
    print(np.array2string(cvresultCSP * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultCSP.mean() * 100))
    print(np.array2string(cvresultCSP2 * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultCSP2.mean() * 100))
    print(np.array2string(cvresultwish * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultwish.mean() * 100))
    print(np.array2string(cvresultCSPwish * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultCSPwish.mean() * 100))
    print(np.array2string(cvresultMfire * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultMfire.mean() * 100))
    print(np.array2string(cvresultMfire_2 * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultMfire_2.mean() * 100))
    print(np.array2string(cvresultMfire2_1 * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultMfire2_1.mean() * 100))
    print(np.array2string(cvresultMfire2_2 * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    print('%2.1f%%' % (cvresultMfire2_2.mean() * 100))
    return [cvresultCSP, cvresultCSP2, cvresultwish, cvresultCSPwish, cvresultMfire, cvresultMfire_2, cvresultMfire2_1,
            cvresultMfire2_2]


def load_and_clfy_Miklodyfirefb(fname, fnamefb, ival, band, classes, nCSP, excllev=1.4, estimator='scm'):
    print('Starting subj: ' + fname)
    print('band= %2.1f to %2.1fHz' % (band[0], band[1]))
    print('ival= %i to %ims' % (ival[0], ival[1]))
    print('classes= %s' % classes)

    data = bbcpy.load.eeg.data(fname)
    data = data[['~E*', '~Fp*', '~AF*', '~FAF*', '~*9', '~*10', '~O*', '~I*', '~PO7', '~PO8']]
    data.mrk = data.mrk.select_classes(classes)
    epo = data.lfilter(band).epochs(ival)

    datafb = bbcpy.load.eeg.data(fnamefb)
    datafb = datafb[['~E*', '~Fp*', '~AF*', '~FAF*', '~*9', '~*10', '~O*', '~I*', '~PO7', '~PO8']]
    datafb.mrk = datafb.mrk.select_classes(classes)
    epofb = datafb.lfilter(band).epochs(ival)

    vary = bbcpy.functions.base.ImportFunc(np.var, axis=2)
    logy = bbcpy.functions.base.ImportFunc(np.log)

    CSPpipeline = make_pipeline(vary, logy, lda())
    CSPpipeline.fit(epo, epo.y)
    cvresultlda = [CSPpipeline.score(epofb, epofb.y),
                   roc_auc_score(epofb.y, CSPpipeline.predict(epofb))]

    CSPpipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=2), vary, logy, lda())
    CSPpipeline.fit(epo, epo.y)
    cvresultCSP = [CSPpipeline.score(epofb, epofb.y),
                   roc_auc_score(epofb.y, CSPpipeline.predict(epofb))]

    CSPpipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=2, excllev=excllev, estimator=estimator), vary,
                                logy, lda())
    CSPpipeline.fit(epo, epo.y)
    cvresultCSP2 = [CSPpipeline.score(epofb, epofb.y),
                    roc_auc_score(epofb.y, CSPpipeline.predict(epofb))]

    pipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=2, excllev=excllev),
                             bbcpy.functions.classifiers.Wishart(excllev=excllev, estimator=estimator))
    pipeline.fit(epo, epo.y)
    cvresultCSPwish = [pipeline.score(epofb, epofb.y),
                       roc_auc_score(epofb.y, CSPpipeline.predict(epofb))]

    pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire(excllev=excllev, n_cmps=nCSP, estimator=estimator))
    pipeline.fit(epo, epo.y)
    cvresultMfire = [pipeline.score(epofb, epofb.y),
                     roc_auc_score(epofb.y, CSPpipeline.predict(epofb))]

    pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire(excllev=excllev, n_cmps=2, estimator=estimator))
    pipeline.fit(epo, epo.y)
    cvresultMfire_2 = [pipeline.score(epofb, epofb.y),
                       roc_auc_score(epofb.y, CSPpipeline.predict(epofb))]

    print('band= %2.1f to %2.1fHz' % (band[0], band[1]))
    print(np.array2string(cvresultlda[0] * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    #print('%2.1f%%' % (cvresultlda[0].mean() * 100))
    print(np.array2string(cvresultCSP[0] * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    #print('%2.1f%%' % (cvresultCSP[0].mean() * 100))
    print(np.array2string(cvresultCSP2[0] * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    #print('%2.1f%%' % (cvresultCSP2[0].mean() * 100))
    print(np.array2string(cvresultCSPwish[0] * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    #print('%2.1f%%' % (cvresultCSPwish[0].mean() * 100))
    print(np.array2string(cvresultMfire[0] * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    #print('%2.1f%%' % (cvresultMfire[0].mean() * 100))
    print(np.array2string(cvresultMfire_2[0] * 100, formatter={'float_kind': lambda x: "%2.1f%%" % x}))
    #print('%2.1f%%' % (cvresultMfire_2[0].mean() * 100))
    return [cvresultlda, cvresultCSP, cvresultCSP2, cvresultCSPwish, cvresultMfire, cvresultMfire_2]


def plot_and_compare(scores, specs, performance, f=np.arange(2, 40)):
    bestcomps = scores.max(axis=1)
    bestcompsi = scores.argmax(axis=1)
    plt.figure()
    plt.subplot(221)
    plt.plot(performance['acc_c'][0], bestcomps * 100, '.')

    GAspec = np.array([spec[:, bestcompsi[i], :] for i, spec in enumerate(specs)]).mean(axis=0)

    plt.subplot(223)
    plt.plot(f, GAspec.T)

    normAvSpec = np.array(
        [spec[0, bestcompsi[i], :] - spec[1, bestcompsi[i], :] for i, spec in enumerate(specs)]).T
    normAvSpec /= -normAvSpec[np.abs(normAvSpec).argmax(axis=0), np.arange(normAvSpec.shape[1])]

    plt.subplot(122)
    plt.imshow(normAvSpec[:, bestcomps.argsort()[::-1]].T, cmap='jet', vmin=-1, vmax=1)
    sortedperform = (np.sort(bestcomps)[::-10] * 100).tolist()
    plt.yticks(np.arange(0, bestcomps.shape[0], 10), ['%2.1f%%' % x for x in sortedperform])
    plt.xticks(f[3::5] - 2, f[3::5])
    plt.xlabel('frequency [Hz]')
    plt.ylabel('accuracy')
    cbar = plt.colorbar()
    cbar.set_label('relative PSD difference between class 1 and 2')


def plot_and_compare_scalps(scores, As, dataset, classes, sorted=False):
    bestcomps = scores.max(axis=1) * 100
    if sorted:
        bestcompssorti = scores.max(axis=1).argsort()[::-1]
    else:
        bestcompssorti = np.arange(bestcomps.shape[0])
    bestcomps = bestcomps[bestcompssorti]
    bestcompsi = scores.argmax(axis=1)[bestcompssorti]

    plt.figure()
    nSubj = dataset.shape[0]
    nRow = int(np.round(np.sqrt(nSubj)))
    for i in range(nSubj):
        plt.subplot(nRow, nRow, i + 1)
        bbcpy.visual.scalp.map(dataset[bestcompssorti[i]], As[bestcompssorti[i]][:, bestcompsi[i]], clim='sym',
                               colorbar=False, senspos=False)
        classesi = classes[bestcompssorti[i]][0][0]
        plt.title('A=%2.1f%%, %s-%s' % (bestcomps[i], classesi[0][0][0].upper(), classesi[1][0][0].upper()))


def plot_and_compare_scalps_bands(Alphascores, Betascores, Thetascores, Broadscores, Broaderscores, Broader100scores,
                                  AlphaAs, BetaAs, ThetaAs, BroadAs, BroaderAs, Broader100As,
                                  Alphaspecs, Betaspecs, Thetaspecs, Broadspecs, Broaderspecs, Broader100specs,
                                  dataset, classes, performances, selection=None):
    import scipy.io as sio
    lf = sio.loadmat('C:/Users/Daniel Miklody/tubCloud/Artefact Headmodel/lf_vol_1922_NY_DiTripoleMuscle_SymEye.mat')
    Broader100tissues = search_sources(Broader100As, Broader100scores, dataset, lf['lf_trip'],
                                       lf['elec'][0][0][3],
                                       lf['sourcemodel'][0][0][0], lf['sourcemodel'][0][0][2])
    Broadertissues = search_sources(BroaderAs, Broaderscores, dataset, lf['lf_trip'], lf['elec'][0][0][3],
                                    lf['sourcemodel'][0][0][0], lf['sourcemodel'][0][0][2])
    Broadtissues = search_sources(BroadAs, Broadscores, dataset, lf['lf_trip'], lf['elec'][0][0][3],
                                  lf['sourcemodel'][0][0][0], lf['sourcemodel'][0][0][2])
    Alphatissues = search_sources(AlphaAs, Alphascores, dataset, lf['lf_trip'], lf['elec'][0][0][3],
                                  lf['sourcemodel'][0][0][0], lf['sourcemodel'][0][0][2])
    Betatissues = search_sources(BetaAs, Betascores, dataset, lf['lf_trip'], lf['elec'][0][0][3],
                                 lf['sourcemodel'][0][0][0], lf['sourcemodel'][0][0][2])
    Thetatissues = search_sources(ThetaAs, Thetascores, dataset, lf['lf_trip'], lf['elec'][0][0][3],
                                  lf['sourcemodel'][0][0][0], lf['sourcemodel'][0][0][2])
    plt.figure()
    if selection is None:
        nSubj = 10  # dataset.shape[0]
        selection = range(nSubj)
    else:
        nSubj = len(selection)
    nCol = 6
    for i, isubj in enumerate(selection):
        ax1 = plt.subplot(nSubj, nCol, nCol * i + 1)
        plot_and_compare_scalp_bands_specs_i(Thetascores[isubj], ThetaAs[isubj], Thetaspecs[isubj], Thetatissues[isubj],
                                             dataset[isubj], classes[isubj][0][0])
        plt.text(-0.25, 0.5, 'orig. %2.0f%%' % performances[i], horizontalalignment='right',
                 verticalalignment='center', transform=ax1.transAxes)

        plt.subplot(nSubj, nCol, nCol * i + 2)
        plot_and_compare_scalp_bands_specs_i(Alphascores[isubj], AlphaAs[isubj], Alphaspecs[isubj], Alphatissues[isubj],
                                             dataset[isubj], classes[isubj][0][0])

        plt.subplot(nSubj, nCol, nCol * i + 3)
        plot_and_compare_scalp_bands_specs_i(Betascores[isubj], BetaAs[isubj], Betaspecs[isubj], Betatissues[isubj],
                                             dataset[isubj], classes[isubj][0][0])

        plt.subplot(nSubj, nCol, nCol * i + 4)
        plot_and_compare_scalp_bands_specs_i(Broadscores[isubj], BroadAs[isubj], Broadspecs[isubj], Broadtissues[isubj],
                                             dataset[isubj], classes[isubj][0][0])

        plt.subplot(nSubj, nCol, nCol * i + 5)
        plot_and_compare_scalp_bands_specs_i(Broaderscores[isubj], BroaderAs[isubj], Broaderspecs[isubj],
                                             Broadertissues[isubj], dataset[isubj], classes[isubj][0][0],
                                             spec_plot_f=np.arange(1, 90))

        plt.subplot(nSubj, nCol, nCol * i + 6)
        plot_and_compare_scalp_bands_specs_i(Broader100scores[isubj], Broader100As[isubj], Broader100specs[isubj],
                                             Broader100tissues[isubj], dataset[isubj], classes[isubj][0][0],
                                             spec_plot_f=np.arange(1, 90))


def plot_and_compare_scalp_bands_specs_i(scores, As, spec, tissues, data, classes, f=None, spec_plot_f=None):
    if f is None:
        f = np.arange(spec.shape[2])
    if spec_plot_f is None:
        spec_plot_f = np.arange(f.shape[0])
    bestcomps = scores.max() * 100
    bestcompsi = scores.argmax()
    ymin = spec[:, bestcompsi, spec_plot_f].min()
    ymax = spec[:, bestcompsi, spec_plot_f].max()
    yextent = ymin  # (ymax-ymin)/4+ymin
    xextent = spec.shape[2] / 3 * 2  # -(ymax-ymin)/4*3
    xspan = spec.shape[2]
    bbcpy.visual.scalp.map(data, As[:, bestcompsi], clim='sym',
                           colorbar=False, senspos=False, aspect='auto', extent=[xextent, xspan, yextent, ymax])
    plt.plot(f[spec_plot_f], spec[:, bestcompsi, spec_plot_f].T)
    plt.axis('on')
    # plt.xlabel('frequency [Hz]')
    # plt.ylabel('PSD [dB]')
    plt.text(5, 0.7 * (ymax - ymin) + ymin, 'A=%2.1f%%, %s, %s-%s' % (bestcomps, tissues[:5], classes[0][0][0].upper(),
                                                                      classes[1][0][0].upper()))


def search_sources(As, scores, dataset, lf, lfelec, grid, gridtissues):
    bestcompsi = scores.argmax(axis=1)
    tissues = []
    for i in range(As.shape[0]):
        chaninds = np.array([dataset[i].chans.index(chan[0][0] , markmissing=True) for chan in lfelec])
        validchans = [not chanind is None for chanind in chaninds]
        s, vmax, imax, dip_mom, dip_loc = bbcpy.functions.sourcespace.music(
            As[i][chaninds[validchans].astype(int), bestcompsi[i]], lf[validchans], grid)
        tissues.append(gridtissues[imax][0][0])
    return tissues


def EPSP(fs, normalize=False):
    tau1 = 0.0001
    tau2 = 0.002
    t = np.arange(0, 0.1, 1 / fs)
    y = 7 * (-np.exp(-t / tau1) + np.exp(-t / tau2))
    if normalize:
        y /= np.abs(y).max()
    return t, y


def IPSP(fs, normalize=False):
    tau1 = 0.005
    tau2 = 0.01
    t = np.arange(0, 0.1, 1 / fs)
    y = -(-np.exp(-t / tau1) + np.exp(-t / tau2))
    if normalize:
        y /= np.abs(y).max()
    return t, y


def MUAP(fs, normalize=False):
    U = 4  # m/s
    t = np.arange(0, 0.1, 1 / fs)
    z = 2 * U * t * 1000 / 100 * 4
    y = 4 * 96 * z * (6 - 6 * z + z ** 2) * np.exp(-z)
    if normalize:
        y /= np.abs(y).max()
    return t, y


def fitPSD(pxx):
    neuronAP = np.load('../NEURONSomaAP.npz')
    fs1 = 1000  # dataset[0].fs
    fs2 = int(1 / (neuronAP['t'][1] - neuronAP['t'][0]))
    yV = neuronAP['V'] - neuronAP['V'][0]
    yV /= np.abs(yV).max()
    tI, yI = IPSP(fs1, True)
    tE, yE = EPSP(fs1, True)
    tM, yM = MUAP(fs2, True)
    f, pxx = welch(np.pad(yV, (0, int(fs2) - neuronAP['V'].shape[0])), fs2,
                   nperseg=int(fs2 / 2), window='hamming', detrend=False)
    fyE, pyyE = welch(np.pad(yE, (0, int(fs1) - yE.shape[0])), fs1,
                      nperseg=int(fs1 / 2), window='hamming', detrend=False)
    fyI, pyyI = welch(np.pad(yI, (0, int(fs1) - yI.shape[0])), fs1,
                      nperseg=int(fs1 / 2), window='hamming', detrend=False)
    fyM, pyyM = welch(np.pad(yM, (0, int(fs2) - yM.shape[0])), fs2,
                      nperseg=int(fs2 / 2), window='hamming', detrend=False)

    return y1, h1, h1ei, y2, h2, h2ei, m
