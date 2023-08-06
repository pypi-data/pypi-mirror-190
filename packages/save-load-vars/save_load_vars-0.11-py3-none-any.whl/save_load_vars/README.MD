# Save and load vars, functions, objects ...


### How to save the global vars (or any other variable)
```python
# Create a file

import pandas as pd
from save_load_vars import save_vars_pkl

df = pd.read_csv(
    "https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv"
)


def myfunction(x):
    return str(x) + "bbbb"


myfunction2 = lambda k: myfunction(k)
partofframe = df.Name.copy()[:50]

# Save the global vars 
save_vars_pkl(g=globals(), folder=f"f:\\pklsavetest", interface="dill", protocol=None)

```


### How to load the saved data
```python
from save_load_vars import load_vars_pkl


load_vars_pkl(folder=f'f:\\pklsavetest',
              name=__name__,interface='dill')

print(df)
print(myfunction(44))
print(partofframe)
print(df.Cabin.apply(myfunction2))
```


### How to create global variables from a dict
```python
from save_load_vars import globals_from_dict
didi={
    'a':'bobo',
    'b':'bobao',
    'c': [4,3,3]
}
globals_from_dict(didi,__name__)
print(a)
print(b)
print(c)
```