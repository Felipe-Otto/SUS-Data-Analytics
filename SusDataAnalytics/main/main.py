import pandas as pd


class Main:
    def __init__(self):
        self.get_dataframe()




    def get_dataframe(self):
        from model.data_utils import DataUtils
        DataUtils().create_dataframe('../data_analysis/sinan_data_original.csv')








main = Main()

