src = """
def r_lambda(*args, **kwargs):
    l = []
    
    for i in zip(kwargs.items(), args):
        l.append(i)
    raise Exception("Test")
    print(l)

r_args = [1, 2, 3]
r_kwargs = {'a': 1, 'b': 2, 'c': 3}
r_schedule = 'interval'
r_interval = 1
r_lambda(*r_args, **r_kwargs)
"""

import sys
from app.utils import Code, PatchStd

if __name__ == '__main__':
    with PatchStd() as std:
        module = Code("test_module", src)
        module.lib.__run()
    print(std.value)