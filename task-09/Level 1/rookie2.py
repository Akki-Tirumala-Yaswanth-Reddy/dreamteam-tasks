# Odd or Even

def oddOrEven(a):
    a = abs(a)
    if a % 2 == 0:
        return 0
    else:
        return 1
    
def test_oddOrEven_positive_even():
    assert oddOrEven(4) == 0

def test_oddOrEven_negative_even():
    assert oddOrEven(-4) == 0

def test_oddOrEven_positive_odd():
    assert oddOrEven(3) == 1

def test_oddOrEven_negative_add():
    assert oddOrEven(-3) == 1

def test_oddOrEven_zero():
    assert oddOrEven(0) == 0