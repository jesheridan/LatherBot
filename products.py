# In order for this program to run, you'll need to setup 4 basic parts to the database: 
# 1) scent collections entered individually as lists under a collection number, 
# 2) a collection dictionary under the name "my_dictionary", 
# 3) a list of collection numbers you want to use in the game named "game_list", and 
# 4) a dictionary named "scoreboard" to track users scores.
# I'll give examples for each one below to use as a template for setting up or updating the database.

# #1 - This is an example of a scent collection, the general format should be:
# db["Collection-No"] = ["Brand","Collection","Scents","Hint"]
# db["000001"] = ["Dapper Dragon","Green Dragon","Leather, Cedar, Bergamot, Rosemary, Lily of the Valley","G\_\_\_\_ D\_\_\_\_\_"]

# #2 This is the general format used to setup "my_dictionary", which includes the search terms for a collection number used in the scent lookup.
# db["my_dictionary"] = {
# "000001": ["Dapper Dragon Green Dragon", "Green Dragon"], 
# "000002": ["Dapper Dragon Black Dragon", "Black Dragon"],
# ...
# "######": ["Brand + Collection", "Collection", "Can add more search terms"]
# }

# #3 This is an an example of "game_list", which is the list which is randomly picked for for the game.
# TO UDPATE THE GAME LIST USE THE FOLLOWING FORMAT
# del db["game_list"]
# if "game_list" not in db:
#    print("game_list deleted successfully.")

# db["game_list"] = [
# "000001",
# "000002",
# ...
# "XXXXXX"
# ]

#if "game_list" in db:
#    print("game_list added successfully.")

# #4 - This is used to create the initial dictionary scoreboard for the scent game. The main.py will handle creating users and adding points to the dictionary.
# db["scoreboard"] = {}

from replit import db

