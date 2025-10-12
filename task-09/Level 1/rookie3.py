# Print first element of a list

def pfl(arr):
    if len(arr) == 0:
        return 0
    return arr[0]

def test_pfl_len_not_0():
    arr = [1,2,3]
    assert pfl(arr) == 1

def test_pfl_len_0():
    arr = []
    assert pfl(arr) == 0