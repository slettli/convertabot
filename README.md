# Convertabot

A Discord bot for converting imperial units to metric, and vice versa. Its main strength lies in being able to do this automatically, without being prompted by a command. Built with Python 3.11 and Hikari as a way to help ease chats between people across the pond. Not currently stable or feature-complete.

## Features

### Auto-conversions

If granted the necessary permissions, the bot will attempt to automatically detect and convert supported units. Options to configure this behavior will be implemented at a later time. 

<img width="514" alt="Auto-conversion example" src="https://user-images.githubusercontent.com/52682352/210027568-ede570b8-a9e9-4de9-89b2-cfb616bbd1b3.png">

### Slash Commands

#### /uptime
How long the bot has been running for the current session. Note that this counter does not reset if it loses connection, only if the program crashes.

#### /set_max `number`
Sets the maximum number of units the bot will convert from a single message. The default is 3, as to not fill up the chat.

#### /convert `unit` `value` 
Same as the auto-conversion. Does not currently support choosing what you want something converted *to*.

## Supported units

More will be added later.

##### Volume and weight:

- liters <-> gallons
- kilograms <-> pounds (lb/lbs)

##### Length:

- kilometers <-> miles
- meters <-> feet
- centimeters <-> inches
- millimeters <-> inches

##### Temperature:

- celsius <-> fahrenheit

## Install & run

Convertabot currently runs on Python 3.11, although 3.10 might work as well. I don't recommend hosting the bot yourself, and I do not give any guarantees, nor will I provide any additional support. 

But if you want to give it a go:

1. Create an application and a bot using Discord's developer console.
  - If you want the auto-conversion feature, make sure you enable 'MESSAGE CONTENT INTENT'. This intent is required to receive messages without being prompted by a command.

2. Clone this repo and create a `.env` file in the root directory with:
  - `TOKEN="YOUR TOKEN HERE"`
  - Don't remove the double quotation marks, but replace YOUR TOKEN HERE with the one generated in the developer console, under bot.

3. From the root folder, install the required following modules using pip:
  - `pip3 install -r requirements.txt`

4. Start the bot:
  - `python3 -m convertabot.main`

Note that the bot currently doesn't store settings on a server-by-server basis, nor does it care *who* asks it to change these.
If you run into issues, check that the bot has the correct permissions (Read Messages), and that the required intents are enabled in the developer console.
