Expression Solver
=================

In this section we describe basic functionality of the expression solver.
This tool has been implemented as a submodule in order to standardize solving of numerical expression in :ref:`units/index:physical units` and logical/numerical expressions in :ref:`dip/index:dimensional input parameters`.
Nevertheless, it can be easily modified and used in other projects that require some mathematical expressions.

Expression solver consist of following classes:

Solver

  Main class that runs the solver
  
Expression

  Expression class handles an expression string that is being parsed into tokens.
  
Tokens

  This class contains list of parsed expression tokens (atoms and operators).

Atom

  Class that specifies how data is parsed from atomic expressions and implements mathematical operations on the data.
 
Operators

  Each operator (e.g. addition, multiplication, logarithm....) is implemented as a separate class and performs corresponding operations with tokens.
  
Expression solver comes with already existing atom parser that can be used straight out of the box on basic numerical,

.. code-block::

   >>> from scinumtools.solver import *
   >>> with ExpressionSolver(AtomBase) as es:
   ...     es.solve("1 * ((2+3) / +3 - -10 ) + (-23 *++2) + 23**2")
   Atom(494.6666666666667)
   >>> 1 * ((2+3) / +3 - -10 ) + (-23 *++2) + 23**2
   494.6666666666667
   
comparisons and logical expressions.

.. code-block::

   >>> import numpy as np
   >>> with ExpressionSolver(AtomBase) as es:
   ...     es.solve("sin(23) < 1 && 3*2 == 6 || !(23 > 43) && cos(0) == 1")
   Atom(True)
   >>> np.sin(23) < 1 and 3*2 == 6 or not (23 > 43) and np.cos(0) == 1
   True

Atoms
^^^^^

Atom parser is a central part of every solver, because it converts atomic expression into specific data type and implements operations on the data. Default atom class implements parsing and operation on float numbers. Functionality of the atom can be easily modified, as shown in the example below.

.. code-block::

    >>> foo = 3
    >>> bar = 4
    >>> class Atom(AtomBase):
    >>>     def __init__(self, value:str):
    >>>         if value=='foo':
    >>>             self.value = foo
    >>>         elif value=='bar':
    >>>             self.value = bar
    >>>         else:
    >>>             self.value = float(value)
    >>> with ExpressionSolver(Atom) as es:
    >>>     es.solve('foo < bar && foo * bar == 12')
    Atom(True)
    >>> foo < bar and foo*bar==12
    True

Operators
^^^^^^^^^

List of available default operations is given in the table below. 

.. csv-table:: List of operators
   :widths: 30 30
   :header-rows: 1

   Operation,                Operators
   Addition,                 "unary +A and binary A+B"
   Subtraction,              "unary -A and binary A-B"
   Multiplication,           "A*B"
   Division,                 "A/B"
   Parenthesis,              "\(E\)"
   Exponential function,     "A**B, exp(E), powb(E1,E2)"
   Logarithmic functions,    "log(E), log10(E), logb(E1,E2)"
   Trigonometric functions,  "sin(E), cos(E), tan(E)"
   Equality,                 "A==B, A!=B, A<B, A>B, A<=B, A>=B"
   Logical operators,        "A&&B, A||B, !B"
   
Symbols ``A`` and ``B`` used in the table stand for atoms and ``E`` for expressions.

Operators can be easily overloaded or modified to match the need of your project.

.. code-block::

    >>> class CustomOperatorNot(OperatorNot):
    >>>     symbol: str = 'not'
    >>> operators = {'not':CustomOperatorNot}
    >>> with ExpressionSolver(AtomBase, operators) as es:
    >>>     es.solve('not 1')
    False

Operation steps
^^^^^^^^^^^^^^^

Decomposition of a string expression into tokens and subsequent action of operators on atoms is depicted in the figure below.

.. image:: ../_static/figures/operation_flow.png