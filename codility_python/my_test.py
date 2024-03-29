def display_summary(summary):
    longest_name = 0
    longest = 0
    for tuple_ in summary:
        if longest_name < len(tuple_[0]):
            longest_name = len(tuple_[0])
        longest = max(longest, len(str(tuple_[1])))

    for j, tuple_ in enumerate(summary, start=1):
        name = tuple_[0]
        while len(name) < longest_name:
            name = ' ' + name

        answer = tuple_[1]
        while len(str(answer)) < longest:
            answer = ' ' +  answer

        if isinstance(answer, bool):
            print(f'{j}, {name} - {answer}: Time Consumed: {tuple_[2]}')
        elif isinstance(answer, int):
            print(f'{j}, {name} - {answer:,}: Time Consumed: {tuple_[2]}')
        else:
            print(f'{j}, {name} - {answer}: Time Consumed: {tuple_[2]}')

"""
def get_summary(solution_list, module_name, arr):
    import time
    import importlib
    module = importlib.import_module(module_name, package=None)
    print(f'module: {module}')
    summary = []
    for j, solution in enumerate(solution_list, start=1):
        #from module import solution
        method = str(solution).split()[1]
        #answer = module.solution_mine(arr)
        #elapsed = round(time.time() - start, 4)
        #print(method, answer, elapsed)
        print(f'method: {method}, solution: {solution}, solution type: {type(solution)}')
        #summary.append((method, answer, elapsed))
"""

