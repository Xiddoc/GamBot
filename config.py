"""
Configuration file.
"""

# Customizable
##################################################

# Auto-Delete timer (seconds)
MSG_DELAY = 10.0

# How many messages to save cache
MAX_HISTORY = 50

# Maximum fake messages to send per 1 message from you
MAX_FAKE_MSGS = 2

# Directory to write cache files to
CACHE_DIR = "./cache"

# Path to get bot auth env keys from
AUTH_FILE = "./auth_keys.env"

# Log to console
CONSOLE_LOGGING = True

# Bot commands
BACKDOOR_COMMAND = "/backdoor"
STATUS_COMMAND = "/status"
REQUEST_COMMAND = "/request"
REPLAY_COMMAND = "/replay"

# Recommended not to change
##################################################

# Telegram Bot API URL
API_URL = "https://api.telegram.org/bot{}/{}"

# Timeout for API requests
REQ_TIMEOUT = 10

# Cache file paths
FAKE_MSG_PATH = CACHE_DIR + "/GAM_CHAT.txt"
LAST_UPDATE_PATH = CACHE_DIR + "/LAST_UPD.txt"
BACKDOOR_USER_PATH = CACHE_DIR + "/BCK_USR.txt"
FRONTDOOR_CHAT_PATH = CACHE_DIR + "/FRT_CHT.txt"
GENERAL_USER_PATH = CACHE_DIR + "/GNR_USR.txt"
