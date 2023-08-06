import warnings

import numpy as np
import scipy as sp
from matplotlib import pyplot as plt


def map(eegdata, v=None, clim='minmax', cb_label='', colorbar=True, senspos=True, aspect='equal',
        extent=None):
    '''
    Usage:
        scalpmap(mnt, v, clim='minmax', cb_label='')
    Parameters:
        mnt: a 2D array of channel coordinates (channels x 2)
        v:   a 1D vector (channels)
        clim: limits of color code, either
          'minmax' to use the minimum and maximum of the data
          'sym' to make limits symmetrical around zero, or
          a two element vector giving specific values
        cb_label: label for the colorbar
    '''
    mnt = eegdata.chans.mnt
    if np.any(np.isnan(mnt)):
        v = v[~np.isnan(mnt[:, 0])]
        mnt = mnt[~np.isnan(mnt[:, 0]), :]
        warnings.warn('Some sensor positions are undefined and thus excluded from plotting.')

    maxx = np.max([mnt[:, 0].max(), 1])
    maxy = np.max([mnt[:, 1].max(), 1])
    maxi = np.max([maxx,maxy])
    if extent is None:
        extent = np.array([-1, 1, -1, 1]) * maxi
    # interpolate between channels
    xi, yi = np.linspace(-1, 1, 100) * maxx, np.linspace(-1, 1, 100) * maxy
    xi, yi = np.meshgrid(xi, yi)
    rbf = sp.interpolate.Rbf(mnt[:, 0], mnt[:, 1], v, function='linear')
    zi = rbf(xi, yi)

    # mask area outside of the scalp
    a, b, n, r = 50, 50, 100, 50
    mask_y, mask_x = np.ogrid[-a:n - a, -b:n - b]
    mask = mask_x * mask_x + mask_y * mask_y >= r * r
    zi[mask] = np.nan

    if clim == 'minmax':
        vmin = v.min()
        vmax = v.max()
    elif clim == 'sym':
        vmin = -np.absolute(v).max()
        vmax = np.absolute(v).max()
    else:
        vmin = clim[0]
        vmax = clim[1]

    plt.imshow(zi, vmin=vmin, vmax=vmax, aspect=aspect, origin='lower', extent=extent, cmap='jet')
    if colorbar:
        plt.colorbar(shrink=.5, label=cb_label)
    if senspos:
        plt.scatter(mnt[:, 0], mnt[:, 1], c='k', marker='+', vmin=vmin, vmax=vmax)
    plt.axis('off')
