"""
Rapid implementation timeseries analysis. 

Collection of utilities for timeseries analysis with a focus on rapid implementation, not rapid runtimes. Code interfaces with numpy, scipy, xarray, matplotlib  

"""

import numpy as np, scipy.signal as signal, xarray as xr
import matplotlib.pyplot as plt

import afloat.time as ztime
import afloat.clean as zclean

import importlib, sys

############################################################
### Wanted to keep sfoda as a dependency here, but as I've 
### made a lot of changes it might be easier for now to use it 
### port it over here for now. Discuss with Matt. 
############################################################

# if (spec := importlib.util.find_spec('sfoda')) is not None:
#     module = importlib.util.module_from_spec(spec)
#     sys.modules['sfoda'] = module
#     spec.loader.exec_module(module)
# else:
#     raise(Exception(f"This function requires sfoda"))

# from sfoda.utils import harmonic_analysis as sha
from afloat.sfodautils import harmonic_analysis as sha

@xr.register_dataset_accessor("floatds")
class DataSet():
    """
    Accessor for xarray DataSet.

    Accessor for xarray DataSet which provides functionality for rapid implementation of timeseries analysis.

    Parameters
        ds : xarray.DataSet
            The DataSet to be accessed

    Returns
        ds : timeseries.DataSet
            The xarray accessor object

    Examples
        XXXXXXXX

    See Also
        xarray.DataSet
    """

    def __init__(self, ds): 
    
        self._obj = ds

    @property
    def _ds(self):
        return self._obj

    def __repr__(self):

        return self._ds.__repr__()

    def __getitem__(self, item):
        
        return DataArray(self._ds[item])

@xr.register_dataarray_accessor("floatda")
class DataArray():
    """
    Accessor for xarray DataArray.

    Accessor for xarray DataArray which provides functionality for rapid implementation of timeseries analysis.

    Parameters
        da : xarray.DataArray
            The DataArray to be accessed

    Returns
        da : timeseries.DataArray
            The xarray accessor object

    Examples
        XXXXXXXX

    See Also
        xarray.DataArray
    """

    def __init__(self, da):

        if 'units' in da.attrs:
            self.units = da.attrs['units']
        else:
            self.units = '?'
        
        dims = da.dims
        if not dims[0].lower() == 'time':
            raise(Exception("First dimension must be time"))

        self._obj = da

    @property
    def _da(self):

        return self._obj

    @property
    def dims(self):

        return self._obj.dims

    @property
    def other_dims(self):

        return [dim for dim in self._obj.dims if (not dim.lower()=='time')]

    @property
    def coords(self):
        return self._obj.coords

    def __repr__(self):

        return self._da.__repr__()

    @property
    def _timeseries(self):

        return TimeSeries(self._da.time.values, self._da.values, units=self.units, other_dims=self.other_dims)

    def plot(self, **kwargs):
        
        set_xlim = kwargs.pop("set_xlim", False)
        
        self._da.plot(**kwargs)
        
        ax = kwargs.pop("ax", plt.gca())

        if set_xlim:
            ax.set_xlim([min(self._da.time.values), max(self._da.time.values)])

    def interp(self, **kwargs):

        return self._timeseries.interp(**kwargs)

    def despike_gn02(self, **kwargs):

        return self._timeseries.despike_gn02(**kwargs)

    def butter(self, **kwargs):

        return self._timeseries.butter(**kwargs)

    def psd(self, **kwargs):

        return self._timeseries.psd(**kwargs)

    def psd_welch(self, **kwargs):

        return self._timeseries.psd_welch(**kwargs)

    def tidal_harmonic(self, Fin=None, **kwargs):

        return self._timeseries.tidal_harmonic(Fin=Fin, **kwargs)

    def rolling_tidal_harmonic(self, Fin=None, **kwargs):

        return self._timeseries.rolling_tidal_harmonic(Fin=Fin, **kwargs)

