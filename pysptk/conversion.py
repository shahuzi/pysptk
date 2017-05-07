# coding: utf-8

"""
Other conversions
-----------------
.. autosummary::
    :toctree: generated/

    mgc2b

"""

from __future__ import division, print_function, absolute_import

import numpy as np

from pysptk.sptk import mc2b, gnorm, freqt


def mgc2b(mgc, alpha=0.35, gamma=0.0):
    """Mel-generalized cepstrum to MGLSA filter coefficients

    Parameters
    ----------
    mgc : array, shape
        Mel-generalized cepstrum

    alpha : float
        All-pass constant. Default is 0.35.

    gamma : float
        Parameter of generalized log function. Default is 0.0.

    Returns
    -------
    b : array, shape(same as ``mgc``)
        MGLSA filter coefficients

    See Also
    --------
    pysptk.sptk.mlsadf
    pysptk.sptk.mglsadf
    pysptk.sptk.mc2b
    pysptk.sptk.b2mc
    pysptk.sptk.mcep
    pysptk.sptk.mgcep
    pysptk.sptk.mgcep

    """

    b = mc2b(mgc, alpha)
    if gamma == 0:
        return b

    b = gnorm(b, gamma)

    b[0] = np.log(b[0])
    b[1:] *= gamma

    return b


def sp2mc(powerspec, order, alpha):
    # |X(ω)|² -> log(|X(ω)²|)
    logperiodogram = np.log(powerspec)

    # transform log-periodogram to real cepstrum
    # log(|X(ω)|²) -> c(m)
    c = np.fft.irfft(logperiodogram)
    c[0] /= 2.0

    # c(m) -> cₐ(m)
    return freqt(c, order, alpha)


def mc2sp(mc, alpha, fftlen):
    # back to cepstrum from mel-cesptrum
    # cₐ(m) -> c(m)
    c = freqt(mc, int(fftlen // 2), -alpha)
    c[0] *= 2.0

    symc = np.zeros(fftlen)
    symc[0] = c[0]
    for i in range(1, len(c)):
        symc[i] = c[i]
        symc[-i] = c[i]

    # back to power spectrum
    # c(m) -> log(|X(ω)|²) -> |X(ω)|²
    return np.exp(np.fft.rfft(symc).real)
