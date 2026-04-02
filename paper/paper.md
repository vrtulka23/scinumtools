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

Scientific and engineering computations frequently combine numerical operations, physical units, parameter definitions, and derived expressions. While libraries such as `NumPy` and `SciPy` provide efficient numerical primitives, they do not address how inputs are structured, validated, and evaluated in a unit-consistent workflow. To our knowledge, there is no widely used Python framework that provides declarative, unit-aware parameter graphs with integrated expression evaluation in a single execution model.

`SciNumTools2` is a Python framework that integrates unit-aware computation, expression evaluation, and declarative parameter definition into a single system. Its primary contribution is a unified abstraction that allows users to define scientific computations as structured, unit-aware parameter sets with automatically evaluated dependencies.

The framework is particularly suited for simulation setup, engineering calculations, and scientific prototyping, where dimensional correctness and reproducibility are required.

# Statement of need

Scientific software development often requires combining multiple independent tools:

- unit-handling libraries,
- configuration formats,
- expression evaluators.

In practice, integrating these components requires additional code for:

- parsing and validating input parameters,
- documentation of the parameters,
- enforcing dimensional consistency,
- evaluating derived quantities,
- maintaining reproducible configurations.

This leads to duplicated validation logic, inconsistent abstractions, and error-prone workflows. For example, combining YAML-based configuration with a unit library typically requires manual parsing and explicit validation of units and expressions—tasks not handled by existing tools. As a result, scientists often spend significant time developing and testing their own input handling and validation code instead of focusing on the underlying scientific questions.

`SciNumTools2` addresses this gap by providing a unified framework in which parameter definition, unit handling, and expression evaluation are integrated into a single execution model. This approach enables scientists to move quickly and safely past the initial hurdles of parameter definition, validation, and documentation, allowing them to concentrate on solving physics or engineering problems.

# State of the field

Existing tools address individual aspects of scientific parameter handling but do not provide an integrated, unit-aware workflow combining structured parameter definition, dependency resolution, and expression evaluation.

Unit libraries such as **Pint** [@pint] and **astropy.units** [@astropy2013] support dimensional computation but operate at the level of numerical values rather than structured parameter systems. Expression tools such as **SymPy** [@sympy] enable evaluation of mathematical expressions but are not designed for unit-aware parameter workflows.

Configuration formats such as **YAML** [@yaml122] and **TOML** [@toml100], along with frameworks like **Hydra** [@hydra], provide structured and composable parameter definitions, but treat data as static and lack native support for units, expression evaluation, and dimensional validation.

Frameworks such as **OpenMDAO** [@openmdao2019] come closest to integrating parameter dependencies with unit-aware computation, but target large-scale optimization workflows and impose a heavier, model-centric architecture.

In practice, scientific applications combine multiple such tools, requiring additional glue code for parsing, validation, and evaluation. `SciNumTools2` addresses this gap by providing a unified, declarative system in which parameters, units, and expressions are defined and evaluated together with automatic dependency resolution and dimensional consistency.

The decision to develop a new framework rather than extend existing tools is motivated by this integration gap: current libraries operate at different abstraction levels and do not provide a cohesive model for unit-consistent parameter workflows.

# Software design

The architecture of `SciNumTools2` consists of four integrated components: the **Expression Solver** (EXS), **Physical Units & Quantities** (PUQ), the **Dimensional Input Parameter** (DIP) parser, and the **Material Properties** (MAT) solver. At its core is the general-purpose EXS engine, which is utilized across all other components. The PUQ and MAT modules can operate as standalone tools or be seamlessly integrated within the DIP parser.

## Expression solver (EXS)

An extensible expression parser allows evaluation of mathematical expressions involving variables, functions, and units. Features include:

- evaluation of user-defined expressions,
- integration with unit-aware quantities,
- extensibility via custom functions and operators.

This enables definition of derived quantities directly within parameter specifications.

## Physical Units & Quantities (PUQ)

The framework provides physical quantities with associated units, supporting:

- arithmetic operations with automatic unit propagation,
- runtime validation of dimensional consistency,
- unit conversion,
- compatibility with NumPy arrays,
- support for multiple unit systems.

Invalid operations (e.g., adding incompatible units) are detected during computation.

## Dimensional Input Parameters (DIP)

`SciNumTools2` introduces **Dimensional Input Parameters (DIP)**, a lightweight domain-specific language for defining structured, unit-aware parameters with dependencies.

