import numpy as np
import scipy as sp
from numpy.lib.stride_tricks import sliding_window_view
from scipy import signal
from sklearn.base import BaseEstimator, TransformerMixin
import mne

from bbcpy.functions.base import ImportFunc


def lfilter(obj, band, axis=-1, order=5, filttype='*', filtfunc=sp.signal.butter):
    band = np.array(band)
    if len(band.shape):
        assert band.shape == (2,)
    if filttype == '*':
        if band.shape == (2,):
            filttype = 'bandpass'
        else:
            filttype = 'low'
    [b, a] = filtfunc(order, band / obj.fs * 2, filttype)
    return obj.__class__(sp.signal.lfilter(b, a, obj, axis=axis), *obj.__initargs__())

def lfilter_sos(obj, band, axis=-1, order=5, filttype='*', filtfunc=sp.signal.butter):
    band = np.array(band)
    if len(band.shape):
        assert band.shape == (2,)
    if filttype == '*':
        if band.shape == (2,):
            filttype = 'bandpass'
        else:
            filttype = 'low'
    sos = filtfunc(order, band / obj.fs * 2, filttype)
    return obj.__class__(signal.sosfilt(sos, obj, axis=axis), *obj.__initargs__())


#todo re-write as function? also could be done by lfilter
class NotchFilter(BaseEstimator, TransformerMixin):
    """Transformer for mne notch filtering.
    ----------
    sample_rate : int
        Signal sample rate.
    line_noise : int
        Line noise
    """

    def __init__(self, sample_rate, line_noise):
        self.sample_rate = sample_rate
        self.line_noise = line_noise

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_ = self._notch_filter(X)
        return X_

    def fit_transform(self, X, y=None):
        X_ = self._notch_filter(X)
        return X_

    def _notch_filter(self, dat_):
        filt = mne.filter.notch_filter(x=dat_.T,
                                       Fs=self.sample_rate,
                                       trans_bandwidth=7,
                                       freqs=np.arange(self.line_noise,
                                                       4*self.line_noise,
                                                       self.line_noise),
                                       fir_design='firwin',
                                       verbose=False,
                                       notch_widths=1,
                                       filter_length=dat_.shape[0] - 1)
        return filt.T


class BandPassFilter(BaseEstimator, TransformerMixin):
    """Wrapper for MNEs Band Pass filtering.

        Parameter
        ----------
        filter_bands : list
            List of filter bands.
        sample_rate : int
            Signal sample rate
        filter_len : int or str
            lenght of the filter. The default is 1000ms.
        l_trans_bandwidth : int, optional
            The default is 4.
        h_trans_bandwidth : int, optional
            The default is 4.
    """

    def __init__(self, *,
                 filter_bands,
                 sample_rate,
                 filter_len='1000ms',
                 l_trans_bandwidth=4,
                 h_trans_bandwidth=4):
        self.filter_bands = filter_bands
        self.sample_rate = sample_rate
        self.filter_len = filter_len
        self.l_trans_bandwidth = l_trans_bandwidth
        self.h_trans_bandwidth = h_trans_bandwidth
        self.filters = _calc_band_filters(self.filter_bands,
                                          self.sample_rate,
                                          self.filter_len,
                                          self.l_trans_bandwidth,
                                          self.h_trans_bandwidth)

    def fit(self, X, y=None):
        self.filters = _calc_band_filters(self.filter_bands,
                                          self.sample_rate,
                                          self.filter_len,
                                          self.l_trans_bandwidth,
                                          self.h_trans_bandwidth)
        return self

    def transform(self, X, y=None):
        X_ = _apply_filter(X, self.filters)
        return X_

    def fit_transform(self, X, y=None):
        self.filters = _calc_band_filters(self.filter_bands,
                                          self.sample_rate,
                                          self.filter_len,
                                          self.l_trans_bandwidth,
                                          self.h_trans_bandwidth)
        X_ = _apply_filter(X, self.filters)
        return X_


