import pytest
from unittest.mock import MagicMock
from PyQt6.QtWidgets import QComboBox
from PyQt6.QtWidgets import QLineEdit
from ui.core.revenue_by_product_type import RevenueByProdType

def fake_data_entries(prod_type, price, qty, rate):
    combo = QComboBox()
    combo.addItem(prod_type)
    combo.setCurrentText(prod_type)
    price_field = QLineEdit()
    price_field.setText(price)
    qty_field = QLineEdit()
    qty_field.setText(qty)
    rate_field = QLineEdit()
    rate_field.setText(rate)
    return {
        'product_type': combo,
        'price': price_field,
        'quantity': qty_field,
        'rate': rate_field
    }

def test_widget_exists(app):
    widget = RevenueByProdType()
    assert widget is not None

def test_generate_revenue_data_single_type(app):
    widget = RevenueByProdType()
    sections = [fake_data_entries("Hot Food", "10.00", "1", "30")]
    totals = widget.generate_revenue_data(sections)
    assert totals["Hot Food"] == 7.00
    assert totals["General"] == 0.0
    assert totals["Produce"] == 0.0
    assert totals["Total"] == 7.00

def test_generate_revenue_data_two_type(app):
    widget = RevenueByProdType()
    sections = [fake_data_entries("Hot Food", "10.00", "1", "30"),
                fake_data_entries("General", "10.00", "1", "25")]
    totals = widget.generate_revenue_data(sections)
    assert totals["Hot Food"] == 7.00
    assert totals["General"] == 7.50
    assert totals["Produce"] == 0.0
    assert totals["Total"] == 14.50

def test_generate_revenue_data_all_type(app):
    widget = RevenueByProdType()
    sections = [fake_data_entries("Hot Food", "10.00", "1", "30"),
                fake_data_entries("General", "10.00", "1", "25"),
                fake_data_entries("Produce", "10.00", "1", "25")]
    totals = widget.generate_revenue_data(sections)
    assert totals["Hot Food"] == 7.00
    assert totals["General"] == 7.50
    assert totals["Produce"] == 7.50
    assert totals["Total"] == 22.00

def test_generate_revenue_data_empty(app):
    widget = RevenueByProdType()
    totals = widget.generate_revenue_data([])
    assert totals["Hot Food"] == 0.0
    assert totals["General"] == 0.0
    assert totals["Produce"] == 0.0
    assert totals["Total"] == 0.0

def test_update_display_works(app):
    widget = RevenueByProdType()
    totals = {"Hot Food": 7.00, "General": 7.50, "Produce": 7.50, "Total": 22.00}
    widget.update_display_values(totals)
    assert widget.totals['Hot Food'] == 7.00
    assert widget.totals['General'] == 7.50
    assert widget.totals['Produce'] == 7.50
    assert widget.totals["Total"] == 22.00

def test_clear_works(app):
    widget = RevenueByProdType()
    widget.totals = {"Hot Food": 7.00, "General": 7.50, "Produce": 7.50, "Total": 22.00}
    widget.clear()
    assert widget.totals['Hot Food'] == 0.0
    assert widget.totals['General'] == 0.0
    assert widget.totals['Produce'] == 0.0
    assert widget.totals["Total"] == 0.0