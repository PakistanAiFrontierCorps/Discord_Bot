import discord
from discord import app_commands

TOKEN = "---------"  # replace with your token

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()

client = MyClient()

@client.tree.command(name="fallin", description="Responds with Aye Aye Captain")
@app_commands.describe(text="Any text you want to send")
async def fallin(interaction: discord.Interaction, text: str):
    await interaction.response.send_message("Aye Aye Captain")

client.run(TOKEN)
