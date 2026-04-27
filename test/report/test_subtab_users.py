import pytest

from PyQt6.QtTest import QTest
from unittest.mock import patch

from handlers.api_handler import APIHandler
from services.connect_database import db_connection
from ui.tabs.subtabs import UsersTab

from PyQt6.QtWidgets import QApplication, QPushButton
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox


@pytest.fixture
def users_tab(app):
    api = APIHandler()
    yield UsersTab(api, db_connection)

@pytest.fixture
def create_user_dialog(app, users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    assert tab.create_btn is not None, "Expected Create New User button to exist"

    with patch("PyQt6.QtWidgets.QDialog.exec", return_value=None):
        tab.create_btn.click()
        QApplication.processEvents()
        QTest.qWait(100)

        popup = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, QDialog):
                popup = w

    return popup

@pytest.fixture
def create_user_fields(app, create_user_dialog):
    popup = create_user_dialog
    QApplication.processEvents()
    QTest.qWait(50)

    buttons = popup.findChildren(QPushButton)
    create_btn = buttons[0]
    cancel_btn = buttons[1]

    fields = {
        "username_field": popup.findChild(QLineEdit, "username_input"),
        "first_name_field": popup.findChild(QLineEdit, "first_name_input"),
        "last_name_field": popup.findChild(QLineEdit, "last_name_input"),
        "password_field": popup.findChild(QLineEdit, "password_input"),
        "question1_field": popup.findChild(QComboBox, "question1"),
        "response1_field": popup.findChild(QLineEdit, "response1"),
        "question2_field": popup.findChild(QComboBox, "question2"),
        "response2_field": popup.findChild(QLineEdit, "response2"),
        "admin_question_field": popup.findChild(QComboBox, "admin_question"),
        "create_btn": create_btn,
        "cancel_btn": cancel_btn
    }
    return fields


