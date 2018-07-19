# dwdopen

Python library to access DWD Open Data from https://opendata.dwd.de


This is a work in progress.

Currently implemented: pollen forecast for Germany.

## Examples

Initialize

```python
from dwdopen import Pollen
p = Pollen()
```

Display possible values for pollen types

```python
p.pollen
{'Ambrosia', 'Beifuss', 'Birke', ...}
```

Display possible values for region id

```python
p.regions
{11: 'Inseln und Marschen',
 12: 'Geest, Schleswig-Holstein und Hamburg',
 ...}
```

Get forecast

```python
p.report(region=12,
         pollen=('Ambrosia', 'Graeser'),
         forecast=0)
```
Return values range from 0 (no pollution) to 7 (high pollution).
