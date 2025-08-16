import discord
from discord.ext import commands
from discord import app_commands
import datetime
import json
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# JSON file to store notes
FILE_NAME = "notes.json"

# Load existing notes if file exists
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as f:
        note_session = json.load(f)
        # Convert string time back to datetime
        if note_session["start_time"]:
            note_session["start_time"] = datetime.datetime.fromisoformat(note_session["start_time"])
else:
    note_session = {"start_time": None, "notes": []}

def save_notes():
    # Save session to file (convert datetime to string)
    data = note_session.copy()
    if data["start_time"]:
        data["start_time"] = data["start_time"].isoformat()
    with open(FILE_NAME, "w") as f:
        json.dump(data, f)

def is_expired():
    if note_session["start_time"] is None:
        return True
    return (datetime.datetime.utcnow() - note_session["start_time"]).total_seconds() > 12*3600

def get_notes_text():
    if not note_session["notes"]:
        return "No notes yet."
    return "\n".join(f"{i+1}. {n}" for i, n in enumerate(note_session["notes"]))

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("Commands synced!")
    except Exception as e:
        print(e)

# ---------------- NOTE COMMANDS ----------------

@bot.tree.command(name="note", description="Add a personal note")
@app_commands.describe(text="Text of your note")
async def note_command(interaction: discord.Interaction, text: str):
    global note_session
    
    if is_expired():
        note_session["start_time"] = datetime.datetime.utcnow()
        note_session["notes"] = []

    note_session["notes"].append(text)
    save_notes()
    
    await interaction.response.send_message(f"**Your Notes:**\n{get_notes_text()}")

@bot.tree.command(name="show", description="Show your current notes")
async def show_command(interaction: discord.Interaction):
    if is_expired():
        await interaction.response.send_message("No active notes. Use `/note` to start a new session.")
        return

    await interaction.response.send_message(f"**Your Notes:**\n{get_notes_text()}")

@bot.tree.command(name="clear", description="Clear all notes and start a new session")
async def clear_command(interaction: discord.Interaction):
    global note_session
    
    note_session["start_time"] = datetime.datetime.utcnow()
    note_session["notes"] = []
    save_notes()

    await interaction.response.send_message("✅ Notes cleared! A new session has started.")

@bot.tree.command(name="fallin", description="Ping everyone to join a meeting")
async def fallin_command(interaction: discord.Interaction):
    await interaction.response.send_message("@everyone Join for meeting")

@bot.tree.command(name="cadets-update", description="Ping everyone to give task updates")
async def cadets_update_command(interaction: discord.Interaction):
    await interaction.response.send_message('@everyone Give Update on tasks')

# PUT YOUR BOT TOKEN HERE
# --------------------
bot.run("------")
