import discord
from discord.ext import commands
from discord import app_commands
import requests
from langdetect import detect  # language detection buggy sometimes spits out any language

class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="news", description="Get the latest news about any coin listed on CoinGecko")
    async def news(self, interaction: discord.Interaction, coin_name: str):
        """Get's the latest news for any coin listed on CoinGecko."""
        
        # Getting news from both api's
        newsapi_results = self.fetch_news_from_newsapi(coin_name)
        coingecko_results = self.fetch_news_from_coingecko(coin_name)
        
        # combining results to prevent probability of getting strange outputs
        combined_results = self.combine_news_results(newsapi_results, coingecko_results)
        
        if not combined_results:  # If no news is found
            await interaction.response.send_message(f"Sorry, no news found for `{coin_name}`.")
            return
        
        # Limit to top 5 news articles
        limited_results = combined_results[:5]  # Limit the results to top 5

        # Format the news for Discord
        formatted_news = self.format_news_for_discord(limited_results)
        
        # If passes discord limit print message
        if len(formatted_news) > 2000:
            await interaction.response.send_message("The news is too long to display here.")
            return
        
        # Getting icons from coingecko
        icon_url = self.fetch_coin_icon(coin_name)

        # Create and send the embed with the news articles
        embed = discord.Embed(
            title=f"Latest News on {coin_name.capitalize()}",
            description=formatted_news,
            color=discord.Color.blue()  
        )

        # Add the coin icon next to the title
        if icon_url:
            embed.set_thumbnail(url=icon_url)  # Set the thumbnail to the coin's logo

        # Add the footer image and footer text
        embed.set_footer(text="Navi powered by NewsAPI & CoinGecko | Latest Updates")
        embed.set_image(url="https://i.ytimg.com/vi/MxzQCnyc3Zc/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYAC0AWKAgwIABABGGUgZChNMA8=&rs=AOn4CLAcGDfJE7XD6d4F3CXec5sA8ieUtw")

        # Send the embed message
        await interaction.response.send_message(embed=embed)

    # function for news api
    def fetch_news_from_newsapi(self, query):
        url = f"https://newsapi.org/v2/everything?q={query}&apiKey=33ad2bf3db9c4bd09a0176f5ef2f4f87"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get('articles', [])
        return []

    # function for coingecko api
    def fetch_news_from_coingecko(self, coin_name):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_name}/news"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []

    # Combine results from both APIs
    def combine_news_results(self, newsapi_results, coingecko_results):
        # combining both results into one list
        combined_results = newsapi_results + coingecko_results

        # duplicated results fix
        seen = set()
        unique_results = []
        for article in combined_results:
            # Use the title or URL to check for uniqueness
            title = article.get('title')
            url = article.get('url')

            if title not in seen and url not in seen:
                seen.add(title)
                seen.add(url)
                unique_results.append(article)

        # sort the articles by published date (newest first)
        unique_results.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)

        return unique_results

    # formatting the news
    def format_news_for_discord(self, news_articles):
        formatted_news = ""
        for article in news_articles:
            title = article.get('title', 'No title')
            url = article.get('url', '#')
            description = article.get('description', 'No description available.')

            # Check the language of the description or title using langdetect
            try:
                if detect(description) != 'en' and detect(title) != 'en':
                    continue  # Skip articles that aren't in English
            except Exception as e:
                print(f"Error detecting language for article: {e}")
                continue

            # Add each article to the formatted output with spacing /  "Read more"
            formatted_news += f"**{title}**\n{description}\n\n[Click here to read more]({url})\n\n**Source:** {article.get('source', {}).get('name', 'Unknown Source')}\n\n"
            formatted_news += "\n"  # Extra space between articles for cleaner look
            
        return formatted_news

    # get the logos from CoinGecko
    def fetch_coin_icon(self, coin_name):
        url = f"https://api.coingecko.com/api/v3/coins/{coin_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data.get("image", {}).get("large")  # Thumbnail Icon
        return None

# Setup the cog
async def setup(bot):
    await bot.add_cog(News(bot))

