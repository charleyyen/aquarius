import data_generator # in house
from aquarius.codility_python import my_test # in house

import inspect
import random
import tempfile
import time
from array import *

#from scipy.signal import find_peaks # find_peak_valley
import scipy.signal #import find_peaks # find_peak_valley
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


def find_peaks(data, height=0):
    # Intentionally mock scipy.signal.find_peaks() when height is set
    function_name = inspect.currentframe().f_code.co_name
    peak_indices, peak_values = [], []
    possible_peak_index = -1
    if height is None:
        print(f'In function_name(): Height is {height}. TBI')
    else:
        for index in range(1, len(data) - 1):
            if data[index] >= height:
                if data[index] > data[index - 1]:
                    if data[index] > data[index + 1]:
                        peak_indices.append(index)
                        peak_values.append(data[index])
                    elif data[index] == data[index + 1]:
                        possible_peak_index = index
                elif data[index] == data[index - 1]:
                    if data[index] > data[index + 1] and possible_peak_index > -1:
                        new_index = (index + possible_peak_index)//2
                        peak_indices.append(new_index)
                        peak_values.append(data[new_index])
                        possible_peak_index = -1

    return peak_indices, peak_values


def find_peak_valley_1(data, thresh=0, valley_included=False, debug=False):
    # This method is intentionally mocked find_peak_valley_2 with one key difference:
    # it does not call scipy.signal.find_peaks, because codility.com does not accept
    # scipy.py module
    function_name = inspect.currentframe().f_code.co_name
    if debug:
        print(f'In {function_name}(), data type: {type(data)}')
        print(f'A. data: {data}')

    if isinstance(data, list):
        data = np.array(data)

    peak_indices, peak_values = find_peaks(data, height=thresh)
    if valley_included:
        valley_indices, valley_values = find_peaks(-data, height=thresh)
        return peak_indices, peak_values, valley_indices, -(np.array(valley_values))
    return peak_indices, peak_values, None, None


def find_peak_valley_2(data, thresh=0, debug=False):
    function_name = inspect.currentframe().f_code.co_name
    if debug:
        print(f'\nIn {function_name}()')
    if isinstance(data, list):
        data = np.array(data)

    peak_idx, peak = scipy.signal.find_peaks(data, height=thresh)
    valley_idx, valley = scipy.signal.find_peaks(-data, height=thresh)
    if debug:
        print(f'thresh: {thresh}\n{data}\n{data.tolist()}')
        print(f'peak type: {type(peak)}, length: {len(peak)}\n{peak_idx}\n{peak}')
        print(f'==-->>peak_idx: {peak_idx}\npeak value: {peak}')
        print(f'valley type: {type(valley)}, length: {len(valley)}\n{valley_idx}\n{valley}')
        print(f'==-->>valley_idx: {valley_idx}\nvalley value: {valley}')
    return peak_idx, peak, valley_idx, valley


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
    peak_idx, _ = scipy.signal.find_peaks(series, height=thresh)

    # Find indices of valleys (from inverting the signal)
    valley_idx, _ = scipy.signal.find_peaks(-series, height=thresh)
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
        size=100_000
        high=10_000
        low = (-1)*high
        loop = 20
        i = 0
        while i < loop:
            #temp_dir = tempfile.TemporaryDirectory()
            #source_data = temp_dir.name + "/source_data.txt"
            source_data = f"/tmp/source_data_{i}.txt"

            data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
            arr = data_hash['array_']
            print(f'Array length in test: {len(arr):,}, source_data: {source_data}')

            with open(source_data, "w") as file_handle:
                file_handle.write(",".join(map(str, arr.tolist())))
                file_handle.write("\n")

            start = time.time()
            thresh = 0
            if thresh is None:
                answer_1 = find_peak_valley_1(arr, thresh=thresh)
            else:
                answer_1 = find_peak_valley_1(arr, valley_included=True, thresh=thresh)
                elapsed = round(time.time() - start, 4)
                print(f'find_peak_valley_1: Peak Counts: {len(answer_1[0]):,}', end='') 
                print(f', Valley Counts: {len(answer_1[2]):,}, Time Consumed: {elapsed}')

            start = time.time()
            answer_2 = find_peak_valley_2(arr)
            elapsed = round(time.time() - start, 4)

            print(f'find_peak_valley_2: Peak Counts: {len(answer_2[0]):,}', end='')
            print(f', Valley Counts: {len(answer_2[2]):,}, Time Consumed: {elapsed}')
            print()

            i += 1

            if thresh is not None:
                assert len(answer_1[0]) == len(answer_2[0]), \
                        f'Peak Indices Mismatch!! Check source data used in this test: {source_data}\n\n'
                assert len(answer_1[2]) == len(answer_2[2]), \
                        f'Valley Indices Mismatch!! Check source data used in this test: {source_data}\n\n'

            # use temp_dir, and when done:
            #temp_dir.cleanup()
