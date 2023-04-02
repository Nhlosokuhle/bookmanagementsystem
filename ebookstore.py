# import modules
import sqlite3
from tabulate import tabulate

# This variable will store table headings
table_headings = ['ID', 'TITLE', 'AUTHOR', 'QTY']


def get_book_title_data():
    """This function will extract book titles from the database and store them in a list.
        This function will return that list."""
    book_title_list = []
    try:
        # Create or open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        # Execute a command that will retrieve data from the book table
        cursor.execute('SELECT Title FROM books')
        # This variable will store data that is retrieved from the table
        results = cursor.fetchall()
        # Display a table to the user
        for books_title in results:
            for book_title in books_title:
                book_title_list.append(book_title)
        return book_title_list
    except Exception as e:
        # Roll back any changes that were made if something wrong occurs
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def get_book_id_data():
    """This function will extract book ids from the database and store them in a list.
            This function will return that list."""
    book_id_list = []
    try:
        # Create or open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        # Execute a command that will retrieve data from the book table
        cursor.execute('SELECT id FROM books')
        # This variable will store data that is retrieved from the table
        results = cursor.fetchall()
        # Display a table to the user
        for books_id in results:
            for book_id in books_id:
                book_id_list.append(book_id)
        return book_id_list
    except Exception as e:
        # Roll back any changes that were made if something wrong occurs
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def create_table():
    """This function will create the table if it does not exist"""
    try:
        # Create or open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        # Execute a command that will create a table if it does not exist
        cursor.execute('CREATE TABLE IF NOT EXISTS books(id INTEGER PRIMARY KEY, Title TEXT, Author TEXT, Qty INTEGER)')
        # Commit changes to the database
        db.commit()
    except Exception as e:
        # Roll back any changes made to the database if there are any errors
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def view_books():
    """This function will display the table records on the console"""
    try:
        # Create or open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        # Execute a command that will retrieve data from the book table
        cursor.execute('SELECT * FROM books')
        # This variable will store data that is retrieved from the table
        results = cursor.fetchall()
        # Display a table to the user
        print(tabulate(results, table_headings))
    except Exception as e:
        # Roll back any changes that were made if something wrong occurs
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def add_book():
    """This function will allow the user to add new books to the database"""
    book_id = int(input('Enter the id of the book: '))
    book_title = input('Enter the title of the book: ')
    book_author = input('Enter the author of the book: ')
    book_qty = int(input('Enter the quantity of the book: '))
    try:
        # Create or open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        # Execute a command that will add data to the book table
        cursor.execute('INSERT INTO books VALUES(?, ?, ?, ?)', (book_id, book_title, book_author, book_qty))
        # Commit changes to the database
        db.commit()
        # Display a message to the user
        print(f'\n{book_title} was successfully added to the system.')
    except Exception as e:
        # Roll back any changes made to the database if there are errors
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def update_book():
    """This function will allow the user to update book information"""
    try:
        # Open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        book_id = input('Enter the id of the book you want to update: ')
        book_id_list = get_book_id_data()
        if book_id in book_id_list:
            while True:
                field = input('Which field do want to update? (Title/Author/Qty): ')
                value = input(f'Enter the new {field} of the book: ')
                # Execute a command that will update the information of the book
                cursor.execute(f'UPDATE books SET {field} = ? WHERE id = ?', (value, book_id))
                # Commit changes that were made to the database
                db.commit()
                # Display a message to the user
                print('\nRecord was successfully updated.\n')
                changes = input('Do you want to make more changes to the record? (Y/N): ').lower()
                if changes == 'n':
                    break
        else:
            print(f'\nError! Book ID {book_id} does not exist in the database.')
        input('\nPress ENTER to return the main menu...')
    except Exception as e:
        # Roll back any changes made to the database if something is wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def delete_book():
    """This function will allow the user to delete books from the database"""
    book_id = input('\nEnter the book id of the book you want to delete: ')
    books_id_list = get_book_id_data()
    try:
        # Open a file called ebookstore.db
        db = sqlite3.connect('ebookstore.db')
        # Get a cursor object
        cursor = db.cursor()
        if book_id in books_id_list:
            # Execute a command that will delete a record chosen by the user
            cursor.execute('DELETE FROM books WHERE id = (?) ', [book_id])
            # Commit the change made to the database
            db.commit()
            print(f'\nBook ID {book_id} was successfully removed from the system.')
        else:
            print(f'\nError! Book ID {book_id} does not exist in the database.')
        input('\nPress ENTER to return the main menu...')
    except Exception as e:
        # Roll back any changes make to the database
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()


def search_book():
    """This function will allow the user to search the database to find a specific book"""
    book_title = input('\nEnter the title of the book: ')
    books_title_list = get_book_title_data()
    if book_title in books_title_list:
        try:
            # Open a file called ebookstore
            db = sqlite3.connect('ebookstore.db')
            # Get a cursor object
            cursor = db.cursor()
            # Execute a command that will retrieve the details of the book enter by the user
            cursor.execute('SELECT * FROM books WHERE Title = ? ', [book_title])
            # This variable will store the details of the books
            results = cursor.fetchall()
            # Display the result
            print(tabulate(results, table_headings))
        except Exception as e:
            # Roll back any changes made to the database if there is something wrong
            db.rollback()
            raise e
        finally:
            # Close the db connection
            db.close()
    else:
        print(f'\nError! {book_title} was not found.')
    input('\nPress ENTER to return to the main menu...')


def generate_report():
    number_of_books = get_book_id_data()
    print(f"""
*** REPORT ****
Number of books: {len(number_of_books)}
    """)
    input('\nPress ENTER to return to the main menu...')


create_table()
while True:
    get_book_id_data()
    user_choice = input('''
Please choose one of the following options:
e - Enter book
u - Update book
d - Delete book
s - Search books
v - view report
c - Close the program 
---------> ''').lower()
    if user_choice == 'e':
        add_book()
    elif user_choice == 'u':
        view_books()
        update_book()
    elif user_choice == 'd':
        view_books()
        delete_book()
    elif user_choice == 's':
        search_book()
    elif user_choice == 'v':
        generate_report()
    elif user_choice == 'c':
        print('Goodbye!')
        break
    else:
        print('\nError! Please choose the correct menu option.')
