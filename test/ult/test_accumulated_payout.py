from unittest.mock import patch

from ui.core.accumulated_payout import AccumulatedPayout


def test_setup_ui(app):
    widget = AccumulatedPayout()
    assert widget.signed_vendor.text() == "$0.00", "Expected initial value for signed_vendor to be 0"
    assert widget.signed_super_x.text() == "$0.00", "Expected initial value for signed_super_x to be 0"
    assert widget.accumulated_vendor.text() == "$0.00", "Expected initial value for accumulated_vendor to be 0"
    assert widget.accumulated_super_x.text() == "$0.00", "Expected initial value for accumulated_super_x to be 0"
    assert widget.remaining_vendor.text() == "$0.00", "Expected initial value for remaining_vendor to be 0"
    assert widget.remaining_super_x.text() == "$0.00", "Expected initial value for remaining_super_x to be 0"


def test_load_with_accumulated(app):
    widget = AccumulatedPayout()
    fake_consignment = {
        'revenue': {
            'accumulated': {
                'signed_vendor': 88.0,
                'signed_super_x': 32.0,
                'vendor': 7.0,
                'super_x': 3.0
            }
        }
    }
    with patch("ui.core.accumulated_payout.get_item", return_value=fake_consignment):
        widget.load("184") # fake consignment that this data was copied from

    assert widget.signed_vendor.text() == "$88.00", "Expected value for signed_vendor to be 88"
    assert widget.signed_super_x.text() == "$32.00", "Expected value for signed_super_x to be 32"
    assert widget.accumulated_vendor.text() == "$7.00", "Expected value for accumulated_vendor to be 7"
    assert widget.accumulated_super_x.text() == "$3.00", "Expected value for accumulated_super_x to be 3"
    assert widget.remaining_vendor.text() == "$81.00", "Expected value for remaining_vendor to be 81"
    assert widget.remaining_super_x.text() == "$29.00", "Expected value for remaining_super_x to be 29"


def test_load_without_accumulated(app):
    widget = AccumulatedPayout()
    fake_consignment = {
        'revenue': {
            'shared': [
                {'vendor': 22, 'percentage': '25%', 'super_x': 8},
                {'vendor': 44, 'percentage': '50%', 'super_x': 16},
                {'vendor': 66, 'percentage': '75%', 'super_x': 24},
                {'vendor': 88, 'percentage': '100%', 'super_x': 32}
            ],
            'accumulated': {}
        }
    }
    with patch("ui.core.accumulated_payout.get_item", return_value=fake_consignment):
        widget.load("184")

    assert widget.signed_vendor.text() == "$88.00", "Expected value for signed_vendor to be 88"
    assert widget.signed_super_x.text() == "$32.00", "Expected value for signed_super_x to be 32"
    assert widget.accumulated_vendor.text() == "$0.00", "Expected initial value for accumulated_vendor to be 0.00"
    assert widget.accumulated_super_x.text() == "$0.00", "Expected initial value for accumulated_super_x to be 0.00"
    assert widget.remaining_vendor.text() == "$88.00", "Expected value for remaining_vendor to be 88"
    assert widget.remaining_super_x.text() == "$32.00", "Expected value for remaining_super_x to be 32"