class TimeSeries():
    """
    An object to hold timeseries data and wrap the quick timeseries methods within this module. 
    """

    def __init__(self, time, data, other_dims=[], **kwargs):
        """

        """
        ## Start with no validation. Build organically. 
        
        quick_validate(time, data)

        units = kwargs.pop("units", '?')

        s = data.shape
        n_other_dims = len(s) - 1

        assert n_other_dims==len(other_dims), "If data is multidimensional, must specify names of other dimensions"
        assert len(time) == s[0], "Length of time must equal first dimension of data" 

        self.time = time
        self.data = data

        self.units = units

    def plot(self, ax=None, **kwargs):

        set_xlim = kwargs.pop("set_xlim", False)

        if ax is None:
            ax = plt.gca()

        ax.plot(self.time, self.data, **kwargs)
        ax.grid('on')

        if set_xlim:
            ax.set_xlim([min(self.time.values), max(self.time.values)])

    def interp(self, **kwargs):

        return quick_interp(self.time, self.data, **kwargs)

    def despike_gn02(self, **kwargs):

        return quick_despike_gn02(self.time, self.data, **kwargs)

    def butter(self, **kwargs):

        return quick_butter(self.time, self.data, **kwargs)

    def psd(self, **kwargs):

        return quick_psd(self.time, self.data, data_unit=self.units, **kwargs)

    def psd_welch(self, **kwargs):

        return quick_psd_welch(self.time, self.data, data_unit=self.units, **kwargs)

    def rolling_tidal_harmonic(self, Fin=None, **kwargs):

        return quick_rolling_tidal_harmonic(self.time, self.data, Fin=Fin, **kwargs)

    def tidal_harmonic(self, Fin=None, **kwargs):

        return quick_tidal_harmonic(self.time, self.data, Fin=Fin, **kwargs)

def quick_butter(time, data, T_cut_seconds, order=4, btype='lowpass', use_sos=False):
    """
    Very quick butterworth filter that works with python time objects. 
    
    Usage:
        filtered = quick_butter(time, data, T_cut_seconds, order=4, btype='lowpass')

    args:
        time: numpy array of time objects that can be converted by zutils.time.seconds_since and zutils.time.is_well_spaced
        data: np.array to be filtered. Can be higher dimensional but goes into signal.butter as is.
        T_cut_seconds: cutoff period in seconds
        
    kwargs: 
        btype: 'lowpass' or 'highpass'
        order: order of the butterworth

    """

    quick_validate(time, data)
    
    # Convert to seconds
    t_sec = ztime.seconds_since(time)

    dt = t_sec[1] - t_sec[0]
    f_s_Hz = 1/dt # my sampling freq
    f_N_Hz = 1/dt # Nyqvist frequency in function of my sampling frequency

    # Validation [should be fine for mopdel data]
    ztime.is_well_spaced(time, f_s_Hz)

    # Filter design
    if type(T_cut_seconds) == list:
        T_cut_seconds = np.array(T_cut_seconds)

    f_cut_Hz = 1/T_cut_seconds

    f_cut_norm = f_cut_Hz/f_N_Hz  # normalized cut_off frequency
    f_cut_norm = f_cut_Hz/(f_N_Hz/2)  # normalized cut_off frequency

    if np.any(f_cut_norm == 1) or np.any(f_cut_norm == 0):
        raise(Exception('Cutoff time of {} seconds is not acceptable for thge time spacing on this dataset.'.format(T_cut_seconds)))

    if order > 4:
        if not use_sos:
            use_sos = True
            print('Order greater than 4, using sos')

    if use_sos:
        # sos = signal.butter(order, Wn, btype=btype, analog=0, output='sos', fs=1)
        # out = signal.sosfiltfilt(sos, ytmp, axis=axis, padlen=0)
        # sos = signal.butter(order, f_cut_norm, btype=btype, analog=0, output='sos', fs=1)
        sos = signal.butter(order, f_cut_norm, btype=btype, output='sos')
        out = signal.sosfiltfilt(sos, data)
    else:
        #(b, a) = signal.butter(order, Wn, btype=btype, analog=0, output='ba')
        #return signal.filtfilt(b, a, ytmp, axis=-1)
        b, a = signal.butter(order, f_cut_norm, btype)
        out = signal.filtfilt(b, a, data, axis=0)

    return out

