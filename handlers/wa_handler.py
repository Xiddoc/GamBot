from random import randint

from config import FAKE_MSG_PATH
from handlers.gam_logging import log


class WAHandler:
    def __init__(self):
        # Get messages
        log.info("Getting message cache file...")
        with open(FAKE_MSG_PATH, encoding='utf-8') as f:
            msg_data = f.read()

        log.info("Cleaning messages...")
        # clean raw_msgs
        self.__msgs = self.filter_msgs(msg_data)

        # init index
        self.__msg_index = 0

    def get_msg(self) -> str:
        # Re-random if invalid index
        if not (0 < self.__msg_index < len(self.__msgs)):
            self.__msg_index = randint(0, len(self.__msgs) - 1)

        # pull msg
        msg = self.__msgs[self.__msg_index]

        # increment raw_msgs
        self.__msg_index += 1

        # return the pulled message
        return msg

    @staticmethod
    def filter_msgs(raw_msgs: str) -> list[str]:
        msgs = []

        for line in raw_msgs.splitlines():
            no_date = " - ".join(line.split(" - ")[1:])
            split_msg = no_date.split(": ")
            # extract data
            msg = ": ".join(split_msg[1:]).strip()

            # check validity
            if len(split_msg) > 1 \
                    and "<Media omitted>" not in msg \
                    and "null" not in msg \
                    and "This message was deleted" not in msg:
                # Add to list if valid
                msgs.append(msg)

        return msgs
