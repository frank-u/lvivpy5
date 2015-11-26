#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

from threading import Thread

import socket
import click
import logging

SERVER_IP = '192.168.99.100'
SITE_URL = 'http://lvivpy.org.ua/'
log = logging.getLogger(__name__)


def handle_client(max_conns):
    for connection_num in range(max_conns):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_IP, 8888))
        req = SITE_URL.encode('utf-8') + b'\n'
        client.send(req)
        resp = client.recv(1024)
        if resp:
            result = int(resp)
            if result == 200:
                log.info('{} is available'.format(SITE_URL))
            else:
                log.error('{} is not available'.format(SITE_URL))
        else:
            log.error('Server does not respond')


@click.command()
@click.option('--max-clients', default=1, help='Maximum number of clients')
@click.option('--max-conns', default=1, help='Maximum number of connections per client')
def check_site(max_clients, max_conns):
    """
        Test client
        Args:
            max_clients(int)
            max_conns(int)
    """
    for client_num in range(max_clients):
        Thread(target=handle_client, args=(max_conns,)).start()


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG', format="%(threadName)s: %(message)s")
    check_site()
