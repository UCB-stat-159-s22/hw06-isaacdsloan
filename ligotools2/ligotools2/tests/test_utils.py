import ligotools2.readligo as rl
import ligotools2.utils as utils 


import numpy as np
from scipy import signal
from scipy.interpolate import interp1d
from scipy.io import wavfile
from pathlib import Path
import h5py
import matplotlib.mlab as mlab
from scipy.signal import butter, filtfilt, iirdesign, zpk2tf, freqz
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab



def test_whiten():
    fn_H1 = "/home/jovyan/hw/hw06-isaacdsloan/data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = 4096, NFFT = 4*4096)
    psd_H1 = interp1d(freqs, Pxx_H1)

    time = time_H1
# the time sample interval (uniformly sampled!)
    dt = time[1] - time[0]
    
    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    assert type(strain_H1_whiten) == np.ndarray
    assert len(strain_H1_whiten) == 131072
    

def test_write_wav():
    fn_H1 = "/home/jovyan/hw/hw06-isaacdsloan/data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    
    fs = 4096
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = fs, NFFT = 4*4096)
    psd_H1 = interp1d(freqs, Pxx_H1)

    time = time_H1
# the time sample interval (uniformly sampled!)
    dt = time[1] - time[0]
    deltat_sound = 2.   # seconds around the event

# index into the strain time series for this time interval:
    tevent = 1126259462.44
    indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))

    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    
    utils.write_wavfile("/home/jovyan/hw/hw06-isaacdsloan/audio/test.wav",int(fs), strain_H1_whiten)
    
    
    my_file = Path("/home/jovyan/hw/hw06-isaacdsloan/audio/test.wav")
    assert my_file.exists()
    

def test_reqshift():
    fn_H1 = "/home/jovyan/hw/hw06-isaacdsloan/data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')


    
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = 4096, NFFT = 4*4096)
    psd_H1 = interp1d(freqs, Pxx_H1)

    time = time_H1
# the time sample interval (uniformly sampled!)
    dt = time[1] - time[0]
    deltat_sound = 2.   # seconds around the event

# index into the strain time series for this time interval:
    tevent = 1126259462.44
    indxd = np.where((time >= tevent-deltat_sound) & (time < tevent+deltat_sound))

    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    
    
    
    fs = 4096
    fshift = 400.
    speedup = 1.
    fss = int(float(fs)*float(speedup))

    # shift frequency of the data
    strain_H1_shifted = utils.reqshift(strain_H1_whiten,fshift=fshift,sample_rate=fs)
    
    assert type(strain_H1_whiten) == np.ndarray
    assert len(strain_H1_whiten) == 131072 


def test_plot_filtering():
    fn_template = "/home/jovyan/hw/hw06-isaacdsloan/data/GW150914_4_template.hdf5"
    
    
    f_template = h5py.File(fn_template, "r")
    template_p, template_c = f_template["template"][...]
    
    
    fn_H1 = "/home/jovyan/hw/hw06-isaacdsloan/data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    
    fn_L1 = "/home/jovyan/hw/hw06-isaacdsloan/data/L-L1_LOSC_4_V2-1126259446-32.hdf5"
    strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')
    
    fs = 4096

    
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = 4096, NFFT = 4*4096)
    psd_H1 = interp1d(freqs, Pxx_H1)

    time = time_H1
# the time sample interval (uniformly sampled!)
    dt = time[1] - time[0]
    template_offset = 16.
    
    
    Pxx_H1, freqs = mlab.psd(strain_H1, Fs = 4096, NFFT = 4*4096)
    psd_H1 = interp1d(freqs, Pxx_H1)
    
    Pxx_L1, freqs = mlab.psd(strain_L1, Fs = 4096, NFFT = 4*4096)
    psd_L1 = interp1d(freqs, Pxx_L1)
    
    strain_H1_whiten = utils.whiten(strain_H1,psd_H1,dt)
    strain_L1_whiten = utils.whiten(strain_L1,psd_L1,dt)
    bb = np.random.rand(9)
    ab = np.random.rand(9)
    
    normalization = 0.3542432515235823
    make_plots = 1
    
    utils.plot_matched_filtering(template_p, template_c, template_offset, time, strain_L1, strain_H1, strain_L1_whiten, strain_H1_whiten, dt, ab, bb, normalization, make_plots, fs = 4096, eventname = 'TEST')
    
    
    
    
    # PATH = Path("/home/jovyan/hw/hw06-isaacdsloan/figures/TEST_H1_matchfreq.png")
    # assert PATH.exists()
