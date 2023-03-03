import data_generator # in house

import random
import time
from array import *

from scipy.signal import find_peaks # find_peak_valley
import numpy as np # find_peak_valley
import matplotlib.pyplot as plt # find_peak_valley

def split_list_by_value_1(value, data_list, more_or_less=0):
    if more_or_less < 0:
        indices = [i for i, x in enumerate(data_list) if x <= value]
    elif more_or_less > 0:
        indices = [i for i, x in enumerate(data_list) if x >= value]
    else: # more_or_less == 0:
        indices = [i for i, x in enumerate(data_list) if x == value]

    blocks = []
    i = 0
    for e in indices:
        blocks.append(data_list[i:e])
        i = e + 1

    blocks.append(data_list[i:])
    return blocks, indices


def split_list_by_value_2(value, data_list, more_or_less=0):
    chunk = []
    for val in data_list:
        if more_or_less < 0:
            if val <= value:
                yield chunk
                chunk = []
            else:
                chunk.append(val)
        elif more_or_less > 0:
            if val >= value:
                yield chunk
                chunk = []
            else:
                chunk.append(val)
        else: # more_or_less == 0
            if val == value:
                yield chunk
                chunk = []
            else:
                chunk.append(val)
    yield chunk

def find_peak_valley_1(arr, thresh=0, debug=False):
    #print(f'In find_peak_valley_1() - arr: {arr}')
    peak = min(arr) - 1
    valley = max(arr) + 1
    peak_index_value = {}
    #peak_value_index = {}
    valley_index_value = {}
    #for i, value in enumerate(arr[1:-1], start=1):
    for i, value in enumerate(arr):
        if i == 0:
            continue

        if peak <= value:
            if value >= thresh:
                peak = value
        else:
            peak_index_value[i-1] = arr[i-1]
            peak = min(arr) - 1

        if valley >= value:
            if value < thresh:
                valley = value
        else:
            #print(f'i: {i}, valley: {valley}, value: {value}, arr[{i-1}]: {arr[i-1]}')
            if valley < arr[i-2]:
                valley_index_value[i-1] = arr[i-1]
                valley = max(arr) + 1


    #print('peak_index_value:')
    #for k in sorted(peak_index_value.keys()):
    #    print(f'k: {k} - {peak_index_value[k]}')

    #print('valley_index_value:')
    #for k in sorted(valley_index_value.keys()):
    #    print(f'k: {k} - {valley_index_value[k]}')

    return sorted(peak_index_value.keys()), sorted(valley_index_value.keys())

def find_peak_valley_2(data, thresh=0, debug=False):
    peak_idx, _ = find_peaks(data, height=thresh)
    valley_idx, _ = find_peaks(-data, height=thresh)
    if debug:
        print(f'thresh: {thresh}')
        print(f'peak_idx type: {type(peak_idx)}, length: {len(peak_idx)}\n{peak_idx}')
        print(f'valley_idx type: {type(valley_idx)}, length: {len(valley_idx)}\n{valley_idx}')
    return peak_idx, valley_idx

def find_peak_valley_ref(debug=False):
    # https://stackoverflow.com/questions/50756793/peak-detection-algorithm-in-python
    # Input signal
    t = np.arange(100)
    series = 0.3*np.sin(t)+0.7*np.cos(2*t)-0.5*np.sin(1.2*t)
    print(f'series: {type(series)}')
    
    # Threshold value (for height of peaks and valleys)
    thresh = 0.95
    thresh = 0
    
    # Find indices of peaks
    peak_idx, _ = find_peaks(series, height=thresh)
    
    # Find indices of valleys (from inverting the signal)
    valley_idx, _ = find_peaks(-series, height=thresh)
    print(f'peak_idx type: {type(peak_idx)}, length: {len(peak_idx)}\n{peak_idx}')
    if debug:
        # Plot signal
        plt.plot(t, series)
        
        # Plot threshold
        plt.plot([min(t), max(t)], [thresh, thresh], '--')
        plt.plot([min(t), max(t)], [-thresh, -thresh], '--')
        
        # Plot peaks (red) and valleys (blue)
        plt.plot(t[peak_idx], series[peak_idx], 'r.')
        plt.plot(t[valley_idx], series[valley_idx], 'b.')
        
        plt.show()


# --------testing codes below----------------------

class TestArrayManipulation:

    def test_split_array(self):
        high=15
        size=30
        data_hash = data_generator.create_random_number_array(high=high, size=size)
        data = data_hash['list_']
        print(data)
        separator_index = random.randint(0, len(data))
        print(f'A. separator_index: {separator_index}')
        assert data[separator_index] in data
        separator = data[separator_index]
        separator_count = data.count(separator)
        print(f'separator: {separator}, separator_count: {separator_count}')

        start = time.time()
        blocks1, indices = split_list_by_value_1(separator, data)
        print(f'   split_list_by_value_1(): Total run time: {round((time.time() - start), 3)}')
        assert separator_count == len(indices)
    
        start = time.time()
        results = split_list_by_value_2(separator, data) # Very efficient
        print(f'A. split_list_by_value_2(): Total run time: {round((time.time() - start), 3)}')
        blocks2 = []
        #for element in split_list_by_value_2(separator, data):
        for element in results:
            # Time consuming
            blocks2.append(element)
        print(f'B. split_list_by_value_2(): Total run time: {round((time.time() - start), 3)}')
        assert len(blocks2) == len(blocks1)

    def test_find_peak_valley(self):
        size=50
        high=50
        low = (-1)*high
        data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
        data = data_hash['array_']
        #data = [9,-5,7,-5,6,10,7,-1,3,4]
        data = np.array(data)
        print(data.tolist())
        find_peak_valley_1(data)
        peak_index_1, valley_index_1 = find_peak_valley_1(data)
        print(f'peak_index_1 type: {type(peak_index_1)}\n{peak_index_1}')
        print(f'valley_index_1 type: {type(valley_index_1)}\n{valley_index_1}')
        print()
        peak_index_2, valley_index_2 = find_peak_valley_2(data)
        print(f'peak_index_2 type: {type(peak_index_2)}\n{peak_index_2.tolist()}')
        print(f'valley_index_2 type: {type(valley_index_2)}\n{valley_index_2.tolist()}')
        assert peak_index_1 == peak_index_2.tolist()
        assert valley_index_1 == valley_index_2.tolist()
