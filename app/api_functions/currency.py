import discord
from discord import Embed
from forex_python.converter import CurrencyRates, CurrencyCodes


async def currency_convert(p_message_list, channel, username, is_private):
    thumbnail_url = "https://plus.unsplash.com/premium_photo-1679255807252-3c568399dfc2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Z29sZCUyMGNvaW5zfGVufDB8fDB8fHww&w=1000&q=80"
    amount = float(p_message_list[1])
    from_currency = p_message_list[2].upper()
    to_currency = p_message_list[4].upper()

    c = CurrencyCodes()

    from_currency_name = c.get_currency_name(from_currency)
    to_currency_name = c.get_currency_name(to_currency)

    c = CurrencyRates()
    converted_amount = c.convert(from_currency, to_currency, amount)
    converted_amount = round(converted_amount, 2)
    embed = Embed(title="Converted Currency",
                  description=f"{amount} {from_currency} ({from_currency_name}) is equal to:\n {converted_amount} {to_currency} ({to_currency_name})", 
                  color=discord.Color.dark_orange())
    embed.set_thumbnail(url=thumbnail_url)
    if is_private:
        await username.send(embed=embed)
    else:
        await channel.send(embed=embed)