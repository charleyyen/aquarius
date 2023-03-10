import data_generator # in house
#from aquarius.codility_python import my_test # in house

import inspect
import pathlib
import random
import sys
import tempfile
import time
from array import *

#from scipy.signal import find_peaks # find_peak_valley
import scipy.signal #import find_peaks # find_peak_valley
import numpy as np # find_peak_valley
import matplotlib.pyplot as plt # find_peak_valley

print_limit = 101
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

    if isinstance(data, list):
        data = np.array(data)

    peak_indices, peak_values = find_peaks(data, height=thresh)
    if debug:
        #print(f'thresh: {thresh}\n{data}\n{data.tolist()}\n')
        print(f'Source Data: {data.tolist()}\n')
        if len(data) < print_limit:
            print(f'  peak_indices: {peak_indices}')
            print(f'    peak value: {peak_values}')
    if valley_included:
        valley_indices, valley_values = find_peaks(-data, height=thresh)
        valley_values = (-(np.array(valley_values))).tolist()
        if debug:
            if len(data) < print_limit:
                print(f'valley_indices: {valley_indices}')
                print(f'  valley value: {valley_values}')
            print()
        return peak_indices, peak_values, valley_indices, valley_values
    else:
        if debug:
            print()
    return peak_indices, peak_values, None, None


