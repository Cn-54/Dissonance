import os
import discord
import requests

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")
HOSTNAME = socket.gethostname()

MODULES_CATEGORY_NAME = "MODULES"
MODULES_CHANNEL_NAME = "modules"
AGENTS_CATEGORY_NAME = "AGENTS"

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)


async def setup():
    guild = bot.get_guild(GUILD_ID)

    if not guild: # checks if guild actually exists
        print(" [!] Guild not found")
        exit()
    
    category = discord.utils.get(guild.categories, name = AGENTS_CATEGORY_NAME) 

    if not category: # checks if AGENTS category exists if it doesnt create it
        category = await guild.create_category(AGENTS_CATEGORY_NAME)

    categoryModules = discord.utils.get(guild.categories, name = MODULES_CATEGORY_NAME) 

    if not categoryModules: # checks if MODULES category exists if it doesnt create it
        category = await guild.create_category(MODULES_CATEGORY_NAME)
    
    
    agent_channel = discord.utils.get(guild.text_channels, name=HOSTNAME)

    if not agent_channel: # checks if this agents channel exists if not it creates the channel
        agent_channel = await guild.create_text_channel( HOSTNAME, category=category)
    
    modules_channel = discord.utils.get( guild.text_channels,name=MODULES_CHANNEL_NAME)

    if not modules_channel:
        agent_channel = await guild.create_text_channel(MODULES_CHANNEL_NAME, category=category)


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")
    await setup()




bot.run(TOKEN)