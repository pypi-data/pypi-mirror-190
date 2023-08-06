import numpy as np
import bbcpy
#from bbcpy.pipeline import ImportFunc

def makeepochs(x: bbcpy.datatypes.eeg.Data, ival: np.ndarray, mrk = None) -> bbcpy.datatypes.eeg.Epo:
    """
    Usage:
        makeepochs(X, ival)
    Parameters:
        x: 2D array of multi-channel timeseries (channels x samples) of type EEGdata
        ival: a two element vector giving the time interval relative to markers (in ms)
    Returns:
        epo: a 3D array of segmented signals (samples x channels x epochs) of type EEGepo
    """
    if isinstance(ival, slice):
        if ival.start is None:
            start = 0
        else:
            start = ival.start
        if ival.stop is None:
            stop = 0
        else:
            stop = ival.stop
        if not ival.step is None:
            x = x[::ival.step]
            start = start / ival.step
            stop = stop / ival.step
        ival = [start, stop]
    if mrk is None:
        mrk = x.mrk.copy()
    time = np.arange(int(np.floor(ival[0] * x.fs / 1000)),
                     int(np.ceil(ival[1] * x.fs / 1000)) + 1, dtype=int)[np.newaxis, :]
    T = time.shape[1]
    nEvents = len(mrk)
    nChans = x.shape[0]
    idx = (time.T + np.array([mrk.in_samples(x.fs)])).reshape(T * nEvents).astype(int)
    epo = np.array(x)[:, idx].reshape(nChans, T, nEvents)
    epo = np.transpose(epo, (2, 0, 1))
    epo_t = np.linspace(ival[0], ival[1], T)
    epo = bbcpy.datatypes.eeg.Epo(epo, epo_t, x.fs, mrk, x.chans)
    return epo
