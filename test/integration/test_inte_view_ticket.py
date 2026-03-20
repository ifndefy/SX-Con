import pytest
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from services.get_item_by_property import get_item_by_property
from ui.core.view_ticket import ViewTicket


@pytest.fixture
def ticket_data():
    ticket_id = 1
    data = get_item_by_property("Consignments", "consignment", "consignment_id", ticket_id)
    return {
        'ticket_id': ticket_id,
        'ticket_data': data,
        'ticket_section': {
            'details_container': QWidget(),
            'product_details_layout': QVBoxLayout()
        },
        'ticket_details': {'ticket_data': data}
    }

def test_integration_products_show_up(app, ticket_data):
    view = ViewTicket(ticket_data['ticket_id'])
    view.setup_ui(ticket_data['ticket_section'], ticket_data['ticket_details'])
    assert len(view.product_widgets) > 0, "Expected to find at least one product widget"

def test_integration_revenue_shows_up(app, ticket_data):
    view = ViewTicket(ticket_data['ticket_id'])
    view.setup_ui(ticket_data['ticket_section'], ticket_data['ticket_details'])
    assert ticket_data['ticket_data'].get('revenue') is not None, "Expected to find revenue data"