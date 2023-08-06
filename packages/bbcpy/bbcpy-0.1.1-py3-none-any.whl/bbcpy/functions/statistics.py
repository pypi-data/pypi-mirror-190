import numpy as np
import pandas as pd
import pyriemann as pr
import sklearn as sk
from sklearn.base import BaseEstimator, TransformerMixin

import bbcpy
from bbcpy.functions.base import ImportFunc
import warnings


def cov(obj, axis=1, estimator='scm', target='trial', keep=True):
    """
    :param obj: obj with dim (nTime x nCh) or (nTime x nCh x nEpo)
    :param axis: -1 for time, -2 (default) for channels, 0 for epochs
    :param estimator: 'SCM' (default) for ... (see doc of pyriemann)
    :param target: 'class' (default), 'all' or 'trial' - subgroups for covariance if trialwise data
    :param keep:
    :return:
    Covariance estimation for continous and epoched data
    """
    if type(obj) == bbcpy.datatypes.eeg.Data:
        # different covariance estimators possible
        if hasattr(obj, '_C') & (axis == -2):  # only makes sense for one possible cov which is mostly ChxCh
            return obj.__C
        C = pr.utils.covariance._check_est(estimator)(np.transpose(obj, (-2, -1)))
        if keep & (axis == -2):
            obj.__C = C
        return C
    elif type(obj) == bbcpy.datatypes.eeg.Epo:
        # different covariance estimators possible
        if hasattr(obj, '_C') & (axis == -2) & (target == 'class'):  # only makes sense if only one possible cov
            return obj.__C
        if np.ndim(obj) == 3:
            if (axis == 2) | (axis == -1):
                permord = (2, 1, 0)
                reshapeord = [obj.nT(), obj.nCh()]
                targetint = 1
                covdim = obj.shape[axis]
            elif (axis == 1) | (axis == -2):
                permord = (1, 2, 0)
                reshapeord = [obj.nCh(), obj.nT()]
                targetint = 1
                covdim = obj.shape[axis]
            elif axis == 0:
                permord = (0, 2, 1)
                reshapeord = [1, obj.nT() * obj.nCh()]
                targetint = 0
                if target == 'class':
                    covdim = obj.nClass()
                else:
                    covdim = obj.shape[axis]
                if target == 'trial':
                    warnings.warn('.cov() Ignoring target \'trial\' for axis = 2 because cannot calculate covariance'
                                  ' over trials for each trial')
                    target = 'all'
            else:
                raise ValueError('Unknown axis for cov(): ' + str(axis))
        else:
            if (axis == 1) | (axis == -1):
                permord = (1, 0)
                reshapeord = [obj.shape[1], 1]
                targetint = 1
                covdim = obj.shape[axis]
            elif axis == 0:
                permord = (0, 1)
                reshapeord = [1, obj.shape[1]]
                targetint = 0
                if target == 'class':
                    covdim = obj.nClass()
                else:
                    covdim = obj.shape[axis]
                if target == 'trial':
                    warnings.warn('.cov() Ignoring target \'trial\' for axis = 2 because cannot calculate covariance'
                                  ' over trials for each trial')
                    target = 'all'
            else:
                raise ValueError('Unknown axis for cov(): ' + str(axis))
        if target == 'class':
            C = np.empty((obj.nClass(), covdim, covdim))
            reshapeord2 = reshapeord.copy()
            for i in range(obj.nClass()):
                reshapeord2[targetint] = reshapeord[targetint] * (obj.y == i).sum()
                epoc = np.transpose(obj[obj.y == i], permord)
                epoc = epoc.reshape(reshapeord2)
                C[i] = pr.utils.covariance._check_est(estimator)(epoc)
        elif target == 'trial':
            C = np.empty((obj.nEpo(), covdim, covdim))
            for i in range(obj.nEpo()):
                epoc = np.transpose(obj[i], permord)
                epoc = epoc.reshape(reshapeord)
                C[i] = pr.utils.covariance._check_est(estimator)(epoc)
        elif target == 'all':
            reshapeord[targetint] *= obj.nEpo()
            C = np.empty((covdim, covdim))
            epoc = np.transpose(obj, permord)
            epoc = epoc.reshape(reshapeord)
            C = pr.utils.covariance._check_est(estimator)(epoc)
        else:
            raise ValueError('Unknown target for cov(): ' + target)
        if keep & (axis == -2) & (target == 'class'):
            obj.__C = C
        return C




class ZScore(BaseEstimator, TransformerMixin):
    """Calculate z-score.

        Parameter
        ----------
        mean : float, optional (default: None)
            mean to use for zscoring
        std : float, optional (default: None)
            standard deviation used for zscoring
        online : Bool, optional (default: False)
            trigger for Online zscore estimation. If True, zscore is estimated
            in windows with lenght specified in the 'window' parameter.
        window : int, optional (default: 1000)
            Window length for online zscore estimation. Ignored if
            online=False.
    """

    def __init__(self, mean=None, std=None, online=False, window=1000):
        self.online = online
        self.mean = mean
        self.std = std
        self.window = window

    def fit(self, X, y=None):
        """Fit the Transformer.

        Parameter
        ----------
        X : ndarray, shape (n_samples, n_channels)
            Training data.
        y : ndarray, shape (n_samples), optional (default: None)
            Training data labels.

        """

        if not self.online:
            if self.mean is None:
                self.mean = np.mean(X, axis=0)
            if self.std is None:
                self.std = np.std(X, axis=0)

        return self

    def transform(self, X, y=None):
        """Fit the Transformer.

        Parameter
        ----------
        X : ndarray, shape (n_samples, n_channels)
            Data set.
        y : ndarray, shape (n_samples), optional (default: None)
            Labels for data set.

        """
        if self.online:
            m = np.array([pd.Series(xtmp).rolling(window=self.window,
                                                  min_periods=1).mean() for xtmp
                          in X.T]).T
            s = np.array([pd.Series(xtmp).rolling(window=self.window,
                                                  min_periods=1).std() for xtmp
                          in X.T]).T
            s[0] = np.ones(X.shape[-1])

            zs = (X - m) / s
        else:
            zs = (X - self.mean) / self.std
        # nan_to_num is needed when a signal is constant over a window length
        return np.nan_to_num(zs, posinf=0.0, neginf=0.0)




#todo re-write as simple function?
class LogVariance(sk.base.BaseEstimator, sk.base.TransformerMixin):
    """Return the logarithm of the variance
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.log(np.var(X, axis=2))

# Implementing simple numpy var as a transformer type:
var = ImportFunc(np.var, axis=2)

#todo delete the following?
class Variance(sk.base.BaseEstimator, sk.base.TransformerMixin):
    """Return the logarithm of the variance
    """

    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return np.var(X, axis=2)
