import utils.logger.logger as log
import pandas as pd

def get_average_price(price_data: list):
    """
    :Gets the average item price from a list containing all price data for a product
    :args- price_data = list of dicts that contain the previous sales info 
    :returns aggregate mean as float on success, -1 on fail
    """
    if price_data is None:
        log.error("price_data cannot be NoneType")
        return -1
    elif not price_data:
        log.error("price_data is empty")
        return -1
    
    dataframe = pd.DataFrame(price_data)

    if 'price' not in dataframe.columns:
        log.error("no price field found in price_data")
        return -1
    
    average = dataframe['price'].mean()
    print(average)

    return average