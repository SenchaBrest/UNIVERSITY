#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //Загрузка картинки из файла
    QImage img("c:\\tmp\\lab1\\debug\\1.jpg");

    //Передача картинки в рисовальщик
    QPainter painter(&img);

    //Задаем непрерывную линию
    painter.setPen(Qt::SolidLine);
    //Рисуем ее
    painter.drawLine(10, 10, 20, 20);

    //Задаем красный цвет
    painter.setPen(QColor(255,0,0));
    //Рисуем точку
    painter.drawPoint(30, 30);

    painter.end();

    //Передаем виджету картинку для отрисовки
    QPixmap pict(QPixmap::fromImage(img));
    ui->image->setPixmap(pict);
}

MainWindow::~MainWindow()
{
    delete ui;
}