def quick_interp(time, data, **kwargs):
    """
    Very quick interp of timeseries data. 

    Usage:
        time_out_secs, time_out_np64, var_interp = quick_interp(time, data, **kwargs)

    Arguments:
        time
        data
    
    Key word arguments:
        dt_sec
        start
        end

    Outputs:
        time_out_secs
        time_out_np64 
        var_interp
    """
    dt_sec = kwargs.pop('dt_sec', 60)
    start = kwargs.pop('start', None)
    end = kwargs.pop('end', None)
    
    dt_file = time[1] - time[0]
    print('File dt initial: {}'.format(dt_file))
    print('dt out: {}'.format(dt_sec))
    
    ref_time = time[0]

    time_in_secs = ztime.seconds_since(time, ref_time)
    
    if start is None:
        start_sec = time_in_secs[0]
    else:
        start = np.datetime64(start)
        start_sec = ztime.seconds_since(start, ref_time)
        
    if end is None:
        end_sec = time_in_secs[-1]
    else:
        end = np.datetime64(end)
        end_sec = ztime.seconds_since(end, ref_time)
        end_sec += dt_sec

    time_out_secs = np.arange(start_sec, end_sec, dt_sec) 
    time_out_np64 = np.array([ref_time + np.timedelta64(int(i), 's') for i in time_out_secs])

    if len(data.shape) == 1:
        var_interp = np.interp(time_out_secs, time_in_secs, data) 
    else:
        var_interp = np.array([np.interp(time_out_secs, time_in_secs, var_row) for var_row in data])

    return time_out_secs, time_out_np64, var_interp

def quick_interp_tknown(time, data, interp_time):
    """
    Very quick interp of timeseries data. Here the time vector is known. 

    Usage:
        time_out_secs, time_out_np64, var_interp = quick_interp(time, data, interp_time)

    Arguments:
        time
        data
        interp_time
    
    Key word arguments:
        

    Outputs:
        time_out_secs
        var_interp
    """
    
    
    ref_time = time[0]

    time_in_secs = ztime.seconds_since(time, ref_time)
    time_out_secs = ztime.seconds_since(interp_time, ref_time)
    time_out_np64 = np.array([ref_time + np.timedelta64(int(i), 's') for i in time_out_secs])

    if len(data.shape) == 1:
        var_interp = np.interp(time_out_secs, time_in_secs, data) 
    else:
        var_interp = np.array([np.interp(time_out_secs, time_in_secs, var_row) for var_row in data])

    return time_out_secs, time_out_np64, var_interp

def tslice(time, start, end):
    """
    Get a quick time index for a slice between start and end dates. Does this by first converting to seconds_since. This is not fast, but it is easy for the operator as seconds_since handles the object conversion. 
    
    Usage:
        tind = tslice(time, start, end)

    Inputs:
        time: Time vector
        start: datetime.datatime np.datetime64 for the start time
        end: datetime.datatime np.datetime64 for the end time
    """

    time = ztime.seconds_since(time)
    start = ztime.seconds_since(start)
    end = ztime.seconds_since(end)
    
    tind = np.logical_and(time>=start, time<=end)
    
    return tind

def tnearest(time, target):
    """
    Get a quick time index for nearest point to target time. Does this by first converting to seconds_since. This is not fast, but it is easy for the operator as seconds_since handles the object conversion. 
    
    Usage:
        tind = tnearest(time, start, end)

    Inputs:
        time: Time vector
        target: datetime.datatime np.datetime64 for the target time
    """

    time = ztime.seconds_since(time)
    target = ztime.seconds_since(target)
    
    d = abs(time-target)
    tind = np.where(d==min(d))[0][0]
    
    return tind


