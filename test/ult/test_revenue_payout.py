import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from ui.core.revenue_payout import RevenuePayout


def test_widget_exists(app):
    widget = RevenuePayout()
    assert widget is not None

def test_fields_start_at_zero(app):
    widget = RevenuePayout()
    assert widget.vendor_input.text() == "$0.00"
    assert widget.super_x_input.text() == "$0.00"

def test_get_payout_data_should_return_zero(app):
    widget = RevenuePayout()
    data = widget.get_payout_data()
    assert data["vendor"] == 0.0
    assert data["super_x"] == 0.0

def test_get_payout_data_after_recalculate(app):
    widget = RevenuePayout()
    widget.vendor_input.setText("$7.00")
    widget.super_x_input.setText("$3.00")
    data = widget.get_payout_data()
    assert data["vendor"] == 7.00
    assert data["super_x"] == 3.00