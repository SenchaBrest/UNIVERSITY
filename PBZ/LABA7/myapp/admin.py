# В файле myapp/admin.py
from django.contrib import admin
from .models import Зачетки, Группа, Студенты

@admin.register(Зачетки)
class ЗачеткиAdmin(admin.ModelAdmin):
    search_fields = ['ФИО', 'группа']
    list_display = ['номер_зачетки', 'ФИО', 'группа']

@admin.register(Группа)
class ГруппаAdmin(admin.ModelAdmin):
    search_fields = ['группа', 'факультет', 'специальность']
    list_display = ['группа', 'факультет', 'специальность']

@admin.register(Студенты)
class СтудентыAdmin(admin.ModelAdmin):
    search_fields = ['ФИО', 'год_рождения', 'адрес', 'телефон']
    list_display = ['ФИО', 'год_рождения', 'адрес', 'телефон']