def quick_psd(time, data, data_unit='m', time_unit='s', radians=False, plot=False, **kwargs):
    """
    Quick power spectral density.There are a few ways to code this. I've chosen to use scipysignal.welch
    but setting the overlap and nperseg such that there is no averaging.

    """

    quick_validate(time, data)

    plot_kwargs = kwargs.pop('plot_kwargs', {'color': 'k'})
    ax = kwargs.pop('ax', None)

    if not type(time) == np.ndarray:
        raise(Exception('Time must be an np array'))
        
    # time = ztime.seconds_since(time)
    # d_time = np.diff(time)
    # dd_time = np.abs(np.diff(d_time))

    # if not np.all(dd_time<1e-4):
    #     raise(Exception("Time must be evenly spaced"))
    t_sec = ztime.seconds_since(time)

    dt = t_sec[1] - t_sec[0]
    Fs = 1/dt # my sampling freq

    ztime.is_well_spaced(time, Fs)

    # Fs = 1/d_time[0]
    f_psd, y_psd = signal.welch(data, fs=Fs, window='hann', nperseg=len(time), noverlap=0, axis=0)

    if time_unit.lower() in ['hour', 'hours', 'h']:
        time_unit='h'
        sf = 3600
    elif time_unit.lower() in ['day', 'days', 'd']:
        time_unit='d'
        sf = 86400
    elif time_unit.lower() in ['second', 'seconds', 's']:
        time_unit='s'
        sf = 1
    else:
        raise(Exception('Time unit not recognised.'))


    if radians:
        sf *=2 *np.pi
        freq_unit = '{}$^{{-1}}$'.format(time_unit)
    else:
        freq_unit = 'cp' + time_unit

    spec_unit = '[{}]$^2$/{}'.format(data_unit, freq_unit)

    f_psd = f_psd*sf
    y_psd = y_psd/sf

    if plot:
        if len(data.shape)>1:
            print("Plotting not enabled for n dimensional data.")
        else:
            if ax is None:
                ax = plt.gca()
            # ax = plt.figure(figsize=(15, 4))
            ax.plot(f_psd, y_psd, **plot_kwargs)
            ax.set_ylabel(spec_unit)
            ax.set_xlabel(freq_unit)
            ax.set_xscale('log')
            ax.set_yscale('log')

    return f_psd, y_psd, freq_unit, spec_unit
    
def quick_psd_welch(time, data, nperseg=1024, data_unit='m', time_unit='s', radians=False, plot=False, **kwargs):
    """

    """

    quick_validate(time, data)

    plot_kwargs = kwargs.pop('plot_kwargs', {'color': 'k'})
    ax = kwargs.pop('ax', None)

    if not type(time) == np.ndarray:
        raise(Exception('Time must be an np array'))
        
    # time = ztime.seconds_since(time)
    # d_time = np.diff(time)
    # dd_time = np.abs(np.diff(d_time))

    # if not np.all(dd_time<1e-4):
    #     raise(Exception("Time must be evenly spaced"))
    t_sec = ztime.seconds_since(time)

    dt = t_sec[1] - t_sec[0]
    Fs = 1/dt # my sampling freq

    ztime.is_well_spaced(time, Fs)

    # Fs = 1/d_time[0]
    f_welch, y_welch = signal.welch(data, fs=Fs, window='hann', nperseg=nperseg, noverlap=nperseg/2, axis=0)

    if time_unit.lower() in ['hour', 'hours', 'h']:
        time_unit='h'
        sf = 3600
    elif time_unit.lower() in ['day', 'days', 'd']:
        time_unit='d'
        sf = 86400
    elif time_unit.lower() in ['second', 'seconds', 's']:
        time_unit='s'
        sf = 1
    else:
        raise(Exception('Time unit not recognised.'))


    if radians:
        sf *=2 *np.pi
        freq_unit = '{}$^{{-1}}$'.format(time_unit)
    else:
        freq_unit = 'cp' + time_unit

    spec_unit = '[{}]$^2$/{}'.format(data_unit, freq_unit)

    f_welch = f_welch*sf
    y_welch = y_welch/sf

    if plot:
        if len(data.shape)>1:
            print("Plotting not enabled for n dimensional data.")
        else:
            if ax is None:
                ax = plt.gca()
            # ax = plt.figure(figsize=(15, 4))
            ax.plot(f_welch, y_welch, **plot_kwargs)
            ax.set_ylabel(spec_unit)
            ax.set_xlabel(freq_unit)
            ax.set_xscale('log')
            ax.set_yscale('log')

    return f_welch, y_welch, freq_unit, spec_unit

