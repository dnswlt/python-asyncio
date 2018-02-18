# python-asyncio

A collection of attempts to grasp coroutines in Python :-)

- `asyncio-procwatch.py` shows how to watch the output of multiple subprocesses line-by-line.
- `asyncio-filewatch.py` shows how to watch multiple files that other processes append to. (Classical log-watching
  scenario.)
- `sync-filewatch.py` shows how much simpler `asyncio-filewatch.py` becomes when you do it in a good-old-fashioned
  synchronous way :)

