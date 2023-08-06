# import pyriemann as pr
import numpy as np
import sklearn
import scipy as sp
import scipy.signal
import warnings
import fnmatch

import bbcpy


class Marker(np.ndarray):
    def __new__(cls, mrk_pos, mrk_class, mrk_class_name=None, mrk_fs=1):
        obj = np.asarray(mrk_pos).view(cls)
        obj.y = np.array(mrk_class)
        if mrk_class_name is None:
            mrk_class_name = np.unique(mrk_class)
        obj.className = mrk_class_name
        obj.fs = mrk_fs
        return obj

    def __array_wrap__(self, out_arr, context=None):  #
        obj = super().__array_wrap__(out_arr, context)
        obj.y = np.copy(self.y)
        obj.className = np.copy(self.className)
        obj.fs = np.copy(obj.fs)
        return obj

    def __array_finalize__(self, obj):  #
        self.y = getattr(obj, 'y', None)
        self.className = getattr(obj, 'className', None)
        self.fs = getattr(obj, 'fs', None)

    def __init__(self, mrk_pos, mrk_class, mrk_class_name=None, mrk_fs=1):
        return  # super().init()

    def __getitem__(self, key):
        newy = self.y[key].copy()
        if isinstance(key, int) or ((not isinstance(key, slice)) and len(key) == 1):
            newy = [newy]
        leftclasses = np.unique(self.y[key])
        if len(leftclasses) < len(self.className):
            # if not isinstance(key, int) and len(key) > 1:
            #    warnings.warn('removing void classes')
            newind = 0
            for i in range(len(self.className)):
                if i in leftclasses:
                    newy[newy == i] = newind
                    newind += 1
        newclassName = np.copy([self.className[lc] for lc in leftclasses])
        obj = Marker(super().__getitem__(key).copy(), newy, newclassName, mrk_fs=np.copy(self.fs))
        # add channel selection!
        # if len(self.shape):
        #    obj = Marker(super().__getitem__(key).copy(), newy, newclassName, mrk_fs=np.copy(self.fs))
        # else:
        #    obj = Marker(self.copy(), newy, newclassName, mrk_fs=np.copy(self.fs))
        return obj

    def sort(self, axis=-1, kind=None, order=None):
        sortedinds = self.argsort(axis, kind, order)
        return self[sortedinds]

    def in_ms(self):
        return self / self.fs * 1000

    def in_samples(self, fs=None):
        if fs is None:
            return self
        else:
            return self / self.fs * fs

    def select_classes(self, classes):
        if (type(classes) == list) & (type(classes[0]) == str):
            classes_int = []
            for ii in classes:
                inds = np.where(self.className == ii)[0]
                if inds >= 0:
                    classes_int.append(inds)
                else:
                    warnings.warn('Class not found: "%s"' % ii)
            classes = classes_int
        if type(classes) == int:
            selected = self.y == classes
        else:
            selected = np.zeros(self.shape, dtype=bool)
            for ii in classes:
                selected |= self.y == ii
        obj = self[selected]
        return obj


