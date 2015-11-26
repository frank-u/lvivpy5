#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

from urllib.parse import urlparse
from threading import Thread
from requests.exceptions import (
    Timeout,
    HTTPError,
    ConnectionError
)

import socket
import requests
import logging


log = logging.getLogger(__name__)

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 1


def micro_server(server_address):
    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = REQUEST_QUEUE_SIZE

    # Create a new socket
    listen_socket = socket.socket(
        address_family,
        socket_type
    )
    # Allow to reuse the same address
    listen_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )
    # Bind
    listen_socket.bind(server_address)
    # Activate
    listen_socket.listen(request_queue_size)

    while True:
        # New client connection
        client_connection, client_address = listen_socket.accept()
        # Handle request
        log.info("Start connected %s" % client_address[0])
        Thread(target=handle_request, args=(client_connection,)).start()


def handle_request(client):
    log.info("Start process client request")
    while True:
        request_link = client.recv(1024)
        if not request_link:
            break
        result = process_request(
            request_link.decode('utf-8').strip()
        )
        resp = str(result).encode('utf-8') + b'\n'
        client.send(resp)

    log.info("Closed connection")
    client.close()


def process_request(link):
    try:
        if not urlparse(link).scheme:
            link = "http://" + link
        respond = requests.get(link)
        return respond.status_code
    except (AttributeError, Timeout, HTTPError, ConnectionError):
        return 500

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG', format="%(threadName)s: %(message)s")
    micro_server(SERVER_ADDRESS)
