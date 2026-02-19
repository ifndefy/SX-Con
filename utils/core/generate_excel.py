import pandas as pd
from PyQt6.QtWidgets import QFileDialog
import utils.logger.logger as log

def generate_excel(data):
    #Get Filepath (Using QFileDialog Static methods, might be worth moving to a single universal QFileDialog object instead to handle coordinating exports)
    #file_path contains a tuple of [path, extension]
    try:
        log.info("Creating Save File Dialog")
        file_path = QFileDialog.getSaveFileName(None, "Save Excel File As...", "./", "Excel File (*.xlsx)", "Excel File (*.xlsx)")
    except Exception as e:
        log.error(f"File Dialog Window Error: {e}")

    if not file_path[0]:
        log.info("User aborted dialog")
        return

    log.info(f"User selected path: {file_path[0]} -> Extension: {file_path[1]}")

    try:
        #loop through list of dicts, treat every element as seperate table in excel sheet
        for subsection, contents in data.items():
            #If nested list of elements get index number      
            table_index = range(len(contents)) if isinstance(contents,list) else [0]

            dataframe = pd.DataFrame(contents, index=table_index)
            dataframe.to_excel(f"{subsection}.xlsx")
    except Exception as e:
        log.error(f"Excel Creation failed: {e}")

    return