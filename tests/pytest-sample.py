# Simple pytest example
def function_to_test(x):
    return x + 1

def test_answer():
    assert function_to_test(4) == 5
