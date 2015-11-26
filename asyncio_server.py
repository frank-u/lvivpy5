#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import division

from urllib.parse import urlparse

import asyncio
import aiohttp
import logging
import concurrent.futures

log = logging.getLogger(__name__)

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 1


def micro_server(server_address):
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_request, server_address[0], server_address[1], loop=loop)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    log.debug('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Close the server
        server.close()
        loop.close()


@asyncio.coroutine
def handle_request(client_reader, client_writer):
    addr = client_writer.get_extra_info('peername')
    logging.info('Accepted connection from {}'.format(addr))
    while True:
        try:
            request_link = yield from asyncio.wait_for(client_reader.read(1024), timeout=10.0)
            if not request_link:
                break
            result = yield from process_request(
                request_link.decode('utf-8').strip()
            )
            resp = str(result).encode('utf-8') + b'\n'
            client_writer.write(resp)
        except concurrent.futures.TimeoutError:
            logging.info('Connection from {} closed by timeout'.format(peername))
            break
    client_writer.close()


@asyncio.coroutine
def process_request(link):
    try:
        if not urlparse(link).scheme:
            link = "http://" + link
        respond = yield from aiohttp.get(link)
        try:
            return respond.status
        finally:
            respond.close()
    except asyncio.TimeoutError:
        return 500

if __name__ == '__main__':
    logging.basicConfig(level='DEBUG', format="%(threadName)s: %(message)s")
    micro_server(SERVER_ADDRESS)
