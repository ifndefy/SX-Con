import pandas as pd
import openpyxl
from pathlib import Path
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
        #Create Empty List to store dataframes
        dataframes = []
        #df_titles = [] --Currently ununsed, might come back to add table titles 

        #loop through list of dicts, treat every element as seperate table in excel sheet, collect in dataframe list
        for subsection, contents in data.items():
            #If nested list of elements get index number      
            table_index = range(len(contents)) if isinstance(contents,list) else [0]
            dataframes.append(pd.DataFrame(contents, index=table_index))
            #df_titles.append(f"{subsection}")
        
        sheet = Path(file_path[0]).name
        vpadding = 2

        with pd.ExcelWriter(file_path[0], "openpyxl") as excel_writer:
            dataframes[0].to_excel(excel_writer, 
                                   sheet_name = sheet, 
                                   index_col = False)
            for x in range(1, len(dataframes)):
                dataframes[x].to_excel(excel_writer, 
                                       sheet_name = sheet, 
                                       startrow = excel_writer.sheets[sheet].max_row + vpadding, 
                                       index_col = False)

        #Resize columns to avoid cutoffs + potential additional styling
        excel_file = openpyxl.load_workbook(file_path[0])
        excel_sheet = excel_file[sheet]

        for column in excel_sheet.columns:
            excel_sheet.column_dimensions[column[0].column_letter].auto_size = True

        excel_file.save(file_path[0])
    except Exception as e:
        log.error(f"Excel Creation failed: {e}")
    
    return