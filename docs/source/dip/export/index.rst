Parameter export
================

In the previous section, we showed how to parse DIP files into a list of parameters. In this section, we provide several tools that use such parameter lists and export them into different formats. 

Templates
---------

Template solver was already introduced in previous sections concerning general DIP syntax.
Class ``TemplateSolver`` can be, however, used also separately as a template parser.

Let's take an example of a template file below:

.. code-block:: rst
   :caption: template.txt

   Geometry: {{?box.geometry}}
   Box size: [{{?box.size.x}}, {{?box.size.y}}, {{?box.size.z}}]

This file can be easily processed using ``TemplateSolver`` class

.. code-block:: python

   >>> from scinumtools.dip import DIP
   >>> from scinumtools.dip.solvers import TemplateSolver
   >>> 
   >>> with DIP() as dip:
   >>>     dip.add_file('definitions.dip')
   >>>     env = dip.parse()
   >>> with TemplateSolver(env) as ts:
   >>>     text = ts.template('template.txt','processed.txt')

and exported as following text file:

.. code-block:: rst
   :caption: processed.txt

   Geometry: 3
   Box size: [1e-06, 3.0, 23.0]

Configuration files
-------------------

Low level language like C/C++, Fortran, or Rust usually require some kind of configuration file with settings, or constants. 
Many codes can already read parameters using (YAML, TOML, and other) configurations files.
DIP can easily export parsed parameters into these languages and create corresponding configuration files using ``ExportConfig`` class.
The following example DIP code

.. literalinclude :: ../../_static/export_config/config.dip
   :language: DIP
   :caption: config.dip

can be parsed with ``DIP`` and exported using ``ExportConfig***`` classes

.. code-block:: python

    >>> from scinumtools.dip import DIP
    >>>
    >>> with DIP() as dip:
    >>>    dip.add_file("config.dip")
    >>>    env = dip.parse()

One can also restrict which parameters will be exported using query and tag selectors:

.. code-block:: 

    >>> with ExportConfigC(env) as exp:
    >>>     exp.select(query="box.*", tags=["selection"])        
    >>>     exp.parse()
    
Examples of the corresponding exports are available in `pytests <https://github.com/vrtulka23/scinumtools/tree/main/tests/dip/test_config.py>`_.

Since DIP parameter names are not suitable for all languages mentioned above, in some cases parameter names are automatically converted to upper case and hierarchy separators ``.`` are substituted by underscores. This feature can be switched off using the following export option: ``ExportConfigC(env, rename=False)``.

.. note::

  Not all features of DIP can be mapped to other languages.
  So far exports are implemented only for simple data types and arrays.
  If you are missing some advanced export feature, you are welcome to write a GitHub Issue or implement it yourself.

C configuration
~~~~~~~~~~~~~~~    

DIP parameters can be exported into a C header file in the following way:
    
.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigC
    >>> with ExportConfigC(env) as exp:
    >>>     exp.parse(
    >>>        guard='CONFIG_H',
    >>>        define=['radiation','simulation.name']
    >>>     )
    >>>     exp.save("config_c.h")
   
The header guard name can be modified. Parameters are parsed by default as constants ``const``, but it is also possible to parse them as preprocessor definitions ``#define``. If boolean DIP parameters are parsed, the corresponding C dependency ``<stdbool.h>`` is included.
   
.. literalinclude :: ../../_static/export_config/config_c.h
   :language: c
   :caption: config_c.h

.. note::

   Null values of DIP parameters parsed as preprocessor flags are omitted.

C++ configuration
~~~~~~~~~~~~~~~~~

In C++ configuration files, the DIP parameters are parsed by default as constant expressions ``constexpr``. Nevertheless, it is possible to parse them explicitly as constants ``const``, or preprocessor definitions ``#define``. Examples are shown below.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigCPP
    >>> with ExportConfigCPP(env) as exp:
    >>>     exp.parse(
    >>>        guard='CONFIG_H',
    >>>        define=['radiation','simulation.name'],
    >>>        const=['box.width','box.height']
    >>>     )
    >>>     exp.save("config_cpp.h")
   
.. literalinclude :: ../../_static/export_config/config_cpp.h
   :language: cpp
   :caption: config_cpp.h

.. note::

   In case of C++ there is no dependency ``<stdbool.h>`` included.

Fortran configuration
~~~~~~~~~~~~~~~~~~~~~  

In case of Fortran configuration, DIP variables are export in a separate module ``ConfigurationModule``. The name of the module can be modified.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigFortran
    >>> with ExportConfigFortran(env) as exp:
    >>>     exp.parse(module="ConfigurationModule")
    >>>     exp.save("config_fortran.f90")
   
.. literalinclude :: ../../_static/export_config/config_fortran.f90
   :language: fortran
   :caption: config_fortran.f90

Rust configuration
~~~~~~~~~~~~~~~~~~

Export of DIP parameters into a Rust configuration goes as follows.
Since Rust currently does not support 128 bit floats, all such parameters are exported as 64 bit variables.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigRust
    >>> with ExportConfigFortran(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_rust.rs")
   
.. literalinclude :: ../../_static/export_config/config_rust.rs
   :language: rust
   :caption: config_rust.rs

Bash configuration
~~~~~~~~~~~~~~~~~~  

Since Bash does not natively support multidimensional arrays, such data has to be exported using associative arrays, where keys are coordinates of corresponding values. Parameters with ``none`` values are exported as empty variables. An example of a Bash configuration export is given below.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigBash
    >>> with ExportConfigBash(env) as exp:
    >>>     exp.parse(export=True)
    >>>     exp.save("config_bash.sh")
   
.. literalinclude :: ../../_static/export_config/config_bash.sh
   :language: bash
   :caption: config_bash.sh

YAML configuration
~~~~~~~~~~~~~~~~~~  

Export into YAML uses ``yaml`` Python module.
In addition to all standard ``yaml`` options, it is also possible to show/hide parameter units. An example of an export is given below.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigYAML
    >>> with ExportConfigYAML(env) as exp:
    >>>     exp.parse(units=True, default_flow_style=True)
    >>>     exp.save("config_yaml.yaml")
   
.. literalinclude :: ../../_static/export_config/config_yaml.yaml
   :language: yaml
   :caption: config_yaml.yaml

TOML configuration
~~~~~~~~~~~~~~~~~~  

Export into TOML uses ``toml`` Python module.
In addition to all standard ``toml`` options, it is also possible to show/hide parameter units. An example of an export is given below.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigTOML
    >>> with ExportConfigTOML(env) as exp:
    >>>     exp.parse(units=True)
    >>>     exp.save("config_toml.toml")
   
.. literalinclude :: ../../_static/export_config/config_toml.toml
   :language: toml
   :caption: config_toml.toml

JSON configuration
~~~~~~~~~~~~~~~~~~

Export into JSON uses ``json`` Python module.
In addition to all standard ``json`` options, it is also possible to show/hide parameter units. An example of an export is given below.

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigJSON
    >>> with ExportConfigJSON(env) as exp:
    >>>     exp.parse(units=True, indent=2)
    >>>     exp.save("config_json.json")
   
.. literalinclude :: ../../_static/export_config/config_json.json
   :language: json
   :caption: config_json.json

