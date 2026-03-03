"""
tests if instances of format_price is correctly placing the decimal place
"""
import sys
from PyQt6.QtWidgets import QApplication

from ui.core.format_price import PriceField

def test_format_price():
    app = QApplication(sys.argv)
    test_price_field = PriceField()

    test_price_field.setText("1")
    test_price_field.textEdited.emit("1")
    assert test_price_field.text() == "$1"

    test_price_field.setText("")
    test_price_field.textEdited.emit("")
    assert test_price_field.text() == "$0"

    test_price_field.setText("12")
    test_price_field.textEdited.emit("12")
    assert test_price_field.text() == "$12"

    test_price_field.setText("1")
    test_price_field.textEdited.emit("1")
    assert test_price_field.text() == "$1"

    test_price_field.setText("123")
    test_price_field.textEdited.emit("123")
    assert test_price_field.text() == "$1.23"

    test_price_field.setText("12")
    test_price_field.textEdited.emit("12")
    assert test_price_field.text() == "$12"

    test_price_field.setText("1234")
    test_price_field.textEdited.emit("1234")
    assert test_price_field.text() == "$12.34"

    test_price_field.setText("123")
    test_price_field.textEdited.emit("123")
    assert test_price_field.text() == "$1.23"

    test_price_field.setText("12345")
    test_price_field.textEdited.emit("12345")
    assert test_price_field.text() == "$123.45"

    test_price_field.setText("1234")
    test_price_field.textEdited.emit("1234")
    assert test_price_field.text() == "$12.34"

    test_price_field.setText("123456")
    test_price_field.textEdited.emit("123456")
    assert test_price_field.text() == "$1234.56"

    test_price_field.setText("12345")
    test_price_field.textEdited.emit("12345")
    assert test_price_field.text() == "$123.45"

    test_price_field.setText("1234567")
    test_price_field.textEdited.emit("1234567")
    assert test_price_field.text() == "$12345.67"

    test_price_field.setText("123456")
    test_price_field.textEdited.emit("123456")
    assert test_price_field.text() == "$1234.56"

    test_price_field.setText("12345678")
    test_price_field.textEdited.emit("12345678")
    assert test_price_field.text() == "$123456.78"

    test_price_field.setText("1234567")
    test_price_field.textEdited.emit("1234567")
    assert test_price_field.text() == "$12345.67"

    test_price_field.setText("123456789")
    test_price_field.textEdited.emit("123456789")
    assert test_price_field.text() == "$1234567.89"

    test_price_field.setText("12345678")
    test_price_field.textEdited.emit("12345678")
    assert test_price_field.text() == "$123456.78"

    test_price_field.setText("1234567890")
    test_price_field.textEdited.emit("1234567890")
    assert test_price_field.text() == "$12345678.90"

    test_price_field.setText("123456789")
    test_price_field.textEdited.emit("123456789")
    assert test_price_field.text() == "$1234567.89"