# Dividing two numbers
import pytest

def div(a,b):
    if b == 0:
        raise ZeroDivisionError("b cant be zero")
    return a / b

def test_div_b_not_0():
    assert div(50,25) == 2

def test_div_b_0():
    with pytest.raises(ZeroDivisionError):
        div(2,0)