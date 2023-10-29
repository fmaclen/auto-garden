import socket
from typing import Union
from datetime import datetime
from time import sleep, mktime
from requests import get, post, patch
from pytz import utc

from lib.pocketbase import PocketBase

from env import DEVICE, POCKETBASE_DEVICE_ID


class Device:
    def __init__(self, tick_rate: int) -> None:
        print("-> Current device:", DEVICE)
        self.name = DEVICE
        self.tick_rate = tick_rate
        self.sleep = sleep

        self.id = POCKETBASE_DEVICE_ID
        self.pb = PocketBase(get, post, patch, mktime)
        self.socket = self.server_init()

    def get_current_time(self) -> int:
        return int(datetime.now(utc).timestamp())

    def handle_system_error(self, error: str) -> None:
        print("-> Error:", error)

    def server_init(self):
        addr = socket.getaddrinfo('0.0.0.0', 9999)[0][-1]
        s = socket.socket()
        s.bind(addr)
        s.listen(1)
        print('-> Listening on', addr)
        return s

    def server_listen_pot_irrigation(self) -> Union[None, str]:
        client, _ = self.socket.accept()
        request = client.recv(1024).decode('utf-8')
        headers = self.server_parse_request(request)

        if 'OPTIONS' in request:
            # Handling preflight request
            response_headers = [
                "HTTP/1.1 204 No Content",
                "Access-Control-Allow-Origin: *",
                "Access-Control-Allow-Methods: POST, OPTIONS",
                "Access-Control-Allow-Headers: Authorization, Content-Type, Pot-Id",
                "Access-Control-Max-Age: 3600"  # Cache preflight response for 1 hour
            ]
            response = "\r\n".join(response_headers) + "\r\n\r\n"
            client.send(response.encode('utf-8'))

        elif 'POST' in request:
            if 'Authorization' in headers and 'Pot-Id' in headers and self.pb.is_valid_jwt(headers['Authorization']):
                response_headers = [
                    "HTTP/1.1 200 OK",
                    "Content-Type: application/json",
                    "Access-Control-Allow-Origin: *"  # Required for CORS
                ]
                response = "\r\n".join(response_headers)
                client.send(response.encode('utf-8'))

                return headers['Pot-Id']
            else:
                client.send('HTTP/1.1 400 Bad Request\r\n\r\n'.encode('utf-8'))
        else:
            client.send('HTTP/1.1 404 Not Found\r\n\r\n'.encode('utf-8'))

        client.close()

    def server_parse_request(self, request):
        headers = {}
        lines = request.split('\r\n')
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                headers[key] = value
        return headers

    def server_stop(self):
        self.socket.close()
