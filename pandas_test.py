import pandas as pd

a = [
    {'a': 1, 'b': 2},
    {'a': 1, 'b': 2},
    {'a': 3, 'b': 4},
    {'a': 3, 'b': 4}]

d = pd.DataFrame(a)

print(d)