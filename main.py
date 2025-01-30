import discord
from discord.ext import commands
from discord import app_commands

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        
        # Syncing all commands with the new / (this should happen only once)
        try:
            synced = await self.tree.sync()  # Sync globally for all commands
            print(f'Synced {len(synced)} global commands')
        except Exception as e:
            print(f'Error syncing global commands: {e}')
        
        
        try:
            guild = discord.Object(id=1331124719109275709)  # guildID
            synced_admin_commands = await self.tree.sync(guild=guild)  # Only for this channelID
            print(f'Synced admin commands to guild {guild.id}')
        except Exception as e:
            print(f'Error syncing admin commands: {e}')

        # Print the command names for easier reading
        print("Registered commands:")
        for command in self.tree.get_commands():
            print(f"- {command.name}")
    
    async def on_message(self, message):
        """Handle message commands."""
        if message.author == self.user:
            return
        if message.content.startswith('hello'):
            await message.channel.send(f'sup {message.author}')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send('+1 Reaction')

    async def setup_hook(self):
        """Loading all the cogs before the bot starts up"""
        await self.load_extension('cogs.fun')  
        await self.load_extension('cogs.news')  
        await self.load_extension('cogs.price') 
        await self.load_extension('cogs.info')  
     
  

# Initialize the bot with intents
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="$", intents=intents)

# Start the bot (make sure to install all dependencies)
if __name__ == "__main__":
    client.run('Insert your token here')  # (token id needed)