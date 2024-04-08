import discord
from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv
import os
import re

load_dotenv()

# Function to fetch messages containing the specified word
async def fetch_messages(guild, word_to_track, bot_user_id):
    messages_data = []
    pattern = r'\b{}\b'.format(re.escape(word_to_track))  # Match the whole word only
    for channel in guild.text_channels:
        async for message in channel.history(limit=None):
            if (
                re.search(pattern, message.content, re.IGNORECASE) and
                message.author.id != bot_user_id  # Exclude messages sent by the bot
            ):
                messages_data.append((message.author.display_name, message.content, message.created_at))
    return messages_data

# Function to save data to a text file
async def save_data(ctx, word_to_track, message_content, count, filename):
    # Get the current datetime
    now = datetime.now()

    # Use a format with "am" or "pm" indicator
    entry_date_format = '%Y-%m-%d %I:%M:%S %p'

    # Prepare the data entry to save
    entry = f"Date: {now.strftime(entry_date_format)}\nServer: {ctx.guild.name}\nChannel: {ctx.channel.name}\nUser: {ctx.author.display_name}\nWord: {word_to_track}\nMessage : {message_content}\nCount: {count}\n----------------------"

    # Create the file if it doesn't exist
    if not os.path.exists(filename):
        open(filename, 'a').close()

    # Read existing data from file
    with open(filename, 'r') as f:
        lines = f.readlines()

    # Check if the entry already exists in the text file
    existing_entries = [line.split("\n")[0] for line in lines]
    
    if entry.split("\n")[4] in existing_entries:
        print("Entry already exists. No new data written.")
        return True  # Indicate that existing entry was found

    # Increment the count for the new entry
    count += 1

    # Insert the new entry at the correct position based on date
    new_entry_index = 0
    for index, line in enumerate(lines):
        if "Date" in line:
            try:
                entry_date = datetime.strptime(line.strip().split(": ")[1], entry_date_format)
                if entry_date < now:
                    new_entry_index = index
                    break
            except ValueError:
                print(f"Error parsing date from line: {line.strip()}")
                continue

    lines.insert(new_entry_index, entry + '\n')

    # Save data back to file
    with open(filename, 'w') as f:
        f.writelines(lines)

    # Count the number of new entries added
    num_new_entries = sum(1 for line in lines if line.strip() == entry)

    if num_new_entries > 0:
        print(f"{num_new_entries} new entries added to {filename}.")
    else:
        print("No new data written.")


# Set up Discord intents
intents = discord.Intents.default()
intents.messages = True

# Create the bot instance
bot = commands.Bot(command_prefix='/', intents=intents)




# Update track_word_count command
@bot.slash_command(name="track_word_count", description="Track the usage of a specific word")
async def track_word_count(ctx, word_to_track: str):
    try:
        # Acknowledge the interaction and defer the response (ephemeral)
        # await ctx.defer(ephemeral=True)

        # Count occurrences of the specified word across all text channels in the guild
        messages_data = await fetch_messages(ctx.guild, word_to_track, bot.user.id)
        count = len(messages_data)

        # Prepare the message to send
        response_message = f'The tracked word "{word_to_track}" has been used {count} times.'

        # Print the message to the terminal
        print(response_message)

        # Save the response to the data file
        existing_entry_found = False
        for user, message_content, _ in messages_data:
            # Prepare the message content
            message_content_formatted = f"({user}): {message_content}"
            
            # Check if the entry already exists
            if not existing_entry_found:
                print("New data is being written.")
                existing_entry_found = await save_data(ctx, word_to_track, message_content_formatted, count, "word_count_data.txt")

        if existing_entry_found:
            print("Entry already exists. No new data written.")

        # Send the response to the Discord channel
        await ctx.send(response_message)
    except Exception as e:
        print(f"Error in track_word_count: {e}")


# Update track_user_word_count command
@bot.slash_command(name="track_user_word_count", description="Track the number of times a specific user has used a word")
async def track_user_word_count(ctx, word_to_track: str, member: discord.Member):
    try:
        # Acknowledge the interaction and defer the response (ephemeral)
        # await ctx.defer(ephemeral=True)

        # Count occurrences of the specified word by the specified user across all text channels in the guild
        messages_data = await fetch_messages(ctx.guild, word_to_track, bot.user.id)
        count = sum(1 for user, _, _ in messages_data if user == member.display_name)

        # Prepare the message to send
        response_message = f'{member.display_name} has used the word "{word_to_track}" {count} times.'

        # Print the message to the terminal
        print(response_message)

        # Save the response to the data file
        print("New data is being written.")
        await save_data(ctx, word_to_track, response_message, count, "user_word_count_data.txt")  # Change filename here

        # Send the response to the Discord channel
        await ctx.send(response_message)
    except Exception as e:
        print(f"Error in track_user_word_count: {e}")

print("Bot is now online.")  # Add this line
print('Commands: /track_user_word_count and /track_word_count registred')

# Run the bot with the specified token
bot.run(os.getenv('DISCORD_TOKEN'))