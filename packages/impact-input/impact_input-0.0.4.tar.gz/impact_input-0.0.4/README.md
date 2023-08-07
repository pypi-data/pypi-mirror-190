# ImpactIn
Python Class for managing IMPACT-Z/T input files. Includes the ability to read and write input files as well as replace string variables found within the file with numeric values.

## Installation

The class can be installed from PyPI, using the following command:

```bash
pip install impact_input
```

## Read in Input File

Reads in the input file specified by filename. Includes the ability to remove comments (i.e lines beginning with ! or anything occuring after a /) using exclude_comments. By default `exclude_comments = True`.

```python
from impact_input import ImpactIn

impact_file = ImpactIn(filename="ImpactT_original.in")
```

## Get all Variables

Returns a list of all variables found in the input file. Variable names cannot start with a number.

```python
impact_file.variables()
```

## Replace Variables with Values

Replace the list of variables with the numerical values in the respective order they appear in the list (e.g. gunPhaseF1 becomes 0 below).

```python
replace_var = ["gunPhaseF1","gunPhaseF2"]
val = [0,180]
impact_edit = impact_file.replace(varnames=replace_var,varvals=val)
```

## Write New Input File IMPACT

Write an input file with the specified filename. Note it is best practice to make the new file have a different name than the initial input so as not to overwite it. As the IMPACT-Z/T executables require the input file to be named "ImpactZ.in" or "ImpactT.in", the initial input file should have a name other than those two options.

```python
impact_edit.write(filename='ImpactT.in')
```

## Examples

Examples python scripts that use the ImpactIn class to run a phase scan and find the phase with the maximum energy gain for a RF gun can be found [here](Examples/).

