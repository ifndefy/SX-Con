import pandas as pd

def generate_excel(data):
    for subsection, contents in data.items():      
        table_index = range(len(contents)) if isinstance(contents,list) else [0]

        dataframe = pd.DataFrame(contents, index=table_index)
        dataframe.to_excel(f"{subsection}.xlsx")

    pass