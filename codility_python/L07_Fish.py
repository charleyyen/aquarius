""" Lesson 07 - Fish """
def handle_special_cases(fish_size, direction):
    """ handle_special_cases """
    for up_down in [0, 1]:
        if up_down not in direction:
            return len(fish_size)
    return 0


def handle_generic_cases(fish_size, direction):
    """handle_generic_cases"""
    d_live = []
    count = len(fish_size)

    for i, fish_i in enumerate(fish_size):
        if direction[i] > 0:
            d_live.append(fish_i)
        if i == 0:
            continue

        if direction[i] == 0:
            if len(d_live) > 0:
                for d_fish in d_live[::-1]:
                    count -= 1
                    if d_fish > fish_i:
                        break
                    d_live.pop()

    return count


def solution(fish_size, direction):
    """solution 100%"""
    count = handle_special_cases(fish_size, direction)
    if count:
        return count

    auto_survived_downstream_fish_count = direction.index(1)
    auto_survived_upstream_fish_count = direction[::-1].index(0)

    a_new = fish_size[auto_survived_downstream_fish_count:len(fish_size)-auto_survived_upstream_fish_count]
    b_new = direction[auto_survived_downstream_fish_count:len(direction)-auto_survived_upstream_fish_count]
    # Now, the first fish in array a is downstream,
    # and  the last  fish in array a is upstream.
    count = handle_special_cases(a_new, b_new)
    if count:
        return count + auto_survived_downstream_fish_count + auto_survived_upstream_fish_count

    count = handle_generic_cases(a_new, b_new)
    return count + auto_survived_downstream_fish_count + auto_survived_upstream_fish_count


if __name__ == '__main__':
    # All downstreams
    A_=[9,8,4,3,2,7,1,6,5]
    B_=[1,1,1,1,1,1,1,1,1]
    assert solution(A_,B_) == len(A_)

    # A_ll upstreA_ms
    A_=[9,8,4,3,2,7,1,6,5]
    B_=[0,0,0,0,0,0,0,0,0]
    assert solution(A_,B_) == len(A_)

    # The only downstreA_m is A_t the end
    A_=[9,8,4,3,2,7,1,6,5]
    B_=[0,0,0,0,0,0,0,0,1]
    assert solution(A_,B_) == len(A_)

    # The only upstreA_m is A_t the B_eginning
    A_=[9,8,4,3,2,7,1,6,5]
    B_=[0,1,1,1,1,1,1,1,1]
    assert solution(A_,B_) == len(A_)

    # The only downstreA_m is A_t the B_eginning A_nd it's the lA_rgest
    A_=[9,8,4,3,2,7,4,6,1]
    B_=[1,0,0,0,0,0,0,0,0]
    assert solution(A_,B_) == 1

    # The only upstreA_m is A_t the end A_nd it's the lA_rgest
    A_=[5,8,4,3,2,7,1,6,9]
    B_=[1,1,1,1,1,1,1,1,0]
    assert solution(A_,B_) == 1

    # The only downstreA_m is the smA_llest
    A_=[9,8,1,3,2,7,4,6,5]
    B_=[0,0,1,0,0,0,0,0,0]
    #print(solution(A_,B_))
    assert solution(A_,B_) == len(A_) - 1

    # The only upstreA_m is the smA_llest
    A_=[9,8,4,3,2,7,1,6,5]
    B_=[1,1,1,1,1,1,0,1,1]
    assert solution(A_,B_) == len(A_) - 1
    # ---------------------------------
    A_=[5,1,4,3,2,8,9,6,7]
    B_=[0,1,0,0,0,0,1,1,1]
    assert solution(A_,B_) == len(A_) - 1

    A_=[5,9,4,3,2,8,1,6,7]
    B_=[0,1,1,1,1,1,0,1,1]
    assert solution(A_,B_) == len(A_) - 1

    A_=[5,1,4,3,2,8,9,6,7]
    B_=[0,1,0,1,0,0,1,0,1]
    assert solution(A_,B_) == 5

    A_=[4,3,2,1,5]
    B_=[0,1,0,0,0]
    assert solution(A_,B_) == 2
