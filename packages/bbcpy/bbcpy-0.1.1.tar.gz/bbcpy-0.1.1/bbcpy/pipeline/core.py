import sklearn


# from functools import wraps


# class MakeEpochs(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
#     def __call__(self, *args, **kwargs):
#         print('makey')
#         if isinstance(args[0], bbcpy.datatypes.eeg.Data):
#             self.fs = args[0].fs
#             self.ival = args[1]
#             outval, _ = self.transform(args[0], (args[0].mrk, args[0].mrk.y))
#             return outval
#         else:
#             raise TypeError('First argument needs to be of type Data')
#
#     def __init__(self, fs, ival):
#         self.fs = fs
#         self.ival = ival
#
#     def fit(self, X, y=None):
#         '''Nothing. for compatibility purposes'''
#         return self
#
#     # this is a deviation from sklearn standards, as the y-values are transformed as well.
#     # I (gabriel) wrote a custom pipeline for this, I'll try to get it into the official sklearn build
#     def transform(self, X, y):
#         """Make Epochs.
#
#         Parameters
#         ----------
#         X : ndarray, shape (n_matrices, n_channels, n_times)
#             Multi-channel time-series
#         y : ndarray, shape (n_trials, 2)
#             Marker positions and marker class.
#         Returns
#         -------
#         covmats : ndarray, shape (n_matrices, n_channels, n_channels)
#             Covariance matrices.
#         """
#         if isinstance(X, bbcpy.datatypes.eeg.Data):
#             X.y = y[1]
#             X.mrk = bbcpy.datatypes.eeg.Marker(y[0], y[1], X.mrk.className)
#             epo = bbcpy.functions.structural_manipulations.makeepochs(X, self.ival)
#             return epo, epo.y
#         else:
#             epo, epo_t = bbcpy.functions.structural_manipulations._makeepochs(X, self.fs, y[0], self.ival)
#             return epo, y[1]

class AutoTransformer(sklearn.base.BaseEstimator, sklearn.base.TransformerMixin):
    """

        :param func: function to import
        :param stdpars: standard parameters for the function call that can be set

        Parameters
        ----------
        func : function
            function to import
        stdpars : dict
            parameters for the function call becoming standard. Can be set as key-value pairs.

        Examples:
        _______
        var=bbcpy.pipeline.AutoTransformer(numpy.var, axis=0)

        hilbert=bbcpy.pipeline.AutoTransformer(scipy.signal.hilbert,  keepclass=True, axis=1)
        """

    # stdpars = {}
    # def __call__(self, *args, **kwargs):  # leave it although overwritten in __new__ so interpreter knows its callable
    #    return self.func(*args, **kwargs)

    # @classmethod
    def _get_param_names(self):  # needed for compatibility with sklearn
        return list(self.stdpars) + ['func']

    def get_stdpars(self):
        pars = self.get_params().copy()
        pars.pop('func')
        return pars

    # def __new__(cls, func, **stdpars):
    #     # Add stdpars to func.__doc___, here.
    #     tempdoc = "Transformer class of {0}:\n Runs {0} with {1:} by default\n".format(func.__name__, str(stdpars))+str(func.__doc__)
    #
    #     class AutoTrafo(cls):  # Create temporary class Func to be able to set __call__ doc correctly
    #         """ Transformer class of some function"""
    #
    #         __doc__ = tempdoc  # "Transformer class of {0}:\n{1}".format(func.__name__,tempdoc)
    #
    #         # wrap the doc of function to __call__
    #         #@wraps(func)
    #         def __call__(self, *args, **kwargs):
    #             kwargs2 = self.stdpars.copy()
    #             for key, value in kwargs.items():
    #                 kwargs2[key] = value  # reset to kwargs if passed
    #             if kwargs2.get('func'):  # need to remove func in order for call to work (work-around)
    #                 kwargs2.pop('func')
    #             #if keepclass:
    #             #    return args[0].__class__(func(*args, **kwargs2), *(
    #             #        args[0].__initargs__()))  # set __call__ to function,
    #                 # return outclass(func(*args, **kwargs2), *(
    #                 #    args[0].__initargs__()))  # set __call__ to function,
    #             #else:
    #             return func(*args, **kwargs2)  # set __call__ to function
    #         __call__.__doc__ = tempdoc
    #
    #         def __new__(cls2, func, keepclass=True, **stdpars2):
    #             return cls.__base__.__new__(cls2)
    #
    #         # def __init__(self, func, **stdpars2):
    #         #     self.stdpars = stdpars2
    #         #     for key, value in stdpars2.items():
    #         #         setattr(self, key, value)
    #
    #     obj = AutoTrafo(func, **stdpars)
    #     return obj

    def __init__(self, func, **stdpars):
        """Init."""
        self.func = func
        # stdpars['func'] = func
        self.stdpars = stdpars.keys()
        for key, value in stdpars.items():
            setattr(self, key, value)
        tempdoc = \
            "Transformer class of '{0}':\n Runs '{0}' with {1:} by default\n .transform evaluates the function\n " \
            ".fit doing nothing.\n \n Help of the function:".format(func.__name__, str(stdpars)) + str(func.__doc__)
        self.__doc__ = tempdoc

    def fit(self, x, y=None):
        """Nothing. for compatibility purposes"""
        return self

    def transform(self, x, y=None):
        """Make Epochs.

        Parameters
        ----------
        x : ndarray, shape (n_matrices, n_channels, n_times)
            Multi-channel time-series
        y : ndarray, shape (n_trials, 2)
            Marker positions and marker class.
        Returns
        -------
        covmats : ndarray, shape (n_matrices, n_channels, n_channels)
            Covariance matrices.
        """
        if y is not None:
            x.y = y
            x.mrk.y = y
        out = self.func(x, **self.get_stdpars())
        # if len(self.stdpars):
        #    out = self(x, **self.stdpars)
        #    #out = self(x, self.__getattribute__(*self.stdpars))
        # else:
        #    out = self(x)
        if y is None:
            return out
        elif hasattr(out, 'y'):
            return out, out.y
        else:
            return out, y
