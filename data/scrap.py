# Imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
import smtplib
import csv
import time
import datetime


URL = 'https://www.amazon.com/crocs-Unisex-Classic-Black-Women/dp/B0014BYHJE/ref=pd_rhf_d_dp_s_pd_crcbs_sccl_1_1/147-6035204-7134748?pd_rd_w=phxBi&content-id=amzn1.sym.31346ea4-6dbc-4ac4-b4f3-cbf5f8cab4b9&pf_rd_p=31346ea4-6dbc-4ac4-b4f3-cbf5f8cab4b9&pf_rd_r=8CMDCVSYKR86RZ1E6D3T&pd_rd_wg=2RUmj&pd_rd_r=65d30b17-e282-4b68-b386-d483dccc8b9d&pd_rd_i=B0014BYHJE&psc=1'


def checkPrice():
    # Connect to Website
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36", "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    # Get HTML
    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    # Get Data
    title = soup2.find(id='productTitle').get_text()
    price = soup2.find(class_='a-offscreen').get_text()

    title = title.strip()
    price = price.strip()[1:]

    # Create a Timestamp
    today = datetime.date.today()

    # Create CSV & Read CSV
    data = [title, price, today]

    # Appending data to CSV
    with open('Web Scrapping/Dataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    # Send Mail if Price Drops
    if(float(price) < 10):
        sendMail()

    # Reading CSV
    print(pd.read_csv(
        r'D:\Skill\Coding\Language\Python\Projects\Web Scrapping\Dataset.csv'))


def sendMail():
    # Make Connection
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    # server.ehlo()
    server.starttls()
    # server.ehlo()
    server.login('manavgoyaltheboss@gmail.com', 'xxx')

    # Message
    subject = "Now is your chance to Buy!"
    body = "Don't mess it up! Link here: {URL}"
    message = f"Subject: {subject}\n\n{body}"

    # Send Email
    server.sendmail(
        'manavgoyaltheboss@gmail.com',
        'manav.goyal.dev@gmail.com',
        message
    )

    server.quit()


# Creating CSV file and adding Header to it
header = ['Title', 'Price', 'Date']
with open('Web Scrapping/Dataset.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)


while(True):
    checkPrice()
    time.sleep(10)
