from PyQt6.QtWidgets import QWidget

from ui.prompts.view_history import ViewPayoutHistory


FAKE_DATA = [
    {
        'vendor': 7.0,
        'super_x': 3.0,
        'user': 'lee, Joe Lee',
        'datetime': '03/24/26 -- 10:27',
        'products': [
            {'product_id': 1, 'product_name': 'Hot Food', 'sold': 1, 'vendor': 7.0, 'super_x': 3.0}
        ],
        'grouped': [
            {'product_type': 'Hot Food', 'vendor': 7.0, 'super_x': 3.0}
        ]
    },
    {
        'vendor': 7.5,
        'super_x': 2.5,
        'user': 'lee, Joe Lee',
        'datetime': '03/24/26 -- 10:48',
        'products': [
            {'product_id': 2, 'product_name': 'General', 'sold': 1, 'vendor': 7.5, 'super_x': 2.5}
        ],
        'grouped': [
            {'product_type': 'General', 'vendor': 7.5, 'super_x': 2.5}
        ]
    }
]


def test_dialog_opens(app):
    parent = QWidget()
    dialog = ViewPayoutHistory(parent, FAKE_DATA, "184")
    assert dialog is not None, "Expected dialog to be opened"

def test_dialog_title(app):
    parent = QWidget()
    dialog = ViewPayoutHistory(parent, FAKE_DATA, "184")
    assert dialog.windowTitle() == "Payout History", "Expected windowTitle to be 'Payout History'"

def test_dialog_stores_payout_list(app):
    parent = QWidget()
    dialog = ViewPayoutHistory(parent, FAKE_DATA, "184")
    assert dialog.payout_list == FAKE_DATA, "Expected payout_list to be stored"

def test_dialog_empty_payout_list(app):
    parent = QWidget()
    dialog = ViewPayoutHistory(parent, [], "184")
    assert dialog is not None, "Expected dialog to open with empty payout list"

def test_dialog_single_payout(app):
    parent = QWidget()
    dialog = ViewPayoutHistory(parent, [FAKE_DATA[0]], "184")
    assert dialog.payout_list == [FAKE_DATA[0]], "Expected single payout entry"

def test_dialog_multiple_payouts(app):
    parent = QWidget()
    dialog = ViewPayoutHistory(parent, FAKE_DATA, "184")
    assert len(dialog.payout_list) == 2, "Expected 2 payout entries"