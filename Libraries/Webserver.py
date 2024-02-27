# File: webserver.py
__author__ = "Gregori Bucher"
__copyright__ = "Gregori Bucher, 06.02.2024"
__version__ = "1.1"

import socket


class Webserver:
    """
    class: Webserver
    Wird verwendet um Webserver von ESP aus zu hosten und http Struktur zu Erstellen und zu Verwalten
    """
    def __init__(self, adr: (str, int) = ('', 80), conn_allowed: int = 1):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((adr[0], adr[1]))
        self.server_socket.listen(conn_allowed)
        self.paths = dict()
        self.hosting = True

    def add_path(self, path: str, html_code: str = None, get_handler=None, post_handler=None):
        """
        Funktion zum Erstellen von neuem Pfad
        :param path: Sting des Pfads
        :param html_code: html file für entsprechenden Pfad
        :param get_handler: Funktion welche ausgeführt wird, wenn ein GET request für diesen Pfad vorliegt
        :param post_handler: Funktion welche ausgeführt wird, wenn ein POST request für diesen Pfad vorliegt
        :return: None
        """
        self.paths[path] = [html_code, get_handler, post_handler]

    def config_path(self, path: str, html_code: str = None, get_handler=None, post_handler=None):
        """
        Funktion zum Bearbeiten von bestehendem Pfad
        :param path: Sting des Pfads
        :param html_code: html file für entsprechenden Pfad
        :param get_handler: Funktion welche ausgeführt wird, wenn ein GET request für diesen Pfad vorliegt
        :param post_handler: Funktion welche ausgeführt wird, wenn ein POST request für diesen Pfad vorliegt
        :return: None
        """
        if path in self.paths.keys():
            if html_code is not None:
                self.paths[path][0] = html_code
            if get_handler is not None:
                self.paths[path][1] = get_handler
            if post_handler is not None:
                self.paths[path][2] = post_handler

    def host(self):
        """
        Serververbindung starten
        :return: None
        """
        print("Server opened")
        self.hosting = True
        while self.hosting:
            try:
                self.com_socket, address = self.server_socket.accept()
                request = (self.com_socket.recv(1024)).decode("utf-8")
                self.com_socket.sendall("HTTP/1.1 200 OK\n")
                self.com_socket.sendall("Content-Type: text/html\n")
                self.com_socket.sendall("Connection: close\n")
                for path in self.paths.keys():
                    if request[:4] == "GET " and request[4+len(path)] == " " and request[4:(4+len(path))] == path:    # GET request
                        if self.paths.get(path)[0] is not None:
                            self.com_socket.sendall(self.paths.get(path)[0])
                        if self.paths.get(path)[1] is not None:
                            self.paths.get(path)[1]()
                    if request[:5] == "POST " and request[5+len(path)] == " " and request[5:(5+len(path))] == path:    # POST request
                        if self.paths.get(path)[2] is not None:
                            content_length = int((request.split("Content-Length: ")[1]).split("\r\n")[0])
                            content_str = request[len(request) - content_length:]
                            self.paths.get(path)[2](content_str.split("&"))
                self.com_socket.close()
            except OSError as error:
                print(f"Fehler bei Verbindung:\b{error}")
        print("Server closed")

    def close_connection(self):
        """
        Serververbindung stoppen
        :return: None
        """
        self.hosting = False

    def redirect_path(self, path: str):
        """
        Pfad umleiten und Browser aktualisieren
        :param path: Pfad auf welchen umgeleitet werden soll
        :return: None
        """
        self.com_socket.sendall(f"Refresh: 0; url={path}\n\n")
