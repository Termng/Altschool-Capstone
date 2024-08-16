import pytest
from app.calculations import add, multiply


@pytest.mark.parametrize("x, y, expected", [
    (2, 3, 5), 
    (3,4,7), 
    (10, 356, 366)
    ])
def test_add( x, y, expected):
    print("testing for fastapi")
    assert add(x, y) == expected
    

def test_multiply():
    assert multiply(5, 5) == 25