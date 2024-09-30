import pandas as pd
from juliacall import Main as jl

# Wrapper for run_stage_two in Julia
def undid_stage_two(filepath, silo_name, silo_data, time_column, outcome_column, date_format, consider_covariates = True):
    """
    Wrapper for run_stage_two() from Undid.jl.
    Fills in the relevant cells from the empty_diff_df.csv and saves as filled_diff_df_$silo_name.csv.

    Parameters:
    ----------
    - filepath : str
        Filepath to the 'empty_diff_df.csv' file.
    - silo_name : str
        Name of the silo being analyzed, as it is written in the `empty_diff_df.csv`
    - silo_data : pandas.DataFrame
        DataFrame containing the data for the specific silo.
    - time_column : str
        Name of the column in `silo_data` that contains time values. Ensure this is a column of strings.
    - outcome_column : str
        Name of the column in `silo_data` that contains the outcome variable for the analysis.
    - date_format : str
        The format of the date used in the `time_column`. 
    - consider_covariates : bool, optional
        Whether to consider the covariates specified in the empty_diff_df.csv in the analysis. Defaults to True.
    """

    # Ensure Undid.jl is loaded
    jl.seval("using Undid")

    # Load DataFrames.jl in Julia
    jl.seval("using DataFrames")

    # Convert pandas DataFrame to Julia DataFrame
    jl.df = jl.DataFrame(silo_data.to_dict("list"))

    output = jl.Undid.run_stage_two(filepath, silo_name, jl.df, time_column, outcome_column, date_format, consider_covariates = consider_covariates)
    print(output[0][0])
    print(output[1][0])
    return output[0][1], output[1][1]