def find_peak_valley_2(data, thresh=0, debug=False, all_int=False):
    function_name = inspect.currentframe().f_code.co_name
    if debug:
        print(f'\nIn {function_name}()')
    if isinstance(data, list):
        data = np.array(data)

    peak_index, peak = scipy.signal.find_peaks(data, height=thresh)
    valley_index, valley = scipy.signal.find_peaks(-data, height=thresh)
    # The data type of peak_index & valley_index is <class 'numpy.ndarray'>
    # The data type of peak and valley is <class 'dict'>
    #   which has one key 'peak_heights' - <class 'str'> and the corresponding
    #       value's data type is <class 'numpy.ndarray'>
    peak_index = peak_index.tolist()
    valley_index = valley_index.tolist()
    peak = peak["peak_heights"].tolist()
    valley = (-valley["peak_heights"]).tolist()

    if debug:
        #print(f'thresh: {thresh}\n{data}\n{data.tolist()}\n')
        print(f'Source Data: {data.tolist()}\n')
        if len(data) < print_limit:
            print(f'  peak_index: {peak_index}')
            print(f'  peak value: {peak}')
            print(f'valley_index: {valley_index}')
            print(f'valley value: {valley}')
        print()
    return peak_index, peak, valley_index, valley


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

    def find_mismatch(self, data, results_a, results_b, flag):
        function_name = inspect.currentframe().f_code.co_name
        print(f'\nIn {function_name}(), data length: {len(data)}, flag: {flag}\n\n')
        if flag == 'p':
            print("\n\nCheck Peak!!\n")
            self.analyze_results(data, results_a[0], results_b[0], results_a[1], results_b[1])
        else:
            print("\n\nCheck Valley!!\n")
            self.analyze_results(data, results_a[2], results_b[2], results_a[3], results_b[3])


    def analyze_results(self, data, index_a, index_b, value_a, value_b):
        partial = False
        if len(data) > 50:
            partial = True

        index_list = index_a if len(index_a) > len(index_b) else index_b

        for i in range(len(index_list)):
            if i < len(index_a):
                stop_here = False
                real_index_a = index_a[i]
                real_value_a = value_a[i]
            else:
                print(f'Index {i} is not in index_a!!')
                stop_here = True
                
            if i < len(index_b):
                stop_here = False
                real_index_b = index_b[i]
                real_value_b = value_b[i]
            else:
                print(f'Index {i} is not in index_b!!')
                stop_here = True

            if stop_here:
                assert False

            if real_index_a != real_index_b:
                print(f'real_index_a: {real_index_a}, real_value_a: {real_value_a}')
                print(f'real_index_b: {real_index_b}, real_value_b: {real_value_b}')
                if partial:
                    print(f'Head 5: {data[:5]}, Tail 5: {data[-5:]}')
                    print(f'Around real_index_a: {real_index_a}, {data[real_index_a-5:real_index_a+5]}, on spot: {data[real_index_a]}')
                    print(f'Around real_index_b: {real_index_b}, {data[real_index_b-5:real_index_b+5]}, on spot: {data[real_index_b]}')
                else:
                    print(f'data[{real_index_a}] = {data[real_index_a]}')
                    print(f'data[{real_index_b}] = {data[real_index_b]}')

    def read_static_data_from_file(self, source_file):
        with open(source_file, "r") as open_for_read:
            for line in open_for_read.readlines():
                if line[0] == "#":
                    continue
                #list_ = line.rstrip().split(",")
                list_ = [int(x) for x in line.rstrip().split(",")]

        return list_


    def test_find_peak_valley(self):
        static_data_from_file = True
        static_data_from_file = False
        size=100
        high=50
        low = (-1)*high

        random_index = random.randint(1, size-1)
        random_value = random.randint(low, high)
        if size > 50:
            random_index = random.randint(6, size-5)

        loop = 1
        i = 0
        while i < loop:
            #temp_dir = tempfile.TemporaryDirectory()
            #source_data = temp_dir.name + "/source_data.txt"
            source_data = f"/tmp/source_data_{i}.txt"

            data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
            arr = data_hash['array_']
            if static_data_from_file:
                print(f'live arr length: {len(arr)}')
                source_file = "/tmp/source_data_4.txt"
                arr = self.read_static_data_from_file(source_file)
                print(f'static arr length: {len(arr)}')
                #raise SystemExit('force exit')
                #sys.exit('force exit')

            arr = [-15, 1, 1, 28, 25, 25, -21]
            print(f'Array length in test: {len(arr):,}, source_data: {source_data}')
            if len(arr) < print_limit and i == 0:
                print(f'i = {i}, Data Type: {type(arr)}, {arr}')
            print()

            if not static_data_from_file:
                with open(source_data, "w") as file_handle:
                    if isinstance(arr, list):
                        data_2_save = np.array(arr)
                    file_handle.write(",".join(map(str, data_2_save.tolist())))
                    file_handle.write("\n")

            start = time.time()
            thresh = 0
            valley_included = True
            #arr = [8, -7, -10, 3, -9, 5, 9, 1, -2, -4, 2, 0, 1, -3, 2]
            if thresh is None:
                answer_1 = find_peak_valley_1(arr, thresh=thresh, debug=True)
            else:
                answer_1 = find_peak_valley_1(arr, valley_included=valley_included, thresh=thresh, debug=True)
                #answer_1 = find_peak_valley_1(arr, valley_included=valley_included, thresh=thresh)
                elapsed = round(time.time() - start, 4)
                #print(f'answer_1[0] type: {type(answer_1[0])}, answer_1[1] type: {type(answer_1[1])}')
                if valley_included:
                #    print(f'answer_1[2] type: {type(answer_1[2])}, answer_1[3] type: {type(answer_1[3])}')
                    print(f'i: {i}, find_peak_valley_1: Peak Counts: {len(answer_1[0]):,}', end='') 
                    print(f', Valley Counts: {len(answer_1[2]):,}, Time Consumed: {elapsed}')
                else:
                    print(f'find_peak_valley_1: Peak Counts: {len(answer_1[0]):,}') 

            """
            if not static_data_from_file:
                if len(arr) < print_limit:
                    print(f'A. arr length: {len(arr)}, {arr.tolist()}')
                else:
                    print(f'A. arr length: {len(arr)}')
            else:
                if len(arr) < print_limit:
                    print(f'A. arr length: {len(arr)}, {arr}')
                else:
                    print(f'A. arr length: {len(arr)}')
            """
            print(f'random_index: {random_index}, random_value: {random_value}')
            #arr = np.concatenate((arr[:random_index-1], [random_value], arr[random_index:]))
            """
            if not static_data_from_file:
                if len(arr) < print_limit:
                    print(f'B. arr length: {len(arr)}, {arr.tolist()}')
                else:
                    print(f'B. arr length: {len(arr)}')
            else:
                if len(arr) < print_limit:
                    print(f'B. arr length: {len(arr)}, {arr}')
                else:
                    print(f'B. arr length: {len(arr)}')
            """

            #arr = [8, -7, -2, 3, -9, 5, 9, 1, -2, -4, 2, 0, 1, -3, 2]
            start = time.time()
            answer_2 = find_peak_valley_2(arr, debug=True)
            #answer_2 = find_peak_valley_2(arr)
            elapsed = round(time.time() - start, 4)

            peak_asserted = True
            valley_asserted = True
            if thresh is not None:
                if len(answer_1[0]) != len(answer_2[0]) or \
                        answer_1[0] != answer_2[0] or \
                        len(answer_1[1]) != len(answer_2[1]) or \
                        answer_1[1] != answer_2[1]:
                    peak_asserted = False


                if valley_included:
                    if len(answer_1[2]) != len(answer_2[2]) or \
                            answer_1[2] != answer_2[2] or \
                            len(answer_1[3]) != len(answer_2[3]) or \
                            answer_1[3] != answer_2[3]:
                        valley_asserted = False
                """
                #assert len(answer_1[0]) == len(answer_2[0]), \
                #        f'Peak Indices Mismatch!! Check source data used in this test: {source_data}\n\n'
                #print(f'answer_1[0] type: {type(answer_1[0])}, answer_2[0] type: {type(answer_2[0])}')
                #print(f'answer_1[1] type: {type(answer_1[1])}, answer_2[1] type: {type(answer_2[1])}')
                #assert answer_1[0] == answer_2[0]
                #assert answer_1[1] == answer_2[1]
                #if valley_included:
                #    assert len(answer_1[2]) == len(answer_2[2]), \
                #            f'Valley Indices Mismatch!! Check source data used in this test: {source_data}\n\n'
                    #assert answer_1[2] == answer_2[2]
                    #print(f'answer_1[2] type: {type(answer_1[2])}, answer_2[2] type: {type(answer_2[2])}')
                    #print(f'answer_1[3] type: {type(answer_1[3])}, answer_2[3] type: {type(answer_2[3])}')
                    #print(f'answer_1[3]: {answer_1[3]}')
                    #print(f'answer_2[3]: {answer_2[3]}')
                    #assert answer_1[3] == answer_2[3]
                """

            # use temp_dir, and when done:
            #temp_dir.cleanup()

            print(f'i: {i}, find_peak_valley_2: Peak Counts: {len(answer_2[0]):,}', end='')
            print(f', Valley Counts: {len(answer_2[2]):,}, Time Consumed: {elapsed}')
            print()

            i += 1

            if peak_asserted and valley_asserted:
                #print(f'answer_2[0] type: {type(answer_2[0])}, answer_2[1] type: {type(answer_2[1])}')
                #print(f'answer_2[0] type: {type(answer_2[0])}, answer_2[1] type: {type(answer_2[1])}')
                #print(f'answer_2[2] type: {type(answer_2[2])}, answer_2[3] type: {type(answer_2[3])}')

                if not static_data_from_file:
                    path = pathlib.Path(source_data)
                    if path.is_file():
                        print(f'i: {i}, remove "{source_data}"')
                        path.unlink()
            else:
                print(f'i: {i}, Save this: "{source_data}"')
                if not peak_asserted:
                    self.find_mismatch(arr, answer_1, answer_2, flag='p')
                if not valley_asserted: 
                    self.find_mismatch(arr, answer_1, answer_2, flag='v')
