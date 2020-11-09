import requests
from bs4 import BeautifulSoup
import re
from datetime import date
from difflib import SequenceMatcher

today = date.today() #get the date

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

#return a numerical values for the price
def get_converted_price(price):
    converted_price = float(re.sub(r"[^\d.]","",price))
    return converted_price

#function that will take a catalog site and get the individual links
def get_individual_details(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Language' : 'en-US,en;q=0.5',
                'Accept-Encoding' : 'gzip', 
                'DNT' : '1', # Do Not Track Request Header 
                'Connection' : 'close'}

    books = []

    extracted_url = extract_url(url)
    if extracted_url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        links= []
        for link in soup.find_all("a", class_="a-size-base a-link-normal"):
            try:
                page_url = "www.amazon.com/" + link['href']
                test = extract_url(page_url)
                if(test != None):
                    details = get_book_information(test)
                    if(details != None):
                        book_info.append(details)
                #print(link['href'])
            except KeyError:
                pass

    books_checked = []
    total_price = 0

    #check if the books have at least 80% similar titles to the first and last book in the list, in case of outliers
    for book in books:
        if (similar(book["title"], book_info[0]["title"]) > 0.8 and similar(book["title"], book_info[-1]["title"]) > 0.8):
            books_checked.append(book)  

    for book in books_checked:
        print(book)
        total_price = round(total_price + book["price"], 2)

    print("Total price of series:", total_price)

#function that will get the title, price, and url of book
def get_book_information(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
                'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
                'Accept-Language' : 'en-US,en;q=0.5',
                'Accept-Encoding' : 'gzip', 
                'DNT' : '1', # Do Not Track Request Header 
                'Connection' : 'close'}
    details = {"title": "", "price": 0, "status": "", "url": ""}

    last_in_stock = ""

    extracted_url = extract_url(url)
    if extracted_url == "":
        details = None
    else:
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        title = soup.find(id="productTitle")
        price = soup.find(class_="a-size-base a-color-price a-color-price")
        stock_status = soup.find(class_="a-size-medium a-color-success")

        details["title"] = title.get_text().strip()
        if(price != None):
            details["price"] = get_converted_price(price.get_text())
        if(stock_status != None):
            details["status"] = stock_status.get_text().strip()
        details["url"] = url

        #update the last time the book was in stock if currently in stock
        if(stock_status != None and details["status"] == "In Stock."):
            last_in_stock = today.strftime("%B %d, %Y")
            #print("Last in stock: " + last_in_stock)

        return details

#function that returns the similarity of two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

amazon_url = input("Enter an Amazon URL: ")
get_individual_details(amazon_url)
