# Backup-vk-photo-profile
## Задание к итоговой работе:
Возможна такая ситуация, что мы хотим показать друзьям фотографии из социальных сетей, но соц. сети могут быть недоступны по каким-либо причинам. Давайте защитимся от такого.
Нужно написать программу для резервного копирования фотографий с профиля (аватарок) пользователя VK в облачное хранилище Яндекс.Диск.
Для названий фотографий использовать количество лайков, если количество лайков одинаково, то добавить дату загрузки.
Информацию по сохраненным фотографиям сохранить в json-файл.

## Задача:
### Нужно написать программу, которая будет:

1.  Получать фотографии с профиля. Для этого нужно использовать метод photos.get.
2.  Сохранять фотографии максимального размера (ширина/высота в пикселях) на Я.Диске.
3.  Для имени фотографий использовать количество лайков.
4.  Сохранять информацию по фотографиям в json-файл с результатами.
5.  Обратите внимание: токен для ВК можно получить выполнив инструкцию.

## Входные данные:
### Пользователь вводит:

1.  id пользователя VK;
2.  токен с Полигона Яндекс.Диска. Важно: Токен публиковать в github не нужно!
## Выходные данные:
1.  json-файл с информацией по файлу:
    ```
    [{
    "file_name": "34.jpg",
    "size": "z"
    }]
    ```
2.  Измененный Я.Диск, куда добавились фотографии.
## Обязательные требования к программе:
1.  Использовать REST API Я.Диска и ключ, полученный с полигона.
2.  Для загруженных фотографий нужно создать свою папку.
3.  Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске
4.  Сделать прогресс-бар или логирование для отслеживания процесса программы.
5.  Код программы должен удовлетворять PEP8.
6.  У программы должен быть свой отдельный репозиторий.
7.  Все зависимости должны быть указаны в файле requiremеnts.txt.​
