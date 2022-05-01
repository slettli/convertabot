# Convertabot

Discord-bot for automatically detecting and converting imperial to metric, and vice versa. 

Alternatively: *helping friends across the pond communicate.*

## Usage

Convertabot will attempt to automatically detect and convert supported units:
```
American chatter: 
I just love myself some 35 pounds in this 94f weather!

European chatter: 
What? Are you boiling 35 quid mate?

Convertabot:
35 pound is 15.88 kilograms
94 fahrenheit is 34.45 celsius
```
All the confusion is cleared up!

## Supported units

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

If you want to run it yourself, which I don't necessarily recommend, then: 

- Install [discord.py](https://discordpy.readthedocs.io/en/stable/) and [python-dotenv](https://pypi.org/project/python-dotenv/).

- Create a Discord bot from Discord's developer console, and generate a token. 

- Clone this repo, and create a `.env` file in the bot's directory with the contents:
  - `TOKEN="YOUR TOKEN HERE"`
  - Don't remove the double quotation marks.
- Finally, start the bot by opening a shell in its directory:
  - `python bot.py`

Once you've added the bot to a server, it should be good to go.
