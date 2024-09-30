import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.colors as mcolors
from juliacall import Main as jl
from datetime import datetime, date
# Wrapper for run_stage_three in Julia
def undid_stage_three(dir_path, agg = "silo", covariates = False, save_csv = False, interpolation = False):
    """
    Wrapper for run_stage_three() from Undid.jl.

    Parameters:
    ----------
    - dir_path : str
        A string filepath to the folder containing all of the 'filled_diff_df.csv' files.
    - agg : str, optional
        A string specifying the aggregation method. Options are:
        "silo" (default), "g", or "gt".
    - covariates : bool, optional
        A logical value indicating whether to consider covariates in the analysis. Defaults to False.
    - save_csv : bool, optional
        A logical value indicating whether to save the 'combined_diff_df.csv' file. Defaults to False.
    - interpolation : str or bool, optional
        Takes either False or "linear_function" to handle missing values in the 'filled_diff_df.csv' files. 
        Defaults to False.
    """
    # Ensure Undid.jl is loaded
    jl.seval("using Undid")

    return jl.Undid.run_stage_three(dir_path, agg = agg, covariates = covariates, save_all_csvs = save_csv, interpolation = interpolation)

def plot_parallel_trends(dir_path, covariates = False, save_csv = False, combine = False,
    figsize = (10,5), control_colour = ["#D3D3D3", "#4D4D4D"], treated_colour = ["#F08080", "#800020"],
    control_color = None, treated_color = None, linewidth = 2, title = None, xlabel = None, ylabel = None,
    title_fontdict = None, title_loc = "center", title_pad = None, xlabel_fontdict = None, ylabel_fontdict = None,
    xlabel_pad = None, ylabel_pad = None, ylim = None, yticks = None, yticksize = 10,
    xticks = None, xticksize = 10, date_format = "%Y", legend_loc = 'best', legend_fontsize = 12, legend_on = True,
    treatment_indicator_col = "grey", treatment_indicator_linestyle = "--",
    treatment_indicator_linewidth = 1, treatment_indicator_alpha = 0.5, xlim = None, savefig = False, dpi = 300,
    bbox_inches = "tight", overlap_alpha = 0.9, simple_legend = True):
    """
    Plots parallel trends for control and treated groups using data from `Undid.jl`.

    Parameters:
    ----------
    - dir_path : str
        A string filepath to the folder containing the `trends_data.csv` files.
    - covariates : bool, optional
        A logical value indicating whether to consider covariates in the analysis. Defaults to False.
    - save_csv : bool, optional
        A logical value indicating whether to save the combined trends data as .csv file. Defaults to False.
    - combine : bool, optional
        A logical value indicating whether to combine all control silos and and all treated silos. Defaults to False.
    - figsize : tuple, optional
        A tuple specifying the figure size of the plot. Defaults to (10, 5).
    - control_colour : str or list of str, optional
        Can be entered as a single string, or a list of strings defining the colours to use for the control silo(s). 
        To create a gradient, create of a list of two strings indicating the range of colours of the gradient. 
        Defaults to ["#D3D3D3", "#4D4D4D"].
    - treated_colour : list, optional
        Can be entered as a single string, or a list of strings defining the colours to use for the treated silo(s). 
        To create a gradient, create of a list of two strings indicating the range of colours of the gradient. 
        Defaults to ["#F08080", "#800020"].
    - control_color : str or None, optional
        If not None, overrides the control_colour parameter. Defaults to None.
    - treated_color : str or None, optional
        If not None, overrides the treated_colour parameter. Defaults to None.
    - linewidth : int, optional
        The width of the plot lines. Defaults to 2.
    - title : str or None, optional
        The title of the plot. Defaults to None.
    - xlabel : str or None, optional
        The subtitle for the x-axis. Defaults to None.
    - ylabel : str or None, optional
        The subtitle for the y-axis. Defaults to None.
    - title_fontdict : dict or None, optional
        A dictionary of font properties for the title. Defaults to None.
        This inherits the structure of `fontdict` used in `matplotlib`, allowing customization of font size, weight, family, etc. Applies specifically to the plot title.
    - title_loc : str, optional
        The location of the title. Defaults to "center".
        This inherits the structure of `loc` used in `matplotlib`. Applies specifically to the plot title. Defaults to None.
    - title_pad : float or None, optional
        Padding between the title and the plot. Defaults to None.
    - xlabel_fontdict : dict or None, optional
        A dictionary of font properties for the x-axis label. Defaults to None.
    - ylabel_fontdict : dict or None, optional
        A dictionary of font properties for the y-axis label. Defaults to None.
    - xlabel_pad : float or None, optional
        Padding between the x-axis label and the plot. Defaults to None.
    - ylabel_pad : float or None, optional
        Padding between the y-axis label and the plot. Defaults to None.
    - ylim : tuple or None, optional
        A tuple specifying the y-axis limits. Defaults to None.
    - yticks : list or None, optional
        A list of values to appear on the y-axis. Defaults to None.
    - yticksize : int, optional
        Font size for the y-axis tick labels. Defaults to 10.
    - xticks : list or None, optional
        A list of dates to appear on the x-axis. Can be inputted as date objects or as strings.
        If entered as strings, also set `date_format` = to the format that the date strings are written as.
        Defaults to None.
    - xticksize : int, optional
        Font size for the x-axis tick labels. Defaults to 10.
    - date_format : str, optional
        Date format for x-axis tick labels. Defaults to "%Y".
    - legend_loc : str, optional
        The location of the legend. Defaults to 'best'.
    - legend_fontsize : int, optional
        Font size for the legend text. Defaults to 12.
    - legend_on : bool, optional
        Whether to display a legend. Defaults to True.
    - treatment_indicator_col : str, optional
        Color of the vertical treatment indicator lines. Defaults to "grey".
    - treatment_indicator_linestyle : str, optional
        Line style for the treatment indicator lines. Defaults to "--".
    - treatment_indicator_linewidth : int, optional
        Line width for the treatment indicator lines. Defaults to 1.
    - treatment_indicator_alpha : float, optional
        Alpha transparency for the treatment indicator lines. Defaults to 0.5.
    - xlim : tuple or None, optional
        A tuple specifying the x-axis limits. 
        Can be inputted as date objects or as strings. 
        If inputted as strings, ensure `date_format` reflects the date format used here.
        Defaults to None.
    - savefig : bool, optional
        A logical value indicating whether to save the plot as a PNG file. Defaults to False.
    - dpi : int, optional
        The resolution of the saved figure. Defaults to 300.
    - bbox_inches : str, optional
        Specifies how much of the plot to include when saving. Defaults to "tight".
    - overlap_alpha : float, optional
        Alpha transparency for the treated and control lines. Defaults to 0.9.
    - simple_legend : bool, optional
        Whether to simplify the legend to just "Control" and "Treated". Defaults to True.

    Returns:
    -------
    - trends_data : pandas.DataFrame
        A DataFrame containing the processed trends data used in the plot.
    """

    # Ensure Undid.jl is loaded
    jl.seval("using Undid")

    # Ensure colours are vectors
    if control_color is not None:
        control_colour = control_color
    if treated_color is not None:
        treated_colour = treated_color
    if not isinstance(control_colour, list):
        control_colour = [control_colour]
    if not isinstance(treated_colour, list):
        treated_colour = [treated_colour]

    # Load in trends_data and determine whether to use covariates or not
    trends_data = jl.Undid.combine_trends_data(dir_path, save_csv = save_csv)
    if covariates == False:
        trends_data.y = trends_data.mean_outcome
    elif covariates == True:
        trends_data.y = trends_data.mean_outcome_residualized
    else:
        raise ValueError("Please set covariates to either True or False")
    
    # Convert to Pandas DataFrame
    column_names = list(jl.names(trends_data))
    trends_data = pd.DataFrame(jl.eachrow(trends_data), columns = column_names)
    unique_treatments = trends_data['treatment_time'].unique()
    unique_treatments = unique_treatments[unique_treatments != "control"]

    if xticks is not None:
        if all(isinstance(x, str) for x in xticks):
            xticks = pd.to_datetime(xticks, format = date_format)
        elif all(isinstance(x, (datetime, date, pd.Timestamp)) for x in xticks):
            pass
        else:
            raise ValueError("Ensure that xticks are entered all as strings or all as date objects!")

    # Parse xlim if necessary
    if xlim is not None:
        if all(isinstance(x, str) for x in xlim): 
            xlim = pd.to_datetime(xlim, format = date_format)
        elif all(isinstance(x, (datetime, date, pd.Timestamp)) for x in xlim):
            pass
        else:
            raise ValueError("Ensure that xlim is entered as a tuple of strings or of date objects!")

    if combine == True: 
        trends_data['ever_treated'] = trends_data['treatment_time'].apply(lambda x: 'control' if x == 'control' else 'treated')
        trends_data = trends_data.groupby(['ever_treated', 'time']).agg({'y': 'mean'}).reset_index()
        plt.figure(figsize = figsize)
        
        if ylim is None:
            ylim = (min(trends_data['y']) - 0.05*min(trends_data['y']), max(trends_data['y']) + 0.05*max(trends_data['y']))

        plt.ylim(ylim)
        plt.yticks(yticks)
        plt.tick_params(axis='y', labelsize=yticksize)


        if xlim is None:
            xlim = (min(trends_data['time']), max(trends_data['time']))
        
        plt.xlim(xlim)
        plt.xticks(xticks)
        plt.tick_params(axis='x', labelsize=xticksize)


        control = trends_data[trends_data['ever_treated'] == 'control']
        treated = trends_data[trends_data['ever_treated'] == 'treated']
        plt.plot(control['time'], control['y'], label='Control', color = control_colour[0], linewidth = linewidth, alpha = overlap_alpha)
        plt.plot(treated['time'], treated['y'], label='Treated', color = treated_colour[0], linewidth = linewidth, alpha = overlap_alpha)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format)) 
        plt.title(title, fontdict = title_fontdict, loc = title_loc, pad = title_pad)
        plt.xlabel(xlabel, fontdict = xlabel_fontdict, labelpad = xlabel_pad)
        plt.ylabel(ylabel, fontdict = ylabel_fontdict, labelpad = ylabel_pad)
        
        if legend_on == True:
            plt.legend(loc = legend_loc, fontsize = legend_fontsize)
        elif legend_on == False:
            pass
        else:
            raise ValueError("Please set legend_on to either True or False")
    elif combine == False:
        plt.figure(figsize = figsize)
        if ylim is None:
            ylim = (min(trends_data['y']) - 0.05*min(trends_data['y']), max(trends_data['y']) + 0.05*max(trends_data['y']))
        
        plt.ylim(ylim)
        plt.yticks(yticks)
        plt.tick_params(axis='y', labelsize=yticksize)
        
        if xlim is None:
            xlim = (min(trends_data['time']), max(trends_data['time']))
        
        plt.xlim(xlim)
        plt.xticks(xticks)
        plt.tick_params(axis='x', labelsize=xticksize)
        n_treated = len(trends_data[trends_data['treatment_time'] != 'control']['silo_name'].unique())
        n_control = len(trends_data[trends_data['treatment_time'] == 'control']['silo_name'].unique())
        if n_treated > len(treated_colour):  
            cmap_treated = LinearSegmentedColormap.from_list("custom_cmap", treated_colour, N=n_treated)
            treated_colour = [cmap_treated(i / (n_treated - 1)) for i in range(n_treated)] 
        if n_control > len(control_colour):
            cmap_control = LinearSegmentedColormap.from_list("custom_cmap", control_colour, N=n_control)
            control_colour = [cmap_control(i / (n_control - 1)) for i in range(n_control)]
              
        control_silos = trends_data[trends_data['treatment_time'] == 'control']['silo_name'].unique()
        for i in range(len(control_silos)):
            label = None if simple_legend else control_silos[i]
            plt.plot(trends_data[(trends_data['treatment_time'] == 'control') & (trends_data['silo_name'] == control_silos[i])]['time'],
            trends_data[(trends_data['treatment_time'] == 'control') & (trends_data['silo_name'] == control_silos[i])]['y'],
            label = label, color = control_colour[i], linewidth = linewidth, alpha = overlap_alpha)
            
        treated_silos = trends_data[trends_data['treatment_time'] != 'control']['silo_name'].unique()
        for i in range(len(treated_silos)):
            label = None if simple_legend else treated_silos[i]
            plt.plot(trends_data[(trends_data['treatment_time'] != 'control') & (trends_data['silo_name'] == treated_silos[i])]['time'],
            trends_data[(trends_data['treatment_time'] != 'control') & (trends_data['silo_name'] == treated_silos[i])]['y'],
            label = label, color = treated_colour[i], linewidth = linewidth, alpha = overlap_alpha)

        
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter(date_format)) 
        plt.title(title, fontdict = title_fontdict, loc = title_loc, pad = title_pad)
        plt.xlabel(xlabel, fontdict = xlabel_fontdict, labelpad = xlabel_pad)
        plt.ylabel(ylabel, fontdict = ylabel_fontdict, labelpad = ylabel_pad)
        
        if legend_on == True:
            if simple_legend == True:                
                control_rgb = [mcolors.to_rgb(colour) for colour in control_colour]
                treated_rgb = [mcolors.to_rgb(colour) for colour in treated_colour]
                r_sum_c, g_sum_c, b_sum_c = 0, 0, 0
                r_sum_t, g_sum_t, b_sum_t = 0, 0, 0
                for colour in control_rgb:
                    r_sum_c += colour[0]
                    g_sum_c += colour[1]
                    b_sum_c += colour[2]
                for colour in treated_rgb:
                    r_sum_t += colour[0]
                    g_sum_t += colour[1]
                    b_sum_t += colour[2]
                r_avg_c = r_sum_c/n_control
                g_avg_c = g_sum_c/n_control
                b_avg_c = b_sum_c/n_control

                r_avg_t = r_sum_t/n_treated
                g_avg_t = g_sum_t/n_treated
                b_avg_t = b_sum_t/n_treated

                plt.plot([], [], color=(r_avg_c, g_avg_c, b_avg_c), label='Control', linewidth=linewidth)
                plt.plot([], [], color=(r_avg_t, g_avg_t, b_avg_t), label='Treated', linewidth=linewidth)
            plt.legend(loc = legend_loc, fontsize = legend_fontsize)
        elif legend_on == False:
            pass
        else:
            raise ValueError("Please set legend_on to either True or False")
    else:
        raise ValueError("Please set combine to either True or False")

    for treatment_time in unique_treatments:
        plt.axvline(treatment_time, color = treatment_indicator_col, linestyle = treatment_indicator_linestyle, linewidth = treatment_indicator_linewidth, alpha = treatment_indicator_alpha)

    if savefig == True:
        print("Saving plot as `undid_parallel_trends.png` to current working directory.")
        plt.savefig('undid_parallel_trends.png', dpi = dpi, bbox_inches = bbox_inches)
    elif savefig == False:
        pass
    else:
        raise ValueError("Please set savefig as either True or False!")

    return trends_data
