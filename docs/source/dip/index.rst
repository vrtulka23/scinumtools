Dimensional Input Parameters
============================

.. image:: ../_static/logo/dip_logo_128.png

"Make your code tastier and serve your parameters with a nice DIP!"

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   intro/index
   syntax/index
   parsing/index
   export/index
   docs/index
   highlighters/index

Welcome to DIP documentation!

DIPSL, or shorter DIP, is a serialization language for dimensional input parameters.

DIP was specifically designed as a parameter parser for massive parallel codes used in physics, mathematics and engineering that are mostly written in C/C++ and Fortran. Such codes require parameter input of multiple quantities and compilation flags with precisely defined variable types and physical units. In large projects, this can get quickly messy and confusing. Especially when code requires setting parameters using several different, code specific (C/C++ pre-processor constants, Bash/Shell environmental variables, CSV and data tables, or JSON, YAML, TOML and similar), notations and adjustable units.

Using DIP dimensions, data types and options of parameters are explicitly defined, validated and converted into proper numerical values used by a code.

The most notable features of this language are:

- Explicit definitions of parameter data types and units

  .. code-block:: DIP

     weight float = 56 kg
     velocity float = 1.78 km/s

- Hierarchical parameter structure

  .. code-block:: DIP

     human                  # indentation
       head
         nose int = 1
     human.head.eye int = 2 # path
       
- Multiple modifications of parameters

  .. code-block:: DIP

     dimensions int = 1  # definition
     dimensions = 2      # modification 1
     dimensions = 3      # modification 2

- Automatic unit conversion from modification units into definition units

  .. code-block:: DIP

     energy float = 3 J
     energy = 4 erg

     # energy = 4e-7 J

- Explicit definition of parameter options and their properties

  .. code-block:: DIP

     geometry int = 1
       = 1  # line
       = 2  # plane
       = 3  # volume

- Inclusion of parameter values and nodes from local and external sources

  .. code-block:: DIP

     $source wines = ./wines.txt
     $source veggies = ./vegetables.dip
		  
     fruits int = 2
     basket
       pear int = {?fruits}
       wine table = {wines}
       {veggies?legumes.*}

- Conditional serialization of parameters

  .. code-block:: DIP

     source bool = true     
     @case ('{?source}')
        intensity float = 23 W/m2
     @else
        intensity float = none

- Custom unit definition

  .. code-block:: DIP

     units str = 'cgs'
     @case ("{?units} == 'cgs'")
       $unit length = 1 cm
       $unit mass = 1 g
       $unit time = 1 s
     @case ("{?units} == 'mks'")
       $unit length = 1 m
       $unit mass = 1 kg
       $unit time = 1 s
     @end
     energy float = 1 [mass]*[length]2/[time]2

- Modularization of parameter files and parameter search

  .. code-block:: python

        >>> from scinumtools.dip import DIP, Environment
        >>>	  
        >>> with DIP() as p:
        >>>     p.add_string("""
        >>> laser
        >>>   intensity float = 1e25 W/m2
        >>>     """)
        >>>     p.add_file('radiation.dip')
        >>>     p.add_file('gravitation.dip')
        >>> 
        >>> laser_settings = p.nodes.query('laser.*')
        >>> radiation_pressure = p.nodes.query('radiation.pressure')
	 
- Template parsing (e.g. producing of pre-processor flag parameter files)
- Support of tabular data input (e.g. CSV format or similar)

and many others...

DIP was created as a side project and does not have any particular development team. Any kind of help or support is highly appreciated.
