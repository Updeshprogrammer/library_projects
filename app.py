import streamlit as st
import pandas as pd
import datetime

# Load data
books_df = pd.read_csv('books.csv')
users_df = pd.read_csv('users.csv')
borrow_records_df = pd.read_csv('borrow_records.csv')


# Save data function
def save_data(df, filename):
    df.to_csv(filename, index=False)


# Streamlit app
st.title("Library Management System")

# Sidebar for navigation
option = st.sidebar.selectbox("Choose an option",
                              ("View Books", "Add Book", "View Users", "Add User", "Borrow Book", "Return Book"))

if option == "View Books":
    st.header("List of Books")
    st.dataframe(books_df)

elif option == "Add Book":
    st.header("Add a New Book")
    book_id = st.number_input("Book ID", value=books_df['book_id'].max() + 1)
    title = st.text_input("Title")
    author = st.text_input("Author")
    available = st.checkbox("Available", value=True)

    if st.button("Add Book"):
        new_book = pd.DataFrame([[book_id, title, author, available]], columns=books_df.columns)
        books_df = pd.concat([books_df, new_book], ignore_index=True)
        save_data(books_df, 'books.csv')
        st.success("Book added successfully")

elif option == "View Users":
    st.header("List of Users")
    st.dataframe(users_df)

elif option == "Add User":
    st.header("Add a New User")
    user_id = st.number_input("User ID", value=users_df['user_id'].max() + 1)
    name = st.text_input("Name")
    email = st.text_input("Email")

    if st.button("Add User"):
        new_user = pd.DataFrame([[user_id, name, email]], columns=users_df.columns)
        users_df = pd.concat([users_df, new_user], ignore_index=True)
        save_data(users_df, 'users.csv')
        st.success("User added successfully")

elif option == "Borrow Book":
    st.header("Borrow a Book")
    book_id = st.number_input("Book ID", value=0, min_value=0, max_value=books_df['book_id'].max())
    user_id = st.number_input("User ID", value=0, min_value=0, max_value=users_df['user_id'].max())

    if st.button("Borrow"):
        book_idx = books_df[books_df['book_id'] == book_id].index[0]
        if books_df.at[book_idx, 'available']:
            borrow_date = datetime.date.today().isoformat()
            return_date = ''
            new_record = pd.DataFrame([[len(borrow_records_df) + 1, book_id, user_id, borrow_date, return_date]],
                                      columns=borrow_records_df.columns)
            borrow_records_df = pd.concat([borrow_records_df, new_record], ignore_index=True)
            books_df.at[book_idx, 'available'] = False
            save_data(books_df, 'books.csv')
            save_data(borrow_records_df, 'borrow_records.csv')
            st.success("Book borrowed successfully")
        else:
            st.error("Book is not available")

elif option == "Return Book":
    st.header("Return a Book")
    record_id = st.number_input("Record ID", value=0, min_value=0, max_value=borrow_records_df['record_id'].max())

    if st.button("Return"):
        record_idx = borrow_records_df[borrow_records_df['record_id'] == record_id].index[0]
        book_id = borrow_records_df.at[record_idx, 'book_id']
        borrow_records_df.at[record_idx, 'return_date'] = datetime.date.today().isoformat()
        book_idx = books_df[books_df['book_id'] == book_id].index[0]
        books_df.at[book_idx, 'available'] = True
        save_data(books_df, 'books.csv')
        save_data(borrow_records_df, 'borrow_records.csv')
        st.success("Book returned successfully")
