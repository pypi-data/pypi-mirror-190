import bbcpy
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import KFold, ShuffleSplit, GridSearchCV
from bbcpy.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score

cv = KFold()

ival = [1000, 4500]
band = [10.5, 13]
imagVPaw = bbcpy.load.eeg.data('C:/data/bbcpydata/imagVPaw.npz')

cnt_bp = imagVPaw.lfilter(band)
epo_bp = cnt_bp.epochs(ival)

wish = bbcpy.functions.classifiers.Wishart()
wish.fit(epo_bp, epo_bp.y)
y = wish.decision_function(epo_bp)
print(np.mean(y))
plt.figure()
plt.plot(y)
plt.stem(np.arange(epo_bp.y.shape[0]), y.mean() * (2 * epo_bp.y.astype(float) - 1))
from pyriemann.utils import covariance

wish_lwf = bbcpy.functions.classifiers.Wishart(estimator=covariance._lwf)
wish_lwf.fit(epo_bp, epo_bp.y)
y2 = wish_lwf.decision_function(epo_bp)
print(np.mean(y2))

wish_art = bbcpy.functions.classifiers.Wishart(excllev=1.2)
wish_art.fit(epo_bp, epo_bp.y)
y2 = wish_art.decision_function(epo_bp)
print(np.mean(y2))
plt.figure()
plt.plot(y)
plt.stem(np.arange(epo_bp.y.shape[0]), y.mean() * (2 * epo_bp.y.astype(float) - 1))

# parameters = {'excllev': np.concatenate([[None], np.arange(1, 2, 0.05)]), 'autobias': [True, False],
#              'estimator': [covariance._scm, covariance._lwf, covariance._oas]}
# clf = GridSearchCV(bbcpy.functions.classifiers.Wishart(), parameters, cv=cv)
# clf.fit(epo_bp, epo_bp.y)
# print(clf.cv_results_['mean_test_score'])
# print(clf.cv_results_['mean_test_score'].max())
# maxind = clf.cv_results_['mean_test_score'].argmax()
# print([clf.cv_results_['params'][i] for i in np.where(clf.cv_results_['rank_test_score'] == 1)[0]])

pipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=4, excllev=1.5),
                         bbcpy.functions.classifiers.Wishart(excllev=1.5))
print(np.mean(cross_val_score(pipeline, epo_bp, epo_bp.y, cv=cv)))

# pipeline = make_pipeline(bbcpy.functions.classifiers.Wishart(geomean=True))
# print(np.mean(cross_val_score(pipeline, epo_bp, epo_bp.y, cv=cv)))

pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire(excllev=1.5, n_cmps=4))
print(np.mean(cross_val_score(pipeline, epo_bp, epo_bp.y, cv=cv)))

parameters = {'excllev': np.concatenate([[None], np.arange(1, 2, 0.1)]),
              'estimator': [covariance._scm, covariance._lwf], 'n_cmps': [2, 3, 4, 6, 8]}
clf = GridSearchCV(bbcpy.functions.classifiers.Miklodyfire(), parameters, cv=cv)
clf.fit(epo_bp, epo_bp.y)
print(clf.cv_results_['mean_test_score'])
print(clf.cv_results_['mean_test_score'].max())
# maxind = clf.cv_results_['mean_test_score'].argmax()
# print(clf.cv_results_['params'][maxind])
print([clf.cv_results_['params'][i] for i in np.where(clf.cv_results_['rank_test_score'] == 1)[0]])

mik = bbcpy.functions.classifiers.Miklodyfire2(excllev=1.5, n_cmps=4, autobias=False)
mik.fit(epo_bp, epo_bp.y)

pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire2(excllev=1.5, n_cmps=4, autobias=True))
print(np.mean(cross_val_score(pipeline, epo_bp, epo_bp.y, cv=cv)))

parameters = {'excllev': np.concatenate([[None], np.arange(1, 2, 0.05)]), 'autobias': [True, False],
              'estimator': [covariance._scm, covariance._lwf], 'n_cmps': [2, 3, 4, 6, 8]}
clf = GridSearchCV(bbcpy.functions.classifiers.Miklodyfire2(), parameters, cv=cv)
clf.fit(epo_bp, epo_bp.y)
# print(clf.cv_results_['mean_test_score'])
print(clf.cv_results_['mean_test_score'].max())
# maxind = clf.cv_results_['mean_test_score'].argmax()
# print(clf.cv_results_['params'][maxind])
print([clf.cv_results_['params'][i] for i in np.where(clf.cv_results_['rank_test_score'] == 1)[0]])

pipeline = make_pipeline(bbcpy.functions.spatial.CSP(), bbcpy.functions.classifiers.Wishart())

parameters = {'wishart__excllev': np.concatenate([[None], np.arange(1, 2, 0.1)]), 'wishart__autobias': [True, False],
              'wishart__estimator': [covariance._scm, covariance._lwf, covariance._oas], 'csp__n_cmps': [4, 6, 8, 10]}
