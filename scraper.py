import sqlite3
from bs4 import BeautifulSoup
import requests
from dotenv import load_dotenv
import os
import psycopg2


load_dotenv()
# Connect to the Azure database
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_SSL = os.environ.get("DB_SSL")

con = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    sslmode=DB_SSL
)
cur = con.cursor()
# Create table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS books
                  (title TEXT, description TEXT, price TEXT, rating TEXT)''')

# HTML content
html = 'https://books.toscrape.com/'
html_content = requests.get(html)
# Parse the HTML
soup = BeautifulSoup(html_content.text, 'html.parser')
# Find all articles
book_articles = soup.find_all('article', class_='product_pod')
# print(book_articles)

for i in range(1, 51):
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    html_content = requests.get(url)
    soup = BeautifulSoup(html_content.text, 'html.parser')
    book_articles = soup.find_all('article', class_='product_pod')
    for article in book_articles:
        book_name = article.find('h3').find('a')
        title = book_name['title']
        print(i, title)
        url = article.find('h3').find('a')['href']
        # print(url)
        # https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
        url = 'https://books.toscrape.com/catalogue/' + url
        url_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        # print(url_soup)
        try:
            description = url_soup.find('div', {'id': 'product_description'}).find_next('p').text
        except:
            description = ''
        description = description.replace('â', '\'')
        # print(description)
        price = article.find('p', class_='price_color').text
        price = price.replace('Â£', '')
        # print(price)
        rating_classes = article.find('p', class_='star-rating')['class']
        rating = rating_classes[1]
        if rating == 'One':
            rating = 1
        elif rating == 'Two': 
            rating = 2 
        elif rating == 'Three':
            rating = 3
        elif rating == 'Four':
            rating = 4
        elif rating == 'Five':
            rating = 5
            
        # print(rating)
        # Insert data into the database
        cur.execute("INSERT INTO books (title, description, price, rating) VALUES (%s, %s, %s, %s)",
                   (title, description, price, rating))
        con.commit()


