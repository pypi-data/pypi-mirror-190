import numpy as np
from bbcpy.functions.base import ImportFunc


def baseline(epo, ref_ival):
    '''
    Usage:
        epo = baseline(epo, epo_t, ref_ival)
    Parameters:
        epo: a 3D array of segmented signals, see makeepochs
        epo_t: a 1D array of time points of epochs relative to marker (in ms)
        ref_ival: a two element vector specifying the time interval for which the baseline is calculated [ms]
    '''
    if ((ref_ival[0] < epo.t[0]) | (ref_ival[1] > epo.t[-1])):
        raise ValueError('reference interval not inside epo')
    idxref = (ref_ival[0] <= epo.t) & (epo.t <= ref_ival[1])
    eporef = np.mean(epo[:, :, idxref], axis=2, keepdims=True)
    epo = epo - eporef
    return epo


# Now building the function as a transformer type:
baseline = ImportFunc(baseline, ref_ival=[-100, 0])
