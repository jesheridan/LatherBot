import discord
import os
import re
import random
import asyncio
from fuzzywuzzy import process
from unidecode import unidecode
from replit import db

# Only needed when editing database
#import products

my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    client.loop.create_task(random_message())
    client.loop.create_task(hard_random_message())
    client.loop.create_task(easy_random_message())
    client.loop.create_task(duck_game())
  
@client.event
async def on_message(message):
  
    # Won't reply to its own messages
    if message.author.id == client.user.id:
        return
      
    # Simple response
    if message.content.startswith('!hello'):
        await message.reply('Hello!', mention_author=True)
      
    # Loves being called a good bot
    elif message.content.lower() == "good bot":
        await message.add_reaction("♥️")

    # Hates being called a bad bot
    elif message.content.lower() == "bad bot":
        await message.add_reaction("🖕")

    # Morning coffee
    elif message.content.lower() == "gm" or message.content.lower() == "gm ranch" or message.content.lower() == "gm latherbot" or message.content.lower() == "gm all" or message.content.lower() == "gm everyone" or message.content.lower() == "gm folks" or message.content.lower() == "morning folks" or message.content.lower() == "morning ranch" or message.content.lower() == "morning y'all" or message.content.lower() == "good morning ranch" or message.content.lower() == "good morning" or message.content.lower() == "good morning ranchers" or message.content.lower() == "gm ranchers":
        await message.add_reaction("☕")

    # Not a fan of PAA
    elif message.content.lower() == "!paa":
        await message.reply("PAA is on r/wetshaving's Do Not Buy list. You can read more about why on our wiki at https://www.reddit.com/r/Wetshaving/wiki/artisanwiki/paa/")

    # Leaderboard
    elif message.content.lower() == "!leaderboard":
        sorted_scores = sorted(db["scoreboard"].items(), key=lambda x: x[1], reverse=True)
        top_10 = sorted_scores[:10]
        msg = "Top 10 scores:\n"
        for i, (user, score) in enumerate(top_10):
            msg += f"{i+1}. {user}: {score}\n"
        await message.channel.send(msg)

    # Scoreboard
    elif message.channel.id == 'channel id' and message.content == "!scoreboard": # Replace `channel_id` with the actual ID# of the channel you want the command restricted to
        sorted_scores = sorted(db["scoreboard"].items(), key=lambda x: x[1], reverse=True)
        msg = "Full Scoreboard:\n"
        for i, (user, score) in enumerate(sorted_scores):
            msg += f"{i+1}. {user}: {score}\n"
        await message.channel.send(msg)      

    # User's score
    elif message.content.lower() == "!score":
        score_id = str(message.author.display_name) 
        if score_id in db["scoreboard"]:
            await message.channel.send(f'{message.author.display_name} has a score of {db["scoreboard"][score_id]}.')
        else:
            await message.channel.send(f'{message.author.display_name} does not have a score yet.')
      
    #Lookup a scent
    elif message.content.startswith('!soap') or message.content.startswith("!s"):

        #this creates an array of message content and removes !tts
        args = re.split("\s", message.content)
        search = str(args[1:])

        #flattens dictionary to single values
        dic = db["my_dictionary"]
        flat_list = sorted({x for v in dic.values() for x in v})
        
        #fuzzywuzzy serach logic
        fuzzy = process.extractOne(search, flat_list)
        result = fuzzy[0]

        #searches dictionary for key with matching value
        for collectionno, node in dic.items():
            if result in node:
                break
      
        brand = str(db[collectionno][0])
        collection = str(db[collectionno][1])
        scent = str(db[collectionno][2])
      
        await message.channel.send(f'{brand} {collection} - Notes: {scent}')

    # Guessing Game - Practice
    elif message.channel.id == 'channel id' and message.content == '!practice': # Replace `channel_id` with the actual ID# of the channel you want the command restricted to

        #values
        glist = db["game_list"]
        collectionno = random.choice(glist)
        brand = str(db[collectionno][0])
        collection = str(db[collectionno][1])
        scent = str(db[collectionno][2])
        hint = str(db[collectionno][3])
        channel = client.get_channel('channel id')  # Replace `channel_id` with the actual ID# of the channel you want to send the message to
      
        await channel.send(f'I am thinking of a scent from {brand} with the following notes: {scent}')

        correct_answer = unidecode(re.sub(r'[^\w\s]', '', collection)).lower()

        def check(m):
            nonlocal correct_answer
            if m.channel == channel and correct_answer and unidecode(re.sub(r'[^\w\s]', '', m.content)).lower() == correct_answer:
                return True
            return False
        
        hints_given = 0        
        while hints_given < 2:
            try:
                response = await client.wait_for('message', check=check, timeout=15.0)
                if correct_answer:
                    correct_answer = unidecode(re.sub(r'[^\w\s]', '', response.content)).lower()
                      
                    await channel.send(f'Congrats {response.author.display_name}! The correct answer was {collection} by {brand}.')
                    break
                      
            except asyncio.TimeoutError:
                 hints_given += 1
            if hints_given == 1:
                await channel.send(f'Hint: {hint}')
            else:
                await channel.send(f'Time is up! The correct answer was {collection} by {brand}.')
                break

    # Help / Information Embed
    elif message.content.lower() == "!latherbot":
        embed = discord.Embed(
            title="LatherBot",
            description="Here are the commands currently available:",
            color=discord.Color.blue()
        )
        embed.add_field(
            name="!soap [name of the product you want to search]",
            value="LatherBot will attempt a lookup of the scent notes for that product in his database.",
            inline=False
        )            
        embed.add_field(
            name="!score",
            value="Shows the user's current score in the scent game.",
            inline=False
        )
        embed.add_field(
            name="!scoreboard",
            value="Shows all user's current score in the scent game. Only works in the bot-command channel.",
            inline=False
        )
        embed.add_field(
            name="!leaderboard",
            value="Shows the top 10 scores in the scent game.",
            inline=False
        )
        embed.add_field(
            name="!practice",
            value="Lets you practice the scent game. Only works in the bot-command channel.",
            inline=False
        )
        embed.add_field(
            name="!paa",
            value="Tells you where the bad man touched r/wetshaving.",
            inline=False
        )
        embed.set_footer(
           text="Bot managed by @ShavingInCT. Please reach out if you notice any bugs."
        )
        await message.channel.send(embed=embed)   

