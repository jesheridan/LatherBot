# LatherBot

This is a discord bot for the r/wetshaving discord with the purpose of providing an easy way to look up scent notes for wetshaving products in a database and providing entertainment via a quiz game with scorekeeping based upon those wetshaving products. Some other features include simple responses to greetings to make the community feel welcoming and calling up links to other external resources.

## Getting Started
This code was written to be hosted on replit.com, so you'll need to open an account there to use the code as written. Replit is free to use for basic features. If you would prefer to host this code elsewhere the code will likely need some adjustments for that.

You'll need to setup your own discord bot to feed the code to and basic instructions can be found at discord's python site at https://discordpy.readthedocs.io/en/stable/discord.html


## Usage
There are examples of the database structure required for this bot to function in products.py. This will need to be setup prior to most of the functionality of the bot working.

You'll need to add your bot's token to secrets in replit. Outside of replit, a token would typically be in a .env as to be hidden from the publically available code and you don't want other users to have access to your bot's token. 

The commands available to this bot in discord are:
- !latherbot - gives a list of functions delivered in an embed
- !score - returns a user's current score in the scent game
- !scoreboard - returns a full list of all the scores from the scoreboard dictionary. This command is restrict to a specific channel to avoid spamming a long list in general chat.
- !leaderboard - returns the top 10 scores from the scoreboard dictionary
- !practice - runs an unscored practice version of the scent game. This command is restrict to a specific channel to avoid spamming in general chat.
- !paa - pulls up important information to r/wetshaving about that vendor
- !hello - simple response from the bot. First command I got working, so I left it in.
- !bang - A simple chat version of the game duck hunt. On a random timer the bot will release an ascii duck. First user to respond either !bang or .bang gets credit for shooting it down.

The scored version of the scent game has 3 modes - regular, hard, and brand - each of which run on seperate random timers which can be adjusted for preference. Each of those games are also channel specific, so you'll need to update the code to point to a channel your bot is active on. 

Additionally the bot will respond to certain phrases with emojis, such as good morning, good bot and bad bot.

## Contributing
If you have an idea on a feature to add to this project or have suggestions on how to improve this code, please feel free to reach out to me. As of publishing this code, the following items are areas that could use improvement or be update in future versions:
- This code is currently written to be hosted on replit, but due to some limitations and costs with that site, migrating to a new host for the bot may be beneficial and certain portions of the code - especially the handling of the database would need to be updated as part of a migration.
- The hints given as part of the game are currently created via a REGEXREPLACE function in Google Sheets and then hardcoded into the database as a value to the collection number so that it can be referenced during the game. This should be possible to do as part of the code, so that future collections added would not need the hint value loaded and could be generated systematically.
- If a new site with a more robust database of collections becomes available, it would be valuable to update this code to not rely on an internal database, which requires manual adjustments, but to pull that data from an available API so that current products are automatically integrated into the search function.

## License
This project is under the MIT License. Please see LICENSE under the main repository for the full license. 

## Troubleshooting
One issue I found several times during test of the bots is they would be blocked from Discord's API seemingly at random due to 429 issues, which happens when too many requests are made of the API. To the best of my understanding, this is often due to replit using a single IP address for multiple replits, so if collectively too many replits are making requests to an API it can result in all those replits getting an IP ban. You can typically work around this by typing "kill 1" into the shell, which will kill the program and assing your replit a new IP address.

## Acknowledgments
The following list includes external libraries or tools that were used in the project, as reported by pip-licenses as of February 16, 2023, along with links to those resources. Much of this project would not be possible or be significantly less useful without their inclusion and for that I'm grateful to the individuals that create, maintain and share them to be used. This may not be a complete list as this program was developed on replit which has other packages already pre-installed, but should be inclusive of all additional external packages required:

| Name                     | Version     | License                                                 | URL                                                  |
|--------------------------|-------------|---------------------------------------------------------|------------------------------------------------------|
| Levenshtein              | 0.20.9      | GNU General Public License v2 or later (GPLv2+)         | https://github.com/maxbachmann/Levenshtein           |
| Unidecode                | 1.3.6       | GNU General Public License v2 or later (GPLv2+)         | UNKNOWN                                              |
| discord.py               | 2.1.0       | MIT License                                             | https://github.com/Rapptz/discord.py                 | 
| fuzzywuzzy               | 0.18.0      | GNU General Public License v2 (GPLv2)                   | https://github.com/seatgeek/fuzzywuzzy               |
| pip-licenses             | 4.0.3       | MIT License                                             | https://github.com/raimon49/pip-licenses             |
| python-Levenshtein       | 0.20.9      | GNU General Public License v2 or later (GPLv2+)         | https://github.com/maxbachmann/python-Levenshtein    |
| replit                   | 3.2.5       | ISC                                                     | https://github.com/replit/replit-py                  |
