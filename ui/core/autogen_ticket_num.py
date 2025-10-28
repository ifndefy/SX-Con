from services.get_max_value import get_max_value


def autogen_ticket_num():
    ticket_num = str(get_max_value("Consignments", "ticket_num") + 1)
    return ticket_num