#Guessing Game - Timed
async def random_message():
    while True:
        interval = random.uniform(1800, 3600)  # Random interval between 30 and 60 minutes
        await asyncio.sleep(interval)
        #values
        glist = db["game_list"]
        collectionno = random.choice(glist)
        brand = str(db[collectionno][0])
        collection = str(db[collectionno][1])
        scent = str(db[collectionno][2])
        hint = str(db[collectionno][3])
        channel = client.get_channel('channel id')  # Replace `channel_id` with the actual ID# of the channel you want to send the message to
      
        await channel.send(f'I am thinking of a scent from {brand} with the following notes: {scent}')

        correct_answer = unidecode(re.sub(r'[^\w\s]', '', collection)).lower()

        def check(m):
            nonlocal correct_answer
            if m.channel == channel and correct_answer and unidecode(re.sub(r'[^\w\s]', '', m.content)).lower() == correct_answer:
                return True
            return False
        
        hints_given = 0    
        while hints_given < 2:
            try:
                response = await client.wait_for('message', check=check, timeout=30.0)
                if correct_answer:
                    correct_answer = unidecode(re.sub(r'[^\w\s]', '', response.content)).lower()

                    user_id = str(response.author.display_name)
                    if user_id in db["scoreboard"]:
                        db["scoreboard"][user_id] += 1
                    else:
                        db["scoreboard"][user_id] = 1
                      
                    await channel.send(f'Congrats {response.author.display_name}! The correct answer was {collection} by {brand}. Your current score is {db["scoreboard"][user_id]}.')
                    break
                      
            except asyncio.TimeoutError:
                 hints_given += 1
            if hints_given == 1:
                await channel.send(f'Hint: {hint}')
            else:
                await channel.send(f'Time is up! The correct answer was {collection} by {brand}.')
                break

