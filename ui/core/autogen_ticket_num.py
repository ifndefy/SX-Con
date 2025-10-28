from services.get_max_value import get_max_value


def autogen_ticket_num():
    """
    :purpose: returns the max value of ticket_num in Consignment table
    :return(s): string of 1 + max ticket_num from DB table "Consignments"
    :author(s): Joe Lee
    """
    ticket_num = str(get_max_value("Consignments", "ticket_num") + 1)
    return ticket_num