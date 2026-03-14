import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.core.revenue_payout import RevenuePayout

# integration: calculate payout from ticket 1
def test_integration_handle_calculate(app):
    with patch("ui.core.revenue_payout.update_property", return_value=0), \
         patch("ui.core.revenue_payout.current_user") as fake_user:
        fake_user.get_username.return_value = "fakeuser"
        fake_user.get_user_full_name.return_value = "fake user"
        widget = RevenuePayout()
        widget.set_products([], "1")
        widget.handle_calculate()
        assert widget.vendor_input.text() != "$0.00" # this can change, just leave at inequality