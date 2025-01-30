from discord.ext import commands
from discord import app_commands
import discord

# Define the cog class
class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  # The bot instance passed from main.py

    @app_commands.command(name="printer3", description="Prints whatever text hiddenly")
    async def printer(self, interaction: discord.Interaction, printer: str):
        # Check if the user has administrator permissions
        if interaction.user.guild_permissions.administrator:
            # Hard-code the target channel IDs
            target_channel_a = self.bot.get_channel()  # Channel A could point to channel B/target channel (can be different server, no perms needed in the other server) 
            target_channel_b = self.bot.get_channel()  # Channel B points to -> target channel 

            # Send the message to both channels, adjust as needed if both channels arent useful for you
            await target_channel_a.send(printer)
            await target_channel_b.send(printer)

            # Confirmation 
            await interaction.response.send_message(f"Message sent to {target_channel_a.mention} and {target_channel_b.mention}")
        else:
            # If user isn't admin, won't have permission
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)

# setting cog
async def setup(bot):
    await bot.add_cog(Fun(bot))
