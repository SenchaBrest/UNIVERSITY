#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //�������� �������� �� �����
    QImage img("c:\\tmp\\lab1\\debug\\1.jpg");

    //�������� �������� � �����������
    QPainter painter(&img);

    //������ ����������� �����
    painter.setPen(Qt::SolidLine);
    //������ ��
    painter.drawLine(10, 10, 20, 20);

    //������ ������� ����
    painter.setPen(QColor(255,0,0));
    //������ �����
    painter.drawPoint(30, 30);

    painter.end();

    //�������� ������� �������� ��� ���������
    QPixmap pict(QPixmap::fromImage(img));
    ui->image->setPixmap(pict);
}

MainWindow::~MainWindow()
{
    delete ui;
}
