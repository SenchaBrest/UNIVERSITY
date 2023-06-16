import psycopg2

def init():
    try:
        CONNECT = psycopg2.connect(user="postgres", password="P2r3i5m7e11;")
        CURSOR = CONNECT.cursor()
        print("Congrats u are connected!")
    except:
        print("Smth go wrong!")
    return CONNECT, CURSOR

def delete_all():
    table_list = ["books", "reader", "card"] # , "place"
    for table_name in table_list:
        sql = f"DROP TABLE {table_name}"
        CURSOR.execute(sql)
        CONNECT.commit()

def create_tables():
    
    sql = """CREATE TABLE books (
        id bigserial PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        author VARCHAR(150) NOT NULL,
        year INTEGER NOT NULL,
        annotation VARCHAR(1000)
    );
    """
    CURSOR.execute(sql)
    CONNECT.commit()
    
    sql = """CREATE TABLE reader (
        id bigserial PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        birthday VARCHAR(10),
        email VARCHAR(100),
        tel VARCHAR(50)
    );
    """
    CURSOR.execute(sql)
    CONNECT.commit()
    sql = """CREATE TABLE card (
        id bigserial PRIMARY KEY,
        reader_id INT NOT NULL,
        book_id INT NOT NULL,
        date_from VARCHAR(10) NOT NULL,
        date_return VARCHAR(10) NOT NULL,
        state INT NOT NULL,
        book_rating REAL,
        reader_rating REAL
    );
    """
    CURSOR.execute(sql)
    CONNECT.commit()
    sql = """CREATE TABLE place (
        id bigserial PRIMARY KEY,
        book_id INT NOT NULL,
        rack INT,
        shelf INT,
        position INT
    );
    """
    CURSOR.execute(sql)
    CONNECT.commit()

def insert_reader(name, birthday, email, tel):
    sql_statement = f"INSERT INTO books (name, birthday, email, tel) VALUES ('{name}', '{birthday}', {email}, '{tel}')"
    print(sql_statement)
    CURSOR.execute(sql_statement)
    CONNECT.commit()

def insert_book(name, author, year, annotation):
    sql_statement = f"INSERT INTO books (name, author, year, annotation) VALUES ('{name}', '{author}', {year}, '{annotation}')"
    print(sql_statement)
    CURSOR.execute(sql_statement)
    CONNECT.commit()

def insert_card(reader_id, book_id, date_from, date_return, state, book_rating, reader_rating):
    sql_statement = f"INSERT INTO books (reader_id, book_id, date_from, date_return, state, book_rating, reader_rating) \
        VALUES ('{reader_id}', '{book_id}', '{date_from}', '{date_return}', '{state}', '{book_rating}', '{reader_rating}')"
    print(sql_statement)
    CURSOR.execute(sql_statement)
    CONNECT.commit()

def update_book_name(book_id, new_name):
    sql_statement = f"UPDATE books SET name='{new_name}' WHERE id={book_id}"
    print(sql_statement)
    CURSOR.execute(sql_statement)
    CONNECT.commit()

def delete_book(book_id):
    sql_statement = f"DELETE FROM books WHERE id={book_id}"
    print(sql_statement)
    CURSOR.execute(sql_statement)
    CONNECT.commit()

def show_table(table_name):
    sql = f"SELECT * FROM {table_name}"
    print(sql)
    CURSOR.execute(sql)
    result = CURSOR.fetchall()
    print(result)

def find_book_by_id(book_id):
    sql = f"""
          SELECT * FROM place WHERE book_id = {book_id}
          """ 
    print(sql)
    CURSOR.execute(sql)
    result = CURSOR.fetchone()
    print(result)

def find_book_by_name(name):
    sql = f"""
           SELECT * FROM 
           place INNER JOIN books ON place.book_id = books.id
           WHERE books.name LIKE '%{name}%'
           """
    print(sql)
    CURSOR.execute(sql)
    result = CURSOR.fetchone()
    print(result)

def find_book_by_annotation(annotation):
    pass

def find_reader_by_id(reader_id):
    sql = f"""
          SELECT * FROM place WHERE reader_id = {reader_id}
          """ 
    print(sql)
    CURSOR.execute(sql)
    result = CURSOR.fetchone()
    print(result)

def find_reader_by_name(name):
    sql = f"""
           SELECT * FROM 
           place INNER JOIN books ON place.reader_id = reader.id
           WHERE reader.name LIKE '%{name}%'
           """
    print(sql)
    CURSOR.execute(sql)
    result = CURSOR.fetchone()
    print(result)
    
if __name__=="__main__":
    CONNECT, CURSOR = init()

    # create_tables()

    # insert_book("Basic",
    #            "T.Curts",
    #            1965,
    #           "Just for professionals")

    if bool(find_reader_by_name(input("Enter the reader`s name: "))): # 
        print("This reader is in the database.")
    else: 
        print("This reader is not in the database.")
        insert_reader(input("Name: "), input("Birthday: "), input("Email: "), input("Tel: "))
    
    if bool(find_book_by_name(input("Enter the book`s name: "))):
        print("This book is in the library.")
        insert_card()
        delete_book()
    else: 
        print("This book is not in the library.")
        find_book_by_annotation(input("Enter smth: "))
    
    #delete_all()
    CONNECT.close()
    CURSOR.close()