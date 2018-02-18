import asyncio
from datetime import datetime
import os

import sys

# Number of subprocesses to spawn
N_PROC = 10


class WatchProtocol(asyncio.SubprocessProtocol):
    """Protocol that processes piped data line by line, counting occurrences of lines containing "ERROR"."""
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.error_count = 0
        self._partial_line = ''

    def pipe_data_received(self, fd, data):
        s = self._partial_line + data.decode('utf-8', 'backslashreplace')
        lines = s.split('\n')
        if s.endswith('\n'):
            self._partial_line = ''
        else:
            self._partial_line = lines[-1]
            del lines[-1]
        for line in lines:
            self.process_line(line)

    def process_line(self, line):
        self.error_count += int('ERROR' in line)

    def process_exited(self):
        if self._partial_line:
            self.process_line(self._partial_line)
        self.exit_future.set_result(1)


async def watch_subproc(loop, procnum):
    """Coroutine that spawns a subprocess, waits for it exit and returns the error_count of the WatchProtocol."""
    exit_future = asyncio.Future()
    transport, protocol = await loop.subprocess_exec(lambda: WatchProtocol(exit_future),
                                                     'python', 'log-generator.py', '10',
                                                     stdin=None, stderr=None, cwd=os.path.dirname(sys.argv[0]))
    await exit_future
    return procnum, protocol.error_count


def main():
    if sys.platform == 'win32':
        asyncio.set_event_loop(asyncio.ProactorEventLoop())
    loop = asyncio.get_event_loop()
    print("Running with %d subprocesses" % N_PROC)
    print("Started at  %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
    results = loop.run_until_complete(asyncio.gather(*[watch_subproc(loop, i) for i in range(N_PROC)]))
    counts = [c for (_, c) in results]
    print(sum(counts) / len(counts), results)
    print("Finished at %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

if __name__ == "__main__":
    main()
