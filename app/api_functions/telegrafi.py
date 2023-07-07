import requests


async def scrape_telegrafi(p_message_list, channel):
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
    query_params = {}
    
    for argument in p_message_list[2:]: 
        splitted_argument = argument.split(":")  
        argument_name = splitted_argument[0]  
        argument_value = splitted_argument[1]  
        query_params[argument_name] = argument_value

    for url_path in url_paths:
        await channel.send(f"Scraping {url_path} ...")
        query_params["url_path"]=url_path 
        response = requests.get(
            url="http://localhost:8000/telegrafi/scrape",
            params=query_params 
        )
        count += len(response.json())
        await channel.send(f"Scraped {len(response.json())} articles from {url_path}")

    return f"```Done: Scraped {count} articles```"



async def data_telegrafi(p_message_list, channel):
    query_params={}
    for argument in p_message_list[2:]:
        
        splitted_argument=argument.split(":")
        argument_name=splitted_argument[0]
        argument_value=splitted_argument[1]
        query_params[argument_name]=argument_value


    response = requests.get(
        url="http://localhost:8000/telegrafi/data",
        params=query_params
    )
    
    
    results = response.json()["results"]

    for result in results:
        await channel.send(f"{result['name']}\nScraping Date: {result['date_scraped']}\n```{result['details_link']}```")