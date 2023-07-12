import random
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi
from app.api_functions.gjirafa import scrape_gjirafa, data_gjirafa, create_gjirafa_embed
from app.utils.weather import get_weather, format_weather_data


async def handle_response(user_message, channel, username) -> str:
    p_message: str = user_message.lower()
    p_message_list = p_message.split(" ")

    if p_message == "hello":
        return f"Hey there {username}"

    if p_message == "roll":
        return str(random.randint(1, 6))

    if p_message == "!help":
        return "This is a help message"

    if p_message_list[0] == "/scrape":
        if len(p_message_list) >= 2:
            if p_message_list[1] == "telegrafi":
                scrape_result = await scrape_telegrafi(p_message_list, channel)
                return scrape_result

            if p_message_list[1] == "gjirafa":
                scrape_result = await scrape_gjirafa(p_message_list, channel)
                return scrape_result


    if p_message_list[0] == "/data":
        if p_message_list[1] == "telegrafi":
            await data_telegrafi(p_message_list, channel)
            return None

        if p_message_list[1] == "gjirafa":
            if len(p_message_list) >= 3:
                query_params = {}
                for arg in p_message_list[2:]:
                    if ":" in arg:
                        key, value = arg.split(":")
                        query_params[key] = value
                results = await data_gjirafa(p_message_list, channel)
                return results
            else:
                return "Invalid arguments for Gjirafa data retrieval. Use 'name:value' format."

        else:
            return "Incorrect table name! Try one of ['telegrafi', 'gjirafa']"

    if p_message_list[0] == "/weather":
        if len(p_message_list) >= 2:
            location = p_message_list[1]
            weather_data = get_weather(location)
            if weather_data:
                return format_weather_data(weather_data)
            else:
                return "Unable to fetch weather data. Please try again later."
        else:
            return "Please provide a location for the weather command."

    return "Invalid command."
