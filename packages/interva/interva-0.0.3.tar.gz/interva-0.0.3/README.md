# interva

[![image](https://img.shields.io/pypi/pyversions/interva)](https://pypi.org/project/interva/)
[![pytest](https://github.com/verbal-autopsy-software/interva/actions/workflows/python-package.yml/badge.svg)](https://github.com/verbal-autopsy-software/interva/actions)

Python implementation of the InterVA algorithm for assigning causes of death to verbal autopsy data


## Importing package and installing dependencies

To install all package dependencies, run:  

```python
pip install interva
```

To import this package's functions:  

```python
>>> from interva.interva5 import InterVA5
```
## Example data

To access example data from the package:  

```python
>>> from interva.interva5 import get_example_input
>>> va_data = get_example_input()
>>> va_data
       ID i004a i004b i019a i019b i022a  ... i454o i455o i456o i457o i458o i459o
0      d1     .     .     y     .     y  ...     n     n     n     n     n     n
1      d2     .     .     .     y     y  ...     n     n     n     n     n     n
2      d3     .     .     y     .     .  ...     n     n     n     n     n     n
3      d4     .     .     .     y     .  ...     n     n     n     n     n     n
4      d5     .     .     y     .     .  ...     n     n     n     n     n     n
..    ...   ...   ...   ...   ...   ...  ...   ...   ...   ...   ...   ...   ...
195  d196     .     .     .     y     .  ...     n     n     n     n     n     n
196  d197     .     .     y     .     y  ...     n     n     n     n     n     n
197  d198     .     .     y     .     y  ...     n     n     n     n     n     n
198  d199     .     .     .     y     y  ...     n     n     n     n     n     n
199  d200     .     .     .     y     y  ...     n     n     n     n     n     n

[200 rows x 354 columns]
```
  
## Creating and running an InterVA5 object

To initialize an InterVA5 object:  

```python
>>> iv5out = InterVA5(va_data, hiv="h", malaria="l", write=False, directory="VA test", filename="VA5_result", output="extended", append=False, return_checked_data=True)
```
  
To run the InterVA5 algorithm on the InterVA5 object:  

```python
>>> iv5out.run()
Using Probbase version: probbase v19 20210720
..........10% completed
..........20% completed
..........30% completed
..........40% completed
..........50% completed
..........60% completed
..........70% completed
..........80% completed
..........90% completed
..........100% completed
100% completed
>>> iv5out.get_csmf(top=8)
HIV/AIDS related death               0.194408
Undetermined                         0.136583
Digestive neoplasms                  0.083285
Other and unspecified infect dis     0.063096
Renal failure                        0.061253
Reproductive neoplasms MF            0.053655
Other and unspecified cardiac dis    0.047557
Stroke                               0.045583
dtype: float64
```

To access the algorithm output:  

```python
>>> iv5out.out["ID"]
0        d1
1        d2
2        d3
3        d4
4        d5
       ... 
195    d196
196    d197
197    d198
198    d199
199    d200
Name: ID, Length: 200, dtype: object
>>> iv5out.out["VA5"]
       ID MALPREV  ... COMNUM                                          WHOLEPROB
0      d1       l  ...     99  cause
Not pregnant or recently delivered      ...
1      d2       l  ...     91  cause
Not pregnant or recently delivered      ...
2      d3       l  ...     91  cause
Not pregnant or recently delivered      ...
3      d4       l  ...     91  cause
Not pregnant or recently delivered      ...
4      d5       l  ...     99  cause
Not pregnant or recently delivered      ...
..    ...     ...  ...    ...                                                ...
195  d196       l  ...    100  cause
Not pregnant or recently delivered      ...
196  d197       l  ...     99  cause
Not pregnant or recently delivered      ...
197  d198       l  ...     99  cause
Not pregnant or recently delivered      ...
198  d199       l  ...     79  cause
Not pregnant or recently delivered      ...
199  d200       l  ...     62  cause
Not pregnant or recently delivered      ...

[200 rows x 15 columns]
>>> iv5out.out["Malaria"]
'l'
>>> iv5out.out["HIV"]
'h'
>>> iv5out.out["checked_data"]
     ID  i004a  i004b  i019a  i019b  ...  i455o  i456o  i457o  i458o  i459o
0   NaN    NaN    NaN    1.0    NaN  ...      0      0      0      0      0
1   NaN    NaN    NaN    NaN    1.0  ...      0      0      0      0      0
2   NaN    NaN    NaN    1.0    NaN  ...      0      0      0      0      0
3   NaN    NaN    NaN    NaN    1.0  ...      0      0      0      0      0
4   NaN    NaN    NaN    1.0    NaN  ...      0      0      0      0      0
..   ..    ...    ...    ...    ...  ...    ...    ...    ...    ...    ...
195 NaN    NaN    NaN    NaN    1.0  ...      0      0      0      0      0
196 NaN    NaN    NaN    1.0    NaN  ...      0      0      0      0      0
197 NaN    NaN    NaN    1.0    NaN  ...      0      0      0      0      0
198 NaN    NaN    NaN    NaN    1.0  ...      0      0      0      0      0
199 NaN    NaN    NaN    NaN    1.0  ...      0      0      0      0      0

[200 rows x 354 columns]
```
  
To get likelihoods of HIV or malaria as a cause of death from the InterVA5 object:  

```python
>>> hiv = iv5out.get_hiv()
>>> hiv
HIV parameter is h
>>> malaria = iv5out.get_malaria()
>>> malaria
Malaria parameter is l
```
  
To set likelihoods ("h", "l", "v") of HIV or malaria as a cause of death for the InterVA5 object:  

```python
>>> iv5out.set_hiv("l")
'l'
>>> iv5out.get_hiv()
HIV parameter is l
'l'
>>> iv5out.set_malaria("v")
'v'
>>> iv5out.get_malaria()
Malaria parameter is v
'v'
```
  
To get ids from the InterVA5 object:  

```python
>>> ids = iv5out.get_ids()
>>> ids
0        d1
1        d2
2        d3
3        d4
4        d5
       ...
195    d196
196    d197
197    d198
198    d199
199    d200
Name: ID, Length: 200, dtype: object
```
