""" All libs are array related """
import inspect
import random
import time

import scipy.signal #import find_peaks # find_peak_valley
import numpy as np # find_peak_valley
import matplotlib.pyplot as plt # find_peak_valley

import data_generator # in house
#from aquarius.codility_python import my_test # in house


def split_list_by_value_1(value, data_list, more_or_less=0):
    """
    Split an array by a given delimiter
    :param value: delimiter
    :param data_list: a list to be splitted
    :param more_or_less: flag - (-1, 0, 1)
    :return: blocks: sublists as a result of splitted data_list
    :return: indices: indices of all delimiters
    """
    if more_or_less < 0:
        indices = [i for i, x in enumerate(data_list) if x <= value]
    elif more_or_less > 0:
        indices = [i for i, x in enumerate(data_list) if x >= value]
    else: # more_or_less == 0:
        indices = [i for i, x in enumerate(data_list) if x == value]

    blocks = []
    i = 0
    for j in indices:
        blocks.append(data_list[i:j])
        i = j + 1

    blocks.append(data_list[i:])
    return blocks, indices


def split_list_by_value_2(value, data_list, more_or_less=0):
    """
    Split an array by a given delimiter
    :param value: delimiter
    :param data_list: a list to be splitted
    :param more_or_less: flag - (-1, 0, 1)
    :yield: chunk: sublists as a result of splitted data_list
    """
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
    """ Find peaks in a given digit array """
    # Intentionally mock scipy.signal.find_peaks() when height is set
    peak_indices, peak_values = [], []
    possible_peak_index = -1
    if height is None:
        print(f'In function_name(): Height is {height}. TBI')
    else:
        # [-15, 1, 1, 28, 25, 25, -21]
        for index in range(1, len(data) - 1):
            if data[index] >= height:
                if data[index] > data[index - 1]:
                    if data[index] > data[index + 1]:
                        peak_indices.append(index)
                        peak_values.append(data[index])
                        possible_peak_index = -1
                    elif data[index] == data[index + 1]:
                        possible_peak_index = index
                elif data[index] == data[index - 1]:
                    if data[index] > data[index + 1] and possible_peak_index > -1:
                        new_index = (index + possible_peak_index)//2
                        peak_indices.append(new_index)
                        peak_values.append(data[new_index])
                        possible_peak_index = -1

    return peak_indices, peak_values


def find_peak_valley_1(data, thresh=0, valley_included=True, debug=False):
    """ Find peaks/valleys in a given digit array """
    # This method is intentionally mocked find_peak_valley_2 with one key difference:
    # it does not call scipy.signal.find_peaks, because codility.com does not accept
    # scipy.py module
    function_name = inspect.currentframe().f_code.co_name
    if debug:
        print(f'In {function_name}(), data type: {type(data)}, valley_included: {valley_included}')

    if isinstance(data, list):
        data = np.array(data)

    peak_indices, peak_values = find_peaks(data, height=thresh)

    if valley_included:
        valley_indices, valley_values = find_peaks(-data, height=thresh)
        valley_values = (-(np.array(valley_values))).tolist()
        return peak_indices, peak_values, valley_indices, valley_values
    return peak_indices, peak_values, None, None


def find_peak_valley_2(data, thresh=0, debug=False):
    """ Find peaks/valleys in a given digit array through 3rd libs """
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

    return peak_index, peak, valley_index, valley


def find_peak_valley_ref(debug=False):
    """ https://stackoverflow.com/questions/50756793/peak-detection-algorithm-in-python """
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


def read_static_data_from_file(source_file):
    """
    Read comma separated digit string from a file and convert it into a list
    """
    with open(source_file, "r") as open_for_read:
        for line in open_for_read.readlines():
            if line[0] == "#":
                continue
            list_ = [int(x) for x in line.rstrip().split(",")]

    return list_


# --------testing codes below----------------------

class TestArrayManipulation:
    """ PyTest class """

    def test_split_array(self):
        """ Test split_array() """
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
        """
        This method is called when there is at least one mismatch in
        results_a & results_b
        """
        function_name = inspect.currentframe().f_code.co_name
        print(f'\nIn {function_name}(), data length: {len(data)}, flag: {flag}\n\n')
        if flag == 'p':
            print("\n\nCheck Peak!!\n")
            self.analyze_results(data, results_a[0], results_b[0], results_a[1], results_b[1])
        else:
            print("\n\nCheck Valley!!\n")
            self.analyze_results(data, results_a[2], results_b[2], results_a[3], results_b[3])


    def analyze_results(self, data, index_a, index_b, value_a, value_b):
        """Analyze where is the mismatch"""
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
                    print(f'Around real_index_a: {real_index_a}, \
                            {data[real_index_a-5:real_index_a+5]}, \
                            on spot: {data[real_index_a]}')
                    print(f'Around real_index_b: {real_index_b}, \
                            {data[real_index_b-5:real_index_b+5]}, \
                            on spot: {data[real_index_b]}')
                else:
                    print(f'data[{real_index_a}] = {data[real_index_a]}')
                    print(f'data[{real_index_b}] = {data[real_index_b]}')


    def test_find_peak_valley(self):
        """ Test find_peak_vally() """
        size=100_000
        high=10_000
        low = (-1)*high
        i = 0
        while i < 5:
            data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
            arr = data_hash['array_']

            start = time.time()
            valley_included = True
            #answer_1 = find_peak_valley_1(
            #    arr,
            #    valley_included=valley_included,
            #    thresh=thresh,
            #    debug=True
            #)
            answer_1 = find_peak_valley_1(arr, valley_included=valley_included)
            elapsed = round(time.time() - start, 4)
            if valley_included:
                print(f'\ni: {i}, find_peak_valley_1: Peak Counts: {len(answer_1[0]):,}', end='')
                print(f', Valley Counts: {len(answer_1[2]):,}, Time Consumed: {elapsed}')
            else:
                print(f'find_peak_valley_1: Peak Counts: {len(answer_1[0]):,}')

            start = time.time()
            answer_2 = find_peak_valley_2(arr)
            elapsed = round(time.time() - start, 4)

            peak_asserted = True
            valley_asserted = True
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

            print(f'i: {i}, find_peak_valley_2: Peak Counts: {len(answer_2[0]):,}', end='')
            print(f', Valley Counts: {len(answer_2[2]):,}, Time Consumed: {elapsed}')
            assert peak_asserted
            if valley_included:
                assert valley_asserted

            if not peak_asserted:
                self.find_mismatch(arr, answer_1, answer_2, flag='p')
            if not valley_asserted:
                self.find_mismatch(arr, answer_1, answer_2, flag='v')

            i += 1
        # end of while i < 5:
