# undidPyjl
Difference-in-differences for unpoolable data. Python wrapper for Undid.jl.

## Installation
**Option 1 (recommended): Install from [PyPI](https://pypi.org/project/undidPyjl/)**
```bash
pip install undidPyjl
```

**Option 2: Install from GitHub**
```bash
git clone https://github.com/ebjamieson97/undidPyjl.git
cd undidPyjl
python setup.py install
```

## Requirements
- Julia >= 1.0
- Python >= 3.6
- juliacall >= 0.9.20
- pandas >=1.2.4, <2.0
- numpy >=1.20.3, <1.23.0
- matplotlib >=3.4.0, <3.6

### Utility Functions: For managing the Undid.jl package for Julia from Python.

#### 1. `checkundidversion()`
Checks the version of Undid.jl currently installed in Julia. If it is not installed, installs the most recent version from https://github.com/ebjamieson97/Undid.jl.

#### Example
```python
from undidPyjl import julia_management as jlmg
jlmg.checkundidversion()
```

#### 2. `updateundid()`
Updates Undid.jl to the latest version. This may take a minute or so depending on network and system conditions.

#### Example 
```python
from undidPyjl import julia_management as jlmg
jlmg.updateundid()
```

## Stage One: Initialize

#### 3. `create_init_csv()` - Prints out a filepath to the created `init.csv`
Creates the initial 'init.csv' file from which the 'empty_diff_df.csv' is built. If `create_init_csv()` is called without providing any silo names, start times, end times, or treatment times, an `init.csv` will be created with the appropriate column headers and blank columns. 

Covariates may be specified when calling `create_init_csv()` or when calling `create_diff_df()`.

Ensure that dates are all entered in the same date format, a list of acceptable date formats can be seen [here.](#valid-date-formats)

**Parameters:**

- **silo_names** (*list of str, optional*):  
  List of silo names. Defaults to an empty list.
  
- **start_times** (*list of str, optional*):  
  List of start times for each silo. Defaults to an empty list.

- **end_times** (*list of str, optional*):  
  List of end times for each silo. Defaults to an empty list.

- **treatment_times** (*list of str, optional*):  
  List of treatment times for each silo. Set treatment time to "control" for silos acting as controls. Defaults to an empty list.

- **covariates** (*list of str or bool, optional*):  
  Either a list of covariates to include in the analysis or `False` to omit covariates. Defaults to `False`.

#### Example
```python
from undidPyjl import stageone as stageone
stageone.create_init_csv(["QC", "ON"], ["2000","2000"], ["2019","2019"], ["control","2010"])
```

## Appendix

#### Valid Date Formats
- `ddmonyyyy` → 25aug1990
- `yyyym00` → 1990m8
- `yyyy/mm/dd` → 1990/08/25
- `yyyy-mm-dd` → 1990-08-25
- `yyyymmdd` → 19900825
- `yyyy/dd/mm` → 1990/25/08
- `yyyy-dd-mm` → 1990-25-08
- `yyyyddmm` → 19902508
- `dd/mm/yyyy` → 25/08/1990
- `dd-mm-yyyy` → 25-08-1990
- `ddmmyyyy` → 25081990
- `mm/dd/yyyy` → 08/25/1990
- `mm-dd-yyyy` → 08-25-1990
- `mmddyyyy` → 08251990
- `mm/yyyy` → 08/1990
- `mm-yyyy` → 08-1990
- `mmyyyy` → 081990
- `yyyy` → 1990

