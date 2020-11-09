import requests
from bs4 import BeautifulSoup
import re

#function shortens amazon urls and only accepts valid amazon.com urls
def extract_url(url):
    if url.find("www.amazon.com") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://amazon.com" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://amazon.com" + url[index:index2]
            else:
                url = None
    else:
        url = None

    return url

def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]","",price))
    return converted_price

def get_product_details(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Language' : 'en-US,en;q=0.5',
                'Accept-Encoding' : 'gzip', 
                'DNT' : '1', # Do Not Track Request Header 
                'Connection' : 'close'}
    details = {"name": "", "price": 0, "url": ""}

    extracted_url = extract_url(url)
    if extracted_url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        title = soup.find(id="productTitle")
        price = soup.find(id="price")

        details["name"] = title.get_text().strip()
        details["price"] = get_converted_price(price.get_text())
        details["url"] = extracted_url

    return details

amazon_url = input("Enter an Amazon URL: ")
print(get_product_details(amazon_url))
