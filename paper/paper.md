---
title: "SciNumTools2: Unit-aware scientific computation and declarative parameter workflows in Python"
tags:
  - Python
  - scientific computing
  - numerical methods
  - units
  - domain-specific languages
authors:
  - name: Ondrej Pêgo Jaura
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 2026
bibliography: paper.bib
---

# Summary

Scientific and engineering computations frequently combine numerical operations, physical units, parameter definitions, and derived expressions. While libraries such as `NumPy` and `SciPy` provide efficient numerical primitives, they do not address how inputs are structured, validated, and evaluated in a unit-consistent workflow. To our knowledge, no existing Python framework provides declarative, unit-aware parameter graphs with integrated expression evaluation in a single execution model.

`SciNumTools2` is a Python framework that integrates unit-aware computation, expression evaluation, and declarative parameter definition into a single system. Its primary contribution is a unified abstraction that allows users to define scientific computations as structured, unit-aware parameter sets with automatically evaluated dependencies.

The framework is particularly suited for simulation setup, engineering calculations, and scientific prototyping, where dimensional correctness and reproducibility are required.

# Statement of need

Scientific software development often requires combining multiple independent tools:

- unit-handling libraries (e.g., Pint [@pint]),
- configuration formats (e.g., YAML [@yaml122], TOML [@toml100]),
- expression evaluators (e.g., SymPy [@sympy], asteval [@asteval]).

In practice, integrating these components requires additional code for:

- parsing and validating input parameters,
- enforcing dimensional consistency,
- evaluating derived quantities,
- maintaining reproducible configurations.

This leads to duplicated validation logic, inconsistent abstractions, and error-prone workflows. For example, combining YAML-based configuration with a unit library requires manual parsing and explicit validation of units and expressions, which is not handled by existing tools.

`SciNumTools2` addresses this gap by providing a unified framework in which parameter definition, unit handling, and expression evaluation are part of the same execution model.

# Functionality and design

The architecture of `SciNumTools2` consists of four integrated components.

## Unit-aware numerical system

The framework provides physical quantities with associated units, supporting:

- arithmetic operations with automatic unit propagation,
- runtime validation of dimensional consistency,
- unit conversion,
- compatibility with NumPy arrays,
- support for multiple unit systems.

Invalid operations (e.g., adding incompatible units) are detected during computation.

## Expression evaluation engine

An extensible expression parser allows evaluation of mathematical expressions involving variables, functions, and units. Features include:

- evaluation of user-defined expressions,
- integration with unit-aware quantities,
- extensibility via custom functions and operators.

This enables definition of derived quantities directly within parameter specifications.

## Dimensional Input Parameters (DIP)

`SciNumTools2` introduces **Dimensional Input Parameters (DIP)**, a lightweight domain-specific language for defining structured, unit-aware parameters with dependencies.

A minimal example:

```python
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
>>>     box.height = 2 m
>>>     """)
>>>     env = dip.parse()
>>>     env.data(Format.TUPLE)
{'box.width': (23.0, '[length]'), 'box.height': (200, 'cm'), 'sphere.radius': (34.2, 'mm')}
```
The parameter `box.height`, defined as `2 m`, is automatically converted to `200 cm` to match the internal representation, with dimensional consistency enforced during evaluation. Custom units (e.g., `[length]`) can be defined and used transparently within expressions. Parameters such as `sphere.radius` may reference values from both local definitions and external sources.

DIP supports:

- declarative parameter definitions,
- automatic dependency resolution,
- dimensional validation,
- parsing from text representations,
- integration with expression evaluation.

This removes the need for separate configuration parsing and validation logic.

## Domain-level modeling utilities

The framework provides higher-level abstractions for representing structured scientific entities such as materials and compositions. These build on the unit and expression systems to support:

- computation of derived physical properties,
- structured scientific data representation,
- integration into computational pipelines.
  
# Comparison with existing tools

Existing libraries address parts of the problem but do not provide an integrated workflow.

Pint [@pint] supports unit-aware computation but does not define how parameters are structured or evaluated.
SymPy [@sympy] and asteval [@asteval] evaluate expressions but are not designed for unit-aware parameter workflows.
Configuration formats such as YAML [@yaml122] and TOML [@toml100] provide structured data but lack dimensional validation and computation.

In contrast, `SciNumTools2` combines these capabilities into a single system where parameters, units, and expressions are defined and evaluated together. This reduces boilerplate code and ensures consistency across the workflow.

# Example use case

A typical workflow consists of:

Defining input parameters using DIP,
Parsing and validating parameters with units,
Evaluating derived expressions,
Performing computations with guaranteed dimensional consistency.

For example, in a simulation setup, derived quantities (e.g., area, density, or rates) can be defined directly in the parameter specification and automatically validated before execution.

# Availability and reuse

`SciNumTools2` is implemented in Python and distributed via the Python Package Index (PyPI). The source code is available on GitHub under an OSI-approved license, with documentation and usage examples provided online.

The framework is modular and can be used either as a complete workflow system or as individual components (e.g., unit handling or parameter evaluation).

# Acknowledgements

The development of this project was motivated by recurring challenges in scientific workflows involving unit consistency, parameter validation, and reproducibility.

# References
