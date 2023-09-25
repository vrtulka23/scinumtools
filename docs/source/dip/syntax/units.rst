Units
=====

Parsing of units in DIP and their conversion shares basic principles with `The Physical Markup Language <http://web.mit.edu/mecheng/pml/spec_measure.htm>`_ and adopts similar unit nomenclature (case-sensitive) as described in `The Unified Code for Units of Measure <https://ucum.org/ucum>`_.

Each node has default units assigned at definition, or declaration.
Subsequent modification without given units assume to be in default units.
Values of modifications with different units (but same dimension) are converted to default units.

.. code-block:: DIP

   # definitions
   age int = 30 a
   height float = 185 cm
   weight float = 80 kg

   # modifications
   age = 35
   height = 190 cm      
   weight = 90000 g

   # Modified values:
   #
   # age = 35 a
   # height = 190 cm
   # weight = 90 kg

Base units
----------
   
**Quantities** in DIP are defined by a floating point numerical value (NV) and a measure array (MSR) with powers of base units.
A list of base units and their corresponding NV/MSR is summarized in the table below.
   
.. csv-table:: Base units
   :widths: 10 20 6 30
   :header-rows: 1

   Symbol, Description,  NV,      MSR
   1e,     power-of-ten, ``1.0``, "``[1,0,0,0,0,0,0,0,0]``"
   m,      meter,        ``1.0``, "``[0,1,0,0,0,0,0,0,0]``"
   g,      gram,         ``1.0``, "``[0,0,1,0,0,0,0,0,0]``"
   s,      second,       ``1.0``, "``[0,0,0,1,0,0,0,0,0]``"
   K,      Kelvin,       ``1.0``, "``[0,0,0,0,1,0,0,0,0]``"
   C,      Coulomb,      ``1.0``, "``[0,0,0,0,0,1,0,0,0]``"
   cd,     candela,      ``1.0``, "``[0,0,0,0,0,0,1,0,0]``"
   mol,    mole,         ``1.0``, "``[0,0,0,0,0,0,0,1,0]``"
   rad,    radian,       ``1.0``, "``[0,0,0,0,0,0,0,0,1]``"

Dimension of a quantity
  is determined by all but first (i.e. power-of-ten) MRS values.

Dimensional quantities
  | can have arbitrary powers in MRS.
  | e.g. MSR of 1 Newton is ``[3,1,1,-2,0,0,0,0,0]``

Dimensionless quantities
  | have all powers of MSR zero, except powers-of-ten.
  | e.g. MSR of :math:`10^{-3}` is ``[-3,0,0,0,0,0,0,0,0]``

Prefixes
--------
  
All dimensional units can be raised to the power-of-ten using explicit notation ``1e3*m`` or standard prefix notation ``km``.
A list of all supported prefixes with their corresponding NV and MRS is given in table below.

