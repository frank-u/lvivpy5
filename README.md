# Simple servers in python

**simple_server.py** - A simple server which can't processing concurrent requests

**fork_server.py** - A server which use os.fork() for processing concurrent requests 

**thread_server.py** - A server which use threading for processing concurrent requests

**asyncio_server.py** - A server which use asyncio for processing concurrent requests

**client.py** - Emulator concurrent requests

*Example*

```bash
On server:
    python asyncio_server.py
On client:
    ./client.py --max-clients=5 --max-conns=4
```