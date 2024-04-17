from dotenv import load_dotenv
import os
import psycopg2
import streamlit as st


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


def search_books(search_term, min_rating, max_price):
    query = """SELECT * FROM books WHERE (title ILIKE %s OR description ILIKE %s) 
               AND (CAST(rating AS FLOAT) BETWEEN %s AND 5)
               AND (CAST(price AS FLOAT) <= %s)"""
    cur.execute(query, ('%' + search_term + '%', '%' + search_term + '%', min_rating, max_price))
    return cur.fetchall()


def main():
    st.title("Book Search and Filter App")
    
    # Search by name or description
    search_term = st.text_input("Search by name or description:")
    
    # Filter by minimum rating
    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
    
    # Filter by maximum price
    max_price = st.slider("Maximum Price", 0.0, 1000.0, 1000.0, 1.0)
    
    # Retrieve and display books based on search and filters
    books = search_books(search_term, min_rating, max_price)
    if books:
        st.write("### Search Results:")
        for book in books:
            st.write(f"Title: {book[0]}")
            st.write(f"Description: {book[1]}")
            st.write(f"Price: £{book[2]}")
            st.write(f"Rating: {book[3]}")
            st.write("---")
    else:
        st.write("No books found matching the search criteria.")


if __name__ == "__main__":
    main()


