import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.core.revenue_payout import RevenuePayout

# integration: calculate payout from ticket 1
def test_integration_handle_calculate(app):
    fake_consignment = {
        'products': [
            {
                'product_id': 1,
                'product_type': 'Hot Food',
                'price': 10.00,
                'sold': 2,
                'rate': 30
            }
        ]
    }
    with patch("ui.core.revenue_payout.update_property", return_value=0), \
         patch("ui.core.revenue_payout.get_item", side_effect=[fake_consignment, fake_consignment]), \
         patch("ui.core.revenue_payout.current_user") as fake_user, \
         patch("ui.core.view_ticket.QMessageBox"), \
         patch("ui.core.revenue_payout.QMessageBox"):
        fake_user.get_username.return_value = "fakeuser"
        fake_user.get_user_full_name.return_value = "fake user"
        widget = RevenuePayout()
        widget.set_products([], "1")
        widget.handle_calculate()
        assert widget.vendor_input.text() == "$14.00", "Expected accurate calculations"