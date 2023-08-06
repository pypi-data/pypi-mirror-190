import numpy as np
import scipy as sp
import sklearn as sk
from sklearn.base import TransformerMixin, BaseEstimator

import bbcpy.datatypes.eeg
#from bbcpy.functions import ImportFunc
#from bbcpy.datatypes import eeg


class CSP(sk.base.BaseEstimator, sk.base.TransformerMixin):
    def __call__(self, epo: bbcpy.datatypes.eeg.Epo, n_cmps=6):
        transformer = self.__class__(n_cmps)
        transformer.fit(epo)
        return transformer.transform(epo), transformer

    def __init__(self, n_cmps=6, excllev=None, estimator='scm'):
        self.n_cmps = n_cmps
        self.excllev = excllev
        self.estimator = estimator

    def fit(self, x, y=None, n_cmps=None):
        '''Fit CSP'''
        if n_cmps is None:
            n_cmps = self.n_cmps
        if y is not None:
            x.y = y
            x.mrk.y = y
        if self.excllev is not None:
            Sigma_trial = x.cov(target='trial')  # no estimator here because on single trials, this will fuck up excllev
            covtr = np.trace(np.linalg.pinv(x.cov(target='all', estimator=self.estimator)) @ Sigma_trial, axis1=1,
                             axis2=2) / x.shape[1]
            sel_tr = covtr <= self.excllev
            covs = x[sel_tr].cov(target='class', estimator=self.estimator)
        else:
            covs = x.cov(target='class', estimator=self.estimator)
        d, W = sp.linalg.eigh(covs[0], covs[0] + covs[1])
        selected_csps = np.flipud(np.argsort(np.maximum(d, 1 - d)))[:n_cmps]
        self.d = d[selected_csps]
        self.W = W[:, selected_csps]
        covX = x.cov(target='all', estimator=self.estimator)
        self.A = covX@W@(W.T@covX@W)[:, selected_csps]
        return self

    def transform(self, x, y=None):
        """Apply CSP.

        Parameters
        ----------
        x : ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        y : ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        Returns
        -------
        out : ndarray, shape (n_matrices, n_csp, n_time)
            transformed
        """
        return self.W.T@x

class CSP_general(BaseEstimator, TransformerMixin):
    def __init__(self, n_cmps=6):
        self.n_cmps=n_cmps

    def fit(self, x, y=None):
        '''Fit CSP'''
        classes = np.unique(y)
        c1 = sk.covariance.OAS().fit(x[y == classes[0]]).covariance_
        c2 = sk.covariance.OAS().fit(x[y == classes[1]]).covariance_
        d, W = sp.linalg.eigh(c1, c1 + c2)
        selected_csps = np.flipud(np.argsort(np.maximum(d, 1 - d)))[:self.n_cmps]
        self.d = d[selected_csps]
        self.W = W[:, selected_csps]
        return self

    def transform(self, x, y=None):
        """Apply CSP.
        Parameters
        ----------
        x : ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        y : ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        Returns
        -------
        out : ndarray, shape (n_matrices, n_csp, n_time)
            transformed
        """
        return (self.W.T@x.T).T


class BandWiseCSP(BaseEstimator, TransformerMixin):
    """Calculates and applies MNE's CSP.

    Parameters
    ----------
    n_components : int
        Number of components per filtered data subset.
    block_size : int or list
        Block sizes for the individual filter bands. If int, blocks are assumed
        to be of the same size. If a list is passed, the block sized are the
        individual entries.
    """
    def __init__(self, n_components, block_size):
        self.n_components = n_components
        self.block_size = block_size

    def fit(self, X, y=None):
        if type(self.block_size) is int:
            self._blocks = [self.block_size for i in
                            range(int(X.shape[1] // self.block_size))]
        else:
            self._blocks = self.block_size
        self.csps = []
        start = 0
        for i in self._blocks:
            end = start + i
            self.csps.append(CSP_general(n_cmps=self.n_components))
            self.csps[-1].fit(X[:, start:end], y)
            start = end

        return self

    def transform(self, X):
        filtered_signal = np.zeros(
            (X.shape[0], self.n_components * len(self._blocks)))
        start = 0
        for i, (block, csp) in enumerate(zip(self._blocks, self.csps)):
            end = start + block
            filtered_signal[:, i * self.n_components:(i + 1) * self.n_components] = csp.transform( # noqa
                X[:, start:end])
            start = end

        return filtered_signal

# todo rerwrite as simple function not transformer
class Rereferencing(BaseEstimator, TransformerMixin):
    """Rereferencing.
        ----------
        method : str
            Rereferencing method.
        reref_idx : list
            list of rereferencing electrodes for each channel for custom
            rereferencing.
        """

    def __init__(self, method, reref_idx=None):
        self.method = method
        self.reref_idx = reref_idx
        self.reref_function = self.reref_methods[method]

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return self.reref_function(self, X)

    def fit_transform(self, X, y=None):
        return self.reref_function(self, X)

    def reref_avg(self, X, reref_idx=None):
        return (X.T - X.mean(axis=1)).T

    def reref_bipolar(self, X, reref_idx=None):
        X_ = np.roll(X, 1)
        return X - X_

    def reref_custom(self, X):
        X_T = X.T
        for i, x in enumerate(X_T):
            x -= np.mean(X[self.reref_idx[i]], axis=1)
        return X_T.T

    reref_methods = {
        'average': reref_avg,
        'bipolar': reref_bipolar,
        'custom': reref_custom
    }


def car(data):
    return data - np.mean(data, axis=1)


def laplace(data):
    if hasattr(data, 'chans') and hasattr(data.chans, 'mnt'):
        return
    else:
        return

def laplace_dan2D(data):
    if hasattr(data, 'chans') and hasattr(data.chans, 'mnt'):
        return
    else:
        return
