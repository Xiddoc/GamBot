"""
If you come back to this, remember that you wrote this on your phone...
with limited internet access...
and some of it written on a flight.

So understandably some of the code sucks.
"""
from hashlib import md5
from json import loads, dumps
from os import mkdir
from os.path import exists
from random import randint
from time import sleep

from config import *
from gam_logging import log
from wa_handler import WAHandler
from telebot import TeleBot

log.info("\n\n" + "=" * 50 + "\n\nStarting...")

# Initialize objects for bot to use later
msg_history = []
ALL_COMMANDS = [BACKDOOR_COMMAND, STATUS_COMMAND, REQUEST_COMMAND, REPLAY_COMMAND]

log.info(f"Checking if cache dir exists at '{CACHE_DIR}'...")
if not exists(CACHE_DIR):
    log.info("Directory does not exist, creating...")
    mkdir(CACHE_DIR)

log.info("Checking last update cache...")
if exists(LAST_UPDATE_PATH):
    log.info("Cache found, loading...")
    with open(LAST_UPDATE_PATH, encoding='utf-8') as f:
        last_update = int(f.read())
else:
    last_update = 0

log.info("Checking general user cache...")
if exists(GENERAL_USER_PATH):
    log.info("Cache found, loading...")
    with open(GENERAL_USER_PATH, encoding='utf-8') as f:
        user_to_id = loads(f.read())
else:
    user_to_id = {}

# The warning triggers if the dict is empty, not only if the file is not found
if not user_to_id:
    log.warn(f'No user cache found, users will need to register using the "{BACKDOOR_COMMAND}" command.')

log.info("Checking backdoor user cache...")
if exists(BACKDOOR_USER_PATH):
    log.info("Cache found, loading...")
    with open(BACKDOOR_USER_PATH, encoding='utf-8') as f:
        backdoor_user = int(f.read())
else:
    log.warn(f'No backdoor user found (make sure to register using the "{BACKDOOR_COMMAND}" command).')
    backdoor_user = 0

log.info("Checking frontend chat cache...")
if exists(FRONTDOOR_CHAT_PATH):
    log.info("Cache found, loading...")
    with open(FRONTDOOR_CHAT_PATH, encoding='utf-8') as f:
        frontdoor_chat = int(f.read())
else:
    frontdoor_chat = 0

log.info("Initializing main bot ID...")
tele = TeleBot()

log.info("Loading fake messages...")
msg_h = WAHandler()