.. csv-table:: Unit prefixes
   :widths: 8 10 10 8 30
   :header-rows: 1

    Symbol, Description, Definition, NV,      MRS
    Y,      yotta,       1e24,       ``1.0``, "``[ 24, 0, 0, 0, 0, 0, 0, 0, 0]``" 
    Z,      zetta,	 1e21,       ``1.0``, "``[ 21, 0, 0, 0, 0, 0, 0, 0, 0]``"
    E,      exa,  	 1e18,       ``1.0``, "``[ 18, 0, 0, 0, 0, 0, 0, 0, 0]``"
    P,      peta, 	 1e15,       ``1.0``, "``[ 15, 0, 0, 0, 0, 0, 0, 0, 0]``"
    T,      tera, 	 1e12,       ``1.0``, "``[ 12, 0, 0, 0, 0, 0, 0, 0, 0]``"
    G,      giga, 	 1e9,        ``1.0``, "``[  9, 0, 0, 0, 0, 0, 0, 0, 0]``"
    M,      mega, 	 1e6,        ``1.0``, "``[  6, 0, 0, 0, 0, 0, 0, 0, 0]``"
    k,      kilo, 	 1e3,        ``1.0``, "``[  3, 0, 0, 0, 0, 0, 0, 0, 0]``"
    h,      hecto,	 1e2,        ``1.0``, "``[  2, 0, 0, 0, 0, 0, 0, 0, 0]``"
    da,     deka, 	 1e1,        ``1.0``, "``[  1, 0, 0, 0, 0, 0, 0, 0, 0]``"
    d,      deci, 	 1e-1,       ``1.0``, "``[ -1, 0, 0, 0, 0, 0, 0, 0, 0]``"
    c,      centi,	 1e-2,       ``1.0``, "``[ -2, 0, 0, 0, 0, 0, 0, 0, 0]``"
    m,      milli,	 1e-3,       ``1.0``, "``[ -3, 0, 0, 0, 0, 0, 0, 0, 0]``"
    u,      micro,	 1e-6,       ``1.0``, "``[ -6, 0, 0, 0, 0, 0, 0, 0, 0]``"
    n,      nano, 	 1e-9,       ``1.0``, "``[ -9, 0, 0, 0, 0, 0, 0, 0, 0]``"
    p,      pico,	 1e-12,      ``1.0``, "``[-12, 0, 0, 0, 0, 0, 0, 0, 0]``"
    f,      femto,	 1e-15,      ``1.0``, "``[-15, 0, 0, 0, 0, 0, 0, 0, 0]``"
    a,      atto, 	 1e-18,      ``1.0``, "``[-18, 0, 0, 0, 0, 0, 0, 0, 0]``"
    z,      zepto,	 1e-21,      ``1.0``, "``[-21, 0, 0, 0, 0, 0, 0, 0, 0]``"
    y,      yocto,       1e-24,      ``1.0``, "``[-24, 0, 0, 0, 0, 0, 0, 0, 0]``"
		 
Derived units
-------------

As already mentioned in previous chapter, units are fourth type of expressions in DIP.
They play a prominent role in DIP in comparison to other three expressions (logical, numerical and templates), because they are directly integrated into node definitions.
In this section, we closely describe how they are formed and used in DIP.

So far we described base units and their most simple derivates using prefixes.
It is, however, possible to derive new units from already existing units using the following operators.

.. csv-table:: Unit operators
   :widths: 10 20 30
   :header-rows: 1

   Operator,  Example,             Description
   PU,        ``km``,              unit U with a prefix P
   Up,        "``s-1``, ``rad2``", unit U raised on a power of integer number p
   U*U,       ``N*m``,             multiplication of two units U
   N*U,       ``1e3*m``,           multiplication of a unit U and a real number N
   U/U,       ``J/s``,             division of two units U
   N/U,       ``1e3/m``,           division of a unit U and a real number N
   (<expr>),  ``kg*(m2/s2)``,      parenthesis operator with an expression

Multiple operators can be combined into a single expression.
Expressions are written in close form and thus cannot consist of empty spaces.

.. code-block:: DIP
   
   pressure  float = 101   Pa
   distance  float = 123   km
   velocity  float = 60    km/h
   energy    float = 234   kg*(m2/s2)
   potential float = 8.3e2 kg*(m2/(s2*C))

MRS of derived quantities is simply a sum (when units are multiplied) or difference (when units are divided) of progenitor's MRS. NVs are correspondingly multiplied, or divided and rebased to the power-of-ten.
Powers of units multiply values of MRS, calculate power of NV and rebase it to the power-of-ten.

.. note::

   Some natural, dimensionless and custom units have symbols wrapped in square brackets (e.g. ``[c]`` or ``[m_p]``).
   This is to ensure that their notation does not coincide with symbols of standard units.

In the table below, we summarize all derived units that can be used in DIP.
Both base and derived units can be used in combination with prefixes and can serve as progenitors in unit expressions.
   
.. csv-table:: Derived SI units
   :widths: 10 20 30
   :header-rows: 1

   Symbol,     Description,           Definition
   "sr",       "steradian",           "rad2"            
   "Hz",       "hertz",               "s-1"             
   "N",        "newton",              "kg*m/s2"         
   "Pa",       "pascal",              "N/m2"            
   "J",        "joule",               "N*m"             
   "W",        "watt",                "J/s"             
   "A",        "ampere",              "C/s"             
   "V",        "volt",                "J/C"             
   "F",        "farad",               "C/V"             
   "Ohm",      "ohm",                 "V/A"             
   "S",        "siemens",             "Ohm-1"           
   "Wb",       "weber",               "V*s"             
   "T",        "tesla",               "Wb/m2"           
   "H",        "henry",               "Wb/A"            
   "lm",       "lumen",               "cd*sr"           
   "lx",       "lux",                 "lm/m2"           
   "Bq",       "becquerel",           "s-1"             
   "Gy",       "gray",                "J/kg"            
   "Sv",       "sivert",              "J/kg"
		 
