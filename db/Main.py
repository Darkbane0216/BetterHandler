import os
import discord
from discord.ext import commands
from discord.ui import Select, View
from dotenv import load_dotenv
from WorldCommands import load_world_data, search_world_db
from RiseCommands import load_rise_data, search_rise_db

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Display error if Discord Token is missing
if TOKEN is None:
    print("Error: DISCORD_TOKEN is not set in the environment.")
    exit(1)

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Load JSON data from files
world_data = load_world_data('mhw_db.json')
rise_data = load_rise_data('rise_monster_db.json')


# Bot initialization message
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


# Star emotes
def get_star_emotes(stars):
    return "⭐" * stars


# Better Help command
@bot.command(name='help')
async def new_help(ctx):
    help_embed = discord.Embed(title="Help Menu", color=discord.Color.yellow())
    help_embed.add_field(name="!help", value="Display this message", inline=False)
    help_embed.add_field(name="!worldsearch", value="A command to display monster stats from Monster Hunter: World\n"
                                                    "Stats include type, species, weaknesses, and resistances", inline=False)
    help_embed.add_field(name="!risesearch", value="A command to display monster stats from Monster Hunter: Rise\n"
                                                   "Stats include weaknesses, and resistances", inline=False)
    await ctx.send(embed=help_embed)


# Command to search the World database
@bot.command(name='worldsearch')
async def world_search(ctx, *, name_to_search: str):
    # Check if world database is loaded
    if world_data is None:
        await ctx.send("Error: Data is not loaded.")
        return

    # Search length error
    if len(name_to_search) < 3:
        await ctx.send("Search must be at least 3 characters.")
        return

    results = search_world_db(name_to_search, world_data)

    # No results error
    if not results:
        await ctx.send(f"No entries found for '{name_to_search}'.")
        return

    # Display result if there is only 1
    if len(results) == 1:
        await display_world_monster_info(ctx, results[0])
    # Display a select menu of matching monsters and allow the user to select the correct one
    else:
        options = [discord.SelectOption(label=result['name'], value=result['name']) for result in results]

        select = Select(placeholder="Choose a monster...", options=options)

        async def select_callback(interaction: discord.Interaction):
            selected_name = select.values[0]
            selected_monster = next(result for result in results if result['name'] == selected_name)
            await display_world_monster_info(interaction, selected_monster)

        select.callback = select_callback
        view = View()
        view.add_item(select)
        await ctx.send("Multiple results found. Please select one:", view=view)


# noinspection PyUnresolvedReferences
# Function to display World monster info
async def display_world_monster_info(ctx, result):
    embed = discord.Embed(title=f"{result['name']}  |  {result['type'].title()}  |  {result['species'].title()}",
                          color=discord.Color.red())
    # embed.add_field(name="Species", value=result['species'].upper(), inline=True)

    # Add weaknesses if there are any
    if result['weaknesses']:
        embed.add_field(name="Weaknesses:", value="\n".join(
            f"{weakness.split(' - ')[0]} - {get_star_emotes(weakness.count('*'))}"
            for weakness in result['weaknesses'].split(" \n ")
        ), inline=True)

    # Add resistances if there are any
    if result['resistances']:
        embed.add_field(name="Resistances:", value=result['resistances'].upper(), inline=True)

    if isinstance(ctx, discord.Interaction):
        await ctx.response.send_message(embed=embed)
    else:
        await ctx.send(embed=embed)


# Command to search the Rise database
@bot.command(name='risesearch')
async def rise_search(ctx, *, name_to_search: str):
    if rise_data is None:
        await ctx.send("Error: Data is not loaded.")
        return

    # Search length error
    if len(name_to_search) < 3:
        await ctx.send("Search must be at least 3 characters.")
        return

    results = search_rise_db(name_to_search, rise_data)

    # No results error
    if not results:
        await ctx.send(f"No entries found for '{name_to_search}'.")
        return

    # Display result if there is only 1
    if len(results) == 1:
        await display_rise_monster_info(ctx, results[0])
    # Display a select menu of matching monsters and allow the user to select the correct one
    else:
        options = [discord.SelectOption(label=result['name'], value=result['name']) for result in results]

        select = Select(placeholder="Choose a monster...", options=options)

        async def select_callback(interaction):
            selected_name = select.values[0]
            selected_monster = next(result for result in results if result['name'] == selected_name)
            await display_rise_monster_info(interaction, selected_monster)

        select.callback = select_callback
        view = View()
        view.add_item(select)
        await ctx.send("Multiple results found. Please select one:", view=view)


# Function to display Rise monster info
async def display_rise_monster_info(ctx, result):
    embed = discord.Embed(title=result['name'], color=discord.Color.blue())

    # Add weaknesses if there are any
    if result['weaknesses']:
        embed.add_field(name="Weaknesses:", value="\n".join(
            f"{weakness.split(' - ')[0]} - {get_star_emotes(weakness.count('*'))}"
            for weakness in result['weaknesses'].split(" \n ")
        ), inline=True)

    # Add resistances if there are any
    if result['resistances']:
        embed.add_field(name="Resistances:", value=result['resistances'].upper(), inline=True)

    if isinstance(ctx, discord.Interaction):
        # noinspection PyUnresolvedReferences
        await ctx.response.send_message(embed=embed)
    else:
        await ctx.send(embed=embed)


# Run the bot with the specified token
try:
    bot.run(TOKEN)
except discord.LoginFailure as e:
    print(f'Failed to connect to Discord: {e}')
