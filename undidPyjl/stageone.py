import pandas as pd
from juliacall import Main as jl

# Wrapper for create_init_csv in Julia
def create_init_csv(silo_names=None, start_times=None, end_times=None, treatment_times=None, covariates=False):
    """
    Wrapper for create_init_csv() from Undid.jl.
    Creates the initial 'init.csv' file from which the 'empty_diff_df.csv' is built.

    Parameters:
    ----------
    - silo_names : list of str, optional
        List of silo names. Defaults to an empty list.
    - start_times : list of str, optional
        List of start times for each silo. Defaults to an empty list.
    - end_times : list of str, optional
        List of end times for each silo. Defaults to an empty list.
    - treatment_times : list of str, optional
        List of treatment times for each silo. Indicate control silos by setting treatment time for those silos to "control". Defaults to an empty list.
    - covariates : list of str or bool, optional
        Either a list of covariates or `False` to omit covariates. Defaults to False.
    """
    # Load the Undid package in Julia
    jl.seval("using Undid")
    
    # Convert pandas.Series to lists (ensures compatability with Julia)
    if isinstance(silo_names, pd.Series):
        silo_names = silo_names.tolist()
    if isinstance(start_times, pd.Series):
        start_times = start_times.tolist()
    if isinstance(end_times, pd.Series):
        end_times = end_times.tolist()
    if isinstance(treatment_times, pd.Series):
        treatment_times = treatment_times.tolist()
    if isinstance(covariates, pd.Series):
        covariates = covariates.tolist()
        
    # Handle args
    silo_names = silo_names if silo_names is not None else []
    start_times = start_times if start_times is not None else []
    end_times = end_times if end_times is not None else []
    treatment_times = treatment_times if treatment_times is not None else []
    covariates = covariates if covariates is not False else False

    # Ensure covariates are passed as a vector of strings to Julia
    jl.covariates = covariates
    if covariates is not False:
       jl.covariates = jl.seval("convert(Vector{String}, covariates)")


    # Call the create_init_csv function from the Undid package in Julia
    jl.Undid.create_init_csv(silo_names, start_times, end_times, treatment_times, covariates= jl.covariates, printmessage = True)

# Wrapper for create_diff_df in Julia
def create_diff_df(filepath, date_format, freq, covariates = False, freq_multiplier = False):
    """
    Wrapper for create_diff_df() from Undid.jl.
    Creates the initial 'empty_diff_df.csv' file to be sent to each silo.

    Parameters:
    ----------
    - filepath : str
        Filepath to the 'init.csv' file.
    - date_format : str
        The date format used in the 'init.csv' file.
    - freq : str
        Frequency of the data to be considered at each silo.
        Options are "daily", "weekly", "monthly", or "yearly".
    - covariates : list of str or bool, optional
        List of strings to specify covariates at each silo, or `False` to use covariates specified in 'init.csv'. Defaults to False.
    - freq_multiplier : int or bool, optional
        Integer to multiply the `freq` argument by. For example, if the data to be analyzed is in intervals of every 2 weeks, set `freq="weekly"` and `freq_multiplier=2`. Defaults to False.
    """

    # Convert covariates to list if entered as a pd.Series for some reason
    if isinstance(covariates, pd.Series):
        covariates = covariates.tolist()
    
    # Ensure covariates are passed as a vector of strings to Julia
    jl.covariates = covariates
    if covariates is not False:
       jl.covariates = jl.seval("convert(Vector{String}, covariates)")

    # Ensure Undid.jl is loaded
    jl.seval("using Undid")

    # Run Undid.jl function
    output = jl.Undid.create_diff_df(filepath, covariates = jl.covariates, date_format = date_format, freq = freq, freq_multiplier = freq_multiplier)
    return output

