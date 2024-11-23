[![Tests](https://github.com/vitaliy-ukiru/book-library-system/actions/workflows/tests.yml/badge.svg)](https://github.com/vitaliy-ukiru/book-library-system/actions/workflows/tests.yml)

<!-- TOC -->
* [Функционал](#функционал)
* [Реализация](#реализация)
  * [Структура](#структура)
  * [Хранение](#хранение)
  * [Разбивка по страницам](#разбивка-по-страницам)
* [Конфигурация](#конфигурация)
* [Запуск](#запуск)
  * [Добавление книги](#добавление-книги)
  * [Удаление книги](#удаление-книги)
  * [Поиск книг](#поиск-книг)
  * [Вывод всех книг](#вывод-всех-книг)
  * [Обновление статуса](#обновление-статуса)
  * [Тестирование](#тестирование)
<!-- TOC -->

# Функционал
1. Добавление книги: Пользователь вводит title, author и year, после чего книга добавляется в библиотеку с уникальным id и статусом “в наличии”.
2. Удаление книги: Пользователь вводит id книги, которую нужно удалить.
3. Поиск книги: Пользователь может искать книги по title, author или year. Доступна разбивка по страницам.
4. Отображение всех книг: Приложение выводит список всех книг с их id, title, author, year и status. Доступна разбивка по страницам.
5. Изменение статуса книги: Пользователь вводит id книги и новый статус (“в наличии” или “выдана”).

# Реализация
Основной функционал приложения реализован без внешних зависимостей. 
Но для тестов используется pytest.


## Структура
Структура базируется на чистой архитектуре, но без сильного углубления.

- config - Определения конфига.
- application/book - Слой приложения, реализация функционала
- domain/book - Сущности доменной области и value objects.
- infrastructure/db - Реализация хранилища для книг
- presentation/cli - Реализация консольного приложения

## Хранение
Данные хранятся в JSON файле. Из-за специфики консольного приложения не реализовывал транзакции. 
Слишком избыточно для консольного приложения.

Для ускорения операций во время работы приложения используется формат, отличный от того, который 
хранится на диске.

Для исключения одинаковых книг (по названию, автору и году) вычисляется хэш для каждой книги.

В основном коде нет зависимости от реализации БД.

## Разбивка по страницам
Если установлено значение `page_size` в конфиге, то для 
команд поиска книг и вывода всех книг доступен вывод по страницам.
Переключение по страницам происходит через ввод в консоль.
Или же можно использовать параметр `--page` для старта с определённой старицы.


# Конфигурация
Пример конфига находиться в [configs](configs/config.ini).
* storage.path - Путь к файлу с данными
* page_size - Размер для страницы для пагинации (Необязательный параметр)

# Запуск
```
usage: python -m src [-h] [--config CONFIG] {add,delete,search,all,status} ...

Book library system

positional arguments:
  {add,delete,search,all,status}
    add                 Add book
    delete              Delete book
    search              Search books
    all                 Output all books
    status              Change book status

options:
  -h, --help            show this help message and exit
  --config CONFIG       Path to config file
```

Справка по команде доступна, как:
```bash
python3 -m src <command> --help
```

## Добавление книги
```bash
python3 -m src add "Title" "Author" Year
```

## Удаление книги
```bash
python3 -m src delete <book_id>
```

## Поиск книг
```
usage: python -m src search [--title TITLE] [--author AUTHOR] [--year YEAR] [--page PAGE]
options:
  --title TITLE    Book title
  --author AUTHOR  Author of the book
  --year YEAR      Year of publication
  --page PAGE      Number of page. Available only in set page_size in config
```

## Вывод всех книг
```
usage: python -m src all [-h] [--page PAGE]
options:
  --page PAGE  Number of page. Available only in set page_size in config
```


## Обновление статуса
```
usage: python -m src status (--return | --take) id

positional arguments:
  id          Book id

options:
  --return    Set available status
  --take      Set taken status
```

## Тестирование
```bash
pytest tests
```