def _calc_band_filters(f_ranges,
                       sample_rate,
                       filter_len="1000ms",
                       l_trans_bandwidth=4,
                       h_trans_bandwidth=4):
    """Calculate band filters.

    This function returns for the given frequency band ranges filter
    coefficients with length "filter_len"
    Thus the filters can be sequentially used for band power estimation

    Parameters
    ----------
    f_ranges : TYPE
        DESCRIPTION.
    sample_rate : float
        sampling frequency.
    filter_len : int,
        lenght of the filter. The default is 1001.
    l_trans_bandwidth : TYPE, optional
        DESCRIPTION. The default is 4.
    h_trans_bandwidth : TYPE, optional
        DESCRIPTION. The default is 4.
    Returns
    -------
    filter_fun : array
        filter coefficients stored in rows.
    """
    filter_fun = []

    for a, f_range in enumerate(f_ranges):
        h = mne.filter.create_filter(None,
                                     sample_rate,
                                     l_freq=f_range[0],
                                     h_freq=f_range[1],
                                     fir_design='firwin',
                                     l_trans_bandwidth=l_trans_bandwidth,
                                     h_trans_bandwidth=h_trans_bandwidth,
                                     filter_length=filter_len,
                                     verbose=False)

        filter_fun.append(h)

    return np.array(filter_fun)


def _apply_filter(dat_, filter_fun):
    """
    For a given channel, apply previously calculated filters
    Parameters
    ----------
    dat_ : array (ns,)
        segment of data at a given channel and downsample index.
    sample_rate : float
        sampling frequency.
    filter_fun : array
        output of calc_band_filters.
    line_noise : int|float
        (in Hz) the line noise frequency.
    seglengths : list
        list of ints with the leght to which variance is calculated.
        Used only if variance is set to True.
    variance : bool,
        If True, return the variance of the filtered signal, else
        the filtered signal is returned.
    Returns
    -------
    filtered : array
        if variance is set to True: (nfb,) array with the resulted variance
        at each frequency band, where nfb is the number of filter bands used to decompose the signal
        if variance is set to False: (nfb, filter_len) array with the filtered signal
        at each freq band, where nfb is the number of filter bands used to decompose the signal
    """ #noqa
    filtered = []

    for filt in range(filter_fun.shape[0]):
        for ch in dat_.T:
            filtered.append(signal.convolve(ch, filter_fun[filt, :], mode='same'))

    return np.array(filtered).T

#todo re-write as function
class SlidingWindows(BaseEstimator, TransformerMixin):
    """Sliding window transformer class.

    Parameter
    ----------
    window_size : int
        Desired size of windows.
    step_size: int
        Step size in between consecutive windows. Must be 1 or larger.
    label_handling: {'unique', 'mean', 'max', 'min', 'first', 'last',
    'center'}
        Decides which label to assign to the extracted sliding windows.
    adjust_class_size: Bool, default: False
        Switch to adjust classes to have the same number of samples.
    max_samples_per_class: int, optional (default: -1)
        Maximum samples per class. Only used, if adjust_class_size=True.
        Can oversample.
        Uses size of largest class if set to -1.
        Uses size of smallest class if set to 0.
    feature_transformer: sklearn Transformer, optional (default: None)
        Sklearn transformer to call on sliding windows to return features.
    """
    def __init__(self,
                 *,
                 window_size=100,
                 window_size_test=None,
                 step_size=100,
                 step_size_test=None,
                 label_handling='unique',
                 label_handling_test=None,
                 adjust_class_size=False,
                 adjust_class_size_test=None,
                 max_samples_per_class=0,
                 max_samples_per_class_test=None,
                 feature_transformer=None):
        self.window_size = window_size
        self.window_size_test = window_size_test
        self.step_size = step_size
        self.step_size_test = step_size_test
        self.label_handling = label_handling
        self.label_handling_test = label_handling_test
        self.adjust_class_size = adjust_class_size
        self.adjust_class_size_test = adjust_class_size_test
        self.max_samples_per_class = max_samples_per_class
        self.max_samples_per_class_test = max_samples_per_class_test
        self.feature_transformer = feature_transformer
        self.class_count_test = None
        self.class_count_train = None

    def fit(self, X, y=None):
        """Fit (do nothing)."""
        return self

    def transform(self, X, y=None):
        """Transform X into sliding windows.

        Parameters
        ----------
        X : ndarray, shape (n_trials, n_channels)
            Multi-channel time-series.
        y : ndarray, shape (n_trials,)
            Label for each trial.
        Returns
        -------
        out :   ndarray, shape ((n_matrices-window_size)/step_size, n_channels,
                window_size)
            Sliding windows.
        """
        window_size = ifaisnonethenbelsea(self.window_size_test,
                                          self.window_size)
        step_size = ifaisnonethenbelsea(self.step_size_test, self.step_size)
        label_handling = ifaisnonethenbelsea(self.label_handling_test,
                                             self.label_handling)
        adj = ifaisnonethenbelsea(self.adjust_class_size_test,
                                  self.adjust_class_size)
        mspc = ifaisnonethenbelsea(self.max_samples_per_class_test,
                                   self.max_samples_per_class)

        res = sliding_windows(X,
                              y=y,
                              window_size=window_size,
                              step_size=step_size,
                              label_handling=label_handling,
                              adjust_class_size=adj,
                              max_samples_per_class=mspc)
        if y is None:
            return res

        Xt, yt = res
        self.class_count_test = np.unique(yt, return_counts=True)
        if self.feature_transformer is not None:
            Xt = self.feature_transformer.transform(Xt)
        return Xt, yt

    def fit_transform(self, X, y=None):
        res = sliding_windows(X,
                              y=y,
                              window_size=self.window_size,
                              step_size=self.step_size,
                              label_handling=self.label_handling,
                              adjust_class_size=self.adjust_class_size,
                              max_samples_per_class=self.max_samples_per_class)
        if y is None:
            return res

        Xt, yt = res
        self.class_count_train = np.unique(yt, return_counts=True)
        if self.feature_transformer is not None:
            Xt = self.feature_transformer.fit_transform(Xt, yt)
        return Xt, yt


