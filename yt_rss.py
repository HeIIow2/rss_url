from requests_html import HTMLSession
from bs4 import BeautifulSoup as bs 

import time
import random

INPUT_PATH = "channel_input.txt"
OUTPUT_PATH = "rss_output.txt"

def random_delay():
    time.sleep(random.randint(7, 14))

def get_ch_id(channel_url: str) -> (str, str):
    session = HTMLSession()

    response = session.get(channel_url)
    response.html.render(sleep=1)
    soup = bs(response.html.html, "html.parser")
    
    # print("\n".join([str(i) for i in soup.find_all("meta")]))
    
    channel_meta = soup.find("meta", property="al:web:url")
    if channel_meta is None:
        return None, None
    channel_url_id = str(channel_meta['content'])
    channel_name_ = soup.find("meta", property="og:title")
    if channel_name_ is None:
        return None, None
    channel_name = str(channel_name_['content'])
    
    return channel_url_id.replace("https://www.youtube.com/channel/", "").replace("?feature=applinks", ""), channel_name

def get_rss_url(channel_url: str) -> str: 
    YT_RSS_BASE = "https://www.youtube.com/feeds/videos.xml?channel_id="
    ch_id, ch_name = get_ch_id(channel_url)
    while ch_id is None or ch_name is None:
        print("retry")
        random_delay()
        ch_id, ch_name = get_ch_id(channel_url)
    return YT_RSS_BASE + ch_id, ch_name


if __name__ == "__main__":
    rss_urls = []

    with open(INPUT_PATH, "r") as f:
        lines = f.read().split("\n")
        for line in lines:
            print(line)
            rss_urls.append(get_rss_url(line))
            print(rss_urls[-1], "\n")
            random_delay()
            
    with open(OUTPUT_PATH, "w") as f:
        f.write("\n".join([f"{i[0]} {i[1]}" for i in rss_urls]))