def test_fields_exist(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    assert tab.user_id_input is not None, "Expected User ID field to exist"
    assert tab.username_input is not None, "Expected Username field to exist"
    assert tab.last_consignment_input is not None, "Expected Last Consignment field to exist"
    assert tab.first_name_input is not None, "Expected First Name field to exist"
    assert tab.last_name_input is not None, "Expected First Name field to exist"
    assert tab.admin_field is not None, "Expected Admin Field to exist"


def test_buttons_exist(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    assert tab.create_btn is not None, "Expected Create Button field to exist"
    assert tab.clear_btn is not None, "Expected Clear Button field to exist"
    assert tab.search_btn is not None, "Expected Search Button field to exist"


def test_id_input(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.user_id_input, "1")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.user_id_input.text() == '1', "Expected User ID field to accept single-digit integer input"

    QTest.keyClicks(tab.user_id_input, "2")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.user_id_input.text() == '12', "Expected User ID field to accept 2 digit integer input"

    QTest.keyClicks(tab.user_id_input, "3")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.user_id_input.text() == '123', "Expected User ID field to accept 3 digit integer input"

    QTest.keyClicks(tab.user_id_input, "4")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.user_id_input.text() == '1234', "Expected User ID field to accept 4 digit integer input"

    QTest.keyClicks(tab.user_id_input, "5")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.user_id_input.text() == '1234', "Expected User ID field to only accept input up to 4 digits long"


def test_username_input(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "user")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.username_input.text() == "user", "Expected username field to accept valid input"

    QTest.keyClicks(tab.username_input, "123")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.username_input.text() == "user", "Expected username field to reject numeric input"

    QTest.keyClicks(tab.username_input, "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.username_input.text() == "user", "Expected username field to reject special characters"


def test_first_name_input(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.first_name_input, "first")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.first_name_input.text() == "first", "Expected first name field to accept valid input"

    QTest.keyClicks(tab.first_name_input, "123")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.first_name_input.text() == "first", "Expected first name field to reject numeric input"

    QTest.keyClicks(tab.first_name_input, "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.first_name_input.text() == "first", "Expected first name field to reject special characters"


def test_last_name_input(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.last_name_input, "last")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.last_name_input.text() == "last", "Expected last name field to accept valid input"

    QTest.keyClicks(tab.last_name_input, "123")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.last_name_input.text() == "last", "Expected last name field to reject numeric input"

    QTest.keyClicks(tab.last_name_input, "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.last_name_input.text() == "last", "Expected last name field to reject special characters"


def test_last_consignment_input(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.last_consignment_input, "01")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.last_consignment_input.text() == "01", "Expected last consignment field to accept valid input"

    QTest.keyClicks(tab.last_consignment_input, "abc")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.last_consignment_input.text() == "01abc", "Expected last consignment field to accept numeric input"

    QTest.keyClicks(tab.last_consignment_input, "!@#$%^&*()-_=+[{]}\\|;:")
    QApplication.processEvents()
    QTest.qWait(10)
    assert tab.last_consignment_input.text() == "01abc!@#$%^&*()-_=+[{]}\\|;:", "Expected last consignment field to accept special characters"


def test_admin_input(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    admin_field = tab.admin_field

    admin_field.setCurrentIndex(-1)
    QApplication.processEvents()
    QTest.qWait(10)
    assert admin_field.currentText() == "", "Expected an out of bounds index for the admin field to have a blank selection"

    admin_field.setCurrentIndex(999)
    QApplication.processEvents()
    QTest.qWait(10)
    assert admin_field.currentText() == "", "Expected an out of bounds index for the admin field to have a blank selection"

    admin_field.setCurrentIndex(0)
    QApplication.processEvents()
    QTest.qWait(10)
    assert admin_field.currentText() in ["True", "False"], "Expected the first option of the admin field to be either True or False"

    admin_field.setCurrentIndex(1)
    QApplication.processEvents()
    QTest.qWait(10)
    assert admin_field.currentText() in ["True", "False"], "Expected the second option of the admin field to be either True or False"


def test_users_layout(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    results_count = tab.users_layout.count()
    assert results_count > 0, "Expected results to display for a blank search"

    for i in range(results_count):
        result = tab.users_layout.itemAt(i).widget()
        fields = result.findChildren(QLineEdit)

        user_id_field = fields[0]
        username_field = fields[1]
        last_consignment_field = fields[2]
        first_name_field = fields[3]
        last_name_field = fields[4]
        admin_field = result.findChild(QComboBox)

        assert user_id_field.text() is not None, "Expected result to have a user id"
        assert username_field.text() is not None, "Expected result to have a username"
        assert last_consignment_field.text() is not None, "Expected result to have a last consignment"
        assert first_name_field.text() is not None, "Expected result to have a first name"
        assert last_name_field.text() is not None, "Expected result to have a last name"
        assert admin_field.currentText() in ['True','False'], "Expected result to have an admin value of either True or False"

        buttons = result.findChildren(QPushButton)
        assert len(buttons) == 2, "Expected 2 buttons for result"

        reset_password_button = buttons[0]
        edit_button = buttons[1]

        assert reset_password_button.text() == "Reset Password", "Expected first button for result to be 'Reset Password'"
        assert edit_button.text() == "Edit", "Expected second button for result to be 'Edit'"


def test_clear_button(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    results_count = tab.users_layout.count()
    assert results_count > 0, "Expected results to display for a blank search"

    tab.clear_btn.click()
    QApplication.processEvents()
    QTest.qWait(50)

    assert tab.users_layout.count() == 0, "Expected results to clear / disappear after clicking the 'Clear' button"


def test_search_filters_results(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "user")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    results_count = tab.users_layout.count()
    assert results_count >= 0, "Expected at least one result for search on username 'user'"

    for i in range(results_count):
        result = tab.users_layout.itemAt(i).widget()
        username_field = result.findChildren(QLineEdit)[1]

        assert "user" in username_field.text().lower(), "Expected search to properly filter results"


def test_search_no_results(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "zzzzzzzzzz")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    assert tab.users_layout.count() == 0, "Expected no search results for search on username 'zzzzzzzzzz'"


def test_edit_button_read_only(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    results_count = tab.users_layout.count()
    assert results_count > 0, "Expected results to display for a blank search"

    for i in range(results_count):
        result = tab.users_layout.itemAt(i).widget()
        fields = result.findChildren(QLineEdit)

        user_id_field = fields[0]
        username_field = fields[1]
        last_consignment_field = fields[2]
        first_name_field = fields[3]
        last_name_field = fields[4]
        admin_field = result.findChild(QComboBox)

        buttons = result.findChildren(QPushButton)
        reset_password_button = buttons[0]
        edit_button = buttons[1]

        assert user_id_field.isReadOnly(), "Expected user id field to be read-only"
        assert username_field.isReadOnly(), "Expected username field to be read-only"
        assert last_consignment_field.isReadOnly(), "Expected last consignment field to be read-only"
        assert first_name_field.isReadOnly(), "Expected first name field to be read-only"
        assert last_name_field.isReadOnly(), "Expected last name field to be read-only"
        assert not admin_field.isEnabled(), "Expected admin field to be read-only"

        edit_button.click()
        QApplication.processEvents()
        QTest.qWait(50)

        assert user_id_field.isReadOnly(), "Expected user id field to stay read-only after clicking edit button"
        assert last_consignment_field.isReadOnly(), "Expected last consignment field to stay ready-only after clicking edit button"

        assert not username_field.isReadOnly(), "Expected username field to be editable after clicking edit button"
        assert not first_name_field.isReadOnly(), "Expected first name field to be editable after clicking edit button"
        assert not last_name_field.isReadOnly(), "Expected last name field to be editable after clicking edit button"
        assert admin_field.isEnabled(), "Expected admin field to be editable after clicking edit button"

        edit_button.click()
        QApplication.processEvents()
        QTest.qWait(50)

        assert user_id_field.isReadOnly(), "Expected user id field to remain read-only after clicking edit button again"
        assert username_field.isReadOnly(), "Expected username field to become read-only after clicking edit button again"
        assert last_consignment_field.isReadOnly(), "Expected last consignment field to remain read-only after clicking edit button again"

        assert first_name_field.isReadOnly(), "Expected first name field to become read-only after clicking edit button again"
        assert last_name_field.isReadOnly(), "Expected last name field to become read-only after clicking edit button again"
        assert not admin_field.isEnabled(), "Expected admin field to be read-only after clicking edit button"


def test_edit_button_change_values(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    results_count = tab.users_layout.count()
    assert results_count > 0, "Expected results to display for a blank search"

    count = min(results_count, 2)

    for i in range(count):
        result = tab.users_layout.itemAt(i).widget()
        fields = result.findChildren(QLineEdit)

        username_field = fields[1]
        first_name_field = fields[3]
        last_name_field = fields[4]

        edit_button = result.findChildren(QPushButton)[1]

        edit_button.click()
        QApplication.processEvents()
        QTest.qWait(50)

        original_username = username_field.text()
        original_first_name = first_name_field.text()
        original_last_name = last_name_field.text()

        QTest.keyClicks(username_field, "O")
        QTest.keyClicks(first_name_field, "O")
        QTest.keyClicks(last_name_field, "O")
        QApplication.processEvents()
        QTest.qWait(50)

        assert username_field.text() == original_username + "O", "Expected to be able to type in username field"
        assert first_name_field.text() == original_first_name + "O", "Expected to be able to type in first name field"
        assert last_name_field.text() == original_last_name + "O", "Expected to be able to type in last name field"

        edit_button.click()
        QApplication.processEvents()
        QTest.qWait(50)

        assert username_field.text() == original_username + "O", "Expected to be able to save edits to username field"
        assert first_name_field.text() == original_first_name + "O", "Expected to be able to save edits to first name field"
        assert last_name_field.text() == original_last_name + "O", "Expected to be able to save edits to last name field"

        edit_button.click()
        QApplication.processEvents()
        QTest.qWait(50)

        username_field.setText(original_username)
        first_name_field.setText(original_first_name)
        last_name_field.setText(original_last_name)

        edit_button.click()
        QApplication.processEvents()
        QTest.qWait(50)

        assert username_field.text() == original_username, "Expected to be able to change username back to original"
        assert first_name_field.text() == original_first_name, "Expected to be able to change first name back to original"
        assert last_name_field.text() == original_last_name, "Expected to be able to change last name back to original"


def test_reset_password_button_executes(users_tab):
    tab = users_tab
    QApplication.processEvents()
    QTest.qWait(50)

    QTest.keyClicks(tab.username_input, "")
    tab.search_btn.click()
    QApplication.processEvents()
    QTest.qWait(100)

    result = tab.users_layout.itemAt(0).widget()
    reset_btn = result.findChildren(QPushButton)[0]

    with patch("ui.tabs.subtabs.users.PasswordChangeDialog") as mock_dialog:
        reset_btn.click()
        QApplication.processEvents()
        QTest.qWait(50)
        assert mock_dialog.called, "Expected password change dialog to be created"

