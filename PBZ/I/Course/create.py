import sqlite3


def create_tables():
    connection_params = {"database": "mydb.sqlite3"}

    connect = sqlite3.connect(connection_params["database"])
    cursor = connect.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Клиент (
            КлиентID INTEGER PRIMARY KEY,
            Имя TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Продавец (
            ПродавецID INTEGER PRIMARY KEY,
            Имя TEXT,
            Категория TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Товар (
            ТоварID INTEGER PRIMARY KEY,
            Название TEXT,
            Цена REAL,
            Описание TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Скидка (
            СкидкаID INTEGER PRIMARY KEY,
            ТоварID INTEGER,
            Размер_скидки REAL,
            FOREIGN KEY (ТоварID) REFERENCES Товар (ТоварID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Чек (
            ЧекID INTEGER PRIMARY KEY,
            ПродавецID INTEGER,
            КлиентID INTEGER,
            Дата_и_время_покупки TEXT,
            Сумма_без_скидки REAL,
            Сумма_со_скидкой REAL,
            FOREIGN KEY (ПродавецID) REFERENCES Продавец (ПродавецID),
            FOREIGN KEY (КлиентID) REFERENCES Клиент (КлиентID)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Покупка (
            ПокупкаID INTEGER PRIMARY KEY,
            КлиентID INTEGER,
            ТоварID INTEGER,
            ЧекID INTEGER,
            Количество INTEGER,
            FOREIGN KEY (КлиентID) REFERENCES Клиент (КлиентID),
            FOREIGN KEY (ТоварID) REFERENCES Товар (ТоварID),
            FOREIGN KEY (ЧекID) REFERENCES Чек (ЧекID)
        )
    ''')

    cursor.execute('''CREATE TRIGGER IF NOT EXISTS update_check_price
AFTER INSERT ON Покупка
BEGIN
    UPDATE Чек
    SET Сумма_без_скидки = Сумма_без_скидки + (SELECT Цена FROM Товар WHERE ТоварID = NEW.ТоварID) * NEW.Количество,
        Сумма_со_скидкой = Сумма_со_скидкой + 
                           (SELECT CASE WHEN Скидка.Размер_скидки IS NOT NULL 
                                       THEN (Цена * (1 - Скидка.Размер_скидки)) * NEW.Количество
                                       ELSE Цена * NEW.Количество
                                  END
                            FROM Товар
                            LEFT JOIN Скидка ON Товар.ТоварID = Скидка.ТоварID
                            WHERE Товар.ТоварID = NEW.ТоварID)
    WHERE ЧекID = (SELECT ЧекID FROM Чек WHERE КлиентID = NEW.КлиентID ORDER BY ЧекID DESC LIMIT 1)
        AND EXISTS (SELECT 1 FROM Покупка WHERE КлиентID = NEW.КлиентID);

    INSERT INTO Чек (ПродавецID, КлиентID, Дата_и_время_покупки, Сумма_без_скидки, Сумма_со_скидкой)
    SELECT 1, NEW.КлиентID, DATETIME('now'), 
            (SELECT Цена FROM Товар WHERE ТоварID = NEW.ТоварID) * NEW.Количество,
            (SELECT CASE WHEN Скидка.Размер_скидки IS NOT NULL 
                         THEN (Цена * (1 - Скидка.Размер_скидки)) * NEW.Количество
                         ELSE Цена * NEW.Количество
                    END
             FROM Товар
             LEFT JOIN Скидка ON Товар.ТоварID = Скидка.ТоварID
             WHERE Товар.ТоварID = NEW.ТоварID)
    WHERE NOT EXISTS (SELECT 1 FROM Чек WHERE КлиентID = NEW.КлиентID);
END;
''')

    connect.commit()
    connect.close()


create_tables()

