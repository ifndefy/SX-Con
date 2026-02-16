from PyQt6.QtWidgets import QPushButton

class ExcelButton(QPushButton):
    def __init__(self, form_gatherer, export_impl, name = None, parent = None):
        super().__init__(name, parent)
        self.link_export_function(export_impl)
        self.link_gather_function(form_gatherer)
        self.clicked.connect(self.exec_function)

    def link_export_function(self, function):
        self.export_func = function

    def link_gather_function(self, function):
        self.gather_func = function

    def exec_function(self):
        if not self.gather_func:
            pass

        data = self.gather_func()
        
        if not self.export_func:
            pass

        self.export_func(data)