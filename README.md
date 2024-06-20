# Better Handler
A Monster Hunter Discord bot

## References:
### monster_hunter_db
A database containing all monsters informations for MHW and MH: Rise. The base World database JSON is from here.
https://docs.mhw-db.com/

### [Neryss](https://github.com/Neryss)
Updated database JSONs were used from their project(https://github.com/Neryss/monster_hunter_db)

They put a lot of work into updating World, and creating Rise, so a huge shoutout is in order.

I will be updating the databases in future updates, but all of the current information came from here.

## Usage
Currently I have just been running the bot through my PyCharm IDE. I will be doing a local install onto a Raspberry Pi 0 for me and my buddies to use privately soon.

This guide will help you get a token and download the dependencies for running the file.

To use the bot, create a .env file and use the provided template by inserting your TOKEN and SERVER NAME. After doing this run the .main file.

### Authorizations needed are:

Read/Edit/Send messages
Embeds

### Currently the commands are:

!help (display commands and descriptions)

!worldsearch <name> (search the world database for monster info)

!risesearch <name> (search the Rise database for monster info)
