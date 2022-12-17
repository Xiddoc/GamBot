from requests import Session, RequestException
from time import sleep

from config import REQ_TIMEOUT
from handlers.gam_logging import log


class ReplayableSession(Session):

    def __init__(self):
        super().__init__()
        # Update the request
        self.request = self.repeat_network_func(self.request)

    @staticmethod
    def repeat_network_func(func):
        # Decorator
        def retry(*args, **kwargs):
            # Iter count
            i = 0
            while True:
                # Catch any OS errors, networking errors, etc.
                try:
                    return func(*args, **kwargs)
                except KeyboardInterrupt:
                    log.error("Program terminated.")
                    exit(0)
                except RequestException:
                    # Don't print if there are internet issues
                    if i < 3:
                        log.error(f"Network error, trying again in {REQ_TIMEOUT} seconds...")
                        sleep(REQ_TIMEOUT)
                    elif i == 3:
                        log.error("Fatal network error, will keep trying but won't log...")

                # Increment iteration count
                i += 1

        return retry
