import sqlite3

# Function to create tables in the database
def create_tables():
    connection_params = {"database": "mydb.sqlite3"}

    # Connect to the database
    connect = sqlite3.connect(connection_params["database"])
    cursor = connect.cursor()

    # Create Table Зачетки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Зачетки (
            №зачетки INTEGER PRIMARY KEY,
            ФИО TEXT,
            группа TEXT
        )
    ''')

    # Insert data into Зачетки
    cursor.execute('''
        INSERT INTO Зачетки (№зачетки, ФИО, группа) VALUES
        (1, 'Иванов Иван', 'Группа A'),
        (2, 'Петров Петр', 'Группа B'),
        (3, 'Сидоров Сидор', 'Группа A')
    ''')

    # Create Table Группа
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Группа (
            Группа TEXT PRIMARY KEY,
            факультет TEXT,
            специальность TEXT
        )
    ''')

    # Insert data into Группа
    cursor.execute('''
        INSERT INTO Группа (Группа, факультет, специальность) VALUES
        ('Группа A', 'Факультет 1', 'Специальность X'),
        ('Группа B', 'Факультет 2', 'Специальность Y'),
        ('Группа C', 'Факультет 1', 'Специальность Z')
    ''')

    # Create Table Студенты
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Студенты (
            ФИО TEXT PRIMARY KEY,
            год_рождения DATE,
            адрес TEXT,
            телефон TEXT
        )
    ''')

    # Insert data into Студенты
    cursor.execute('''
        INSERT INTO Студенты (ФИО, год_рождения, адрес, телефон) VALUES
        ('Иванов Иван', '1998-03-15', 'Адрес 1', '123-456-7890'),
        ('Петров Петр', '1999-07-20', 'Адрес 2', '987-654-3210'),
        ('Сидоров Сидор', '1997-11-10', 'Адрес 3', '555-123-4567')
    ''')

    # Commit changes and close connection
    connect.commit()
    cursor.close()
    connect.close()

if __name__ == "__main__":
    # Call the function to create tables
    create_tables()

    print("Tables created and data inserted successfully.")
