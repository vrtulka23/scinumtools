# Generators

This set of scripts is used to automatically generate parts of codes and tables

## Example

``` bash
# run all generators
python3 tools/generators/generator.py

# run all scripts in a generator
python3 tools/generators/generator.py generate_docs

# run a specific generator script
python3 tools/generators/generator.py generate_docs::generate_temperature_units
```