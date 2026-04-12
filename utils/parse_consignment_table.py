import pandas as pd
from pathlib import Path
import sys

def fetch_consignment_data():
    #Read consignment data from SPOT.csv and return as dict, separate file to be importable by anyone in the program
    __resolved_path = Path(sys._MEIPASS).parent if getattr(sys, 'frozen', False) else Path(__file__).parent.parent
    __csv_location = __resolved_path / "src" / f"SPOT_CR.csv"

    dataframe = pd.read_csv(__csv_location)
    #Convert the dataframe into a series indexed by type and convert to dictionary
    data_as_dict = dataframe.set_index("Type")["Rate"].to_dict()

    return data_as_dict