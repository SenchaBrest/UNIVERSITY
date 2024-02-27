from django.db import models

class Зачетки(models.Model):
    номер_зачетки = models.AutoField(primary_key=True)
    ФИО = models.CharField(max_length=255)
    группа = models.CharField(max_length=255)

    def __str__(self):
        return str(self.номер_зачетки)

class Группа(models.Model):
    группа = models.CharField(primary_key=True, max_length=255)
    факультет = models.CharField(max_length=255)
    специальность = models.CharField(max_length=255)

    def __str__(self):
        return self.группа

class Студенты(models.Model):
    ФИО = models.CharField(primary_key=True, max_length=255)
    год_рождения = models.DateField()
    адрес = models.TextField()
    телефон = models.CharField(max_length=20)

    def __str__(self):
        return self.ФИО
