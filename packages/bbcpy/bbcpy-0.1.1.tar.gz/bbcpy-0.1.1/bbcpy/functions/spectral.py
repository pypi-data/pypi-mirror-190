import sklearn as sk
import numpy as np
from scipy import signal
import bbcpy

#todo rerwrite as simple function not transformer
class PSD(sk.base.BaseEstimator, sk.base.TransformerMixin):
    """Return the PSD
    """

    def __call__(self, data: bbcpy.datatypes.eeg.Data):
        return self.transform(data)

    def __init__(self, freq_range=[], window='hann', nperseg=100, axis=-1, dB=True):
        self.window = window
        self.nperseg = nperseg
        self.axis = axis
        self.freq_range = freq_range
        self.dB = dB

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        f, Pxx = signal.welch(X, fs=X.fs, window=self.window, nperseg=self.nperseg, axis=self.axis)
        if len(self.freq_range):
            fsel = (f >= self.freq_range[0]) & (f <= self.freq_range[1])
            if self.axis == -1:
                Pxx = Pxx[:, :, fsel]
            elif (self.axis == 2) | (self.axis == -2):
                Pxx = Pxx[:, fsel]
            else:
                Pxx = Pxx[fsel]
            f = f[fsel]
        if self.dB:
            Pxx = 10 * np.log10(np.abs(Pxx))
        return X.__class__(Pxx, f, *X.__initargs__()[1:])
