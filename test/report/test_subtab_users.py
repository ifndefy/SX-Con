import pytest

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from unittest.mock import patch

from handlers.api_handler import APIHandler
from services.connect_database import db_connection
from ui.tabs import AdminSettingsTab
from ui.tabs.subtabs import UsersTab

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox



@pytest.fixture
def users_tab(app):
    api = APIHandler()
    yield UsersTab(api, db_connection)

@pytest.fixture
def create_user_dialog(app, users_tab):
    tab = users_tab
    assert tab.create_btn is not None, "Expected Create New User button to exist"

    with patch("PyQt6.QtWidgets.QDialog.exec", return_value=None):
        tab.create_btn.click()

        popup = None
        for w in QApplication.topLevelWidgets():
            if isinstance(w, QDialog):
                popup = w

    return popup

@pytest.fixture
def create_user_fields(app, create_user_dialog):
    popup = create_user_dialog
    fields = {
        "username_field" : popup.findChild(QLineEdit, "username_input"),
        "first_name_field" : popup.findChild(QLineEdit, "first_name_input"),
        "last_name_field" : popup.findChild(QLineEdit, "last_name_input"),
        "password_field" : popup.findChild(QLineEdit, "password_input"),
        "question1_field" : popup.findChild(QComboBox, "question1"),
        "response1_field" : popup.findChild(QLineEdit, "response1"),
        "question2_field" : popup.findChild(QComboBox, "question2"),
        "response2_field" : popup.findChild(QLineEdit, "response2"),
        "admin_question_field" : popup.findChild(QComboBox, "admin_question"),
    }
    return fields




def test_fields_exist(users_tab):
    tab = users_tab
    assert tab.user_id_input is not None, "Expected User ID field to exist"
    assert tab.username_input is not None, "Expected Username field to exist"
    assert tab.last_consignment_input is not None, "Expected Last Consignment field to exist"

    assert tab.first_name_input is not None, "Expected First Name field to exist"
    assert tab.last_name_input is not None, "Expected First Name field to exist"
    assert tab.admin_field is not None, "Expected Admin Field to exist"


def test_buttons_exist(users_tab):
    tab = users_tab

    assert tab.create_btn is not None, "Expected Create Button field to exist"
    assert tab.clear_btn is not None, "Expected Clear Button field to exist"
    assert tab.search_btn is not None, "Expected Search Button field to exist"

def test_id_input(users_tab):
    tab = users_tab

    QTest.keyClicks(tab.user_id_input, "1")
    assert tab.user_id_input.text() == '1', "Expected User ID field to accept single-digit integer input"
    QTest.keyClicks(tab.user_id_input, "2")
    assert tab.user_id_input.text() == '12', "Expected User ID field to accept 2 digit integer input"
    QTest.keyClicks(tab.user_id_input, "3")
    assert tab.user_id_input.text() == '123', "Expected User ID field to accept 3 digit integer input"
    QTest.keyClicks(tab.user_id_input, "4")
    assert tab.user_id_input.text() == '1234', "Expected User ID field to accept 4 digit integer input"

    QTest.keyClicks(tab.user_id_input, "5")
    assert tab.user_id_input.text() == '1234', "Expected User ID field to only accept input up to 4 digits long"

def test_username_input(users_tab):
    tab = users_tab

    QTest.keyClicks(tab.username_input, "user")
    assert tab.username_input.text() == "user", "Expected username field to accept valid input"

    QTest.keyClicks(tab.username_input, "123")
    assert tab.username_input.text() == "user", "Expected username field to reject numeric input"

    QTest.keyClicks(tab.username_input, "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?")
    assert tab.username_input.text() == "user", "Expected username field to reject special characters"

def test_first_name_input(users_tab):
    tab = users_tab

    QTest.keyClicks(tab.first_name_input, "first")
    assert tab.first_name_input.text() == "first", "Expected first name field to accept valid input"

    QTest.keyClicks(tab.first_name_input, "123")
    assert tab.first_name_input.text() == "first", "Expected first name field to reject numeric input"

    QTest.keyClicks(tab.first_name_input, "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?")
    assert tab.first_name_input.text() == "first", "Expected first name field to reject special characters"

def test_last_name_input(users_tab):
    tab = users_tab

    QTest.keyClicks(tab.last_name_input, "last")
    assert tab.last_name_input.text() == "last", "Expected last name field to accept valid input"

    QTest.keyClicks(tab.last_name_input, "123")
    assert tab.last_name_input.text() == "last", "Expected last name field to reject numeric input"

    QTest.keyClicks(tab.last_name_input, "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?")
    assert tab.last_name_input.text() == "last", "Expected last name field to reject special characters"


