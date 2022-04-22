from ligotools import readligo as rl
import numpy as np
# from pathlib import Path

def test_loaddata1():
    fn_H1 = "/home/jovyan/hw/hw06-isaacdsloan/data/H-H1_LOSC_4_V2-1126259446-32.hdf5"
    
    strain_H1, time_H1, chan_dict_H1 = rl.loaddata(fn_H1, 'H1')
    assert type(strain_H1) == np.ndarray
    assert type(time_H1) == np.ndarray
    assert type(chan_dict_H1) == dict
    
def test_loaddata2():
    fn_L1 = "/home/jovyan/hw/hw06-isaacdsloan/data/L-L1_LOSC_4_V2-1126259446-32.hdf5"
    
    strain_L1, time_L1, chan_dict_L1 = rl.loaddata(fn_L1, 'L1')
    assert type(strain_L1) == np.ndarray
    assert type(time_L1) == np.ndarray
    assert type(chan_dict_L1) == dict
    

def test_dq_channel_to_seglist1():
    chan_dict = np.zeros(32) + 1
    segment_list = rl.dq_channel_to_seglist(chan_dict)
    assert type(segment_list) == list
    assert type(segment_list[0]) == slice


def test_dq_channel_to_seglist2():
    chan_dict = np.zeros(32) + 1
    segment_list = rl.dq_channel_to_seglist(chan_dict)
    
    random_list = np.zeros(200000)
    new_slice = segment_list[0]
    
    assert len(random_list[new_slice]) == 131072