class Chans(list):
    mnt = None
    shape = ()

    def __init__(self, clab, mnt):
        super().__init__(clab)
        self.mnt = mnt
        self.shape = (len(self),)

    def __initargs__(self):
        return self.mnt

    def __getitem__(self, key):
        if isinstance(key, (list, tuple, np.ndarray)) and len(key) > 1:
            if any([isinstance(k, str) for k in key]):
                key = self.index(key)
            templist = []  # needed because super() does not work inside list comprehension
            for k in key:
                templist.append(super().__getitem__(k))
            obj = self.__class__(templist, self.mnt[key])
        else:
            if isinstance(key, (list, tuple, np.ndarray)) and len(key) == 1:
                key = key[0]
            if isinstance(key, str):
                obj = self.__getitem__(self.index(key))
            else:
                obj = self.__class__(super().__getitem__(key),
                                     self.mnt[key])  # problematic selecting one makes list of char
        obj.shape = (len(obj),)
        return obj

    def copy(self):
        return self.__class__(super().copy(), self.mnt.copy())

    def index(self, __value, __start=..., __stop=..., markmissing=False):
        if isinstance(__value, (list, np.ndarray, tuple)):
            isstr = [isinstance(k, str) for k in __value]
            if any(isstr) and sum(isstr) < len(__value):
                raise ValueError('Either all indices have to be Strings or none.')
            if any(isstr):
                isnot = [x[0] == '~' for x in __value]
                tempChan = self.copy()
                if any(isnot):
                    for i in reversed(np.where(isnot)[0]):
                        tempChan = tempChan[tempChan.index(__value[i])]
                        __value.pop(i)
                if len(__value):  # still commands left after exclusions
                    tempinds = [tempChan.index(name) for name in __value]
                    for i, inds in enumerate(tempinds):
                        if isinstance(inds, int):
                            tempinds[i] = [inds]
                    tempinds = np.unique([item for sublist in tempinds for item in sublist])
                    return [self.index(k) for k in tempChan[tempinds]]
                else:  # only exlcusions
                    tempChan = np.unique(tempChan)
                    return [self.index(k) for k in tempChan]
            else:
                return __value
        else:
            if isinstance(__value, (int, slice)):
                return __value
            keys = __value.split(',')
            if len(keys) > 1:
                return self.index(keys)
            __value = __value.strip()
            if __value[0] == '~':
                exclude = True
                __value = __value[1:]
            else:
                exclude = False
            items = fnmatch.filter(self, __value)
            if (len(items) == 0):
                if markmissing:
                    return None
                else:
                    raise ValueError('\'%s\' not found in channels' % __value)
            if exclude:
                allits = self.copy()
                [allits.remove(it) for it in items]
                items = allits
            outlist = []
            for it in items:
                outlist.append(super().index(it))
            if len(outlist) == 1:
                return outlist[0]
            else:
                return outlist