def test_last_consignment_input(users_tab):
    tab = users_tab

    QTest.keyClicks(tab.last_consignment_input, "01")
    assert tab.last_consignment_input.text() == "01", "Expected last consignment field to accept valid input"

    QTest.keyClicks(tab.last_consignment_input, "abc")
    assert tab.last_consignment_input.text() == "01abc", "Expected last consignment field to accept numeric input"

    QTest.keyClicks(tab.last_consignment_input, "!@#$%^&*()-_=+[{]}\\|;:")
    assert tab.last_consignment_input.text() == "01abc!@#$%^&*()-_=+[{]}\\|;:", "Expected last consignment field to accept special characters"


def test_admin_input(users_tab):
    tab = users_tab

    admin_field = tab.admin_field

    admin_field.setCurrentIndex(-1)
    assert admin_field.currentText() == "", "Expected an out of bounds index for the admin field to have a blank selection"
    admin_field.setCurrentIndex(999)
    assert admin_field.currentText() == "", "Expected an out of bounds index for the admin field to have a blank selection"

    admin_field.setCurrentIndex(0)
    assert admin_field.currentText() in ["True", "False"], "Expected the first option of the admin field to be either True or False"
    admin_field.setCurrentIndex(1)
    assert admin_field.currentText() in ["True", "False"], "Expected the second option of the admin field to be either True or False"


def test_users_section(users_tab):
    tab = users_tab

    # initial size is 0
    print("\nlist size = " + str(len(tab.users_section)))

    # section / results list
    print("\nsection type = " + tab.users_section.__class__.__name__)
    # list in UI form
    print("\nlayout type = " + tab.users_layout.__class__.__name__)



    print("current input fields:")

    print(tab.user_id_input.text())
    print(tab.username_input.text())
    print(tab.first_name_input.text())
    print(tab.last_name_input.text())
    print(tab.last_consignment_input.text())
    print(tab.admin_field.currentText())

    print("end of input fields")


    tab.search_btn.click()
    QTest.qWait(400)

    print("length = " + str(len(tab.users_section)))


    print("ui layout = " + str(tab.users_layout.count()))

    #assert len(tab.users_section) > 1, "Expected user sections for a search"


    #print("\ntype of section elements: " + tab.users_section[1].__class__.__name__)








### Tests for the Create New User prompt/window
def test_create_user_button_fields(create_user_fields):
    fields = create_user_fields
    username_field = fields["username_field"]
    first_name_field = fields["first_name_field"]
    last_name_field = fields["last_name_field"]
    password_field = fields["password_field"]
    question1_field = fields["question1_field"]
    question2_field = fields["question2_field"]
    response1_field = fields["response1_field"]
    response2_field = fields["response2_field"]
    admin_question_field = fields["admin_question_field"]

    assert username_field != None, "Expected Username field to exist"
    assert first_name_field != None, "Expected First name field to exist"
    assert last_name_field != None, "Expected Lastname field to exist"
    assert password_field != None, "Expected Password field to exist"
    assert question1_field != None, "Expected Question1 field to exist"
    assert response1_field != None, "Expected Response1 field to exist"
    assert question2_field != None, "Expected Question2 field to exist"
    assert response2_field != None, "Expected Response2 field to exist"
    assert admin_question_field != None, "Expected Admin Question field to exist"



