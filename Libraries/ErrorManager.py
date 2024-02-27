# File: webserver.py
__author__ = "Gregori Bucher"
__copyright__ = "Gregori Bucher, 27.02.2024"
__version__ = "1.0"

from time import time


class ErrorManager:
    """
    class: ErrorManager
    Wird verwendet, um Exception Handling zu managen.
    """
    def __init__(self, retries: int = 3, reset_time: int = 3):
        self.error_cont = 1
        self.last_error = [0, 0]
        self.handlers = dict()
        self.retries = retries
        self.reset_time = reset_time

    def add_handler(self, error, handler):
        """
        Funktion zum Hinzufügen von Handler-Funktion. Muss vor .handle ausgeführt werden.
        :param error: Error Bezeichnung
        :param handler: Funktion zum Handeln des Errors
        :return:
        """
        self.handlers[error] = handler

    def handle(self, error_no):
        """
        Funktion zum Verarbeiten der Errors. Wenn entsprechender Error ausgeführt wird,
        wird Handler-Funktion ausgeführt. Wenn "retries" Mal derselbe Fehler auftritt,
        wird das Programm abgebrochen (Fehler kann nicht behoben werden)
        :param error_no: Error Message
        :return:
        """
        if error_no in self.handlers.keys():
            for error in self.handlers.keys():
                if error_no == error:
                    self.handlers.get(error)()
        else:
            print("Kein Handler für diesen Error")
            return True

        if error_no == self.last_error[0]:
            self.error_cont += 1
        if ((time() - self.last_error[1]) >= self.reset_time) or (error_no != self.last_error[0]):
            self.error_cont = 1
        self.last_error = [error_no, time()]
        if self.error_cont == self.retries:
            print("Fehler kann nicht behoben werden")
            return True
        else:
            return False
