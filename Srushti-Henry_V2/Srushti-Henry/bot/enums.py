import os
from enum import Enum

START_PATH = os.path.dirname(os.getcwd()) 
UNIQUE_VALUE_FILE = 'Unique_values.txt'

class BAR(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class LINE(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class AREA(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class SCATTER(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class HISTOGRAMS(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class INTERACTIVE(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class MAPS(Enum):

    WORLD_MAP = 'world_map'


class OTHER(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


class CASESSTUDIES(Enum):

    SIMPLE_BAR = 'simple_bar'
    STACKED_BAR = 'stack_bar'
    GROUP_BAR = 'group_bar'


CHART_TYPE = ['bar', 'line', 'area', 'scatter', 'histogram', 
'maps', 'interactive', 'case', 'other']

PATH = {
    'log': {i : os.path.join(START_PATH, "log\\", i) for i in CHART_TYPE},
    'data': os.path.join(START_PATH, "data"),
    'plot': {i : os.path.join(START_PATH, "altair_plots\\", i) for i in CHART_TYPE}
}

#print( START_PATH  )
DATA_NAME_LIST = os.listdir(PATH['data'])
#DATA_NAME_LIST = [ START_PATH + "\\data\\" + i for i in DATA_NAME_LIST ]