log.info("Starting...\n")
while True:
    # Rate limit ourselves
    sleep(1)

    # use the first bot to check if any new messages
    updates_resp = tele.get_updates(last_update)

    # Make sure we aren't rate limited
    if updates_resp.status_code == 200:
        # Get response
        updates = updates_resp.json()

        if "result" in updates:
            updates = updates["result"]
        else:
            log.info(updates)
            log.info("CRITICAL ERR")

        if updates:
            log.info(f"Found {len(updates)} new updates...")
    else:
        # Rate limited probably
        log.error(f"Invalid response, waiting: {updates_resp.text}")
        sleep(10)
        continue

    # check if any updates are relevant
    for upd in updates:
        # if the update is a message
        # as opposed to an update or deletion
        if "message" in upd:
            """
            
            If this is a private message, then this is either:
            - the backend user messaging the frontend user
            - a private command, such as a new user trying to backdoor, or a status check
            
            """
            if upd["message"]["chat"]["type"] == "private":
                """

                Parse private chat bot commands.

                """
                if "text" in upd["message"] and upd["message"]["text"] in ALL_COMMANDS:
                    # and an updater command
                    if upd["message"]["text"] == BACKDOOR_COMMAND:
                        log.info(f"Updated backdoor user to user with ID #{backdoor_user}...")
                        # inform old user of update
                        tele.send_msg(
                            chat_id=backdoor_user,
                            txt=f"Backdoor user has changed. You can message"
                                f" later by running the {BACKDOOR_COMMAND} command.",
                            auto_del=False,
                            rand_bot=False
                        )
                        # get new ID
                        backdoor_user = upd["message"]["chat"]["id"]
                        # Add Username:ID for later searching, if possible
                        if 'username' in upd["message"]["chat"]:
                            user_to_id[upd["message"]["chat"]["username"]] = backdoor_user
                        # inform new user of update
                        tele.send_msg(
                            chat_id=upd["message"]["chat"]["id"],
                            txt="You have been set to the backdoor user. You should now be "
                                "able to send messages to this bot to talk. Still in testing/development.",
                            auto_del=False,
                            rand_bot=False
                        )
                    elif upd["message"]["text"] == STATUS_COMMAND:
                        log.info(f"Status was called...")
                        # convert to username
                        matching_username = None
                        for username, user_id in user_to_id.items():
                            if user_id == backdoor_user:
                                # hash username and send back
                                matching_username = md5(username.encode()).hexdigest()
                                break
                        # send status
                        tele.send_msg(
                            chat_id=upd["message"]["chat"]["id"],
                            txt=f"Bot status is on: {backdoor_user} <{matching_username}>",
                            auto_del=False,
                            rand_bot=False
                        )

                elif upd["message"]["chat"]["id"] == backdoor_user:
                    """
                
                    If the message is FROM the backend user.
                    Get the message and send it to the front end user.
                    
                    """
                    # Get the text from the msg / pic caption
                    txt = "<error>"
                    if "text" in upd["message"]:
                        txt = upd["message"]["text"]
                    elif "photo" in upd["message"]:
                        txt = upd["message"]['caption'] if 'caption' in upd["message"] else ''

                    # Push the message to history
                    if "photo" in upd["message"]:
                        msg_history.append('<photo> ' + txt)
                    else:
                        msg_history.append(txt)

                    # Clear up history if necessary
                    if len(msg_history) > MAX_HISTORY:
                        msg_history = msg_history[-MAX_HISTORY:]

                    # If this is a reply,
                    if 'reply_to_message' in upd["message"] and 'text' in upd["message"]['reply_to_message']:
                        # Format the reply
                        """
                        > Old msg (replied to)
                        > another line
                        
                        New msg (the reply)
                        """
                        txt = "\n".join(
                            '> ' + line for line in upd['message']['reply_to_message']['text'].splitlines()
                        ) + "\n\n" + txt

                    # first check if we have the frontend ID loaded
                    if frontdoor_chat:
                        # send the msg to the front-door user
                        tele.copy_msg(
                            from_chat_id=backdoor_user,
                            to_chat_id=frontdoor_chat,
                            msg_id=upd['message']['message_id'],
                            txt=txt,
                            rand_bot=True,
                            auto_del=True
                        )
                    else:
                        # Send warning
                        log.warn("No frontend chat found...")

            """

            If this is in a group chat, and it's not a bot.
            
            """
            if upd["message"]["chat"]["type"] != "private" and not upd["message"]["from"]["is_bot"]:
                # update front door chat ID
                frontdoor_chat = upd["message"]["chat"]["id"]

                # delete the original message
                tele.del_msg(
                    chat_id=upd["message"]["chat"]["id"],
                    msg_id=upd["message"]["message_id"]
                )

                # obfuscate the chat with fake messages
                for i in range(randint(1, MAX_FAKE_MSGS)):
                    # Rate limit ourselves
                    sleep(0.75)
                    # send request,
                    tele.send_msg(
                        chat_id=upd["message"]["chat"]["id"],
                        txt=msg_h.get_msg(),
                        auto_del=False,
                        rand_bot=True,
                        no_sound=True
                    )

                # if there is a registered backdoor
                if backdoor_user:
                    """

                    Parse public chat bot commands.

                    """
                    if "text" in upd["message"] and upd["message"]["text"] in ALL_COMMANDS:
                        # Get the text of the message
                        txt = upd["message"]["text"]

                        # if the message text is a command
                        if txt.startswith(REQUEST_COMMAND + " @"):
                            # Check if we have the username's ID saved
                            requested_user = txt.split(" ")[1].strip()[1:]
                            if requested_user in user_to_id:
                                tele.send_msg(
                                    chat_id=user_to_id[requested_user],
                                    txt=f"You were requested for summonings. If you choose to accept, "
                                        f"then run the {BACKDOOR_COMMAND} command to start the chat.",
                                    auto_del=False,
                                    rand_bot=False
                                )
                        elif txt.startswith(REPLAY_COMMAND + " "):
                            # Get the amount of messages we want to resend
                            replay_count = txt.split(" ")[1].strip()
                            # Type / argument check
                            if replay_count.isnumeric() and 0 < int(replay_count) <= len(msg_history):
                                # Convert to int
                                replay_count = int(replay_count)

                                # send the msg back to the front door user
                                tele.send_msg(
                                    chat_id=frontdoor_chat,
                                    txt="\n\n".join("USER: " + old_msg for old_msg in msg_history[-replay_count:]),
                                    auto_del=True,
                                    rand_bot=True
                                )
                    else:
                        # Get the text from the msg / pic caption
                        txt = "<error>"
                        if "text" in upd["message"]:
                            txt = upd["message"]["text"]
                        elif "photo" in upd["message"]:
                            txt = upd["message"]['caption'] if 'caption' in upd["message"] else ''

                        # If this is a reply,
                        if 'reply_to_message' in upd["message"] and 'text' in upd["message"]['reply_to_message']:
                            # Format the reply
                            """
                            > Old msg (replied to)
                            > another line

                            New msg (the reply)
                            """
                            txt = "\n".join(
                                '> ' + line for line in upd['message']['reply_to_message']['text'].splitlines()
                            ) + "\n\n" + txt

                        # send the original message back to the backdoor user
                        tele.copy_msg(
                            from_chat_id=frontdoor_chat,
                            to_chat_id=backdoor_user,
                            msg_id=upd['message']['message_id'],
                            txt=txt,
                            rand_bot=False,
                            auto_del=False
                        )
                else:
                    log.warn(
                        f'Removed message but there was no backdoor to'
                        f' send it to (make sure to register using '
                        f'the "{BACKDOOR_COMMAND}" command).'
                    )

        # update the updateID
        last_update = upd["update_id"] + 1

    # save the most recent updates to the cache
    with open(LAST_UPDATE_PATH, "w", encoding='utf-8') as f:
        f.write(str(last_update))
    with open(FRONTDOOR_CHAT_PATH, "w", encoding='utf-8') as f:
        f.write(str(frontdoor_chat))
    with open(BACKDOOR_USER_PATH, "w", encoding='utf-8') as f:
        f.write(str(backdoor_user))
    with open(GENERAL_USER_PATH, "w", encoding='utf-8') as f:
        f.write(dumps(user_to_id))
