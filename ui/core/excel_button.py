from PyQt6.QtWidgets import QPushButton

import utils.logger.logger as log

class ExcelButton(QPushButton):
    ''' 
    :purpose: Extends the QPushButton class to add callbacks to form specific data gathering and export functions
    :return: None
    :author: Maksym Komarov
    '''
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
        ''' 
        :purpose: Gathers and exports the form data into an excel file. 'Clicked' event callback.
        :return: None
        :author: Maksym Komarov
        '''      
        if not self.gather_func:
            #Error out here
            log.error(f"Failed to execute gather function for excel button")
            return

        data = self.gather_func()
        
        if not self.export_func:
            #Error out here
            log.error(f"Failed to execute export function for excel button")
            return

        self.export_func(data)