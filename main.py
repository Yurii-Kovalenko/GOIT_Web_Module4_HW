from http.server import HTTPServer, BaseHTTPRequestHandler

import urllib.parse

from pathlib import Path

from mimetypes import guess_type

import socket

from socket_server import run_server

from threading import Thread

from view_json import view_json_file


UDP_IP = '127.0.0.1'

UDP_PORT = 5000

HTML_FOLDER = "./html/"

HTTP_PORT = 3000

IS_VIEW_MESSAGES = False

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/index.html' or pr_url.path == '/':
            self.send_html_file(f'{HTML_FOLDER}index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file(f'{HTML_FOLDER}message.html')
        else:
            if Path().joinpath(f'{HTML_FOLDER}{pr_url.path[1:]}').exists():
                self.send_static()
            else:
                self.send_html_file(f'{HTML_FOLDER}error.html', 404)

    def send_static(self):
        self.send_response(200)
        mt = guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'{HTML_FOLDER}{self.path}', 'rb') as file:
            self.wfile.write(file.read())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def run_socket_client(self, data):
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server = UDP_IP, UDP_PORT
        socket_client.sendto(data, server)
        socket_client.close()


    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        self.run_socket_client(data)
        self.send_response(302)
        self.send_header('Location', '/thanks.html')
        self.end_headers()


def run_http(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', HTTP_PORT)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()

def main():
    if IS_VIEW_MESSAGES:
        view_json_file()
    print("Servers started.")
    server = Thread(target=run_server, args=(UDP_IP, UDP_PORT))
    client = Thread(target=run_http)
    server.start()
    client.start()
    server.join()
    client.join()

if __name__ == '__main__':
    main()
