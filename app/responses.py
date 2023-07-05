import random
import requests


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
            try:
                page_numbers = int(p_message_list[2])
            except ValueError:
                return "Incorrect type for page numbers"
            scrape_result = await scrape_telegrafi(page_numbers, channel)
            return scrape_result
        else:
            return "Incorrect scraper name! Try one of ['telegrafi']"


async def scrape_telegrafi(page_numbers, channel):
    url_paths = [
        "/lajme/",
        "/sport/",
        "/fun/",
        "/teknologji/",
        "/auto/",
        "/kuzhina/",
        "/shendetesi/",
        "/stili/",
        "/femra/",
        "/kultura/",
        "/magazina/",
        "/ekonomi/",
        "/bote/",
    ]
    count = 0
    for url_path in url_paths:
        await channel.send(f"Scraping {url_path} ...")

        response = requests.get(
            url="http://localhost:8000/telegrafi/scrape",
            params={"url_path": url_path, "page_numbers": page_numbers},
        )
        count += len(response.json())
        await channel.send(f"Scraped {len(response.json())} articles from {url_path}")

    return f"```Done: Scraped {count} articles```"