DIP provides declarative parameter definitions, automatic dependency resolution, dimensional validation, parsing from text representations, and integration with expression evaluation. By unifying these capabilities, it eliminates the need for separate configuration parsing and validation layers in scientific codes, reducing complexity and potential errors.

A minimal example is shown below: the first file defines parameters using DIP syntax, and the second demonstrates parsing and access in Python.

**settings.dip**
```dip
box
  size float = 94.3 cm            # define box size
  volume float = ("pow( {?box.size}, 3)") cm3  # derive box volume
    !condition ("{?} < 0.85 m3")  # constrain maximum volume
  num_spheres int = 245           # define number of spheres
sphere
  density float = 30.4 kg/m3      # set material density
    !constant                     # density must stay constant
  volume float = ("{?box.volume} / {?box.num_spheres} / 2") cm3 # derive volume of a single sphere
  mass float = ("{?sphere.density} * {?sphere.volume}") kg      # get mass of a single sphere
```

Note that the settings allow both the definition of primitive parameters and the use of expressions to derive dependent ones.

**main.py**
```python
>>> from scinumtools.dip import DIP, Format
>>> 
>>> with DIP() as dip:
>>>     dip.add_source("settings", "settings.dip")  # add an external source
>>>     dip.add_string("""                          # add some more DIP code
>>>     system
>>>       # import number of spheres
>>>       {settings?box.num_spheres}
>>>       # calculate mass in gramms
>>>       total_mass float = (" {settings?sphere.mass} * {?system.num_spheres} ") g
>>>     """)
>>>     env = dip.parse()                 # parse DIP code
>>>     data = env.data(Format.QUANTITY)  # extract parameters in a dictionary
>>> 
>>> print("Number of spheres:", data['system.num_spheres'])
>>> print("Total mass:       ", data['system.total_mass'].to('kg'))  # convert to kg
Number of spheres: Quantity(2.450e+02)
Total mass:        Quantity(1.275e+01 kg)
```

The parsing interface accepts multiple DIP sources, provided either as strings or files, and produces a dictionary of normalized, validated parameters for downstream use.

## Material Properties (MAT)

The framework provides higher-level abstractions for representing structured scientific entities such as elements, substances and materials and their corresponding compositions. These build on the unit and expression systems to support:

- computation of derived physical properties,
- structured scientific data representation,
- integration into computational pipelines.
  
## Example use case

A typical workflow with `SciNumTools2` involves defining input parameters using the DIP component, parsing and validating these parameters together with their physical units, evaluating derived expressions, and performing computations with guaranteed dimensional consistency.

In a representative simulation setup, derived quantities (e.g., area, density, or rates) can be specified directly within the parameter definitions. These quantities are then automatically evaluated and validated prior to execution, reducing the risk of unit inconsistencies and runtime errors.

`SciNumTools2` is implemented in Python and distributed via the Python Package Index (PyPI). The source code is publicly available on GitHub under an OSI-approved license, with accompanying documentation and usage examples provided online.

The framework follows a modular design: it can be used as an integrated workflow system or as a set of independent components, such as for unit handling, expression evaluation, or parameter parsing.

# Research impact statement

The software implements core abstractions for dimensional input parameter handling and physical unit-aware computations, aimed at improving robustness and clarity in scientific simulation workflows. These concepts have been applied by the author in a number of astrophysical simulation studies, where they supported the consistent handling of physical quantities across complex parameter spaces. Related approaches have also been explored in plasma physics simulation contexts, including fusion and laser–matter interaction scenarios, further motivating the generality of the design.

While these initial applications were based on earlier, non-public implementations (v1), they informed the design of the present, consolidated framework (v2). The current version generalizes these ideas into a reusable and well-documented software package, with explicit support for reproducible workflows and transparent handling of units and parameters.

The project is developed as an open-source tool with a modular architecture, documented examples, and test coverage to facilitate independent use. Initial external contributions and repository activity indicate emerging interest, and the software is structured to support broader adoption in computational research settings where dimensional consistency and parameter management are critical.

# AI usage disclosure

No generative AI tools were used in the implementation of the software itself; all source code was written by the author. Generative AI tools were used in a limited supporting role, including (i) identifying relevant coding standards and software design practices, (ii) polishing and improving the clarity of the manuscript text, and (iii) providing illustrative code examples for exploration. All AI-assisted outputs were carefully reviewed, validated, and, where necessary, revised by the author to ensure correctness, consistency, and alignment with the scientific and technical goals of the project.

# Acknowledgements

The development of this project was motivated by recurring challenges in scientific workflows involving unit consistency, parameter validation, and reproducibility.

# References
