import string
import time
from datetime import datetime
import random
import sys


def main(run_for_seconds):
    chars = string.ascii_lowercase + string.digits
    started = time.time()
    i = 0
    while time.time() - started < run_for_seconds:  # i < run_for_seconds * 10
        r = random.random()
        t = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        msg = ''.join(random.choices(chars, k=random.randint(80, 200)))
        level = "INFO" if r > 0.05 else "ERROR"  # "INFO" if i % 10 != 0 else "ERROR"
        print("%s %s %s" % (t, level, msg))
        i += 1
        time.sleep(0.01)

if __name__ == "__main__":
    main(int(sys.argv[1]))
