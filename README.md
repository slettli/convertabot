# Convertabot

A Discord bot for converting imperial units to metric, and vice versa. Its main strength lies in being able to do this automatically, without being prompted by a command. Built with Python 3.11 and Hikari as a way to help ease chats between people across the pond. Not currently stable or feature-complete.

## Usage

### Auto-conversions
By default the bot will attempt to automatically detect and convert supported units. Options to configure this behavior will come sometime. 

Example:

```
American chatter: 
I just love myself some 35 pounds in this 94f weather!

European chatter: 
What? Are you boiling 35 quid, mate?

Convertabot:
35 pounds is 15.88 kilograms
94 fahrenheit is 34.45 celsius
```

### Slash Commands

#### /uptime
How long the bot has been running for the current session. Note that this counter does not reset if it loses connection, only if the program crashes.

#### /set_max `number`
Sets the maximum number of units the bot will convert from a single message. The default is 3, as to not fill up the chat.

#### /convert `unit` `value` 
Same as the auto-conversion. Does not currently support choosing what you want something converted *to*.

## Supported units

The list is fairly limited, since all the units have to work with the auto-conversion feature.

##### Volume and weight:

- liters <-> gallons
- kilograms <-> pounds (lb/lbs)

##### Length:

- kilometers <-> miles
- meters <-> feet
- centimeters <-> inches
- millimeters <-> inches

##### Misc:

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