#Guessing Game - Timed [Hard Mode]
async def hard_random_message():
    while True:
        interval = random.uniform(14400, 25200)  # Random interval between 4 and 7 hours
        await asyncio.sleep(interval)
        
        #values
        glist = db["game_list"]
        collectionno = random.choice(glist)
        brand = str(db[collectionno][0])
        collection = str(db[collectionno][1])
        scent = str(db[collectionno][2])
        hint = str(db[collectionno][3])
        channel = client.get_channel('channel id')  # Replace `channel_id` with the actual ID# of the channel you want to send the message to
      
        await channel.send(f'[HARD MODE] I am thinking of a scent from ??? with the following notes: {scent}')

        correct_answer = unidecode(re.sub(r'[^\w\s]', '', collection)).lower()

        def check(m):
            nonlocal correct_answer 
            if m.channel == channel and correct_answer and unidecode(re.sub(r'[^\w\s]', '', m.content)).lower() == correct_answer:
                return True
            return False
        
        hints_given = 0          
        while hints_given < 2:
            try:                                 
                response = await client.wait_for('message', check=check, timeout=30.0)
                if correct_answer:
                    correct_answer = unidecode(re.sub(r'[^\w\s]', '', response.content)).lower()

                    user_id = str(response.author.display_name)
                    if user_id in db["scoreboard"]:
                        db["scoreboard"][user_id] += 1
                    else:
                        db["scoreboard"][user_id] = 1
                      
                    await channel.send(f'Congrats {response.author.display_name}! The correct answer was {collection} by {brand}. Your current score is {db["scoreboard"][user_id]}.')
                    break  
                      
            except asyncio.TimeoutError:
                 hints_given += 1
            if hints_given == 1:
                await channel.send(f'Hint: {hint}')
            else:
                await channel.send(f'Time is up! The correct answer was {collection} by {brand}.')
                break

#Guessing Game - Timed [Easy Mode]
async def easy_random_message():
    while True:
        interval = random.uniform(10800, 18000)  # Random interval between 3 and 5 hours
        await asyncio.sleep(interval)
        
        #values
        glist = db["game_list"]
        collectionno = random.choice(glist)
        brand = str(db[collectionno][0])
        collection = str(db[collectionno][1])
        scent = str(db[collectionno][2])
        hint = str(db[collectionno][3])
        channel = client.get_channel('channel id')  # Replace `channel_id` with the actual ID# of the channel you want to send the message to
      
        await channel.send(f'I am thinking of the brand who created the scent {collection}.')

        correct_answer = unidecode(re.sub(r'[^\w\s]', '', brand)).lower()

        def check(m):
            nonlocal correct_answer
            if m.channel == channel and correct_answer and unidecode(re.sub(r'[^\w\s]', '', m.content)).lower() == correct_answer:
                return True
            return False
          
        while True:       
            try:                      
                response = await client.wait_for('message', check=check, timeout=60.0)
                if correct_answer:
                    correct_answer = unidecode(re.sub(r'[^\w\s]', '', response.content)).lower()

                    user_id = str(response.author.display_name)
                    if user_id in db["scoreboard"]:
                        db["scoreboard"][user_id] += 1
                    else:
                        db["scoreboard"][user_id] = 1
                      
                    await channel.send(f'Congrats {response.author.display_name}! The correct answer was {brand} created {collection}. Your current score is {db["scoreboard"][user_id]}.')
                    break
                  
            except asyncio.TimeoutError:
                await channel.send(f'Time is up! The correct answer was {brand} created {collection}.')
                break
                  
#Duck Game - Timed
async def duck_game():
    while True:
        interval = random.uniform(3600, 43200)  # Random interval between 1 and 12 hours
        await asyncio.sleep(interval)
      
        channel = client.get_channel('channel id')  # Replace `channel_id` with the actual ID# of the channel you want to send the message to
        await channel.send("・゜゜・。。・゜゜\\\_O<")

        while True:
            message = await client.wait_for('message', check=lambda m: m.channel == channel and (m.content == "!bang" or m.content == ".bang"))
            await channel.send(f"Congratulations {message.author.display_name}! You shot a duck!")
            break

async def main():
    await client.start(os.environ['TOKEN'])

asyncio.run(main())
