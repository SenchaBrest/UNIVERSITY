CREATE TABLE "Поставщики S"
(
    П       TEXT    NOT NULL
        CONSTRAINT "Поставщики S_pk"
            PRIMARY KEY,
    "Имя П" TEXT    NOT NULL,
    Статус  INTEGER NOT NULL,
    Город   TEXT    NOT NULL
);
INSERT INTO "Поставщики S" (П, "Имя П", Статус, Город)
VALUES ('П1', 'Петров', 20, 'Москва'),
       ('П2', 'Синицин', 10, 'Таллинн'),
       ('П3', 'Федоров', 30, 'Таллинн'),
       ('П4', 'Чаянов', 20, 'Минск'),
       ('П5', 'Крюков', 30, 'Киев');



CREATE TABLE "Детали P"
(
    Д       TEXT    NOT NULL
        CONSTRAINT "Детали P_pk"
            PRIMARY KEY,
    "Имя Д" TEXT    NOT NULL,
    Цвет    TEXT    NOT NULL,
    Размер  INTEGER NOT NULL,
    Город   TEXT    NOT NULL
);
INSERT INTO "Детали P" (Д, "Имя Д", Цвет, Размер, Город)
VALUES ('Д1', 'Болт', 'Красный', 12, 'Москва'),
       ('Д2', 'Гайка', 'Зеленая', 17, 'Минск'),
       ('Д3', 'Диск', 'Черный', 17, 'Вильнюс'),
       ('Д4', 'Диск', 'Черный', 14, 'Москва'),
       ('Д5', 'Корпус', 'Красный', 12, 'Минск'),
       ('Д6', 'Крышки', 'Красный', 19, 'Москва');



CREATE TABLE "Проекты J"
(
    ПР       TEXT NOT NULL
        CONSTRAINT "Проекты J_pk"
            PRIMARY KEY,
    "Имя ПР" TEXT NOT NULL,
    Город    TEXT NOT NULL
);
INSERT INTO "Проекты J" (ПР, "Имя ПР", Город)
VALUES ('ПР1', 'ИПР1', 'Минск'),
       ('ПР2', 'ИПР1', 'Таллинн'),
       ('ПР3', 'ИПР3', 'Псков'),
       ('ПР4', 'ИПР4', 'Псков'),
       ('ПР5', 'ИПР4', 'Москва'),
       ('ПР6', 'ИПР6', 'Саратов'),
       ('ПР7', 'ИПР7', 'Москва');



CREATE TABLE "Количество деталей, поставляемых одним поставщиком для одного проекта"
(
    П  TEXT    NOT NULL,
    Д  TEXT    NOT NULL,
    ПР TEXT    NOT NULL,
    S  INTEGER NOT NULL
);
INSERT INTO "Количество деталей, поставляемых одним поставщиком для одного проекта" (П, Д, ПР, S)
VALUES ('П1', 'Д1', 'ПР1', 200),
       ('П1', 'Д1', 'ПР2', 700),
       ('П2', 'Д3', 'ПР1', 400),
       ('П2', 'Д2', 'ПР2', 200),
       ('П2', 'Д3', 'ПР3', 200),
       ('П2', 'Д3', 'ПР4', 500),
       ('П2', 'Д3', 'ПР5', 600),
       ('П2', 'Д3', 'ПР6', 400),
       ('П2', 'Д3', 'ПР7', 800),
       ('П2', 'Д5', 'ПР2', 100),
       ('П3', 'Д3', 'ПР1', 200),
       ('П3', 'Д4', 'ПР2', 500),
       ('П4', 'Д6', 'ПР3', 300),
       ('П4', 'Д6', 'ПР7', 300),
       ('П5', 'Д2', 'ПР2', 200),
       ('П5', 'Д2', 'ПР4', 100),
       ('П5', 'Д5', 'ПР5', 500),
       ('П5', 'Д5', 'ПР7', 100),
       ('П5', 'Д6', 'ПР2', 200),
       ('П5', 'Д1', 'ПР2', 100),
       ('П5', 'Д3', 'ПР4', 200),
       ('П5', 'Д4', 'ПР4', 800),
       ('П5', 'Д5', 'ПР4', 400),
       ('П5', 'Д6', 'ПР4', 500);



-- Task 6
SELECT
    ps.П AS "Номер поставщика",
    dp.Д AS "Номер детали",
    pj.ПР AS "Номер проекта"
FROM
    "Поставщики S" ps
    JOIN "Детали P" dp ON ps.Город = dp.Город
    JOIN "Проекты J" pj ON dp.Город = pj.Город;



-- Task 10
SELECT DP.Д AS "Номер детали"
FROM "Поставщики S" PS
INNER JOIN "Количество деталей, поставляемых одним поставщиком для одного проекта" KDP
    ON PS.П = KDP.П
INNER JOIN "Детали P" DP
    ON KDP.Д = DP.Д
INNER JOIN "Проекты J" PJ
    ON KDP.ПР = PJ.ПР
WHERE PS.Город = 'Лондон' AND PJ.Город = 'Лондон';



-- Task 35
SELECT S.П, P.Д
FROM "Поставщики S" AS S
CROSS JOIN "Детали P" AS P
WHERE NOT EXISTS (
    SELECT 1
    FROM "Количество деталей, поставляемых одним поставщиком для одного проекта" AS KP
    WHERE KP.П = S.П AND KP.Д = P.Д
)
ORDER BY S.П, P.Д;