from random import choice
from threading import Timer
from typing import Dict

from requests import Response

from config import AUTH_FILE, API_URL, REQ_TIMEOUT, MSG_DELAY
from gam_logging import log
from replay_session import ReplayableSession


class TeleBot:
    def __init__(self):
        # Get auth keys
        log.info("Reading auth keys from config...")
        with open(AUTH_FILE, 'r') as f:
            self.__keys = f.read().strip().splitlines()

        # Generate new session
        self.__s = ReplayableSession()

        log.info(f"Found {len(self.__keys)} bots, collecting account data...")
        # for each bot, log in and get their ID
        self.__bot_data = {}
        for auth in self.__keys:
            # get data for bots
            log.info(f"Logging into account #{auth}...")
            resp = self.__s.get(API_URL.format(auth, "getMe"))
            log.info("Logged into account successfully...")
            self.__bot_data[auth] = resp.json()["result"]

    def send_msg(self, chat_id: int, txt: str, auto_del: bool, rand_bot: bool, no_sound: bool = False) -> Response:
        # Get the key to use
        key = self.__get_key(rand_bot)

        # Send the message
        resp = self.__s.post(
            url=API_URL.format(key, "sendMessage"),
            data={
                "chat_id": chat_id,
                "text": txt,
                "disable_notification": no_sound
            },
            timeout=REQ_TIMEOUT
        )

        # then check if forgot to add bot
        self.__handle_response(resp, key)
        # and check if we need to delete the message
        self.__handle_auto_del(auto_del, chat_id, resp)

        return resp

    def copy_msg(self,
                 from_chat_id: int, to_chat_id: int,  # Chat identifiers
                 msg_id: int, txt: str,  # Message identifiers
                 rand_bot: bool, auto_del: bool) -> Response:

        # Get the key to use
        key = self.__get_key(rand_bot)

        # Send the message
        resp = self.__s.post(
            url=API_URL.format(key, "copyMessage"),
            data={
                "chat_id": to_chat_id,
                "from_chat_id": from_chat_id,
                "message_id": msg_id,
                "caption": txt,
                "protect_content": True,
                "allow_sending_without_reply": True
            },
            timeout=REQ_TIMEOUT
        )

        # then check if forgot to add bot
        self.__handle_response(resp, key)
        # and check if we need to delete the message
        self.__handle_auto_del(auto_del, to_chat_id, resp)

        return resp

    def get_updates(self, last_update: int) -> Response:
        return self.__s.get(
            url=API_URL.format(self.__keys[0], "getUpdates"),
            params={"offset": last_update},
            timeout=REQ_TIMEOUT
        )

    def del_msg(self, chat_id: int, msg_id: int) -> Response:
        return self.__s.post(
            url=API_URL.format(self.__keys[0], "deleteMessage"),
            data={
                "chat_id": chat_id,
                "message_id": msg_id
            },
            timeout=REQ_TIMEOUT
        )

    def __handle_auto_del(self, auto_del: bool, chat_id: int, resp: Response) -> None:
        # If we should delete
        if auto_del:
            # Convert to JSON
            res: Dict = resp.json()['result']

            # Delete the msg after a wait
            t = Timer(
                MSG_DELAY,
                self.del_msg,
                kwargs={
                    "chat_id": chat_id,
                    "msg_id": res["message_id"]
                },
            )
            # Start timer
            t.start()

    def __handle_response(self, resp: Response, used_key: str) -> None:
        if resp.status_code == 400:
            # get bad bot data
            bad_bot = self.__bot_data[used_key]
            # send error
            log.error(f"Forgot to add bot to chat: {bad_bot['first_name']} (@{bad_bot['username']})")
            # kick bot out of set for now
            self.__keys.remove(used_key)

    def __get_key(self, rand: bool) -> str:
        return choice(self.__keys) if rand else self.__keys[0]
