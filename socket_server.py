import socket

import urllib.parse

from datetime import datetime

from json import dump

from view_json import load_data

file_name = "./storage/data.json"


UDP_IP = '127.0.0.1'

UDP_PORT = 5000


def adapter(data) -> tuple:
    data_parse = urllib.parse.unquote_plus(data.decode())
    data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
    return str(datetime.now()), data_dict

def write_json_file(data) -> None:
     with open(file_name, "w") as fw:
         dump(data, fw)

def run_server(ip, port) -> None:
    dict_messages = load_data()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            time_message, data_dict = adapter(data)
            dict_messages[time_message] = data_dict
            write_json_file(dict_messages)
    except KeyboardInterrupt:
        print('Destroy server')
    finally:
        sock.close()


if __name__ == '__main__':
    run_server(UDP_IP, UDP_PORT)