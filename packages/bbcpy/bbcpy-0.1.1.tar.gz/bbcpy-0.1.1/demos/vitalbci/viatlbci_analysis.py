import matplotlib.pyplot as plt
import numpy as np
import bbcpy
import scipy.io as sio
from vitalbci_funcs import *

vp_fb_parameters = sio.loadmat('C:/data/results/studies/vitalbci_season1/vp_fb_parameters.mat')
classes = vp_fb_parameters['classes']

performance = sio.loadmat('C:/data/results/studies/vitalbci_season1/performance.mat')
data = np.load('C:/data/results/studies/vitalbci_season1/bbcpy_cv_results_broader.npz', allow_pickle=True)
for key in data.files:
    globals()[key] = data.get(key)
data.close()
Broaderspecs = Broadspecs  # correcting error in variable name

data = np.load('C:/data/results/studies/vitalbci_season1/bbcpy_cv_results.npz', allow_pickle=True)
for key in data.files:
    globals()[key] = data.get(key)
data.close()

dataset = bbcpy.load.eeg.dataset('C:/data/results/studies/vitalbci_season1/bbcpy_datsnip.npy')

# plot_and_compare(Broadscores, Broadspecs, performance)
# plot_and_compare(Alphascores, Alphaspecs, performance)
# plot_and_compare(Betascores, Betaspecs, performance)
# plot_and_compare(Thetascores, Thetaspecs, performance)

# plot_and_compare(Broaderscores, Broaderspecs, performance, f=np.arange(0, 101))
# plot_and_compare(Broader100scores, Broader100specs, performance, f=np.arange(0, 101))

# plot_and_compare_scalps(Alphascores, AlphaAs, dataset, classes, sorted=True)
# plot_and_compare_scalps(Betascores, BetaAs, dataset, classes, sorted=True)
# plot_and_compare_scalps(Thetascores, ThetaAs, dataset, classes, sorted=True)
# plot_and_compare_scalps(Broadscores, BroadAs, dataset, classes, sorted=True)

plot_and_compare_scalps_bands(Alphascores, Betascores, Thetascores, Broadscores, Broaderscores,
                              Broader100scores, AlphaAs, BetaAs, ThetaAs, BroadAs, BroaderAs,
                              Broader100As, Alphaspecs, Betaspecs, Thetaspecs, Broadspecs, Broaderspecs,
                              Broader100specs, dataset, classes, performance['acc_c'][0],
                              selection=np.random.default_rng().choice(len(dataset), size=10,
                                                                       replace=False))

neuronAP = np.load('../NEURONSomaAP.npz')
from scipy.signal import resample, resample_poly, decimate, welch

fs1 = 1000  # dataset[0].fs
fs2 = int(1 / (neuronAP['t'][1] - neuronAP['t'][0]))
y = resample_poly(neuronAP['V'] - neuronAP['V'][0], fs1, fs2)
y2 = resample(neuronAP['V'] - neuronAP['V'][0], int(fs1 / fs2 * neuronAP['V'].shape[0]))
y3 = decimate(neuronAP['V'] - neuronAP['V'][0], int(fs2 / fs1))
t = np.linspace(0, y.shape[0] / fs1, y.shape[0])
t2 = np.linspace(0, y2.shape[0] / fs1, y2.shape[0])
t3 = np.linspace(0, y3.shape[0] / fs1, y3.shape[0])
plt.figure()
plt.plot(neuronAP['t'], neuronAP['V'] - neuronAP['V'][0])
plt.plot(t, y)
plt.plot(t2, y2)
plt.plot(t3, y3)

yV = neuronAP['V'] - neuronAP['V'][0]
yV /= np.abs(yV).max()
tI, yI = IPSP(fs1, True)
tE, yE = EPSP(fs1, True)
tM, yM = MUAP(fs2, True)
plt.figure()
plt.plot(neuronAP['t'], yV)
plt.plot(tE, yE)
plt.plot(tI, yI)
plt.plot(tM, yM)
plt.xlim((0, 0.02))

f, pxx = welch(np.pad(yV, (0, int(fs2) - neuronAP['V'].shape[0])), fs2,
               nperseg=int(fs2), window='hamming', detrend=False)
plt.figure()
plt.semilogy(f, pxx * 10)
fy, pyy = welch(np.pad(y, (0, int(fs1) - y.shape[0])), fs1,
                nperseg=int(fs1), window='hamming', detrend=False)
# plt.plot(fy, pyy)
fyE, pyyE = welch(np.pad(yE, (0, int(fs1) - yE.shape[0])), fs1,
                  nperseg=int(fs1), window='hamming', detrend=False)
plt.semilogy(fyE, pyyE)
fyI, pyyI = welch(np.pad(yI, (0, int(fs1) - yI.shape[0])), fs1,
                  nperseg=int(fs1), window='hamming', detrend=False)
plt.semilogy(fyI, pyyI / 100)
fyM, pyyM = welch(np.pad(yM, (0, int(fs2) - yM.shape[0])), fs2,
                  nperseg=int(fs2), window='hamming', detrend=False)
