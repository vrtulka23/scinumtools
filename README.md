[![PyPI](https://img.shields.io/pypi/v/scinumtools)](https://pypi.org/project/scinumtools)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/scinumtools)](https://pypi.org/project/scinumtools/)
[![PyTest](https://github.com/vrtulka23/scinumtools/actions/workflows/pytest.yml/badge.svg)](https://github.com/vrtulka23/scinumtools/actions/workflows/pytest.yml)

# SciNumTools v2

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

Besides several useful tools, the package `scinumtools` consists of four main submodules: expression solver, physical units, material properties and DIP.

### Expression Solver

Using `expression solver` one can quickly build a custom parser that can process numerical, logical and textual expressions. This module is an integral part of other submodules.
For more description and examples of [Expression Solver](https://vrtulka23.github.io/scinumtools/solver/index.html), please refer to the documentation. C++ implementation of this module is available in a separate [GitHub repository](https://github.com/vrtulka23/scnt-exs).

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

This submodule has an aim to make calculations with `physical units` quick and easy. It includes multiple types of units, constants and implements standard numerical operations with physical quantities. Besides that, it features a unit convertor, supports calculations with uncertainties and can be used in combination with third-party libraries like NumPy, or Decimal.
For more description and examples of [Physical Units](https://vrtulka23.github.io/scinumtools/units/index.html), please refer to the documentation.
A C++ implementation of this module [scnt-puq](https://github.com/vrtulka23/scnt-puq) is currently available also as a Python module [pypuq](https://pypi.org/project/pypuq) on PyPi.

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

### Material Properties

Simulation setups often require atomic and molecular properties of various materials. The core of this submodule, molecular expression solver, is designed to simplify calculations of such properties from a given molecular formula.
For more descriptions and examples of [Material Properties](https://vrtulka23.github.io/scinumtools/materials/index.html), please refer to the documentation.

``` python
>>> from scinumtools.units import Quantity
>>> from scinumtools.materials import Substance
>>> s = Substance('H2O', natural=False, mass_density=Quantity(997,'kg/m3'), volume=Quantity(1,'l'))
>>> s.print()
Components:

expr element  isotope  ionisation  mass[Da]  count  Z  N  e
   H       H        1           0  1.007825    2.0  1  0  1
   O       O       16           0 15.994915    1.0  8  8  8

Composite:

Total mass:     Quantity(1.801e+01 Da)
Total number:   3.0

expr  mass[Da]         Z        N         e       x[%]       X[%]
   H  2.015650  2.000000 0.000000  2.000000  66.666667  11.191487
   O 15.994915  8.000000 8.000000  8.000000  33.333333  88.808513
 avg  6.003522  3.333333 2.666667  3.333333  33.333333  33.333333
 sum 18.010565 10.000000 8.000000 10.000000 100.000000 100.000000

Matter:

Mass density:   Quantity(9.970e-01 g*cm-3)
Number density: Quantity(3.334e+22 cm-3)
Volume:         Quantity(1.000e+00 l)
Mass:           Quantity(9.970e+02 g)

expr      n[cm-3]  rho[g/cm3]            N       M[g]
   H 6.667280e+22    0.111579 6.667280e+25 111.579129
   O 3.333640e+22    0.885421 3.333640e+25 885.420871
 avg 3.333640e+22    0.332333 3.333640e+25 332.333333
 sum 1.000092e+23    0.997000 1.000092e+26 997.000000
```

### Dimensional Input Parameters

`DIP` is a serialization language that was designed to collect, manage, convert, document and validate dimensional input parameters used by numerical codes. The main goal of this package is to help developers to focus less on the initialization processes mentioned above and more on actual code development. `DIP` should serve as a quick tool that makes the user interface with the code clear and straightforward. 
For more description and examples of [DIP](https://vrtulka23.github.io/scinumtools/dip/index.html), please refer to the documentation. A C++ implementation of this library is currently being developed in a [separate GIT repository](https://github.com/vrtulka23/scnt-dip/tree/main).

``` python
>>> from scinumtools.dip import DIP, Format
>>> with DIP() as dip:
>>>     dip.add_source("settings", 'settings.dip')
>>>     dip.add_unit("length", 1, "m")
>>>     dip.add_string("""
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

The alternative Python module [dipl](https://github.com/vrtulka23/dipl) implements basic loading and dumping functionality of DIP and provides a quick solution for data parsing using DIP.

``` python
>>> import dipl
>>>
>>> dipl.load("""
>>> width float = 173.34 cm
>>> age int = 24 yr
>>> """)
{'width': (173.34, 'cm'), 'age': (24, 'yr')}
>>>
>>> dipl.dump({
>>> 'children': ['John','Jenny','Jonah'],
>>> 'car': True
>>> })
children str[3] = ["John","Jenny","Jonah"]
car bool = true
```
