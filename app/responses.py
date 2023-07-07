import random
from app.api_functions.telegrafi import scrape_telegrafi, data_telegrafi


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
        # TODO: add checks for all cases
        if p_message_list[1] == "telegrafi":
           
            scrape_result = await scrape_telegrafi(p_message_list, channel)
            return scrape_result
        
        else:
            return "Incorrect scraper name! Try one of ['telegrafi']"
        
    if p_message_list[0] == "/data":

        if p_message_list[1] == "telegrafi":
            await data_telegrafi(p_message_list, channel)

            
        else:
            return "Incorrect table name! Try one of ['telegrafi']"