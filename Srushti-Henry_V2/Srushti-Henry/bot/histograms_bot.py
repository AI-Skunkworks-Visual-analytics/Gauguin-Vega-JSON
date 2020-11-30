import json
import os

import altair as alt
import numpy  as np
import pandas as pd
from enums import PATH, BAR, DATA_NAME_LIST


class BarBot():
    """ Vega JSON Bar Chart Bot Class.
    Develop a script and usevega to generate as many visualzation as possible,
    data cleaning the null value, classify the catgorical and numercial type,
    Output as JSON format for different type of Bar Charts.
    """


    def __init__(self, file_name: str, chart_type: str ) -> None :
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
        self.df = pd.read_csv(self.file_name)

        # Categorical and numbercial type
        self.cat_col = [] 
        self.num_col = []

        # Unique Value
        self.uniques = []

    @property
    def chart_type(self):
        return self._chart_type

    @property
    def file_name(self):
        return self._file_name

    @property
    def df(self):
        return self._df

    @property
    def cat_col(self):
        return self.cat_col  

    @property
    def num_col(self):
        return self.num_col

    @property
    def uniques(self):
        return self._uniques

    @file_name.setter
    def file_name(self, file_name):
        self._file_name = file_name
        self._df = pd.read_csv(self.file_name)


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

        if ( dummy_data ) :
            #self._generate_dummy_data()
            pass
        else :
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
        """Generate dummmy data for null column.
        """
        pass

    def unique_value_list(self) -> any:
        """Finding all the unique values to in each column.
        """
        self.uniques = {col: self.df[col].unique().tolist() for col in self.columns}

    def write_unique_value_list(self) -> any:
        """Writing the above created dictionary to a text file.
        """

        file_name = "{fname}_Unique_values.txt".format(fname=self.file_name)
        unique_list_file_path = os.path.join(PATH['data'], file_name )

        if os.path.exists(unique_list_file_path):
            print( "{fname} already existed".format( fname = file_name ) )
        else:
            with open(unique_list_file_path, 'w') as json_file:
                json.dump(uniques, json_file)
            print( "Generate {fname} Successfully".format( fname = file_name ) )

    def new_folder_for_log_and_plot(self, charts) -> any:
        """Generate new folder for log file and Json plot.

        Arguments:
        ----
        charts: Enum Type import from enums.py 
        """
        log_folder  = PATH["log"][self.chart_type]
        plot_folder = PATH["plot"][self.chart_type]

        # Generate Log folder
        for char in (charts):
            print(self._generate_new_folder( log_folder, char.name ))

        # Generate plot folder
        for char in (charts):
            print(self._generate_new_folder( plot_folder, char.name ))
        
       
    def _generate_new_folder( folder_path: str, folder_name: str ) -> str:
        """Generate new folder return generate result.

        Arguments:
        ----
        folder_path: parent path

        folder_name: name of folder
        """
        folder_path =  os.path.join(folder_path, folder_name)
        if os.path.exists(folder_path):
            return "{fname} folder already existed".format( fname = folder_path ) 
        else:
            os.mkdir(log_folder_path)
            return "Generate {fname} folder Successfully".format( fname = folder_path ) 


    def dtypes_conversion(self) -> any:
        """
        . Converting columns to categorical having less than or equal to 10.
        . Integer and Float dataype will classify as numberical type
        . Check 
        """
        #unique values in a column

        for k,v in self.uniques.items():
            if len(pd.Index(v)) <=10:
                self.df[k]= self.df[k].astype('category')

        self.cat_col = self.df.select_dtypes(include=['category']).columns.tolist()
        self.num_col = self.df.select_dtypes(include=['int64','float64']).columns.tolist()

        self._dtypes_conversion_datetime()
        #self._dtypes_conversion_geograph() [!FIX] 

        print("Numerical Column : '\n'  {num_col}".format( num_col = str(self.num_col) ) )
        print("Categorical Column : '\n'{cat_col}".format( cat_col = str(self.cat_col) ))

    def _dtypes_conversion_datetime(self) -> any:
        """Check object columns is datetime or not.
        . Check the object columns is datetime datatype
        . Add new Column according to datetime datatype
        """
        types = self.df.dtypes[self.df.dtypes == 'object']
        for i, j in types.items():
            try:
                self.df[i] = pd.to_datetime(df[i])
                self.df[i + '_year'] = pd.DatetimeIndex(self.df[i]).year
                self.df[i + '_month'] = pd.DatetimeIndex(self.df[i]).month
                self.cat_col.append(i + '_year')
                self.cat_col.append(i + '_month')
            except:
                pass

    def _dtypes_conversion_geograph(self) -> any:
        """Identify Numercial type as longtitude or lantitude.
        """
        pass

    def _generate_plot_path(self, cat_name: str, num_name: str, chart_name: str ) -> str:
        """Generate Plot path according to catgorical and numercial column.

        Arguments:
        ----
        cat_name: catgorical column name

        num_name: numercial column name

        chart_name: Specific name of chart.
        """
        file_name = "{cat_name} Vs {num_name}_plot.json".format( cat_name, num_name  )
        plot_path = os.path.join(PATH['plot'][self.chart_type], chart_name, file_name)

        if os.path.exists(plot_path):
            print( "{fname} file already existed".format( fname = plot_path ) )
            return ""
        else:
            print( "Generate {fname} folder Successfully".format( fname = folder_path )  )
            return plot_path



    def simple_bar_JSON_generator(self) -> any:
        """Generating  Simple bar JSON using altair methods.
        """

        for i in range(len(self.cat_col)):
            for j in range(len(self.num_col)):
                file_path = self._generate_plot_path( str(self.cat_col[i]), str(self.num_col[j]),  BAR.SIMPLE_BAR.name)
                if file_path == "":
                    pass
                else:
                    chart=alt.Chart(self.df).mark_bar().encode(
                        x=self.cat_col[i],
                        y=self.num_col[j])
                    chart.save(file_path)
        print("{} Graph JSON generated in ""altair_plots"" folder for the combinations".format("Simple Bar"))

    def stacked_bar_JSON_generator(self) -> any:
        """ Generating Stacked bar JSON using altair methods.
        """

        for i in range(len(self.cat_col)-1):
            file_path = self._generate_plot_path( str(cat_col[i]), str(cat_col[i+1]),  BAR.STACKED_BAR.name)
            if file_path == "" :
                pass
            else:
                chart=alt.Chart(self.df).mark_bar(
                    cornerRadiusTopLeft=3,
                    cornerRadiusTopRight=3
                    ).encode(x=self.cat_col[i], y='count():Q', color=self.cat_col[i+1])
                chart.save(file_path)
        print("{} Graph JSON generated in ""altair_plots"" folder for the combinations".format("Stacked Bar"))


if __name__ == "__main__":
    my_bar = BarBot( file_name = DATA_NAME_LIST[0], chart_type = 'bar' )

    my_bar.null_count()

    my_bar.unique_value_list()

    my_bar.new_folder_for_log_and_plot()

    my_bar.write_unique_value_list()

    my_bar.dtypes_conversion()

    # cat_col = my_bar.cat_col

    # num_col = my_bar.cat_col

    my_bar.simple_bar_JSON_generator()

    my_bar.stacked_bar_JSON_generator()