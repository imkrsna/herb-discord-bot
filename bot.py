# Importing Modules
import os
import discord
from dotenv import load_dotenv
from discord.ext import commands

# Loading Env File
load_dotenv()
TOKEN = os.environ.get("TOKEN")

# Defining Variables
PREFIX = "."
DESCRIPTION = "Highly Efficient Rather Bot"
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(
    command_prefix=PREFIX,
    case_insenstive=True,
    description=DESCRIPTION,
)
bot.theme_color = 0x549d8a

# Bot Events
@bot.event
async def on_ready():
    print(f"Login as {bot.user}")

# Loading Cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Running Bot
bot.run(TOKEN, reconnect=True)
