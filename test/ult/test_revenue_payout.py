import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.core.revenue_payout import RevenuePayout


def test_widget_exists(app):
    widget = RevenuePayout()
    assert widget is not None, "Expected RevenuePayout widget to exist"

def test_fields_start_at_zero(app):
    widget = RevenuePayout()
    assert widget.vendor_input.text() == "$0.00", "Expected initial values to be $0.00"
    assert widget.super_x_input.text() == "$0.00", "Expected initial values to be $0.00"

def test_get_payout_data_should_return_zero(app):
    widget = RevenuePayout()
    data = widget.get_payout_data()
    assert data["vendor"] == 0.0, "Expected payout data to be $0.0 on retrieval before actions"
    assert data["super_x"] == 0.0, "Expected payout data to be $0.0 on retrieval before actions"

def test_get_payout_data_after_recalculate(app):
    widget = RevenuePayout()
    widget.vendor_input.setText("$7.00")
    widget.super_x_input.setText("$3.00")
    data = widget.get_payout_data()
    assert data["vendor"] == 7.00, "Expected payout data to be $7.00 on retrieval"
    assert data["super_x"] == 3.00, "Expected payout data to be $3.00 on retrieval"