def quick_psd_welch_taylor_fth(time, data, U, nperseg=1024, data_unit='m/s', radians=False, plot=False, verbose=True, **kwargs):
    """
    A quick pwelch with Taylor's frozen turbulence hypothesis. 
    
    This is simply quick_psd but takes the mean velocity U in m/s. 
    
    time_unit is no longer an option. 
    
    """

    quick_validate(time, data, verbose=verbose)

    plot_kwargs = kwargs.pop('plot_kwargs', {'color': 'k'})
    ax = kwargs.pop('ax', None)

    time_unit='s'

    if not type(time) == np.ndarray:
        raise(Exception('Time must be an np array'))
        
    time = ztime.seconds_since(time)
    d_time = np.diff(time)
    dd_time = np.abs(np.diff(d_time))

    if not np.all(dd_time<1e-4):
        raise(Exception("Time must be evenly spaced"))

    Fs = 1/d_time[0]
    f_welch, y_welch = signal.welch(data, fs=Fs, window='hann', nperseg=nperseg, noverlap=nperseg/2, axis=0)

    if time_unit.lower() in ['second', 'seconds', 's']:
        time_unit='s'
        sf = 1
    else:
        raise(Exception('Time unit not recognised.'))

    kPSD = U*y_welch
    k    = f_welch/U
    wavenumber_unit = 'm'

    if radians:
        sf *=2 *np.pi
        k_unit = '{}$^{{-1}}$'.format(wavenumber_unit)
    else:
        k_unit = 'cp' + wavenumber_unit

    kPSD_unit = '[{}]$^2$/{}'.format(data_unit, k_unit)

    k = k*sf
    kPSD = kPSD/sf
    
    out = {}
    out['k']    = k
    out['kPSD'] = kPSD
    
    out['k_unit']    = k_unit
    out['kPSD_unit'] = kPSD_unit

    if plot:
        if len(data.shape)>1:
            print("Plotting not enabled for n dimensional data.")
        else:
            if ax is None:
                ax = plt.gca()
            ax.plot(out['k'], out['kPSD'] , **plot_kwargs)
            ax.set_xlabel(k_unit)
            ax.set_ylabel(kPSD_unit)
            ax.set_xscale('log')
            ax.set_yscale('log')

    return out 

def quick_despike_gn02(time, data, intensity=[0.7], **kwargs):
    """
    Quick despike by GN02
    
    If intensity is iterable GN02 is iterated with variable intensity on each iteration. 
    
    If intensity is a number only one iteration is performed.
    """
    
    quick_validate(time, data)
    
    if not type(time) == np.ndarray:
        raise(Exception('Time must be an np array'))
        
    t_sec = ztime.seconds_since(time)
    d_time = np.diff(t_sec)
    dd_time = np.abs(np.diff(d_time))

    fs = 1/d_time[0]
    
    # if not np.all(dd_time<1e-6):
    #     raise(Exception("Time must be evenly spaced"))
    ztime.is_well_spaced(time, fs)

    fs = None      # Not actually used

    data_c = data.copy()
    any_clean = np.isnan(data_c)

    if not type(intensity) is list:
        intensity = [intensity]
    
    n_iter = len(intensity)
    for i, int_val in enumerate(intensity):
        # print('GN iteration {}'.format(i))
        # print(np.isnan(data_c))
        data_c, di = zclean.despikei(data_c, fs=fs, intensity=int_val)
        any_clean = np.logical_or(any_clean, di)
        

    return data_c, any_clean