clf = GridSearchCV(pipeline, parameters, cv=cv)
clf.fit(epo_bp, epo_bp.y)
print(clf.cv_results_['mean_test_score'])
print(clf.cv_results_['mean_test_score'].max())
# maxind = clf.cv_results_['mean_test_score'].argmax()
# print(clf.cv_results_['params'][maxind])
print([clf.cv_results_['params'][i] for i in np.where(clf.cv_results_['rank_test_score'] == 1)[0]])

from scipy.spatial import distance_matrix

Sigma_tr = epo_bp.cov(target='trial')
Sigma = epo_bp.cov(target='class')
x_n = np.random.randn(*epo_bp.shape[1:])
x_n += 1. / distance_matrix(epo_bp.chans.mnt, epo_bp.chans['C3'].mnt[np.newaxis]+[0, 0.1]) * np.sin(
    2 * np.pi * 10 * np.arange(epo_bp.shape[2]) / epo_bp.fs)
Sigma_tr += x_n @ x_n.T
wx = np.trace((np.linalg.pinv(Sigma[0]) - np.linalg.pinv(Sigma[1])) @ Sigma_tr, axis1=1, axis2=2)
#wx -= np.trace((np.linalg.pinv(Sigma[0]) - np.linalg.pinv(Sigma[1])) @ x_n @ x_n.T, axis1=0, axis2=1)
#wx -= np.trace((np.linalg.pinv(Sigma[0]) - np.linalg.pinv(Sigma[1])) @ np.mean(Sigma_tr, axis=0), axis1=0, axis2=1)
b = (np.log(np.linalg.det(Sigma[0])) - np.log(np.linalg.det(Sigma[1])))
n = epo_bp.shape[-1]
y = (n - 1) * wx + n * b

plt.figure()
plt.hist([y[epo_bp.y == 0], y[epo_bp.y == 1]], 50, density=True)

y_corrected = y - (n-1) * np.trace((np.linalg.pinv(Sigma[0]) - np.linalg.pinv(Sigma[1])) @
                                   (1/(Sigma_tr.shape[0]) * np.sum(Sigma_tr, axis=0)), axis1=0, axis2=1)
# problems: if x_n and epo_bp are correlated? uneven means in the classes?
plt.figure()
plt.hist([y_corrected[epo_bp.y == 0], y_corrected[epo_bp.y == 1]], 50, density=True)

Sigma_tr = epo_bp.cov(target='trial')
Sigma = epo_bp.cov(target='class')
Sigma_tr += Sigma[0] - Sigma[1]
wx = np.trace((np.linalg.pinv(Sigma[0]) - np.linalg.pinv(Sigma[1])) @ Sigma_tr, axis1=1, axis2=2)
b = (np.log(np.linalg.det(Sigma[0])) - np.log(np.linalg.det(Sigma[1])))
n = epo_bp.shape[-1]
y = (n - 1) * wx + n * b
plt.figure()
plt.hist([y[epo_bp.y == 0], y[epo_bp.y == 1]], 50, density=True)

csp = bbcpy.functions.spatial.CSP()
for X in [epo_bp, csp(epo_bp)[0]]:
    Sigma_trial = X.cov(target='trial')
    Sigma_ = X.cov(target='class')
    Sigmainv_ = [np.linalg.pinv(Sigma_[0]), np.linalg.pinv(Sigma_[1])]
    n = X.shape[2]
    px1 = (n - 1) * np.trace(Sigmainv_[0] @ Sigma_trial, axis1=1, axis2=2) + n * np.log(np.linalg.det(Sigma_[0]))
    px2 = (n - 1) * np.trace(Sigmainv_[1] @ Sigma_trial, axis1=1, axis2=2) + n * np.log(np.linalg.det(Sigma_[1]))

    plt.figure()
    plt.plot(px1, px2, color=[0.8] * 3, linestyle='dashed')
    plt.scatter(px1, px2, c=X.y)
    pmax = np.max([px1, px2])
    plt.plot([0, pmax], [0, pmax])

    plt.figure()
    plt.plot(px1)
    plt.plot(px2)

    # plt.figure()
    # plt.plot(np.exp(-px1), np.exp(-px2), color='grey', linestyle='dashed')
    # plt.scatter(np.exp(-px1), np.exp(-px2), c=X.y)

from sklearn import svm

pipeline = make_pipeline(bbcpy.functions.spatial.CSP(n_cmps=2), bbcpy.functions.classifiers.Wishart(excllev=1.4),
                         svm.SVC(C=1))
print(np.mean(cross_val_score(pipeline, epo_bp, epo_bp.y, cv=cv)))

pipeline = make_pipeline(bbcpy.functions.classifiers.Miklodyfire(excllev=1.4), svm.SVC(C=1))
print(np.mean(cross_val_score(pipeline, epo_bp, epo_bp.y, cv=cv)))

wish_art = bbcpy.functions.classifiers.Miklodyfire(excllev=1.5, n_cmps=4)
wish_art.fit(epo_bp, epo_bp.y)
y = wish_art.transform(epo_bp)
plt.figure()
plt.plot(y[:, 0], y[:, 1], color=[0.8] * 3, linestyle='dashed')
plt.scatter(y[:, 0], y[:, 1], c=epo_bp.y)
