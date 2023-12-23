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

.. code-block:: DIP
    :caption: config.dip

    simulation
      name str = 'Configuration test'
      output bool = true
    box
      width float32 = 12 cm
        !tags ["selection"]
      height float = 15 cm
    density float128 = 23 g/cm3
    num_cells int = 100
      !tags ["selection"]
    num_groups uint64 = 2399495729

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
Exports are currently available for following languages:


.. csv-table::

    C,       ``ExportConfigC``
    C++,     ``ExportConfigCPP``
    Fortran, ``ExportConfigFortran``
    Rust,    ``ExportConfigRust``
    Bash,    ``ExportConfigBash``
    YAML,    ``ExportConfigYAML``
    TOML,    ``ExportConfigTOML``
    JSON,    ``ExportConfigJSON``

Since DIP parameter names are not suitable for all languages mentioned above.
In some cases parameter names are automatically converted to upper case and hierarchy separators ``.`` are substituted by underscores.

.. note::

  Not all features of DIP can be mapped to other languages.
  So far exports are implemented only for simple data types and arrays.
  If you are missing some advanced export feature, you are welcommed to write a GitHub Issue or implement it yourself.
    
C configuration
~~~~~~~~~~~~~~~    
    
.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigC
    >>> with ExportConfigC(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_c.h")
   
.. literalinclude :: ../../_static/export_config/config_c.h
   :language: c

C++ configuration
~~~~~~~~~~~~~~~~~
    
.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigCPP
    >>> with ExportConfigCPP(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_cpp.h")
   
.. literalinclude :: ../../_static/export_config/config_cpp.h
   :language: cpp

Fortran configuration
~~~~~~~~~~~~~~~~~~~~~  

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigFortran
    >>> with ExportConfigFortran(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_fortran.f90")
   
.. literalinclude :: ../../_static/export_config/config_fortran.f90
   :language: fortran

Rust configuration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigRust
    >>> with ExportConfigFortran(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_rust.rs")
   
.. literalinclude :: ../../_static/export_config/config_rust.rs
   :language: rust

Bash configuration
~~~~~~~~~~~~~~~~~~  

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigBash
    >>> with ExportConfigBash(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_bash.sh")
   
.. literalinclude :: ../../_static/export_config/config_bash.sh
   :language: bash

YAML configuration
~~~~~~~~~~~~~~~~~~  

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigYAML
    >>> with ExportConfigYAML(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_yaml.yaml")
   
.. literalinclude :: ../../_static/export_config/config_yaml.yaml
   :language: yaml

TOML configuration
~~~~~~~~~~~~~~~~~~  

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigTOML
    >>> with ExportConfigTOML(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_toml.toml")
   
.. literalinclude :: ../../_static/export_config/config_toml.toml
   :language: toml

JSON configuration
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    >>> from scinumtools.dip.config import ExportConfigJSON
    >>> with ExportConfigJSON(env) as exp:
    >>>     exp.parse()
    >>>     exp.save("config_json.json")
   
.. literalinclude :: ../../_static/export_config/config_json.json
   :language: json

