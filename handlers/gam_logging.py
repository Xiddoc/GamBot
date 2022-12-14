"""
Configuration of the logging.
"""
import logging
from pathlib import Path
from config import CONSOLE_LOGGING

# Root path for logging
log_path: str = f'{Path(__file__).parent.resolve()}/my_debug.log'

# Level config
levels = {
	logging.DEBUG: "[+]",
	logging.INFO: "[+]",
	logging.WARN: "[!]",
	logging.ERROR: "[X]",
}

# Set the level names
for level, level_text in levels.items():
	logging.addLevelName(level, level_text)

# Get the logger we will use everywhere
log = logging.getLogger()
log.setLevel(logging.INFO)

# Set the format
logFormatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')

# Create file handler and add it to the logger
fileHandler = logging.FileHandler(log_path)
fileHandler.setFormatter(logFormatter)
log.addHandler(fileHandler)

# Create console handler and add it to the logger
if CONSOLE_LOGGING:
	consoleHandler = logging.StreamHandler()
	consoleHandler.setFormatter(logFormatter)
	log.addHandler(consoleHandler)
