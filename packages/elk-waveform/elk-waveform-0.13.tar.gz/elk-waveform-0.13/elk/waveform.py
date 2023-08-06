"""
This module contains code for wrapping lalsuite functionality
in a more pythonic manner to allow the creation of waveforms.
"""

import torch
import pycbc.types.timeseries
from pycbc.waveform import get_td_waveform
import h5py
from astropy import constants as c
# import lal
# import lalsimulation as lalsim
import numpy as np
from .exceptions import LalsuiteError
from scipy.interpolate import interp1d
from scipy.integrate import simps
from scipy.optimize import minimize


def inner_product(x, y, sample_f, asd="LIGODesign",
                  fmin=30, phase=0, nfft=512):
    """
    Calculate the inner product of two timeseries.


    Parameters
    ----------
    x, y : np.ndarray
       The two timeseries to calculate the inner product for.
    psd : np.ndarray or str or None
       The ASD to use to calculate the match.
       Defaults to "LIGODesign" which is the LIGO design sensitivity.
    fmin : float
       The minimum frequency to be used to calculate the match.
    phase : float
       The phase shift, in radians, to apply to the second time series.

    """
    if asd == "LIGODesign":
        asd = np.loadtxt("fig1_aligo_sensitivity.txt")
        asd = torch.tensor(asd)
    freqs = torch.linspace(0, sample_f/2, int(nfft/2)+1)
    x_f = torch.fft.rfft(torch.hamming_window(len(x))*x, n=nfft)
    y_f = torch.fft.rfft(torch.hamming_window(len(y))*y, n=nfft) * torch.exp(1j * phase)
    asd_interp = interp1d(asd[:, 0], asd[:, -2])
    integrand = ((x_f[freqs > fmin]) * torch.conj(y_f[freqs > fmin]))
    integrand /= asd_interp(freqs[freqs > fmin])**2
    integral = simps(integrand, x=freqs[freqs > 30])
    return 4*torch.real(integral)


def components_from_total(total_mass, mass_ratio):
    """
    Calculate the component black hole masses from the total mass
    of the system and the mass ratio.
    """
    m1 = total_mass / (mass_ratio + 1)
    m2 = total_mass - m1

    return m1, m2


class FrequencySeries:
    """
    A class to represent a frequency series (spectrum)
    Optionally, a variance frequency series can be provided.

    Parameters
    ----------
    data : {array-like, pycbc timeseries}
        An array of data points.
    variance : array-like, optional
        An array of variances.
    times : array-like
        An array of timestamps
    """

    def __init__(self, data, frequencies=None, variance=None, covariance=None):
        if isinstance(frequencies, (np.ndarray, torch.Tensor)):
            # This looks like separate times and data
            self.frequencies = frequencies
            self.data = data
            self.df = self.frequencies[1] - self.frequencies[0]

        if isinstance(variance, (np.ndarray, torch.Tensor)):
            self.variance = variance
        else:
            self.variance = variance

        if isinstance(covariance, (np.ndarray, torch.Tensor)):
            self.covariance = covariance
        else:
            self.covariance = covariance

        self.dt = 1./self.df

    def __len__(self):
        return len(self.data)

        
class Timeseries:
    """
    A class to represent a timeseries from LALSuite in a more
    Python-friendly manner.
    """

    def __init__(self, data, times=None, variance=None, covariance=None, detector=None):
        """
        Create a Timeseries from a LALSuite timeseries or from data and times.

        Optionally, a variance timeseries can be provided.

        Parameters
        ----------
        data : {array-like, pycbc timeseries}
           An array of data points.
        variance : array-like (optional)
           An array of variances.
        times : array-like
           An array of timestamps
        detector : str
           The initialism for the detector, e.g. 'L1' for LIGO Livingston.
        """

        if detector:
            self.detector = detector
        else:
            self.detector = None
        
        if isinstance(data, pycbc.types.timeseries.TimeSeries):
            # This looks like a LALSuite timeseries
            self.dt = np.diff(data.sample_times)[0]
            self.times = np.array(data.sample_times)
            self.data = np.array(data.data)
        elif isinstance(times, (np.ndarray, torch.Tensor)):
            # This looks like separate times and data
            self.times = times
            self.data = data
            self.dt = self.times[1] - self.times[0] # Do this to deal with differences in numpy and torch behaviour

        if isinstance(variance, (np.ndarray, torch.Tensor)):
            self.variance = variance
        else:
            self.variance = None

        if isinstance(covariance, (np.ndarray, torch.Tensor)):
            self.covariance = covariance
        else:
            self.covariance = None
            
        self.df = 1./self.dt


    def __len__(self):
        return len(self.data)
        
    def __getitem__(self, key):
        """
        Return the mean values of the waveform, to make the waveform object behave as if it's in fact an array.
        """
        return self.data[key]

    def __mul__(self, other):
        """
        Multiply the components of the timeseries by a suitable value or set of values.
        """
        self.data *= other
        if self.variance:
            self.variance *= other
            
        return self

    def to_frequencyseries(self, window=torch.blackman_window):
        """
        Convert this timeseries to a frequency series.
        """
        
        strain_f = torch.fft.rfft(window(len(self.data), device=self.data.device) * self.data) * self.dt
        
        #if not isinstance(self.covariance, type(None)):
        #    cov_f = torch.fft.fft2(self.covariance)[:int(self.covariance.shape[0]/2+1),:int(self.covariance.shape[1]/2+1)]
        #    variance_f = torch.diag(cov_f.real)
        if not isinstance(self.variance, type(None)):
            variance_f = torch.fft.rfft(window(len(self.data), device=self.data.device)*torch.tensor(self.variance)) * self.dt**2
            cov_f = None
        else:
            variance_f = None
            cov_f = None

        if not isinstance(self.times, torch.Tensor):
            times = torch.tensor(self.times)
        else:
            times = self.times
            
        if torch.any(times):
            srate = 1/torch.diff(times).mean()
            nf = int(np.floor(len(times)/2))+1
            frequencies = torch.linspace(0, srate, nf)

        return FrequencySeries(data=strain_f,
                               variance=variance_f,
                               covariance=cov_f,
                               frequencies=frequencies)

    
    def pycbc(self):
        """
        Return the timeseries as a pycbc timeseries.
        """
        return pycbc.types.TimeSeries(self.data, self.dt)

    def apply_phase_offset(self,
                           phase,
                           nfft=512,
                           window=torch.hamming_window):
        """
        Generate the timeseries of this waveform with a defined phase offset.

        Parameters
        ----------
        phase : float
           The phase offset, in radians, to be introduced into the waveform.
        nfft : int
           The length of the fourier transform. Defaults to 512, and should
           be a power of 2 for speed.
        window : numpy window function
           The windowing function to use for the FFT.

        Returns
        -------
        Shifted timeseries : `numpy.ndarray`
           The phase-shifted timeseries.
        """

        def pow2(x):
            """Find the next power of 2"""
            return 1 if x == 0 else 2**(int(x) - 1).bit_length()

        y = self.data

        nfft = pow2(len(y)+torch.abs(phase))
        ik = torch.tensor([2j*np.pi*k for k in range(0, nfft)]) / nfft
        y_f = torch.fft.fft(window(len(y))*y, n=nfft) * np.exp(- ik * phase)

        return torch.real(torch.fft.ifft(y_f, len(y)))


