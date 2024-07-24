import requests
import smtplib
import time
import datetime
import sys
from dotenv import dotenv_values
from bs4 import BeautifulSoup

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}
SECONDS = 150
config = dotenv_values(".env")
MATCHA_NAMES = [
    "Isuzu",
    "Wako"
]
URLS = {
    MATCHA_NAMES[0]: "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1/?currency=USD",
    MATCHA_NAMES[1]: "https://www.marukyu-koyamaen.co.jp/english/shop/products/1161020c1/?currency=USD"
}

def get_page_html(url):
    page = requests.get(url=url)
    return page.content

def is_in_stock(html):
    soup = BeautifulSoup(html, 'html.parser')
    in_stock = soup.find_all("p", {"class": "in-stock"})
    return len(in_stock) > 0

def send_message(phone_number, carrier, matcha_name, url):
    recipient = phone_number + CARRIERS[carrier]
    auth = (config["EMAIL"], config["PASSWORD"])
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    message = "The " + matcha_name +" matcha is now in stock! Please proceed to " + url
    server.sendmail(auth[0], recipient, message)

i = -1
while(True):
    output = ""
    i += 1
    url = URLS[MATCHA_NAMES[i % len(MATCHA_NAMES)]]
    if is_in_stock(get_page_html(url)):
        send_message(config["PHONE_NUMBER"], "verizon", MATCHA_NAMES[i], url)
        print("["+str(datetime.datetime.now())+"]: The " + MATCHA_NAMES[i] + " matcha is in stock. Text Message Sent!")
        break
    print("["+str(datetime.datetime.now())+"]: The " + MATCHA_NAMES[i] + " matcha is not in stock. Checking again in " + str(SECONDS * len(MATCHA_NAMES)) + " seconds.")
    time.sleep(SECONDS)