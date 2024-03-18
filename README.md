# Виртуальная стажировка

В ходе работы над проектом был разработан REST API для создания базы горных перевалов. С помощью приложения люди будут вносить данные о преодаленных перевалах в приложение и отправлять их в ФСТР, как только появится доступ в Интернет.

Для реализации проекта был создан проект tourist (команда в терминал: django-admin startproject tourist).

Далее создано приложение height (команда в терминал: python manage.py startapp height).

### Для создания таблиц созданы модели:

1. class AddUser. Класс для внесения данных о пользователе (ФИО, № телефона, адрес электронной почты)

class AddUsers(models.Model):

surname = models.CharField(max_length=255)

name = models.CharField(max_length=255)

patronymic = models.CharField(max_length=255)

email = models.EmailField(max_length=255)

phone = models.CharField(max_length=255)

def \__str_\_(self):

return f'Фамилия: {self.surname}, Имя: {self.name}, Эл.адрес: {self. email}'

2. class Coords. Класс для внесения координат вершины.

class Coords(models.Model):

latitude = models.FloatField(max_length=50, verbose_name: ‘Широта’)

longitude = models.FloatField(max_length=50, verbose_name: ‘Долгота’)

height = models.IntegerField(verbose_name: ‘Высота’)

3. class Level. Класс отражающий уровень сложности преодоления вершины.

class Level(models.Model):

winter = models.CharField(max_length=2, choices=LEVEL, verbose_name: ‘Зима’, null = True, blank=True)

summer = models.CharField(max_length=2, choices=LEVEL, verbose_name: ‘Лето’, null = True, blank=True)

autumn = models.CharField(max_length=2, choices=LEVEL, verbose_name: ‘Осень’, null = True, blank=True)

spring = models.CharField(max_length=2, choices=LEVEL, verbose_name: ‘Весна’, null = True, blank=True)

def \__str_\_(self):

return f'зима: {self.winter}, лето: {self.summer}, осень: {self.autumn}, весна: {self.spring}

4. class Mount. Класс самой вершины.

class Mount(models.Model):

beautyTitle = models.CharField(max_length=255, verbose_name: ‘Общее название’, defauil=None)

title = models.CharField(max_length=255, verbose_name: ‘Название горы’, null=True, blank=True)

other_titles = models.CharField(max_length=255, verbose_name: ‘Альтернативное название горы')

connect = models.TextField(null=True, blank=True)

add_time = models.DateTimeField(auto_now_add=True)

coords = models.OneToOneField(Coords, on_delete=models.CASCADE)

level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True, blank=True)

status = models.CharField(max_length=10, choices=STATUS, default=new)

user = models.ForeignKey(AddUsers, on_delete=models.CASCADE, default=Nobe)

def \__str_\_(self):

return f'{self.pk}, {self.beautyTitle}

5. class Photo. Класс для добавления фотографий вершины.

class Photo(models.Model):

mount = models.ForeignKey(Mount, on_delete=models.CASCADE)

data = models.URLFiled(verbose_name: ‘Изображение’, null=True, blank=True)

title = models.CharField(max_length=255, verbose_name: ‘Название’)

def \__str_\_(self):

return f'{self.pk}, {self.title}

**Для реализации проекта были импортированы библиотеки:**

1. pip install django
2. pip install djangorestframework
3. pip install django-filter
4. pip install drf-eritable-nested

С помощью метода POST submitData турист вносит нужную информацию с помощью мобильного приложения и отправляет на сервер для обработки.

### Реализованные сериалайзеры:

1. AddUserSerializer
2. Coords Serializer
3. LevelSerializer
4. PhotoSerializer
5. MountSerializer. В данном сериалайзере реализована функция def validate для отсутствия возможности изменения данных о пользователе при редактировании данных о вершине.

### На втором этапе в REST API добавлено три метода:

1. GET /submitData/&lt;id&gt; — для получения одной записи (перевал) по её id.
2. PATCH /submitData/&lt;id&gt; — для редактировать существующей записи, если она в статусе new. Редактировать можно все поля, кроме тех, что содержат в себе ФИО, адрес почты и номер телефона. Метод принимает тот же самый json, который принимал уже реализованный тобой метод submitData.