class Waveform(object):
    
    pass


class NRWaveform(Waveform):
    """
    This class represents a waveform object, and can produce
    either the time-domain or the frequency-domain
    representation of the waveform.
    """

    def __init__(self, data_file, parameters):
        """
        Create the waveform object.

        Parameters
        ----------
        data_file : str
           The filepath to the datafile containing this waveform.
        parameters : dict
           A dictionary of this waveform's parameters.

        """

        self.data_file = data_file

        for key, value in parameters.items():
            setattr(self, key, value)

        self.mass_ratio = parameters['q']
            
        self.spins = [self.s1x, self.s1y, self.s1z,
                      self.s2x, self.s2y, self.s2z]

    def __repr__(self):
        return "<NR Waveform {} at q={}>".format(self.tag, self.mass_ratio)

    def minimum_frequency(self, total_mass):

        return self.Mflower / total_mass

    def _match(self, x, y, sample_f=1024, fmin=30, phase=0):
        top = inner_product(x, y, sample_f, phase=phase)
        bottom = np.sqrt(inner_product(x, x, sample_f)
                         * inner_product(y, y, sample_f))
        return np.abs(top / bottom)

    def optim_match(self, x, y, sample_f, fmin=30):
        """
        Calculate the optimal match, maximised over the phase shift of the
        two waveforms.
        """
        def neg_match(phase, x, y, sample_f, fmin):
            # Return the neagtive of the match which we can minimise.
            return - self._match(x, y, sample_f, fmin, phase)

        phase_op = minimize(neg_match, x0=0, args=(x, y, sample_f, fmin))

        return -phase_op['fun'], phase_op['x']

    def timeseries(self,
                   total_mass,
                   sample_rate=4096,
                   f_low=None,
                   distance=1,
                   coa_phase=0,
                   ma=None,
                   t_min=None,
                   t_max=None,
                   f_ref=None,
                   t_align=True):
        """
        Generate the timeseries representation of this waveform.
        """
        try:
            waveform = h5py.File(self.data_file)
            times = np.array(waveform['phase_l2_m2']['X'])

            # Convert times to physical units
            time_factor = (c.c.value**3 / c.G.value)/(total_mass*c.M_sun.value)
            amp_factor = 1./(distance * 1e6 * 3.0857e16 / (c.M_sun / (c.c**2 / c.G)).value)
            
            amp = np.interp(times, np.array(waveform['amp_l2_m2']['X']), np.array(waveform['amp_l2_m2']['Y']) )
            amp_error = np.interp(times, np.array(waveform['amp_l2_m2']['X'])[6:], np.array(waveform['amp_l2_m2']['errors']) )
            strain = amp * np.exp(-1 * 1j * np.array(waveform['phase_l2_m2']['Y']))
            strain_error = amp_error[6:] * np.exp(-1 * 1j * np.array(waveform['phase_l2_m2']['errors']))
            
            cut = 1e-3
            times /= time_factor
            mask = (times > t_min) & (amp > cut) & (times < t_max)
            
            hp = Timeseries(data = (amp_factor * strain[mask].real).astype(np.float64), times = times[mask])
            hx = Timeseries(data = - (amp_factor * strain[mask].imag).astype(np.float64), times = times[mask])

            return hp, hx

        except RuntimeError:
            raise LalsuiteError
