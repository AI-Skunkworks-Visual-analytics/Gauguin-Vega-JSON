import json
import os
import re

import altair as alt
import numpy  as np
import pandas as pd
from enums import PATH, MAPS, DATA_NAME_LIST, START_PATH 
from vega_datasets import data
import random
from geopy.geocoders import Nominatim


class MapBot():
    """ Vega JSON Map Bot Class.
    Develop a script and use vega to generate as many visualization as possible,
    data cleaning the null value, classify the categorical and numerical type,
    Output as JSON format for different type of Bar Charts.
    """

    def __init__(self, file_name: str, chart_type: str) -> None:
        """Creates a new instance of the Bar Bot Object.
        Adding data path, plot output path, log output path

        Arguments:
        ----
        chart_type {str} -- 'chart Type'
        data_path {str}  -- data path of chart
        """

        # Define chart type and read csv file
        self.chart_type = chart_type
        self.file_name = file_name
        self.file_path = START_PATH + "\\data\\" + self.file_name
        self.df = pd.read_csv(self.file_path)

        # Categorical and numbercial type
        self.cat_col = []
        self.num_col = []

        # Unique Value
        self.uniques = []

        # Geography
        self.geo_usa = []
        self.geo_world = []

    def chart_type(self):
        return self.chart_type

    def file_name(self):
        return self.file_name

    def df(self):
        return self.df

    def get_cat_col(self):
        return self.cat_col

    def num_col(self):
        return self.num_col

    def uniques(self):
        return self.uniques

    def file_name(self, file_name):
        self.file_name = file_name
        self.df = pd.read_csv(self.file_name)

    def null_count(self, null_percentage: int, dummy_data: bool = False) -> any:
        """Calculating null values.
        . We are dropping  Columns which have more than 30% of null value
        . Replacing null value with mean in case of int and float
        .If null value persist for other cases we are dropping those rows

        Arguments:
        ----
        null_percentage: pertcentage of dummy want to cut off

        dummy_data: Should replace with dummy or not
        """
        nulls_count = {col: self.df[col].isnull().sum() for col in self.df.columns}
        # print(nulls_count)

        is_null_count_out_of_range = \
            {col: self.df[col].isnull().sum() / self.df.shape[0] * 100 > null_percentage for col in self.df.columns}

        if (dummy_data):
            # self._generate_dummy_data()
            pass
        else:
            for k, v in is_null_count_out_of_range.items():
                if v:
                    self.df.drop(k, axis=1, inplace=True)
                else:
                    if isinstance(self.df[k][0], (np.int64, np.float64)):
                        self.df[k].fillna(self.df[k].mean(), inplace=True)
                    else:
                        drop_list = self.df[self.df[k].isnull()].index.tolist()
                        self.df.drop(drop_list, axis=0, inplace=True)

        nulls_count = {col: self.df[col].isnull().sum() for col in self.df.columns}
        # print(nulls_count)

    def _generate_dummy_data(self) -> any:
        """Generate dummy data for null column.
        """
        pass

    def unique_value_list(self) -> any:
        """Finding all the unique values to in each column.
        """
        self.uniques = {col: self.df[col].unique().tolist() for col in self.df.columns}

    def write_unique_value_list(self) -> any:
        """Writing the above created dictionary to a text file.
        """

        file_name = "{fname}_Unique_values.txt".format(fname=self.file_name)
        unique_list_file_path = os.path.join(PATH['data'], file_name)

        if os.path.exists(unique_list_file_path):
            print("{fname} already existed".format(fname=file_name))
        else:
            with open(unique_list_file_path, 'w') as json_file:
                json.dump(self.uniques, json_file)
            print("Generate {fname} Successfully".format(fname=file_name))

    
    def new_folder_for_log_and_plot(self, charts) -> any:
        """Generate new folder for log file and Json plot.

        Arguments:
        ----
        charts: Enum Type import from enums.py
        """
        log_folder = PATH["log"][self.chart_type]
        plot_folder = PATH["plot"][self.chart_type]

        # Generate Log folder
        for char in (charts):
            print(self._generate_new_folder(log_folder, char.value))

        # Generate plot folder
        for char in (charts):
            print(self._generate_new_folder(plot_folder, char.value))

    def _generate_new_folder(self, folder_path: str, folder_name: str) -> str:
        """Generate new folder return generate result.

        Arguments:
        ----
        folder_path: parent path

        folder_name: name of folder
        """
        folder_path = os.path.join(folder_path, folder_name)
        if os.path.exists(folder_path):
            return "{fname} folder already existed".format(fname=folder_path)
        else:
            os.mkdir(folder_path)
            return "Generate {fname} folder Successfully".format(fname=folder_path)

    def dtypes_conversion(self) -> any:
        """
        . Converting columns to categorical having less than or equal to 10.
        . Integer and Float dataype will classify as numberical type
        . Check
        """
        # unique values in a column

        for k, v in self.uniques.items():
            if len(pd.Index(v)) <= 10:
                self.df[k] = self.df[k].astype('category')

        self.cat_col = self.df.select_dtypes(include=['category']).columns.tolist()
        self.num_col = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        # self._dtypes_conversion_datetime()
        self._dtypes_conversion_geograph()

        # print("Numerical Column : '\n'  {num_col}".format(num_col=str(self.num_col)))
        # print("Categorical Column : '\n'{cat_col}".format(cat_col=str(self.cat_col)))

    def _dtypes_conversion_datetime(self) -> any:
        """Check object columns is datetime or not.
        . Check the object columns is datetime datatype
        . Add new Column according to datetime datatype
        """
        types = self.df.dtypes[self.df.dtypes == 'object']
        for i, j in types.items():
            try:
                self.df[i] = pd.to_datetime(self.df[i])
                self.df[i + '_year'] = pd.DatetimeIndex(self.df[i]).year
                self.df[i + '_month'] = pd.DatetimeIndex(self.df[i]).month
                self.cat_col.append(i + '_year')
                self.cat_col.append(i + '_month')
            except:
                pass

    def _dtypes_conversion_geograph(self) -> any:
        """Identify Numercial type as longtitude or lantitude.
        """
        float_col = self._float_list(self.df)
        permu = self._column_permunator(float_col)
        geo_list = self._get_geo_list(5, permu, self.df)
        self.geo_usa, self.geo_world = self._isUSA(self.df, geo_list, 5, 0.8 )

    def _float_list(self, df):
        for col in df.columns:
            float_col = df.select_dtypes(include=['float64']).columns.tolist()
        return float_col

    def _column_permunator( self, float_list ):
        import itertools
        return list(itertools.permutations(float_list, 2))

    def _is_geograph(self, Latitude,Longitude, geolocator):    
        try:
            location = geolocator.reverse(str(Latitude)+", "+str(Longitude))
            print(location)
            return location
        except Exception as e:
            print(e)
            return ""
    
    def _isUSA( self, df, geo_list, num_of_select, percentage ):
        num_of_select = round(num_of_select/percentage)
        geo_usa = []
        geo_world = []
        geolocator = Nominatim(user_agent="geoapiExercises")
        for i in geo_list:
            num_of_usa = 0
            lat  = random.sample(list(df[i[0]]), num_of_select)            
            long = random.sample(list(df[i[1]]), num_of_select)
            for j in range(len(lat)):
                if self._is_geograph(lat[j], long[j], geolocator).raw['address'].get('country', '')  == 'United States of America': 
                    num_of_usa += 1
            if num_of_usa == num_of_select:
                geo_usa.append(i)
            else:
                geo_world.append(i)
        return geo_usa, geo_world
    
    def _get_geo_list(self, num_of_select, permu, df):
        geolocator = Nominatim(user_agent="geoapiExercises")
        geo_list = []
        for i in permu:
            lat  = random.sample(list(df[i[0]]), num_of_select)            
            long = random.sample(list(df[i[1]]), num_of_select) 
            for j in range(len(lat)):
                if j == num_of_select - 1:
                    geo_list.append(i)
                    break  
                if self._is_geograph(lat[j], long[j], geolocator) == "" :
                    break    
        return geo_list

    def _generate_plot_path(self, cat_name: str, num_name: str, chart_name: str) -> str:
        """Generate Plot path according to catgorical and numercial column.

        Arguments:
        ----
        cat_name: catgorical column name

        num_name: numercial column name

        chart_name: Specific name of chart.
        """
        file_name = "{cat_name} Vs {num_name}_plot.json".format(cat_name, num_name)
        plot_path = os.path.join(PATH['plot'][self.chart_type], chart_name, file_name)

        if os.path.exists(plot_path):
            print("{fname} file already existed".format(fname=plot_path))
            return ""
        else:
            print("Generate {fname} folder Successfully".format(fname=self.folder_path))
            return plot_path

    def _generate_maplot_path(self, feature: str, projection: str, chart_name: str, location: str) -> str:
        """Generate Plot path according to catgorical and numercial column.

        Arguments:
        ----
        cat_name: catgorical column name

        num_name: numercial column name

        chart_name: Specific name of chart.
        """
        file_name = "{}_{}_plot_{}_{}.json".format(feature, projection, self.file_name, location)
        plot_path = os.path.join(PATH['plot'][self.chart_type], chart_name, file_name)

        if os.path.exists(plot_path):
            print("{fname} file already existed".format(fname=plot_path))
            return ""
        else:
            print("Generate {fname} folder Successfully".format(fname=plot_path))
            return plot_path


    def location_graph_JSON_generator(self)-> any:
        if len(self.geo_usa) != 0 :
            projection_list = [
            'albersUsa']
            for i in self.geo_usa:
                self.map_graph_JSON_generator(self.cat_col, 'states', i, data.londonBoroughs.url, projection_list)


        if len(self.geo_world) != 0 :
            projection_list = [
            'azimuthalEqualArea',
            'conicEqualArea',
            'equalEarth',
            'mercator',
            'orthographic']
            for i in self.geo_world:
                self.map_graph_JSON_generator(self.cat_col, 'countries', i, data.world_110m.url, projection_list)


    def map_graph_JSON_generator(self, features, location, geo_loc, map_data,projection_list) -> any:
        """ Generating Stacked bar JSON using altair methods.
        """


        for projection in projection_list:
            for feat in features:
                source  = alt.topo_feature( map_data, feature=location)
                background = alt.Chart(source ).mark_geoshape(
                    fill='lightgray',
                    stroke='white'
                ).properties(
                    width=500,
                    height=300
                ).project(projection)

                # long-lat positions on background
                points = alt.Chart(self.df).transform_aggregate(
                    latitude= "mean({})".format(geo_loc[0]),
                    longitude="mean({})".format(geo_loc[1]),
                    count='count()',
                    groupby=[feat]
                ).mark_circle().encode(
                    longitude="{}:Q".format(geo_loc[1]), 
                    latitude="{}:Q".format(geo_loc[0]),
                    size=alt.Size('count:Q'),
                    color=alt.value('steelblue'),
                    tooltip=[feat+':N', 'count:Q']
                ).properties(
                    # title='Number of airports in US'
                    #title = "Number of {} in US".format(feat)
                )

                chart=background + points
                file_path = self._generate_maplot_path(feat, projection, MAPS.WORLD_MAP.value, location)
                if file_path == "":
                    pass
                else:
                    chart.save(file_path)
                print(file_path)
                #print("{} Graph JSON generated in ""altair_plots"" folder for the combinations".format("Location graph"))


if __name__ == "__main__":
    my_bar = MapBot(file_name=DATA_NAME_LIST[0], chart_type='maps')

    my_bar.null_count(70)

    my_bar.unique_value_list()

    my_bar.new_folder_for_log_and_plot(MAPS)

    my_bar.write_unique_value_list()

    my_bar.dtypes_conversion()

    #cat_col = my_bar.get_cat_col()

    # num_col = my_bar.cat_col


    my_bar.location_graph_JSON_generator()