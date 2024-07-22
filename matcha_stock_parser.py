import requests
import smtplib
from dotenv import dotenv_values
from email.message import EmailMessage
from bs4 import BeautifulSoup

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

config = dotenv_values(".env")

def get_page_html(url):
    page = requests.get(url=url)
    return page.content

def is_in_stock(html):
    soup = BeautifulSoup(html, 'html.parser')
    in_stock = soup.find_all("p", {"class": "in-stock"})
    return len(in_stock) > 0

def send_message(phone_number, carrier):
    recipient = phone_number + CARRIERS[carrier]
    auth = (config["EMAIL"], config["PASSWORD"])
 
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(auth[0], auth[1])
 
    message = "The matcha is now in stock! Please proceed to " + url + " to complete the transaction."
    server.sendmail(auth[0], recipient, message)

url = "https://www.marukyu-koyamaen.co.jp/english/shop/products/1191040c1/?currency=USD"

html = get_page_html(url)
# if is_in_stock(html):
send_message(config["PHONE_NUMBER"], "verizon")