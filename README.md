# <img width=350 src=https://repository-images.githubusercontent.com/560391891/f87fd37e-c20b-42c9-9da4-9bcfa26a7302 />

A program which leverages Telegram bots to create an "obfuscated secret chat".

## Summary

Telegram has secure chats called [Secret Chats](https://telegram.org/faq#q-how-are-secret-chats-different).
These chats have neat features such as very short Auto-Delete timers, which you can set to as low as mere
seconds. This means that you can message someone confidently, knowing that your messages will be gone almost
as quick as you send them.

GamBot adds an extra layer of obfuscation to the game. On top of Auto-Deleting messages, GamBot will also
spoof fake chat messages to make it harder for someone to
[shoulder-surf](https://en.wikipedia.org/wiki/Shoulder_surfing_(computer_security)) you, or if someone outright
takes your phone, you can play it off as messaging/reading a group chat.

## Features

GamBot's toolset includes:

- Customizable Auto-Delete time (as low or high as you want)

- Imports fake chat messages directly from WhatsApp

- Supports any amount of Telegram Bots for spoofing messages (recommended to use more, to not hit rate limits)

- Handful of commands to help contacting, while staying under the radar

## Installation & Setup

As of now, there are no extra dependencies. However, if your version of Python does not include the `requests`
module, then you can install it like so (the command might start with `pip3` on your computer instead):
```cmd
pip install requests
```

Now you need to get a few API keys for your bots. You can do this by 
[messaging the BotFather](https://t.me/BotFather), a Telegram bot which lets you create your own bots (for free).

Then clone/download this repository, and create a new file called `auth_keys.env`. In it, add your Telegram bot
API keys, each on a seperate line. Create a group chat in Telegram, and add all of your bots to there, and give
all of them them admin priveleges (so that they can monitor, read, and write messages).

You must use the first bot as the "main bot". This bot will be responsible for auto-deleting messages, 
responding to commands, and being the 'backend' bot that your hidden user can chat to. Open a Telegram 
chat with this bot and shoot them a message (Telegram bots must be messaged first, before they can message
you back).

Then you can run the bot manager / server program:
```cmd
python gam.py
```

## Notes

This README might be a little outdated or wrong, and the project's code isn't amazing. This was meant to be a small
project to get the job done, but I decided to add more features along the way. If you want to make any improvements,
feel free to create a Pull Request (PR).
