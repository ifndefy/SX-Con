import pandas as pd

def fetch_consignment_data():
    '''
    :purpose: Read consignment data from SPOT.csv and return as dict, separate file to be importable by anyone in the programC
    
    :return: Dictionary containing csv data in (Type : Rate) format
    :author: Maksym Komarov
    '''
    #
    dataframe = pd.read_csv("./src/SPOT_CR.csv")
    #Convert the dataframe into a series indexed by type and convert to dictionary
    data_as_dict = dataframe.set_index("Type")["Rate"].to_dict()

    return data_as_dict