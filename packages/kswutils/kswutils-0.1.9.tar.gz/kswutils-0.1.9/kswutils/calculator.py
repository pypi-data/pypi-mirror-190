import math

import numpy as np
import scipy
import scipy.stats as stat
from scipy import signal
from scipy.fft import fft, fftfreq, rfft, rfftfreq


# Check if a string is number
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def calc_fft(data, sample_rate):
    """Calculate FFT. Transfrom Signal data from
    Time domain to Frequenct domain.

    Args:
        data (numpy.ndarray): Signal data in Time domain
        sample_rate (scalar): Sampling rate [Hz]

    Returns:
        1. numpy.ndarray: x-axis value: frequency
        2. numpy.ndarray: y-axis value: magnitude
    """
    sample_size = len(data)

    # yf = fft(data)
    # xf = fftfreq(sample_size, 1 / sample_rate)

    # yf = rfft(data)  # only get the right side
    yf = rfft(data, norm='forward')  # norm='forward' 'ortho'

    # as used rfft, need to use to rfftfreq to map
    xf = rfftfreq(sample_size, 1 / sample_rate)

    # How to plot:
    # plt.plot(xf, np.abs(yf))
    # plt.show()
    return xf, np.abs(yf)


def calc_spectogram(data, sample_rate):
    f, t, Sxx = signal.spectrogram(data, sample_rate)

    # How to plot:
    # fig, ax = plt.subplots()
    # spectro = ax.pcolormesh(t, f, Sxx, shading='gouraud')
    # fig.colorbar(spectro, label='|FFT Amplitude|')
    # ax.set_ylabel('Frequency [Hz]')
    # ax.set_xlabel('Time [sec]')
    # plt.show()
    return f, t, Sxx


def calc_rolling_rms(data, window_size):
    """Calculate the rolling RMS

    Args:
        data (numpy.ndarray): data
        window_size (scalar): window size

    Returns:
        numpy.ndarray: rolling_rms with the window_size of the data
    """
    # # this particular implementation skips the first valid entry,
    # # so if you want it, you can insert a zero at the beginning of x.
    # xc = np.cumsum(abs(data)**2)
    # return np.sqrt((xc[window:] - xc[:-window]) / window)

    data2 = np.power(data, 2)
    n = np.ones(window_size)/float(window_size)
    return np.sqrt(np.convolve(data2, n, 'valid'))


def calc_peak(data):
    return np.absolute(data).max()


def calc_std(data):
    return np.std(data)


def remove_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]


def calc_rms_value(s):
    return np.sqrt(np.mean(s**2))


def calc_skew_value(s):
    return stat.skew(s)


def calc_kurtosis_value(s):
    return stat.kurtosis(s)


def calc_crest_value(s):
    return s.max()/np.sqrt(np.mean(s**2))


def calc_clearance_value(s):
    return s.max()/np.mean(np.sqrt(abs(s)))**2


def clac_shape_value(s):
    return np.sqrt(np.mean(s**2))/np.mean(abs(s))


def calc_impulse_value(s):
    return s.max()/np.mean(abs(s))


class DF_Rolling:
    def __init__(self, window) -> None:
        self.N = window

    def the_mean(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).mean()

    def the_std(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).std()

    def the_rms(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(calc_rms_value)

    def the_skew(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(calc_skew_value)

    def the_kurtosis(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(calc_kurtosis_value)

    def the_crest_factor(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(calc_crest_value)

    def the_clearance_factor(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(calc_clearance_value)

    def the_shape_factor(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(clac_shape_value)

    def the_impulse_factor(self, serie, **kwargs):
        N = kwargs.get('window', self.N)
        return serie.rolling(N).apply(calc_impulse_value)