def test_create_user_username_input(create_user_fields):
    fields = create_user_fields
    username_field = fields["username_field"]

    #QTest.qWait(100)
    username_field.setText("")

    QTest.keyClicks(username_field, "username")
    assert username_field.text() == "username", "Expected username field to accept valid input"
    username_field.setText("")

    QTest.keyClicks(username_field, "123username123")
    assert username_field.text() == "username" ,"Expected username field constraints to reject/remove integers"
    username_field.setText("")

    QTest.keyClicks(username_field, "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"username")
    assert username_field.text() == "username", "Expected username field constraints to reject/remove special characters"
    username_field.setText("")

def test_create_user_first_name_input(create_user_fields):
    fields = create_user_fields
    first_name_field = fields["first_name_field"]

    first_name_field.setText("")

    QTest.keyClicks(first_name_field, "first")
    assert first_name_field.text() == "first", "Expected First name field to accept valid input"
    first_name_field.setText("")

    QTest.keyClicks(first_name_field, "123first123")
    assert first_name_field.text() == "first" ,"Expected First name field constraints to reject/remove integers"
    first_name_field.setText("")

    QTest.keyClicks(first_name_field, "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"first")
    assert first_name_field.text() == "first", "Expected First name field constraints to reject/remove special characters"
    first_name_field.setText("")

def test_create_user_last_name_input(create_user_fields):
    fields = create_user_fields
    last_name_field = fields["last_name_field"]

    last_name_field.setText("")

    QTest.keyClicks(last_name_field, "last")
    assert last_name_field.text() == "last", "Expected Last name field to accept valid input"
    last_name_field.setText("")

    QTest.keyClicks(last_name_field, "123last123")
    assert last_name_field.text() == "last" ,"Expected Last name field constraints to reject/remove integers"
    last_name_field.setText("")

    QTest.keyClicks(last_name_field, "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"last")
    assert last_name_field.text() == "last", "Expected Last name field constraints to reject/remove special characters"
    last_name_field.setText("")


def test_create_user_password_input(create_user_fields):
    fields = create_user_fields
    password_field = fields["password_field"]

    password_field.setText("")

    QTest.keyClicks(password_field, "pass")
    assert password_field.text() == "pass", "Expected Last name field to accept basic valid string input"
    password_field.setText("")

    QTest.keyClicks(password_field, "123pass123")
    assert password_field.text() == "123pass123" ,"Expected Last name field to accept input with digits"
    password_field.setText("")

    QTest.keyClicks(password_field, "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"pass ")
    assert password_field.text() == "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"pass ", "Expected Last name field to accept input with special characters and spaces"
    password_field.setText("")


def test_create_user_response1_input(create_user_fields):
    fields = create_user_fields
    response1_field = fields["response1_field"]

    response1_field.setText("")

    QTest.keyClicks(response1_field, "pass")
    assert response1_field.text() == "pass", "Expected Response 1 field to accept basic valid string input"
    response1_field.setText("")

    QTest.keyClicks(response1_field, "123pass123")
    assert response1_field.text() == "123pass123" ,"Expected Response 1 field to accept input with digits"
    response1_field.setText("")

    QTest.keyClicks(response1_field, "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"pass ")
    assert response1_field.text() == "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"pass ", "Expected Response 1 field to accept input with special characters and spaces"
    response1_field.setText("")

def test_create_user_response2_input(create_user_fields):
    fields = create_user_fields
    response2_field = fields["response2_field"]

    response2_field.setText("")

    QTest.keyClicks(response2_field, "pass")
    assert response2_field.text() == "pass", "Expected Response 2 field to accept basic valid string input"
    response2_field.setText("")

    QTest.keyClicks(response2_field, "123pass123")
    assert response2_field.text() == "123pass123" ,"Expected Response 2 field to accept input with digits"
    response2_field.setText("")

    QTest.keyClicks(response2_field, "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"pass ")
    assert response2_field.text() == "!@#$%^&*()_+=-{[}]|\:;'<,>.?/\"pass ", "Expected Response 2 field to accept input with special characters and spaces"
    response2_field.setText("")

def test_create_user_security_questions_inputs(create_user_fields):
    fields = create_user_fields
    question1_field = fields["question1_field"]
    question2_field = fields["question2_field"]

    question1_field.setCurrentIndex(-1)
    assert question1_field.currentText() == "", "Expected Question 1 to have a blank selection by default"

    question1_field.setCurrentIndex(0)
    assert question1_field.currentText() != "", "Expected Question 1 to have a valid selection"
    question1_field.setCurrentIndex(1)
    assert question1_field.currentText() != "", "Expected Question 1 to have a valid selection"
    question1_field.setCurrentIndex(2)
    assert question1_field.currentText() != "", "Expected Question 1 to have a valid selection"



    question2_field.setCurrentIndex(-1)
    assert question2_field.currentText() == "", "Expected Question 2 to have a blank selection by default"

    question2_field.setCurrentIndex(0)
    assert question2_field.currentText() != "", "Expected Question 2 to have a valid selection"
    question2_field.setCurrentIndex(1)
    assert question2_field.currentText() != "", "Expected Question 2 to have a valid selection"
    question2_field.setCurrentIndex(2)
    assert question2_field.currentText() != "", "Expected Question 2 to have a valid selection"


    question1_field.setCurrentIndex(-1)
    question1_field.setCurrentText("What was your first pet's name?")
    assert question1_field.currentText() != None, "Expected Question 1 selection to update upon entering exact selection text"
    assert question1_field.currentIndex() != -1, "Expected Question 1 index to update upon entering exact selection text"


    question2_field.setCurrentIndex(-1)
    question2_field.setCurrentText("What was your first pet's name?")
    assert question2_field.currentText() != None, "Expected Question 2 selection to update upon entering exact selection text"
    assert question2_field.currentIndex() != -1, "Expected Question 2 index to update upon entering exact selection text"


def test_create_user_admin_field(create_user_fields):
    fields = create_user_fields
    admin_field = fields["admin_question_field"]

    admin_field.setCurrentIndex(-1)
    assert admin_field.currentText() == "", "Expected an out of bounds index for the admin field to have a blank selection"
    admin_field.setCurrentIndex(999)
    assert admin_field.currentText() == "", "Expected an out of bounds index for the admin field to have a blank selection"

    admin_field.setCurrentIndex(0)
    assert admin_field.currentText() in ["True", "False"], "Expected the first option of the admin field to be either True or False"
    admin_field.setCurrentIndex(1)
    assert admin_field.currentText() in ["True", "False"], "Expected the second option of the admin field to be either True or False"







































