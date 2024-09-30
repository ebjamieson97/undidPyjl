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

### Utility Functions: For managing the Undid.jl package for Julia from Python

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
  List of treatment times for each silo. Set treatment time to "control" for silos which never receive treatment. Defaults to an empty list.

- **covariates** (*list of str or bool, optional*):  
  Either a list of covariates to include in the analysis or `False` to omit covariates. Defaults to `False`.

#### Example
```python
from undidPyjl import stageone as stageone
stageone.create_init_csv(silo_names = ["71", "73"], 
start_times = ["1989","1989"],
end_times = ["2000","2000"], 
treatment_times = ["1991","control"])
```

#### 4. `create_diff_df()` - Returns a filepath and a Julia dataframe
Generates the `empty_diff_df.csv` file. The `empty_diff_df.csv` file is sent to each silo in order to be filled out.

Covariates may be specified when calling `create_init_csv()` or when calling `create_diff_df()`.

**Parameters:**

- **filepath** (*str*):  
  Filepath to the `init.csv` file that was previously created.

- **date_format** (*str*):  
  The date format used in the `init.csv` file (e.g., `"YYYY-MM-DD"` for all possible formats see [here](#valid-date-formats)).

- **freq** (*str*):  
  Frequency of the data to be considered for analysis at each silo. Options are `"daily"`, `"weekly"`, `"monthly"`, or `"yearly"`.

- **covariates** (*list of str or bool, optional*):  
  A list of strings specifying covariates for each silo, or `False` to use the covariates specified in the `init.csv` file. Defaults to `False`.

- **freq_multiplier** (*int or bool, optional*):  
  An integer to multiply the `freq` argument by, to handle intervals larger than the base frequency. For example, for biweekly data, set `freq="weekly"` and `freq_multiplier=2`. Defaults to `False`.

#### Example 
```python
from undidPyjl import stageone as stageone
stageone.create_diff_df("c:\\Users\\User\\Documents\\Project Files\\init.csv",
date_format = "yyyy", freq = "yearly")
```

## Stage Two: Silo

#### 5. `undid_stage_two()` - Prints filepaths and returns Julia dataframes
The `undid_stage_two()` function uses date information from the `empty_diff_df.csv` and the local silo data to fill in the necessary diff_estimates.

Ensure that the `local_silo_name` reflects the spelling of the silo in the `empty_diff_df.csv` file. Likewise, ensure that the covariates specified in the `empty_diff_df.csv` are spelled the same in the local silo data.

Also be sure that the `time_column` contains only `string` values. This is in order to enable passing data back and forth between Julia and R. 

**Parameters:**

- **filepath** (*str*):  
  Filepath to the `empty_diff_df.csv` file.

- **silo_name** (*str*):  
  Name of the silo being analyzed, as it is spelled in the `empty_diff_df.csv`.

- **silo_data** (*pandas.DataFrame*):  
  A pandas DataFrame containing the data for the specific silo.

- **time_column** (*str*):  
  The name of the column in `silo_data` that contains date values. This column should contain date strings whose format is specified by `date_format`.

- **outcome_column** (*str*):  
  The name of the column in `silo_data` that contains the outcome variable for the analysis.

- **date_format** (*str*):  
  The format of the dates in the `time_column` (e.g., `"YYYY/MM/DD"`).

- **consider_covariates** (*bool, optional*):  
  Whether to consider the covariates specified in the `empty_diff_df.csv` during the analysis. Defaults to `True`. Consider setting to `False` if the specified covariates do not exist in the local silo data.

#### Example
```python
import pandas as pd
from undidPyjl import stagetwo as stagetwo
local_silo_data = pd.read_stata("C:\\Users\\User\\Local Data\\State71.dta")
filepath = "C:\\Users\\User\\Downloads\\empty_diff_df.csv"
stagetwo.undid_stage_two(filepath = filepath, silo_name = "71",
silo_data = local_silo_data, time_column = "year", outcome_column = "coll",
date_format = "yyyy") 
```

## Stage Three: Analysis

#### 6. `undid_stage_three()` - 

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

