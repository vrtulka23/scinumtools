About DIP
=========

DIP is a minimalistic programming language that specializes in parsing, managing and validation of dimensional initial parameters (DIP).
Numerical codes used in physics, astrophysics and engineering usually depend on sets of compilation definitions, flags and initial settings.
Description of these parameters is often poorly documented and codes are prone to errors due to wrong input units and lack of proper parameter validation.
DIP is designed to address these issues and provide a standardized and scalable interface between user and a code.
In the long run, DIP aims to become a standard tool for any numerical code and flatten the learning curve to end users.

The following features of DIP are already implemented in the current code version:

* parameter node definition, declaration and modification
* hierarchical structure of nodes
* value data types: boolean, integer, float, string
* parameter values: scalars, arrays, blocks and tables
* definitions of reference sources
* import of local/remote nodes
* injection of local/remote node values
* implements :ref:`solver/index:expression solver`
 
  * numerical for integer and float data types (with scalar values only)
  * logical for boolean data types
  * templates for string data types
* node values generated using functions from interpreter languages (Python,...)
* implements :ref:`units/index:physical units`
  
  * support for standard SI, CGS and AU units
  * definition of custom units
  * automatic unit conversion during node modifications
* parameter properties: options, conditions, format, constants, tags and description
* parameter branching using conditions
* syntax highlighter using "Pygments" in Sphinx and for Emacs editor
* documentation
    * extension for Sphinx
    * PDF format
* export of DIP parameters into C/C++, Fortran and Rust configuration files

The current version of DIP is continously developing.
Goals listed below are not implemented yet and need help from potential codevelopers:

* native implementation of DIP in C/C++, Fortran and Rust
* syntax highlighters for Vim and other code editors

Any kind of help, collaboration, suggestions and further development of this project is heartily welcomed.

DIP is published under MIT license. We kindly ask for a reference in projects that are based on this code.
