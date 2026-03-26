---
title: "SciNumTools2: A framework for unit-aware scientific computation and parameterized workflows in Python"
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

Scientific and engineering workflows frequently require the combination of numerical computation, unit-aware quantities, parameter management, and expression evaluation. While widely used libraries such as `NumPy` and `SciPy` provide efficient numerical primitives, they do not offer integrated support for higher-level workflow definition involving dimensional consistency, structured inputs, and symbolic-like expressions.

`SciNumTools2` is a Python framework designed to address this gap by providing a unified system for defining and executing scientific numerical workflows. It combines unit-aware computation, expression parsing, and structured parameter definition into a cohesive architecture, enabling users to build reproducible and physically consistent computational pipelines.

The framework is particularly suited for simulation setup, scientific prototyping, and engineering calculations where dimensional correctness and flexible parameterization are essential.

# Statement of need

Scientific software development often involves repeated implementation of common patterns:

- handling physical quantities with units and their conversion,
- defining structured input parameters,
- dynamically evaluating mathematical expressions,
- controlling numerical precision,
- validating parameters and ensuring dimensional consistency.

Existing tools typically address these challenges in isolation. For instance, unit-handling libraries such as Pint [@pint] provide robust dimensional analysis, while expression and parsing libraries (e.g., SymPy [@sympy] or asteval [@asteval]) focus on evaluating mathematical expressions. However, combining these capabilities into a cohesive, unit-aware workflow requires substantial additional effort and often leads to fragmented or ad hoc solutions.

`SciNumTools2` addresses this need by providing an integrated framework that combines:

- unit-aware numerical computation,
- extensible expression parsing,
- a domain-specific language `DIP` for parameter definition,
- domain-level abstractions for representing materials, compositions, and derived physical properties

This integration reduces boilerplate code and improves reproducibility by enforcing consistent handling of units and parameters throughout the workflow.

# Functionality and design

The architecture of `SciNumTools2` is organized into four core components:

## Unit-aware numerical system

The framework provides a system for representing and manipulating physical quantities with associated units. It supports:

- arithmetic operations with automatic unit propagation,
- unit conversion,
- compatibility with NumPy arrays,
- unit systems
- handling of uncertainties.

This enables physically consistent computations without requiring manual unit tracking.

## Expression evaluation engine

`SciNumTools2` includes an extensible expression parser capable of evaluating mathematical expressions involving variables, functions, and units. The system allows:

- dynamic evaluation of user-defined expressions,
- integration with the unit system,
- extensibility through custom operators and functions.

This component enables flexible definition of derived quantities within workflows.

## Dimensional Input Parameters (DIP)

A key feature of the framework is the introduction of **Dimensional Input Parameters (DIP)**, a lightweight domain-specific language for defining structured, unit-aware parameters. DIP supports:

- declarative parameter definitions,
- dimensional validation,
- parsing from textual representations,
- integration with expression evaluation.

This allows users to define complex input configurations in a concise and reproducible manner.

The DIP system extends beyond parameter definition by supporting tooling for interoperability and usability. This includes:

- exporting parameter definitions to other formats and languages,
- automatic generation of parameter documentation,
- syntax highlighting for improved readability and editing.

These features enable DIP to function not only as a parameter specification format, but as a lightweight domain-specific language for scientific workflows.

## Domain-level modeling utilities

The framework includes higher-level abstractions for representing domain-specific entities such as materials and compositions. These utilities build on the underlying unit and expression systems to enable:

- computation of derived physical properties,
- structured representation of scientific data,
- integration into larger computational workflows.

# Comparison with existing tools

`SciNumTools2` differs from existing libraries in its focus on integration rather than specialization.

- **Pint** [@pint] provides comprehensive unit handling but does not address structured parameter definition or expression-based workflows.
- General-purpose parsing libraries enable expression evaluation but lack awareness of physical units and scientific context.
- Configuration formats such as JSON, YAML [@yaml122] or TOML [@toml100] provide structured data storage but do not support dimensional validation or computation.

In contrast, `SciNumTools v2` combines these capabilities into a single framework, enabling users to define, validate, and evaluate scientific workflows in a unified environment.

# Example use case

A typical workflow using `SciNumTools2` involves:

1. Defining input parameters using DIP with associated units,
2. Parsing and validating these parameters,
3. Evaluating derived expressions involving physical quantities,
4. Performing computations with guaranteed dimensional consistency.

This approach is particularly useful in simulation pipelines, where input definitions, derived parameters, and computations must remain consistent and reproducible.

# Availability and reuse

`SciNumTools2` is implemented in Python and distributed via the Python Package Index (PyPI). The source code is openly available on GitHub under an OSI-approved license. Comprehensive documentation and usage examples are provided online.

The framework is designed to be modular and extensible, allowing users to integrate individual components or adopt the full system depending on their needs.

Future development includes a C++ reimplementation of the framework targeting high-performance computing (HPC) use cases. This next iteration aims to extend the core concepts of `SciNumTools2` to performance-critical environments while maintaining compatibility with the workflow design principles established in the Python version.

# Acknowledgements

The development of this project was motivated by practical needs in scientific computing workflows requiring consistent handling of units, parameters, and expressions.

# References