def quick_decompose(time, data, T_cut_low, T_cut_high, plot=False, **kwargs):
    
    if 'btype' in kwargs:
        raise Exception("Can't pass btype to decompose")

    if T_cut_low >= T_cut_high:
        raise Exception("T_cut_low >= T_cut_high")

    
    data_hp = quick_butter(time, data, T_cut_low,  btype='highpass')
    data_lp = quick_butter(time, data, T_cut_high,  btype='lowpass')
    data_bp = quick_butter(time, data, [T_cut_high, T_cut_low],  btype='bandpass')

    if plot:

        quick_psd_welch(time, data,    nperseg=8*1024, plot=True, time_unit='d', plot_kwargs={'color': '0.5'})
        quick_psd_welch(time, data_lp, nperseg=8*1024, plot=True, time_unit='d', plot_kwargs={'color': 'c'})
        quick_psd_welch(time, data_bp, nperseg=8*1024, plot=True, time_unit='d', plot_kwargs={'color': 'k'})
        quick_psd_welch(time, data_hp, nperseg=8*1024, plot=True, time_unit='d', plot_kwargs={'color': 'b'})

        ylim = plt.gca().get_ylim()
        plt.plot([24*3600/(T_cut_low)]*2, ylim, 'r--')
        plt.plot([24*3600/(T_cut_high)]*2, ylim, 'r--')
        plt.gca().set_ylim(ylim)

    return data_lp, data_bp, data_hp


def quick_tidal_harmonic(time, data, Fin=None, **kwargs):

    freq, fout = sha.getTideFreq(Fin=Fin)
    # amp, phs, c0, data_fit, data_residual = 
    output = quick_harmonic(time, data, freq, **kwargs)
    output['fout'] = fout

    return output

def quick_rolling_tidal_harmonic(time, data, Fin=None, **kwargs):

    if Fin is None:
        Fin = ['M2', 'M4', 'M6']

    freq, fout = sha.getTideFreq(Fin=Fin)
    output = quick_rolling_harmonic(time, data, freq, **kwargs)
    output['fout'] = fout
    output['freq'] = freq
    # output['fout'] = fout

    return output

def quick_rolling_harmonic(time, data, omega, windowlength=3*86400.0, overlap=12*3600.0, zero_pad_nans=True, **kwargs):
    """

    kwargs:
        remove_trans_in_recon - if true this sets the window swapover point in the reconstructed harmonic signal to np.nan to limit discontinuity.

    """

    if (spec := importlib.util.find_spec('sfoda')) is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules['sfoda'] = module
        spec.loader.exec_module(module)
    else:
        raise(Exception(f"This function requires sfoda"))

    from sfoda.utils import harmonic_analysis as sha

    remove_transition_in_recon = kwargs.pop("remove_transition_in_recon", True)

    pt1, pt2 = window_index_time(time, windowlength, overlap)
    npt = len(pt1)
    nfrq = len(omega)
    amp = np.zeros((nfrq, npt,))
    phs = np.zeros((nfrq, npt,))
    c0 = np.zeros((nfrq, npt,))
    ymean = np.zeros((npt,))

    # I know there is a cleaner way than this, revisit
    if data.ndim>1:
        nother = [1, 1]+[data.shape[i] for i in np.arange(1, data.ndim)] 
        for i in np.arange(data.ndim-1):
            amp = amp[..., np.newaxis]
            phs = phs[..., np.newaxis]
            c0 = c0[..., np.newaxis]
        
        amp = amp*np.ones(nother)
        phs = phs*np.ones(nother)
        c0  = c0*np.ones(nother)

    tmid = []
    ii=-1

    data_fit = np.zeros_like(data)
    data_residual = np.zeros_like(data)

    for t1, t2 in zip(pt1,pt2):
        ii+=1

        time_ = time[t1:t2]
        data_ = data[t1:t2, ...].copy()

        # print(time_.shape)
        # print(data_.shape)

        if zero_pad_nans:
            data_[np.isnan(data_)] = 0

        # print(time_.shape)
        # print(data_.shape)

        a, p, c = sha.harmonic_fit(time_, data_, frq=omega)
        dataf_ = sha.harmonic_signal(time_, a, p, c, omega)

        if remove_transition_in_recon:
            dataf_[0] = np.nan
            dataf_[-1] = np.nan

        data_fit[t1:t2] = dataf_
        data_residual[t1:t2] = data[t1:t2] - dataf_

        amp[:, ii, ...], phs[:, ii, ...], c0[:, ii, ...] = a, p, c

        # Return the mid time point
        ind = int(np.floor(t1 + (t2-t1)/2))
        tmid.append(time[ind])
