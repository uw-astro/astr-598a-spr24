# Generate a set of synthetic time series data with a single frequency,
# a set of synthetic time series data with multiple frequencies, and a set of sampled time series data. 
#
# All lightcurves will have a sinusoidal shape with different phases.

from pathlib import Path

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def generate_data(num_steps: int, period_array: np.array, phase_array:np.array, num_series = None) -> None:
    '''Generate data for sine wave with noise.
        Assume that the time interval is in days.

        if num_series is not None then period_array and phase_array should be of length 1

        Args:
            num_steps: number of time steps in the sine wave 
            period_array: periods of the sine wave (days)
            phase_array: phases of the sine wave (radians)

        Returns:
            Pandas DataFrame with the generated data
        '''
    if num_series is None:
        num_series = len(period_array)
        if len(phase_array) != num_series:
            raise ValueError('period_array and phase_array must have the same length')
    else:
        num_series = num_series
        if len(phase_array) != 1 and len(period_array) != 1:
            raise ValueError('period_array and phase_array must have length 1')
        phase_array = np.random.uniform(low=0, high=2*np.pi, size=num_series)
        period_array = np.repeat(period_array, num_series)  
        
    x = np.linspace(0, num_steps)

    series_list = []
    series_name = []
    for i in range(num_series):
        y = np.sin(2. * np.pi * x / period_array[i] + phase_array[i]) #+ np.random.normal(0, 0.1, x.shape)
        ser = pd.Series(y, index=x)
        series_list.append(ser)
        series_name.append(f'y{i}')

    df = pd.concat(series_list, axis=1)
    df.columns = series_name

    return df

def plot_timeseries(df: pd.DataFrame, indx=0 ) -> None:
    '''Plot the generated time series data.
        Args:
            df: Pandas DataFrame with the generated data
            indx: index of the time series to plot
        '''
    df[f'y{indx}' ].plot(style='o')  

    plt.show()

def select_random_points(series, n):
    '''Select n random points from the time series.
        Args:
            series: Pandas Series with the time series data
            n: number of points to select
        Returns:
            Pandas Series with the selected points  
    '''
    return series.sample(n=n)

num_series = 100000
num_steps = 100
periods = np.array([40])
phases = np.array([0.2])
df = generate_data(num_steps, periods, phases, num_series=num_series)
df.to_feather("timeseries_single_frequency.feather")
plot_timeseries(df, indx=0)
plot_timeseries(df, indx=1)

periods = np.random.uniform(40, 100, num_series)
phases = np.random.uniform(0, 2*np.pi, num_series)
df = generate_data(num_steps, periods, phases, num_series=None)
df.to_feather("timeseries_multiple_frequency.feather")
plot_timeseries(df, indx=0)
plot_timeseries(df, indx=1)

# sample the data 
# pick 30 time stamps (a different number for each time series) 
sampled_df = df.apply(select_random_points, args={20}, axis=0)
sampled_df.to_feather("timeseries_multiple_frequency_sampled.feather")
plot_timeseries(sampled_df, indx=0)
plot_timeseries(sampled_df, indx=1)