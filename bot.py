from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from plugins.helper import START_TXT
import aiohttp
import requests
from plugins.filepress import get_filepress

api_id = 13115322
api_hash = "f28fbd1367ddda2e6f863c3129323743"
bot_token = "5921362645:AAEOVznXBTwqx6XaASwN855j1rKmlN19Ef8"
bot = Client("bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token,workers=50,sleep_threshold=10)

@bot.on_message(filters.command(["start", "help"]) & filters.private)
async def welcome(client, message):
    await message.reply_text(
        text = START_TXT.format(mention = message.from_user.mention)
    )

@bot.on_message(filters.command(["setapi"]) & filters.private)
async def set_api(client, message):
    global api
    try:
        api = message.command[1]
        await message.reply_text(f"You have set your api successfully as\n\n<code>{api}</code>")
    except IndexError:
        await message.reply_text(f"Sorry, I couldn't process your request")

def convert_link(link):
    """Converts a Google Drive link with the `export=download` parameter to a link without the parameter."""
    url = link.split("&export=download")[0]
    return f"https://drive.google.com/file/d/{url}"

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    urls = message.text.split()
    short_links = []
    for url in urls:
        try:
            if url.startswith("https://drive.google.com") or url.startswith("http://drive.google.com") or url.startswith("drive.google.com"):
                fp = await get_filepress(url)
                if fp[0] != "":
                    short_link = await get_shortlink(fp[0])
                    short_links.append(short_link)
            else:
                short_link = await get_shortlink(url)
                short_links.append(short_link)
        except Exception as e:
            await message.reply(f'Error: {e}', quote=True)

    if len(short_links) > 0:
        text = f"Generated Shortened GyaniLinks:\n\n"
        text += "\n".join(short_links)
        await message.reply(text)

async def get_shortlink(link):
    url = 'https://gyanilinks.com/api'
    params = {'api': api, 'url': link, 'format': 'text'}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True) as response:
            short_link = await response.text()
            return short_link.strip()

bot.run()
