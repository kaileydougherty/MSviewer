# Create a 3D visualization for distributed fiber optic sensing data for microseismic events.
# Author: Kailey Dougherty
# Date created: 19-JAN-2025
# Date last modified: 09-MAR-2025

# Import needed libraries
import pandas as pd
import numpy as np
import os
import plotly.graph_objects as go
from PlotObj import PlotObject


class MSPlot():

    """
    A class for loading, parsing, and viewing microseismic events in 3D space given a CSV file.
    
    Attributes
    ----------
    MScatalog : str
        The relative path to the CSV file containing the microseismic data.
        This data set must contain the following column names in order to be compatible:
        - File Name: containing identifying name of microseismic event.
        - Easting: The Easting coordinate of the event in feet.
        - Northing: The Northing coordinate of the event in feet.
        - Depth TVDSS: The depth of the event in feet.
        - Origin Time - Date (UTC): Origin date in MM/DD/YYYY format.
        - Origin Time - Time (UTC): Origin time given in HH:MM:ss format.
        - Origin Time - Millisecond (UTC): Origin time millisecond count which adds to the Origin Time - Time (UTC) value.
        - Brune Magnitude: Brune magnitude of event entered as a negative decimal value.
        - Stage: Stage of event entered as an integer value.
    
    color_by : str
        The attribute used to determine the color of each plot point. Default is 'Stage'.
    
    color_scale : str
        The color scale used for the visualization. Default is 'Viridis'.
    
    size_by : str
        The attribute used to determine the size of each plot point. Default is 'Brune Magnitude'.
    
    size_range : list of int
        The range for scaling the size of the points in the plot. Default is [10, 100].
    
    plot_start_time : str or None
        The start time for the plot's time range in 'YYYY-MM-DD HH:MM:SS' format. Default is None.
    
    plot_end_time : str or None
        The end time for the plot's time range in 'YYYY-MM-DD HH:MM:SS' format. Default is None.
    
    title : str
        The title of the plot. Default is '3D Bubble Chart of Cumulative Seismic Entries'.

    Methods
    -------
    create_plot(self):
        Creates an interactive 3D scatter plot object for seismic data.

    load_csv(self, MScatalog):
        Loads and parses the data from the file specified by the MScatalog attribute, returning a Pandas DataFrame with structured data.
    
    set_colorby(color_by):
        Sets the attribute to be used for color encoding the plot points.
    
    set_colorscale(color_scale):
        Sets the color scale for the plot.
    
    set_sizeby(size_by):
        Sets the attribute to be used for determining the size of the plot points.
    
    set_sizerange(size_range):
        Sets the range for scaling the size of the plot points.
    
    set_start_time(plot_start_time):
        Sets the start time for the plot's time range.
    
    set_end_time(plot_end_time):
        Sets the end time for the plot's time range.
    
    set_title(title):
        Sets the title for the plot.
    
    """

    def __init__(self):
        """
        Initialize the MSViewer with the given parameters.

        Parameters
        ----------
        MScatalog : str
            The relative path to the CSV file containing the microseismic data.
            This data set must contain the following column names in order to be compatible:
            - File Name: containing identifying name of microseismic event.
            - Easting: The Easting coordinate of the event in feet.
            - Northing: The Northing coordinate of the event in feet.
            - Depth TVDSS: The depth of the event in feet.
            - Origin Time - Date (UTC): Origin date in MM/DD/YYYY format.
            - Origin Time - Time (UTC): Origin time given in HH:MM:ss format.
            - Origin Time - Millisecond (UTC): Origin time millisecond count which adds to the Origin Time - Time (UTC) value.
            - Brune Magnitude: Brune magnitude of event entered as a negative decimal value.
            - Stage: Stage of event entered as an integer value.
        
        color_by : str, optional
            The attribute used for color encoding. Default is 'Stage'.
        
        color_scale : str, optional
            The color scale for the visualization. Default is 'Viridis'.
        
        size_by : str, optional
            The attribute used for determining the size of the plot points. Default is 'Brune Magnitude'.
        
        size_range : list of int, optional
            The size range for the plot points. Default is [10, 100].
        
        plot_start_time : str, optional
            The start time for the plot's time range. Default is None.
        
        plot_end_time : str, optional
            The end time for the plot's time range. Default is None.
        
        title : str, optional
            The title for the plot. Default is '3D Bubble Chart of Cumulative Seismic Entries'.
        """

        self.MScatalog = None
        self.color_by = 'Stage'
        self.color_scale = 'Viridis'
        self.size_by = 'Brune Magnitude'
        self.size_range = [10, 100]
        self.plot_start_time = None
        self.plot_end_time = None
        self.title = '3D Bubble Chart of Cumulative Seismic Entries'

    def set_colorby(self, color_by):
        self.color_by = color_by

    def set_colorscale(self, color_scale):
        self.color_scale = color_scale

    def set_sizeby(self, size_by):
        self.size_by = size_by

    def set_sizerange(self, size_range):
        self.size_range = size_range

    def set_start_time(self, plot_start_time):
        self.plot_start_time = plot_start_time

    def set_end_time(self, plot_end_time):
        self.plot_end_time = plot_end_time

    def set_title(self, title):
        self.title = title


    def load_csv(self, MScatalog):
        """
        Load and parse the dataset.
        
        Reads the data from the CSV file by its relative path, processes it by renaming columns, 
        converting columns to appropriate datatypes, and combining time columns.
        Returns a Pandas DataFrame with the cleaned data.

        Parameters
        ----------
        None.

        Returns
        -------
        pandas.DataFrame
            A Pandas DataFrame containing the following columns:
            - File Name: The name of the event file.
            - Easting (ft): The Easting coordinate of the event in feet.
            - Northing (ft): The Northing coordinate of the event in feet.
            - Depth TVDSS (ft): The depth of the event in feet.
            - Origin Time - Date (UTC) - MM/DD/YYYY: The date of origin in UTC in MM/DD/YYYY format (str).
            - Origin Time - Time (UTC) - HH:MM:ss: The time of origin in UTC in HH:MM:ss format (str).
            - Origin DateTime: A combined datetime column of the origin time in UTC in YYYY-MM-DD HH:MM:ss.sss format (str).
            - Brune Magnitude: The Brune magnitude of the event (float).
            - Stage: The stage identifier (int).

        Exceptions:
        --------
        FileNotFoundError: Raised if the file specified by self.catalog does not exist.
        """
       
        # Check if the file exists
        if not os.path.exists(MScatalog):
            raise FileNotFoundError(f"File not found: {MScatalog}")

        # Load in the file
        needed_cols = pd.read_csv(MScatalog,  #Specify file
                 usecols=['File Name', 'Easting', 'Northing', 'Depth TVDSS', 'Origin Time - Date (UTC)', 'Origin Time - Time (UTC)', 
                          'Origin Time - Millisecond (UTC)', 'Brune Magnitude', 'Stage'],  #Specify columns
                 skiprows=[1],  #Skip units row
                 dtype={'File Name': str,    #Specify datatype
                        'Easting': float,
                        'Northing': float, 
                        'Depth TVDSS': float,
                        'Origin Time - Date (UTC)': str,
                        'Origin Time - Time (UTC)': str,
                        'Origin Time - Millisecond (UTC)': int,
                        'Brune Magnitude': float,
                        'Stage': int
                       })
        
        # Rename column names
        parsed_data = needed_cols.rename(columns={'Easting':'Easting (ft)', 
                        'Northing':'Northing (ft)', 
                        'Depth TVDSS':'Depth TVDSS (ft)', 
                        'Origin Time - Date (UTC)':'Origin Time - Date (UTC) - MM/DD/YYYY', 
                        'Origin Time - Time (UTC)':'Origin Time - Time (UTC) - HH:MM:ss', 
                        })

        # Convert UTC to datetime
        # Combine Origin Time - Date (UTC) - MM/DD/YYYY and Origin Time - Time (UTC) - HH:MM:ss columns
        parsed_data['Origin DateTime'] = pd.to_datetime(parsed_data['Origin Time - Date (UTC) - MM/DD/YYYY'] + ' ' + parsed_data['Origin Time - Time (UTC) - HH:MM:ss'])

        # Add milliseconds to new column
        parsed_data['Origin DateTime'] = parsed_data['Origin DateTime'] + pd.to_timedelta(parsed_data['Origin Time - Millisecond (UTC)'], unit='ms')

        # Convert Brune Magnitude column to float datatype
        parsed_data['Brune Magnitude'] = parsed_data['Brune Magnitude'].astype(float)
        
        self.data = parsed_data

        print('Success!')

        return True
    

    def create_plot(self):
        """
        Creates an interactive 3D scatter plot object for seismic data.

        Generates data for a 3D scatter plot where each point represents a seismic event,
        with `Easting (ft)`, `Northing (ft)`, and `Depth (ft)` as the coordinates. The points are colored 
        and sized based on the `Brune Magnitude` of each event.

        The plot is interactive and includes hover text displaying the file name, stage, and 
        magnitude for each seismic event. The user can navigate through the different time frames 
        and explore how the seismic data evolves over time.

        Parameters:
        -----------
        None.

        Returns:
        --------
        plotly.graph_objects.Figure
            A Plotly figure object that can be displayed in a Jupyter notebook or other compatible environments.
            The figure contains an interactive 3D scatter plot with a time-based animation slider.
        
        Notes:
        ------
        - The function currently only processes the first 100 rows of the input data (`data.iloc[:101]`), 
        which is meant for development purposes.
            """

        data = self.data

        # Take the first 100 entries
        df_100 = data.iloc[:101] # for DEVELOPMENT PURPOSES

        # Ensure DateTime values are in chronological order
        df_100 = df_100.sort_values(by='Origin DateTime')

        # Filter data based on the start and stop times

        # Check if start and end times are set
        if self.plot_start_time is None:
            self.plot_start_time = df_100['Origin DateTime'].min()
        
        if self.plot_end_time is None:
            self.plot_end_time = df_100['Origin DateTime'].max()

        # Filter dataframe
        df_filtered = df_100[(df_100['Origin DateTime'] >= self.plot_start_time) & (df_100['Origin DateTime'] <= self.plot_end_time)]

        # Create a list of unique times for the slider
        times = df_filtered['Origin DateTime'].unique()

        # Individual frames for each seismic entry

        # Create the MS Plot
        MSplot = go.Scatter3d(
            x=df_filtered['Easting (ft)'],  #X-axis: Easting
            y=df_filtered['Northing (ft)'],  #Y-axis: Northing
            z=df_filtered['Depth TVDSS (ft)'],  #Z-axis: Depth
            text=df_filtered.apply(lambda row: f"File: {row['File Name']}<br>Stage: {row['Stage']}<br>Magnitude: {row['Brune Magnitude']:.2f}", axis=1),  #Hover text: File Name, Stage, Brune Magnitude
            mode='markers',
            marker=dict(
                sizemode='diameter',  #Set the size mode to diameter
                sizeref=25,  #Adjust the size scaling factor
                size=abs(df_filtered[self.size_by]) * 100,  #Set size
                color=df_filtered[self.color_by],  #Set which column to color by
                colorscale=self.color_scale,  #Set color scale
                cmin=df_filtered[self.color_by].min(),  #Set min
                cmax=df_filtered[self.color_by].max(),  #Set max
                colorbar=dict(title=f'{self.color_by}'),  #Color bar title
            ))

        # Return MS plot object
        return MSplot