#           
        # Return the fitted time series
        ymean[ii] = data[t1:t2].mean()

    tmid = np.asarray(tmid)

    output={}
    output['tmid']              = tmid
    output['amp']               = amp
    output['phs']               = phs
    output['c0']                = c0
    output['data_fit']          = data_fit
    output['data_residual']     = data_residual
    output['omega']             = omega

    return output

def quick_harmonic(time, data, omega, zero_pad_nans=True, **kwargs):
    """

    kwargs:

    """

    if (spec := importlib.util.find_spec('sfoda')) is not None:
        module = importlib.util.module_from_spec(spec)
        sys.modules['sfoda'] = module
        spec.loader.exec_module(module)
    else:
        raise(Exception(f"This function requires sfoda"))

    from sfoda.utils import harmonic_analysis as sha

    nfrq     = len(omega)
    amp      = np.zeros((nfrq, ))
    phs      = np.zeros((nfrq, ))
    c0       = np.zeros((nfrq, ))

    # I know there is a cleaner way than this, revisit
    if data.ndim>1:
        nother = [1]+[data.shape[i] for i in np.arange(1, data.ndim)] 
        for i in np.arange(data.ndim-1):
            amp = amp[..., np.newaxis]
            phs = phs[..., np.newaxis]
            c0 = c0[..., np.newaxis]
        
        amp = amp*np.ones(nother)
        phs = phs*np.ones(nother)
        c0  = c0*np.ones(nother)

    data_fit      = np.zeros_like(data)
    data_residual = np.zeros_like(data)

    time_ = time
    data_ = data.copy()

    if zero_pad_nans:
        data_[np.isnan(data_)] = 0

    a, p, c = sha.harmonic_fit(time_, data_, frq=omega)
    dataf_  = sha.harmonic_signal(time_, a, p, c, omega)

    data_fit = dataf_
    data_residual = data - dataf_

    amp[:, ...], phs[:, ...], c0[:, ...] = a, p, c

    output={}
    output['amp']               = amp
    output['phs']               = phs
    output['c0']                = c0
    output['data_fit']          = data_fit
    output['data_residual']     = data_residual
    output['omega']             = omega

    return output
    
def quick_validate(time, data, verbose=False):

    assert type(time) in [np.array, np.ndarray], "Time must be an np.array"
    assert type(data) in [np.array, np.ndarray], "Data must be an np.array"
    assert len(time)==data.shape[0], "Time must be the same length as the first dimension of Data"

    if verbose:
        print('Validation checks passed')

def window_index_time(t, windowsize, overlap):
    """
    Determines the indices for window start and end points of a time vector
    
    The window does not need to be evenly spaced
    
    Inputs:

        t: list or array of datetime objects

        windowsize: length of the window [seconds]

        overlap: number of overlap points [seconds]
        
    Returns: pt1,pt2 the start and end indices of each window
    """
    
    tsec = ztime.seconds_since(t)
        
    t1=tsec[0]
    t2=t1 + windowsize
    pt1=[0]
    pt2=[np.searchsorted(tsec,t2)]
    while t2 < tsec[-1]:
        t1 = t2 - overlap
        t2 = t1 + windowsize

        pt1.append(np.searchsorted(tsec,t1))
        pt2.append(np.searchsorted(tsec,t2))
        
    return pt1, pt2