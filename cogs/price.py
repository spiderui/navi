import discord
from discord.ext import commands
from discord import app_commands
import requests
import os
from coinbase.wallet.client import Client as CoinbaseClient


# Pricechecker originally made for coingecko
# Coinbase API needed / may be changed

COINBASE_API_KEY = 'Insert-API'
COINBASE_API_SECRET = 'Insert-API-SecretKey'

class Price(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coinbase_client = CoinbaseClient(COINBASE_API_KEY, COINBASE_API_SECRET)

    @app_commands.command(name="price", description="Get the price of any cryptocurrency")
    async def price(self, interaction: discord.Interaction, coin_name: str):
        """Command to get the current price of a coin from Coinbase or CoinGecko."""
        
        coin_id = coin_name.lower()
        price = self.get_coin_price_from_coinbase(coin_id)

        if not price:  # token not on coinbase?, fallback to CoinGecko
            price = self.get_coin_price_from_coingecko(coin_id)

        if price:
            await interaction.response.send_message(f"The current price of {coin_name.capitalize()} is ${price}.")
        else:
            await interaction.response.send_message(f"Sorry, I couldn't find the price for {coin_name}.")

    def get_coin_price_from_coinbase(self, coin_id: str):
        """Get's current price of a coin using the Coinbase API."""
        try:
            price = self.coinbase_client.get_spot_price(currency_pair=f"{coin_id}-USD")
            return price.amount  # The price is in the 'amount' field
        except Exception as e:
            print(f"Error fetching from Coinbase: {e}")
            return None

    def get_coin_price_from_coingecko(self, coin_id: str):
        """Get's current price of a coin using the CoinGecko API."""
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if coin_id in data:
                return data[coin_id]['usd']
        return None

# cog setup
async def setup(bot):
    await bot.add_cog(Price(bot))