def ifaisnonethenbelsea(a, b):
    """Return a if a is not None, else return b

    Parameters
    ----------
    a : Object
    b : Object

    Returns
    -------
    out : Object
    """
    if a is None:
        return b
    else:
        return a

def sliding_windows(X,
                    y=None,
                    *,
                    window_size=100,
                    step_size=100,
                    label_handling='unique',
                    adjust_class_size=False,
                    max_samples_per_class=-1):

    x_windowed = sliding_window_view(X,
                                     window_size,
                                     axis=0)[::step_size]
    if y is None:
        return x_windowed

    y_windowed = sliding_window_view(y,
                                     window_size,
                                     axis=0)[::step_size]

    Xt, yt = label_window_decision(y_windowed,
                                   x_windowed,
                                   label_handling)
    if adjust_class_size:
        idx = adjust_class_sizes(yt, max_samples_per_class)
        Xt, yt = Xt[idx], yt[idx]

    return Xt, yt


def adjust_class_sizes(y, max_samples_per_class=0):
    """Equalize class sizes.

        Parameters
        ----------
        y : ndarray, shape (n_trials,)
            Label vector.
        max_samples_per_class : int, default: 0
            Maximum number of samples that are extracted per class. Allows for
            oversampling. If -1, the maximum number of samples for any class
            is used. If 0, the minimum number of samples for any class is used.

        Returns
        -------
        idx :   ndarray, shape (max_samples_per_class*n_classes)
            Indices of elements in y to be extracted to adjust the class sizes.
    """
    classes, counts = np.unique(y, return_counts=True)
    if max_samples_per_class == -1:
        max_samples_per_class = np.max(counts)
    if max_samples_per_class == 0:
        max_samples_per_class = np.min(counts)
    full_idx = np.arange(0, len(y))
    reduced_idx = []
    for cl in classes:
        cl_idx = full_idx[y == cl]
        idx_subset = np.round(np.linspace(-0.5,
                                          len(cl_idx) - .501,
                                          max_samples_per_class)
                              ).astype(int)
        cl_idx_subset = cl_idx[idx_subset]
        reduced_idx.append(cl_idx_subset)
    reduced_idx = np.sort(np.concatenate(reduced_idx))
    return reduced_idx


def label_window_decision(y_windows, x_windows, handler='unique'):
    """Decide how to handle labels in windows.
        Parameter
        ----------
        y_windows : ndarray, shape (??)
            Label windows.
        x_windows: ndarray, shape (??)
            Data Windows.
        handler: {'unique', 'mean', 'max', 'min', 'first', 'last', 'center'}
            Decides which label to assign to the extracted sliding windows.
    """
    if handler == 'unique':
        # all labels are set to at least 1, otherwise it would fail for negative
        # labels
        y2 = y_windows + y_windows.min() + 1
        # substract first entry from full windows for each window then take sum
        unique_label = np.sum((y2.T - y2[:, 0]), axis=0)
        # if the sum is 0, labels across window are the same
        return x_windows[unique_label == 0], y_windows[unique_label == 0, 0]

    elif handler == 'mean':
        return x_windows, np.mean(y_windows, axis=1)
    elif handler == 'max':
        return x_windows, np.max(y_windows, axis=1)
    elif handler == 'min':
        return x_windows, np.min(y_windows, axis=1)
    elif handler == 'first':
        return x_windows, y_windows[:, 0]
    elif handler == 'last':
        return x_windows, y_windows[:, -1]
    elif handler == 'center':
        midpoint = y_windows.shape[-1]//2
        return x_windows, y_windows[:, int(midpoint)]
    else:
        print('Handler method not known. Returning original array.')
        return x_windows, y_windows
