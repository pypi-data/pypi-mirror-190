import numpy as np


class array(np.ndarray):
    def save(self, fname):
        dims = self.shape
        savelist = [ x.dataDict for x in np.nditer(self)]
        np.save(fname, np.reshape(savelist,dims))