plt.semilogy(fyM, pyyM / 5)
plt.xlim([0, 200])
plt.legend(['AP', 'EPSP', 'IPSP', 'EMG'])
plt.ylim([1e-9, 1e-6])

plt.figure()
plt.loglog(f, pxx)
# plt.loglog(fy, pyy)
plt.loglog(fyE, pyyE)
plt.loglog(fyI, pyyI)
plt.loglog(fyM, pyyM)
# plt.xlim([0, 2500])

specmodel = lambda f, E, I, A, M: (E * np.sqrt(pyyE[:f.shape[0]]) + I * np.sqrt(pyyI[:f.shape[0]]) +
                                   A * np.sqrt(pxx[:f.shape[0]]) + M * np.sqrt(pyyM[:f.shape[0]]))
from scipy import optimize

res = optimize.curve_fit(specmodel, fyE, np.sqrt(pyyE))  # santiy test
print(res[0])
testspec1 = 10 ** (Alphaspecs[0, 0, 0, :] / 20)
testspec2 = 10 ** (Alphaspecs[0, 1, 0, :] / 20)
f = np.arange(1, Alphaspecs.shape[3] + 1)
plt.figure()
plt.plot(f, testspec1)
plt.plot(f, testspec2)
plt.legend(['class0', 'class1'])

res = optimize.curve_fit(specmodel, f, testspec1 - testspec2, maxfev=100000)
plt.figure()
plt.plot(f, testspec1 - testspec2)
plt.plot(f, specmodel(f, *res[0]))

specmodelnonlin = lambda f, E, I, A, M, E2, I2, A2, M2: specmodel(f, E, I, A, M) + np.log(
    1 / specmodel(f, E2, I2, A2, M2) - 1)
resnonlin = optimize.curve_fit(specmodelnonlin, f, testspec1 - testspec2, maxfev=100000)
plt.figure()
plt.plot(f, testspec1 - testspec2)
plt.plot(f, specmodelnonlin(f, *resnonlin[0]))


def estimateSpec(f, spec1, spec2, pyyE, pyyI, pxx, startval=np.ones(5)):
    specnonlin = np.log(1 / spec1 - 1)
    logistic = lambda h: 1 / (1 + np.exp(-h))
    #EIspec = lambda EI: EI * np.sqrt(pyyE[:f.shape[0]]) + (1 - EI) * np.sqrt(pyyI[:f.shape[0]])
    EIspec = lambda EI: EI * np.sqrt(pyyE[:f.shape[0]]) + 1 / EI * np.sqrt(pyyI[:f.shape[0]])
    specmodel = lambda f, Amp, EI, A, EI2, Amp2: Amp * spec1 + EIspec(EI) + A * np.sqrt(pxx[:f.shape[0]]) + \
                                                 logistic(Amp2 * specnonlin + EI2)
    res = optimize.curve_fit(specmodel, f, spec2, startval, maxfev=100000)
    return res[0], specmodel(f, *res[0])


def estimateSpecwMuscle(f, spec1, spec2, pyyE, pyyI, pxx, pyyM, startval=np.ones(6)):
    specnonlin = np.log(1 / spec1 - 1)
    logistic = lambda h: 1 / (1 + np.exp(-h))
    EIspec = lambda EI: EI * np.sqrt(pyyE[:f.shape[0]]) + (1 - EI) * np.sqrt(pyyI[:f.shape[0]])
    specmodel = lambda f, Amp, EI, A, M, EI2, Amp2: Amp * spec1 + EIspec(EI) + A * np.sqrt(pxx[:f.shape[0]]) + \
                                                    M * np.sqrt(pyyM[:f.shape[0]]) + logistic(Amp2 * specnonlin + EI2)
    res = optimize.curve_fit(specmodel, f, spec2, startval, maxfev=100000)
    return res[0], specmodel(f, *res[0])


isubj = np.random.randint(Alphaspecs.shape[0])
f = np.arange(1, Alphaspecs.shape[3] + 1)
if Alphaspecs[isubj, 0, 0, 9] > Alphaspecs[isubj, 1, 0, 9]:
    testspec1 = 10 ** (Alphaspecs[isubj, 0, 0, :] / 20)
    testspec2 = 10 ** (Alphaspecs[isubj, 1, 0, :] / 20)
else:
    testspec2 = 10 ** (Alphaspecs[isubj, 0, 0, :] / 20)
    testspec1 = 10 ** (Alphaspecs[isubj, 1, 0, :] / 20)

res, estspec = estimateSpec(f, testspec1, testspec2, pyyE, pyyI, pxx, [1, 1, 0.1, 0.1, 0.1])

plt.figure()
plt.plot(f, 20 * np.log10(testspec1))
plt.plot(f, 20 * np.log10(testspec2))
plt.plot(f, 20 * np.log10(estspec))
plt.legend(['class0', 'class1', 'estimated'])
plt.title('%2.1f' % Alphascores[isubj, 0])
