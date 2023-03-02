def handle_special_cases(A, B):
    print(f'In handle_special_cases()\n{A}\n{B}\n')
    for up_down in [0, 1]:
        if up_down not in B:
            # All fish are in the same direction
            return len(A)

    """
    if B.count(1) == 1:
        # There is only one downstream fish
        if B[-1] == 1:
            # The only downstream fish is the last one at the far right point
            print(f'the only downstream fish: {A[-1]}')
            return len(A)

        if B[0] == 1 and A[0] == max(A):
            # The only downstream fish is at the start point and it's the largest
            return 1

        index = B.index(1)
        if A[index] == min(A):
            # The only downstream fish is the smallest
           return len(A) - 1


    if B.count(0) == 1:
        print(f'B[-1]: {B[-1]}, A[-1]: {A[-1]}, max(A): {max(A)}')
        # There is only one upstream fish
        if B[0] == 0:
            # A[0] is the only upstream fish
            print(f'the only upstream fish: {A[0]}')
            return len(A)

        if B[-1] == 0 and A[-1] == max(A):
            # The only upstream fish is at the end point and it's the largest
            return 1

        index = B.index(0)
        if A[index] == min(A):
            # The only upstream fish is the smallest
            return len(A) - 1
    
    """
    print('In handle_special_cases(). Return 0!!\n')
    return 0


def handle_generic_cases(A, B):
    print(f'In handle_generic_cases()\n{A}\n{B}\n')
    D = []
    U = []
    for i, fish_i in enumerate(A):
        if B[i] > 0:
            D.append(fish_i)

        print(f'i: {i}, fish_i: {fish_i}, B[{i}]: {B[i]}, D: {D}')
        if i > 0:
            if B[i-1] > B[i]:
                if A[i-1] > A[i]:
                    print(f'=->A1. i: {i}, D: {D}, U: {U}, B[{i-1}]: {B[i-1]}, B[{i}]: {B[i]}, A[{i-1}]: {A[i-1]}, A[{i}]: {A[i]}')
                    pass
                else:
                    print(f'#=->B1. i: {i}, D: {D}, U: {U}, B[{i-1}]: {B[i-1]}, B[{i}]: {B[i]}, A[{i-1}]: {A[i-1]}, A[{i}]: {A[i]}')
                    if len(D) > 0:
                        for d in D[::-1]:
                            if d > fish_i:
                                break
                            else:
                                D.pop()
                    if len(D) == 0:
                        U.append(fish_i)
                    print(f'#=->B2. i: {i}, D: {D}, U: {U}, B[{i-1}]: {B[i-1]}, B[{i}]: {B[i]}, A[{i-1}]: {A[i-1]}, A[{i}]: {A[i]}')
            else: # B[i-1] <= B[i]
                if A[i-1] > A[i]:
                    print(f'PASS!! C1. i: {i}, D: {D}, U: {U}, A[{i}]: {A[i]}')
                    if len(D) == 0:
                        U.append(fish_i)
                    print(f'PASS!! C2. i: {i}, D: {D}, U: {U}, A[{i}]: {A[i]}')
                else:
                    print(f'==-->>TBI!! D1. i: {i}, fish_i: {fish_i}, D: {D}, U: {U}, A[{i}]: {A[i]}')
                    if len(D) > 0 and B[i] == 0:
                        for d in D[::-1]:
                            if d > fish_i:
                                break
                            else:
                                D.pop()
                    if len(D) == 0:
                        if B[i] == 0:
                            U.append(fish_i)
                    print(f'==-->>TBI!! D2. i: {i}, fish_i: {fish_i}, D: {D}, U: {U}, A[{i}]: {A[i]}')
        print()

    print(f'In handle_generic_cases()\nD: {D}\nU: {U}\nA: {A}\n')
    return len(D) + len(U)


def solution(A, B):
    # Task Score 75% Correctness 100% Performance 50%
    # medium_random small medium test, N = ~5,000
    # WRONG ANSWER got 39 expected 41
    # large_random large random test, N = ~100,000
    # WRONG ANSWER got 774 expected 840
    print(f'A: {A}\nB: {B}')
    count = handle_special_cases(A, B)
    if count:
        return count

    auto_survived_downstream_fish_count = B.index(1)
    print(f'auto_survived_downstream_fish_count: {auto_survived_downstream_fish_count}')
    auto_survived_upstream_fish_count = B[::-1].index(0)
    print(f'  auto_survived_upstream_fish_count: {auto_survived_upstream_fish_count}')

    a = A[auto_survived_downstream_fish_count:len(A)-auto_survived_upstream_fish_count]
    b = B[auto_survived_downstream_fish_count:len(B)-auto_survived_upstream_fish_count]
    # Now, the first fish in array a is downstream,
    # and  the last  fish in array a is upstream.
    count = handle_special_cases(a, b)
    if count:
        print(f"a: {a}")
        print(f"b: {b}")
        print(f"count: {count}")
        return count + auto_survived_downstream_fish_count + auto_survived_upstream_fish_count

    count = handle_generic_cases(a, b)
    print(f'A: {A}\nB: {B}')
    print(f'count = {count}')
    print(f'auto_survived_downstream_fish_count: {auto_survived_downstream_fish_count}')
    print(f'auto_survived_upstream_fish_count: {auto_survived_upstream_fish_count}')
    return count + auto_survived_downstream_fish_count + auto_survived_upstream_fish_count


if __name__ == '__main__':
    """
    # All downstreams
    A=[9,8,4,3,2,7,1,6,5]
    B=[1,1,1,1,1,1,1,1,1]
    assert solution(A,B) == len(A)

    # All upstreams
    A=[9,8,4,3,2,7,1,6,5]
    B=[0,0,0,0,0,0,0,0,0]
    assert solution(A,B) == len(A)

    # The only downstream is at the end
    A=[9,8,4,3,2,7,1,6,5]
    B=[0,0,0,0,0,0,0,0,1]
    assert solution(A,B) == len(A)

    # The only upstream is at the beginning
    A=[9,8,4,3,2,7,1,6,5]
    B=[0,1,1,1,1,1,1,1,1]
    assert solution(A,B) == len(A)
    
    # The only downstream is at the beginning and it's the largest
    A=[9,8,4,3,2,7,4,6,1]
    B=[1,0,0,0,0,0,0,0,0]
    assert solution(A,B) == 1

    # The only upstream is at the end and it's the largest
    A=[5,8,4,3,2,7,1,6,9]
    B=[1,1,1,1,1,1,1,1,0]
    assert solution(A,B) == 1
    """

    # The only downstream is the smallest
    A=[9,8,1,3,2,7,4,6,5]
    B=[0,0,1,0,0,0,0,0,0]
    #assert solution(A,B) == len(A) - 1
    answer = solution(A,B)
    print(f'answer: {answer}')
    assert answer == len(A) - 1

    # The only upstream is the smallest
    A=[9,8,4,3,2,7,1,6,5]
    B=[1,1,1,1,1,1,0,1,1]
    assert solution(A,B) == len(A) - 1
    # ---------------------------------
    A=[5,1,4,3,2,8,9,6,7]
    B=[0,1,0,0,0,0,1,1,1]
    assert solution(A,B) == len(A) - 1
    
    A=[5,9,4,3,2,8,1,6,7]
    B=[0,1,1,1,1,1,0,1,1]
    assert solution(A,B) == len(A) - 1

    A=[5,1,4,3,2,8,9,6,7]
    B=[0,1,0,1,0,0,1,0,1]
    print(solution(A,B))
    A=[4,3,2,1,5]
    B=[0,1,0,0,0]
    print(solution(A,B))
