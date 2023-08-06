from bbcpy.pipeline.core import AutoTransformer
import warnings


# inherit from functools?!
class ImportFunc:
    """
        Import any function working on data to the bbcpy toolbox. These are automatically usable by the pipeline with
        an automated transformer type.
        :parameter
        func: function to import
        outClass: class that the function should return. Can be None to not care about the class, "same" for same class
         as input or a class type.
        **kwargs: arguments to the class
        Examples:
            var = ImportFunc(np.var,outClass=None
    """

    def __call__(self, data, *args, **kwargs):
        if not len(args) and not len(kwargs):
            args = self.args
            kwargs = self.kwargs
        if self.outClass is None:
            return self.__func__(data, *args, **kwargs)
        elif self.outClass == 'same':
            try:
                return data.__class__(self.__func__(data, *args, **kwargs), *data.__initargs__())
            except (TypeError):
                warnings.warn('Same class not possible as output, returning as Numpy array')
                return self.__func__(data, *args, **kwargs)
        else:
            if hasattr(self.outClass, '__initargs__'):
                return self.outClass(self.__func__(data, *args, **kwargs),
                                     *self.outClass.__initargs__())#to be improved: attribute check, if there
            else:
                return self.outClass(self.__func__(data, *args, **kwargs)) #to be improved: attribute check, if there

    def __init__(self, func,  *args, outClass=None, **kwargs):  # safe imports? give option for where to put in lib?
        self.__func__ = func
        self.args = args
        self.kwargs = kwargs
        self.outClass = outClass

    def trafo(self):
        return AutoTransformer(self.__func__, *self.args, **self.kwargs)
