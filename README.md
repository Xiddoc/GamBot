# GamBot

A program which leverages Telegram bots to create an "obfuscated secret chat".

## Summary

Telegram has secure chats called [Secret Chats](https://telegram.org/faq#q-how-are-secret-chats-different).
These chats have neat features such as very short Auto-Delete timers, which you can set to as low as mere seconds.
This means that you can message someone confidently, knowing that your messages will be gone almost as quick as you send them.

GamBot adds an extra layer of obfuscation to the game. On top of Auto-Deleting messages, GamBot will also spoof fake chat messages
to make it harder for someone to [shoulder-surf](https://en.wikipedia.org/wiki/Shoulder_surfing_(computer_security)) you, or if someone
outright takes your phone, you can play it off as messaging/reading a group chat.

## Features

GamBot's toolset includes:

- Customizable Auto-Delete time (as low or high as you want)

- Imports fake chat messages directly from WhatsApp

- Supports any amount of Telegram Bots for spoofing messages (recommended to use more, to not hit rate limits)

- Handful of commands to help contacting, while staying under the radar
