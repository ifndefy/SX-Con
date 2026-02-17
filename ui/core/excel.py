from PyQt6.QtWidgets import QPushButton

class ExcelButton(QPushButton):
    def __init__(self, form_gatherer, export_impl, path_func = None, name = None, parent = None):
        super().__init__(name, parent)
        self.link_export_function(export_impl)
        self.link_gather_function(form_gatherer)
        self.link_prompt_function(path_func)
        self.clicked.connect(self.exec_function)

    def link_prompt_function(self,function):
        self.path_func = function

    def link_export_function(self, function):
        self.export_func = function

    def link_gather_function(self, function):
        self.gather_func = function

    def exec_function(self):
        path = None
        
        if self.path_func:
            path = self.path_func()
            if not path:
                #Abort save
                return
        
        if not self.gather_func:
            #Error out here
            return

        data = self.gather_func()
        
        if not self.export_func:
            #Error out here
            return

        if path:
            self.export_func(data, path)
        else:
            self.export_func(data)