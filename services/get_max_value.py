from pathlib import Path

from services.connect_database import db_connection
from src import SPOT
import utils.logger.logger as log


def get_max_value(container_name, property_name):
    """
    :purpose: gets the max value of a property through the database if online or through local files if offline
    :param container_name: name of the container
    :param property_name: name of the property
    :return: max value of a property
    :author(s): Joe Lee
    """
    if not SPOT.OFFLINE:
        try:
            container = db_connection.connect(container_name)
        except Exception as e:
            log.error(f"Error connecting to container {container_name}: {e}")
            return -1

        try:
            query = f"SELECT VALUE MAX(c.{property_name}) FROM c"

            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True
            ))

            if items and items[0] is not None:
                return items[0]
            else:
                return 0
        except Exception as e:
            log.error(f"Error querying max value: {e}")
            return -1
    else:
        log.warning("OFFLINE - Unable to connect to Database. OFFLINE semantics used to generate ticket number")
        offline_tickets_dir = Path(__file__).parent.parent / 'utils' / 'OFFLINE_tickets'
        if not offline_tickets_dir.exists():
            return 0
        max_value = 0
        for file in offline_tickets_dir.iterdir():
            if file.is_file() and file.stem.startswith('OFFLINE_'):
                try:
                    ticket_num = int(file.stem.split('_')[1])
                    if ticket_num > max_value:
                        max_value = ticket_num
                except ValueError:
                    log.error(f"Error: Could not parse ticket number from {file}")
        if max_value > 0:
            return f"OFFLINE_{max_value}"
        else:
            return "OFFLINE_0"