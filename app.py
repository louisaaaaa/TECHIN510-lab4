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


def search_books(search_term, min_rating, max_rating, min_price, max_price):
    query = """SELECT title, price, rating, description FROM books 
               WHERE (title ILIKE %s OR description ILIKE %s) 
               AND (CAST(rating AS FLOAT) BETWEEN %s AND %s)
               AND (CAST(price AS FLOAT) BETWEEN %s AND %s)"""
    cur.execute(query, ('%' + search_term + '%', '%' + search_term + '%', min_rating, max_rating, min_price, max_price))
    return cur.fetchall()


def main():
    st.title("Book Search and Filter App")
    
    # Search by name or description
    search_term = st.text_input("Search by name or description:")
    
    # Filter by rating range
    min_rating, max_rating = st.slider("Rating Range", 0, 5, (0, 5), 1)
    
    # Filter by price range
    min_price, max_price = st.slider("Price Range", 0, 100, (0, 100), 1)
    
    # Retrieve and display books based on search and filters
    books = search_books(search_term, min_rating, max_rating, min_price, max_price)
    st.write("### See serach result below book description section!")
    if books:
        # Allow user to select a book for more details
        selected_book_index = st.selectbox("Use ID to select a book for detailed description:", range(len(books)))
        selected_book = books[selected_book_index]
        st.write("### Book Description:")
        # Display description of the selected book
        st.write(f"Description: {selected_book[3]}")
        
        st.write("### Search Results:")
        # Display search results in a table with column names
        table_data = [[book[0], f"${book[1]}", book[2]] for book in books]
        st.table(data=table_data)
        
        
    else:
        st.write("No books found matching the search criteria.")





if __name__ == "__main__":
    main()


