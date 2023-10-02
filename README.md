[![PyPI](https://img.shields.io/pypi/v/scinumtools)](https://pypi.org/project/scinumtools)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/scinumtools)](https://pypi.org/project/scinumtools/)
[![PyTest](https://github.com/vrtulka23/scinumtools/actions/workflows/pytest.yml/badge.svg)](https://github.com/vrtulka23/scinumtools/actions/workflows/pytest.yml)

# scinumtools

![scinumtools](https://raw.githubusercontent.com/vrtulka23/scinumtools/main/docs/source/_static/snt/snt_128.png)

Python package `scinumtools` contains essential tools for scientific and numerical calculations, simulation setup and data analysis. 

## Documentation

For more information, see the scinumtools [documentation](https://vrtulka23.github.io/scinumtools/).
The documentation is currently in a process of writing, so any comments and suggestions for improvement are heartily welcomed.

## Quick start

The newest release of `scinumtools` is available on [PyPi](https://pypi.org/project/scinumtools/) and can be easily installed using `pip` package manager:

``` python
pip3 install scinumtools
```

Besides several useful tools, package `scinumtools` consist of three main submodules: expression solver, physical units and DIP.

### Expression Solver

Using `expression solver` one can quickly build a custom parser that can process numerical, logical and textual expressions. This module is an integral part of both, physical units and DIP modules.
For more description and examples of [Expression Solver](https://vrtulka23.github.io/scinumtools/solver/index.html) please refer to the documentation.

``` python
>>> from scinumtools.solver import *
>>> class AtomCustom(AtomBase):
>>>     value: str
>>>     def __init__(self, value:str):
>>>         self.value = str(value)
>>>     def __add__(self, other):
>>>         return AtomCustom(self.value + other.value)
>>>     def __gt__(self, other):
>>>         return AtomCustom(len(self.value) > len(other.value))
>>> operators = {'add':OperatorAdd,'gt':OperatorGt,'par':OperatorPar}
>>> steps = [
>>>     dict(operators=['par'],  otype=Otype.ARGS),
>>>     dict(operators=['add'],  otype=Otype.BINARY),
>>>     dict(operators=['gt'],   otype=Otype.BINARY),
>>> ]
>>> with ExpressionSolver(AtomCustom, operators, steps) as es:
>>>     es.solve("(limit + 100 km/s) > (limit + 50000000000 km/s)")
'False'
```

### Physical Units

This submodule has an aim to make calculations with `physical units` quick and easy. It includes multiple types of units, constants and implements standard numerical operations with physical quantities. Besides that, it features unit convertor, supports calculations with uncertainties and can be used in combination with third party libraries like NumPy, or Decimal.
For more description and examples of [Physical Units](https://vrtulka23.github.io/scinumtools/units/index.html) please refer to the documentation.

``` python
>>> import numpy as np
>>> from scinumtools.units import Quantity, Unit
>>> Quantity(23.34, 'kg*m2/s2').to('erg')     # unit conversions
Quantity(2.334e+08 erg)
>>> u = Unit()                                # calculations with units
>>> 34*u.cm + 53*u.dm  
Quantity(5.640e+02 cm)
>>> Quantity(23.34, 'cm', abse=0.03)          # uncertainities
Quantity(2.3340(30)e+01 cm)
>>> Quantity(3, 'A').value('dBA')             # logarithmic units
9.542425094393248
>>> np.sqrt(Quantity([23,59,20,10], 'm2'))    # arrays and NumPy
Quantity([4.796 7.681 4.472 3.162] m)
```

### Dimensional Input Parameters

`DIP` is a serialization language that was designed to collect, manage, convert, document and validate dimensional input parameters used by numerical codes. The main goal of this package is to help developers to focus less on initialization processes mentioned above and more on actual code development. `DIP` should serve as a quick tool that makes user interface with the code clear and straightforward. 
For more description and examples of [DIP](https://vrtulka23.github.io/scinumtools/dip/index.html) please refer to the documentation.

``` python
>>> from scinumtools.dip import DIP, Format
>>> with DIP() as dip:
>>>     dip.add_source("settings", 'settings.dip')
>>>     dip.add_unit("length", 1, "m")
>>>     dip.from_string("""
>>>     box
>>>       width float = 23 [length]
>>>       height float = 11.5 cm
>>>     sphere
>>>       radius float = {settings?sphere.radius}
>>>     """)
>>>     env = dip.parse()
>>>     env.data(Format.TUPLE)
{'box.width': (23.0, '[length]'), 'box.height': (11.5, 'cm'), 'sphere.radius': (34.2, 'mm')}
```
