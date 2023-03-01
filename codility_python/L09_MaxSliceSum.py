bogus = 1.11

def handle_special_cases(arr):

    return bogus


def solution(A):
    # Score 100%
    if max(A) < 0:
        # All negative
        return sorted(A)[-1]
    if min(A) > 0:
        # All positive
        return sum(A)
    if len(A) == 1:
        return A[0]
    if len(A) == 2:
        return max(A)

    first_positive = next(x for x, val in enumerate(A) if val > 0)

    A.append(-1)
    all_positive = 0
    max_positive = 0
    for x in A[first_positive:]:
        if x > -1:
            all_positive += x
        else:
            max_positive = max(max_positive, all_positive)
            all_positive += x
            if all_positive < 0:
                all_positive = 0
                continue
    return max_positive


if __name__ == '__main__':
    arr = [30,-1,2,-1,9,-6,4,0,-1]
    arr = [3,2,-6,4,0]
    arr = [-1,99,-98,94,5]
    solution = solution_4
    print(solution(arr))
