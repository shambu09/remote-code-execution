code = """
def r_lambda(*args, **kwargs):
    l = []
    
    for i in zip(kwargs.items(), args):
        l.append(i)
    
    print(l)

r_args = [1, 2, 3]
r_kwargs = {'a': 1, 'b': 2, 'c': 3}
r_schedule = 'interval'
r_interval = 1
"""

# response = requests.post("http://127.0.0.1:5000/" + "run", json={"name": "test_module", "code": code})
# print(response.json())

import sys
from app.utils import Code, PatchStd

if __name__ == '__main__':
    with PatchStd() as std:
        module = Code("test_module", code)
        module.run.r_lambda(*module.run.r_args, **module.run.r_kwargs)

    print(std.out.getvalue())