class Data(np.ndarray):
    def nT(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[1]

    def nCh(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[0]

    def __new__(cls, data, fs, mrk=None, chans=None):
        obj = np.asarray(data).view(cls)
        obj.fs = fs
        obj.mrk = mrk
        obj.chans = chans
        return obj

    # def __init__(self, data, fs, mrk=None, chans=None):
    # data = np.array(data)
    #    return

    def __array_wrap__(self, out_arr, context=None, *args, **kwargs):  # used for printing,squeezing etc
        # return self.__class__(self, *self.__initargs__())
        obj = super().__array_wrap__(out_arr, context)
        obj.fs = self.fs.copy()
        obj.mrk = self.mrk.copy()
        obj.chans = self.chans.copy()
        return obj

    def __array_finalize__(self, obj):  #
        if obj is None: return
        self.fs = getattr(obj, 'fs', None)
        self.mrk = getattr(obj, 'mrk', None)
        self.chans = getattr(obj, 'chans', None)

    def __initargs__(self):
        return self.fs, self.mrk, self.chans

    def __getitem__(self, key):
        if isinstance(key, type(np.newaxis)):
            chans = self.chans.copy()
        elif isinstance(key, (int, str, slice, list, np.ndarray)) or (len(key) == 1):  # or \
            #        (isinstance(key, np.ndarray) and key.dtype == bool):
            key = self.chans.index(key)
            chans = self.chans.copy()[key]
        elif isinstance(key, tuple) and (isinstance(key[0], (int, str, slice, list, np.ndarray))) and (
                len(self.chans.shape) > 0):  # or \
            # (isinstance(key[0], np.ndarray) and key[0].dtype == bool):
            key = list(key)
            key[0] = self.chans.index(key[0])
            key = tuple(key)
            chans = self.chans.copy()[key[0]]
        else:
            chans = self.chans.copy()
        if isinstance(key, tuple) and len(key) > 1 and (isinstance(key[1], (str, list, np.ndarray))):
            key = list(key)
            key[1] = gettimeindices(key[1], self.fs)
            key = tuple(key)

        x = super().__getitem__(key).copy()
        if isinstance(key[1], slice):
            fs = self.fs / key[1].step
        else:
            fs = self.fs
        if x.ndim < 2:  # dimension is lost, keep dimensionnality ?
            if isinstance(key, tuple) and (isinstance(key[0], int) or len(key[0]) == 1):
                x = x[np.newaxis]
            else:
                x = x[:, np.newaxis]
        obj = Data(x, fs, self.mrk, chans)
        return obj

    def copy(self):
        obj = self.__class__(self, *self.__initargs__())
        obj.fs = self.fs.copy()
        obj.mrk = self.mrk.copy()
        obj.chans = self.chans.copy()
        return obj

    def epochs(self, ival, mrk=None, clsinds=None):
        if mrk is None:
            try:
                mrk = self.mrk
            except (NameError, AttributeError):
                raise AttributeError('Error: Cannot make epochs: mrk not provided.')
        if clsinds is not None:
            mrk = mrk.select_classes(clsinds)
        ival = gettimeindices(ival, 1000)
        epo = bbcpy.functions.structural.makeepochs(self, ival, mrk)
        return epo

    def lfilter(self, band, order=5, filttype='*', filtfunc=sp.signal.butter):
        return bbcpy.functions.temporal.lfilter(self, band, order=order, filttype=filttype, filtfunc=filtfunc)
        # band = np.array(band)
        # if filttype == '*':
        #     if band.shape == (2,):
        #         filttype = 'bandpass'
        #     else:
        #         filttype = 'low'
        # [b, a] = filtfunc(order, band / self.fs * 2, filttype)
        # return Data(sp.signal.lfilter(b, a, self, axis=-1), *self.__initargs__())

    # @wraps(bbcpy.functions.statistics.cov)  #does not work due to circular import no solution found so far
    def cov(self, **kwargs):
        return bbcpy.functions.statistics.cov(self, **kwargs)

    def pca(self, **kwargs):
        pca_fitter = sklearn.decomposition.PCA(**kwargs)
        pca_fitter = pca_fitter.fit(self)
        # data = pca_fitter.transform(self)
        data = Data(pca_fitter.transform(self), self.fs, self.mrk)
        data.pcaobj = pca_fitter  # all values like W, A, d are stored in pca object of the EEGdata object
        # self.flat = data.flatten()
        return data

    def save(self, fname, saveData=True):
        np.savez(fname, **self.dataDict(withData=saveData))
        # warnings.warn('Unfinished saving procedure.') could not find what was missing.

    def append(self, data, axis=-1):
        obj = np.concatenate([self, data], axis=axis)
        if axis in (1, -1):  # append in time
            if self.fs != data.fs:
                raise ValueError('Sampling rates must match!')
            if len(self.chans) != len(data.chans) or (
                    np.any(np.isnan([self.chans.index(chan, markmissing=True) for chan in data.chans]))):
                raise ValueError('Channels must match, they do not.')
            mrk = bbcpy.datatypes.eeg.Marker(np.concatenate([self.mrk, data.mrk + self.shape[-1] / self.fs]),
                                             np.concatenate([self.mrk.y, data.mrk.y]), self.mrk.className, self.mrk.fs)
            return bbcpy.datatypes.eeg.Data(obj, self.fs, mrk, self.chans)
        else:  # append in channels
            raise NotImplementedError('not implemented, yet, sorry')

    def dataDict(self, withData=True):
        if withData:
            if self.mrk is None:
                return {'X': np.asarray(self), 'fs': self.fs, 'clab': np.asarray(self.chans), 'mnt': self.chans.mnt}
            return {'X': np.asarray(self), 'fs': self.fs, 'clab': np.asarray(self.chans), 'mnt': self.chans.mnt,
                    'mrk_pos': np.asarray(self.mrk), 'mrk_class': self.mrk.y, 'mrk_className': self.mrk.className}
        else:
            if self.mrk is None:
                return {'fs': self.fs, 'clab': np.asarray(self.chans), 'mnt': self.chans.mnt}
            return {'fs': self.fs, 'clab': np.asarray(self.chans), 'mnt': self.chans.mnt,
                    'mrk_pos': np.asarray(self.mrk), 'mrk_class': self.mrk.y, 'mrk_className': self.mrk.className}


class Epo(Data):
    def __new__(cls, data, time, fs, mrk, chans=None):
        obj = np.asarray(data).view(cls)
        obj.fs = fs
        obj.y = mrk.y
        obj.className = mrk.className
        obj.mrk = mrk
        obj.chans = chans
        obj.t = time
        return obj

    # def __init__(self, data, time, fs, mrk, chans=None):
    # data = np.array(data)
    # assert len(data.shape) < 4

    def __initargs__(self):
        return self.t, self.fs, self.mrk, self.chans

    def __array_wrap__(self, out_arr, context=None, *args, **kwargs):
        obj = super().__array_wrap__(out_arr, context, *args, **kwargs)
        obj.y = np.copy(self.y)
        obj.className = np.copy(self.className)
        return obj

    def __array_finalize__(self, obj):  #
        if obj is None: return
        self.fs = getattr(obj, 'fs', None)
        self.t = getattr(obj, 't', None)
        self.y = getattr(obj, 'y', None)
        self.className = getattr(obj, 'className', None)
        self.mrk = getattr(obj, 'mrk', None)
        self.chans = getattr(obj, 'chans', None)

    def __getitem__(self, key):
        if isinstance(key, type(np.newaxis)):
            mrk = self.mrk.copy()
            choosingmrk = True
        elif isinstance(key, (int, slice, list, np.ndarray)) or (len(key) == 1):  # or \
            #        (isinstance(key, np.ndarray) and key.dtype == bool):
            mrk = self.mrk.__getitem__(key).copy()
            choosingmrk = isinstance(key, slice) and slice.start == slice.stop or isinstance(key, int) or \
                          isinstance(key, (list, tuple)) and (len(key) == 1 or key.dtype == bool and key.sum() == 1)
        elif isinstance(key, tuple) and (isinstance(key[0], (int, slice, list, tuple, np.ndarray))):  # or \
            # (isinstance(key[0], np.ndarray) and key[0].dtype == bool):
            mrk = self.mrk.__getitem__(key[0]).copy()
            choosingmrk = isinstance(key[0], slice) and slice.start == slice.stop or isinstance(key[0], int) or \
                          isinstance(key[0], (list, tuple, np.ndarray)) and \
                          (len(key[0]) == 1 or key[0].dtype == bool and key[0].sum() == 1)
        else:
            mrk = self.mrk.copy()
            choosingmrk = False
        if isinstance(key, tuple) and len(key) > 1 and (isinstance(key[1], (int, str, slice, list, tuple, np.ndarray))) \
                and (len(self.chans.shape) > 0):
            key = list(key)
            if isinstance(key[1], (list, tuple, np.ndarray)) and len(key[1]) == 1:
                key[1] = key[1][0]
            key[1] = self.chans.index(key[1])
            key = tuple(key)
            chans = self.chans.copy()[key[1]]
        else:
            chans = self.chans.copy()
        if isinstance(key, tuple) and len(key) > 2 and (isinstance(key[2], str) or
                                                        (isinstance(key[2], (list, np.ndarray)) and any(
                                                            [isinstance(k, str) for k in key[2]]))):
            key = list(key)
            key[2] = gettimeindices(key[2], 1000)
            # recalculate according to t
            if isinstance(key[2], slice):
                if key[2].start is None:
                    start = None
                else:
                    start = np.where(self.t >= key[2].start)[0][0]
                if key[2].stop is None:
                    stop = None
                else:
                    stop = np.where(self.t >= key[2].stop)[0][0]
                if key[2].step is None:
                    step = None
                else:
                    if np.round(key[2].step / 1000 * self.fs) < 1:
                        raise ValueError('Step size too small.')
                    step = int(np.round(key[2].step / 1000 * self.fs))
                key[2] = slice(start, stop, step)
            else:
                for i, k in enumerate(key[2]):
                    if k < self.t[0] or k > self.t[-1]:
                        raise ValueError('indexed timepoint %f is out of range of data' % k)
                    key[2][i] = np.argmin(np.abs(k - self.t))
                tempkey = np.unique(key[2])
                if len(tempkey) < len(key[2]):
                    warnings.warn('Some indices where used multiple times, reducing to unique indices. '
                                  'This might be caused by sampling rate issues')
                key[2] = tempkey
            key = tuple(key)
        x = np.ndarray.__getitem__(self, key).copy()  # super() would be Data thats why ndarray
        if isinstance(key, tuple) and len(key) > 2:
            t = self.t[key[2]]
            if isinstance(key[2], slice) and key[2].step is not None:
                fs = float(self.fs) / key[2].step
            else:
                fs = self.fs
        else:
            t = self.t
            fs = self.fs

        if x.ndim < 3 and choosingmrk:
            x = x[np.newaxis]
        obj = Epo(x, t, fs, mrk, chans)
        return obj

    # def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
    # print('Hello ufunc')
    #    return super().__array_ufunc__(ufunc, method, np.asarray(*inputs), **kwargs)
    # return self.__class__(super().__array_ufunc__(ufunc, method, np.asarray(*inputs), **kwargs), *self.__initargs__())
    #    if method == '__call__':
    #        return self.__class__(ufunc(*inputs, **kwargs), self.__initargs__())
    #    else:
    #        return ufunc(*inputs, **kwargs)

    # def __array_function__(self, ufunc, method, *inputs, **kwargs):
    #    print('Hello array function')
    #    if method=='__call__':
    #        return self.__class__(ufunc(*inputs, **kwargs), self.__initargs__())
    #    else:
    #        return ufunc(*inputs, **kwargs)

    def dataDict(self, withData=True):
        if withData:
            if self.mrk is None:
                return {'X': np.asarray(self), 'fs': self.fs, 'time': self.t, 'clab': np.asarray(self.chans),
                        'mnt': self.chans.mnt}
            return {'X': np.asarray(self), 'fs': self.fs, 'time': self.t, 'clab': np.asarray(self.chans),
                    'mnt': self.chans.mnt,
                    'mrk_pos': np.asarray(self.mrk), 'mrk_class': self.mrk.y, 'mrk_className': self.mrk.className}
        else:
            if self.mrk is None:
                return {'fs': self.fs, 'clab': np.asarray(self.chans), 'mnt': self.chans.mnt}
            return {'fs': self.fs, 'clab': np.asarray(self.chans), 'mnt': self.chans.mnt,
                    'mrk_pos': np.asarray(self.mrk), 'mrk_class': self.mrk.y, 'mrk_className': self.mrk.className}

    def nT(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[2]

    def nCh(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[1]

    def nEpo(self):
        if np.isscalar(self):
            return 1
        else:
            return self.shape[0]

    def nClass(self):
        if np.isscalar(self):
            return 1
        else:
            return len(self.mrk.className)

    def lfilter(self, band, order=5, filttype='*', filtfunc=sp.signal.butter):
        band = np.array(band)
        if len(band.shape):
            assert band.shape == (2,)
        warnings.warn(
            'Filtering the epoched data is not optimal due to filter artefacts. Consider filtering the continous data before segmentation.')
        return super().lfilter(band, order=order, filttype=filttype, filtfunc=filtfunc)

    def classmean(self, classid=None):
        """"""
        if classid == None:
            outdata = np.empty((self.nClass(), *self.shape[1:]))
            for i in range(self.nClass()):
                outdata[i] = self[self.y == i].mean(axis=0)
            return Epo(outdata, *self.__initargs__())
        return self[self.y == classid]


def gettimeindices(orig_key, fs):
    if isinstance(orig_key, (list, np.ndarray)):
        key = orig_key
        for i in range(len(orig_key)):
            key[i] = gettimeindices(orig_key[i], fs)
            if isinstance(key[i], slice):
                if len(key) > 1:
                    raise ValueError('It is not possible to combine multiple indexings if any of them is a slice.')
                return key[i]
        newkey = []
        for sublist in key:
            if isinstance(sublist, (list, np.ndarray)):
                for item in sublist:
                    newkey.append(item)
            else:
                newkey.append(sublist)
        key = newkey

    elif isinstance(orig_key, str):  # str "100ms:450ms" or "100ms,230ms,..."
        slice_found = False
        key = orig_key.split(",")
        for i, k in enumerate(key):
            key[i] = k.split(":")
            if isinstance(key[i], list) and len(key) > 1 and len(key[i]) > 1:
                raise ValueError('It is not possible to combine multiple indexings if any of them is a slice.')

        key = [[k.strip() for k in k2] for k2 in key]
        for i, k in enumerate(key):
            for i2, k2 in enumerate(k):
                # inums = np.sum([s.isnumeric() for s in k2]) does not work for floats due to point
                inums = len(k2) - np.sum([s.isalpha() for s in k2])
                num = float(k2[:inums])
                if inums < len(k2):
                    unit = k2[inums:]
                    if unit == 'ms':
                        factor = float(fs) / 1000
                    elif unit in ('s', 'sec'):
                        factor = float(fs)
                    elif unit in ('m', 'min'):
                        factor = float(fs) * 60
                    elif unit == 'h':
                        factor = float(fs) * 3600
                    k[i2] = int(np.round(num * factor))
                else:
                    k[i2] = int(k2)
                    warnings.warn(
                        'No unit given for one or more elements in [%s], assuming samples for these.' % (orig_key))
            if len(k) > 1:
                key = slice(*key[i])
                slice_found = True
        if not slice_found:
            key = [item for sublist in key for item in sublist]
    else:
        key = orig_key
    return key
