# Add

def add(a, b):
    return a + b

def test_add_positive_numbers():
    assert add(2,3) == 5

def test_add_negative_numbers():
    assert add(-2,-3) == -5

def test_add_positive_negative():
    assert add(-2,3) == 1

def test_add_decimals():
    assert add(1.5, 2) == 3.5