# book-management-system

# Описание
Необходимо разработать консольное приложение для управления библиотекой книг. 
Приложение должно позволять добавлять, удалять, искать и отображать книги. 
Каждая книга должна содержать следующие поля:
- id (уникальный идентификатор, генерируется автоматически)
- title (название книги)
- author (автор книги)
- year (год издания)
- status (статус книги: “в наличии”, “выдана”)

# Требования
1. Добавление книги: Пользователь вводит title, author и year, после чего книга добавляется в библиотеку с уникальным id и статусом “в наличии”.
2. Удаление книги: Пользователь вводит id книги, которую нужно удалить.
3. Поиск книги: Пользователь может искать книги по title, author или year.
4. Отображение всех книг: Приложение выводит список всех книг с их id, title, author, year и status.
5. Изменение статуса книги: Пользователь вводит id книги и новый статус (“в наличии” или “выдана”).

# Дополнительные требования
- Реализовать хранение данных в текстовом или json формате.
- Обеспечить корректную обработку ошибок (например, попытка удалить несуществующую книгу).
- Написать функции для каждой операции (добавление, удаление, поиск, отображение, изменение статуса).
- Не использовать сторонние библиотеки.


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