.. csv-table:: Derived CGS units
   :widths: 10 20 30
   :header-rows: 1

   Symbol,     Description,           Definition
   "dyn",      "dyne",                "g*cm/s2"         
   "erg",      "erg",                 "dyn*cm"
   "G",        "Gauss",               "1e-4*T"
   
.. csv-table:: Other derived units
   :widths: 10 20 30
   :header-rows: 1

   Symbol,     Description,           Definition
   "deg",      "angle degree",        "2*[pi]*rad/360"   
   "'",        "angle minute",        "deg/60"           
   "''",       "angle second",        "'/60" 
   "l",        "liter",               "dm3"             
   "L",        "liter",               "l"               
   "ar",       "are",                 "100*m2"          
   "min",      "minute",              "60*s"            
   "h",        "hour",                "60*min"          
   "d",        "day",                 "24*h"            
   "a_t",      "tropical year",       "365.24219*d"     
   "a_j",      "Julian year",         "365.25*d"        
   "a_g",      "Gregorian year",      "365.2425*d"      
   "a",        "year",                "a_j"             
   "eV",       "electronvolt",        "[e]*V"           
   "au",       "astr. unit",          "149597.870691*Mm"
   "AU",       "astr. unit",          "au"                

.. csv-table:: Natural units
   :widths: 10 20 30
   :header-rows: 1

   Symbol,     Description,           Definition
   "[c]",      "velocity of light",   "299792458*m/s"           
   "[h]",      "Planck const.",       "6.6260755e-34*J*s"      
   "[k]",      "Boltzmann const.",    "1.380658e-23*J/K"       
   "[eps_0]",  "permit. of vac.",     "8.854187817e-12*F/m"    
   "[mu_0]",   "permeab. of vac.",    "4*[pi]*1e-7*N/A2"       
   "[e]",      "elem. charge",        "1.60217733e-19*C"       
   "[m_e]",    "electron mass",       "9.1093897e-28*g"        
   "[m_p]",    "proton mass",         "1.6726231e-24*g"        
   "[G]",      "grav. const.",        "6.67259e-11*m3/(kg*s2)" 
   "[g]",      "grav. accel.", 	      "9.80665*m/s2"           
   "atm",      "atm. pressure",	      "101325*Pa"              
   "ly",       "light-year",          "[c]*a_j"

.. csv-table:: Dimensionless units
   :widths: 10 20 30
   :header-rows: 1

   Symbol,     Description,           Definition
   "[pi]",     "pi",                  "3.141593"    
   "[euler]",  "Euler's num.",        "2.718282"    
   "[N_A]",    "Avogadro's num.",     "6.022137e23" 
   "%",        "percent",             "1e-2"        
   "[ppth]",   "promile",             "1e-3"        

Custom units
------------

Similarly as in case of references, it is also possible to define new units directly in the DIP code. This can be achieved by a special node directive ``$unit``.

.. code-block:: DIPSchema
   :caption: Schema of a custom unit definition
	     
   <indent>$unit <name> = <value> <unit>  # if value is a number
   <indent>$unit <name> = <value>         # if value is reference, or expression

Names of the custom units are automatically wrapped into square brackets.
If the name of a custom unit is already used, the code will raise an error.

.. code-block:: DIP

   $unit mass = 30 AU
   $unit length = 10 pc
   $unit time = 1 Gy

   velocity float = 2 [length]/[time]
   density float = 34 [mass]/[lenght]3

Units can also be defined outside the code using ``DIP::add_unit()`` method before code is parsed:

.. code-block:: python

   with DIP() as dip:
       dip.add_unit("length", 1, "m")
       dip.from_string("""
       width float = 23 [length]
       """)
       env = dip.parse()
