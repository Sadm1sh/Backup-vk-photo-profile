import requests
import time
import json
import sys
from user_info import vktoken, yatoken, id_vk
from tqdm import tqdm
VK_TOKEN: str = vktoken
YANDEX_TOKEN: str = yatoken
user_id: str = id_vk


def time_convert(time_unix: int):  # Функция возвращает дату и время из формата UNIX в UTC
    time_utc = time.gmtime(time_unix)
    str_date = time.strftime("%m/%d/%Y", time_utc)
    str_time = time.strftime("%H:%M:%S", time_utc)
    return str_date, str_time


def find_max_size_photos(info_photos):  # Функция возвращает url фотографии с максимальным размером и её размер
    max_size = 0
    desired_object = 0
    for index in range(len(info_photos)):
        area_photos = info_photos[index].get('height') * info_photos[index].get('width')
        if area_photos > max_size:
            max_size = area_photos
            desired_object = index
    return info_photos[desired_object].get('url'), info_photos[desired_object].get('type')


class VKRequest:
    def __init__(self, token, count="5", versions='5.131', album_id='profile'):  # метод передаваемых переменных
        self.token = token
        self.user_id = user_id
        self.count = count
        self.vers = versions
        self.a_id = album_id

    def info_photos(self):  # Метод возвращает информацию по фотографиям
        uri_method: str = "https://api.vk.com/method/"
        method_photos_get = uri_method + "photos.get"
        params = {
            "access_token": self.token,
            "extended": "1",
            "owner_id": self.user_id,
            "album_id": self.a_id,
            "count": self.count,
            "v": self.vers
        }
        get_info_photos = requests.get(method_photos_get, params=params)
        if get_info_photos.status_code == 200:
            info_json = get_info_photos.json()
            return info_json.get('response')
        sys.exit(f"Ошибка ответа, код: {get_info_photos.status_code}")

    def json_info_photos(self):  # Метод возвращает словарь по информации о загруженных фотографиях
        photos_items = self.info_photos().get('items')
        json_info_list = []
        json_file = {
            "count": self.count,
            "info": json_info_list
                    }
        for photo_info in photos_items:
            count_likes = photo_info['likes']['count']
            max_size_url = find_max_size_photos(photo_info['sizes'])
            date_of_download = time_convert(photo_info['date'])
            json_info_list.append({
                "name": f"{count_likes}.jpg",
                "id": photo_info['id'],
                'date': date_of_download[0],
                'time': date_of_download[1],
                "likes": count_likes,
                'url': max_size_url[0],
                'size': max_size_url[1]
                                   })
        return json_file


class YAuploader:
    def __init__(self, token, folder_path, count=5):  # Метод передаваемых переменных
        self.token = token
        self.url = "https://cloud-api.yandex.net/v1/disk/resources"
        self.count = count
        self.folder_path = folder_path
        self.headers = {
            "Authorization": f"OAuth {self.token}",
            "Content-Type": "application/json"
        }

    def create_folder(self):  # метод создаёт папку на диске по указанному пути
        params = {
            "path": self.folder_path
        }
        create_folder = requests.put(self.url, headers=self.headers, params=params)
        if create_folder.status_code == 409:
            return f'По указанному пути /{self.folder_path} уже существует папка ' \
                   f'с таким именем файлы будут загруженны туда'
        elif create_folder.status_code != 201 != 409:
            sys.exit(f"Ошибка ответа, код: {create_folder.status_code}")
        return f'По указанному пути /{self.folder_path} успешно создана папка'

    def delete_folder(self):
        params = {
            "path": self.folder_path
        }
        delete_folder = requests.delete(self.url, headers=self.headers, params=params)
        if delete_folder.status_code < 300:
            return
        sys.exit(f'Ошибка ответа, код: {delete_folder.status_code}')

    def upload_files(self, info_list):  # Метода загружает файлы по url
        print(self.create_folder())
        url_upload = self.url + "/upload"
        info = info_list['info']
        for index in tqdm(range(len(info)), desc="Прогресс загрузки файлов", unit=" File"):
            name = info[index]['name']
            url_photo = info[index]['url']
            params = {
                "path": f"{self.folder_path}/{name}",
                "url": url_photo
            }
            upload_photo = requests.post(url_upload, headers=self.headers, params=params)
            if upload_photo.status_code != 202:
                self.delete_folder()
                sys.exit(f"Ошибка ответа, код: {upload_photo.status_code}\n"
                         f"Папка перемещена в корзину")
        return "Все файлы успешно загрузились в папку"


if __name__ == '__main__':
    json_name = input('Введите название папки на диске:')  # Вводим название папки
    VKreq = VKRequest(VK_TOKEN)  # передаём вк токен классу
    with open(json_name + ".json", "w") as file:  # Создаём JSON файл с именем папки
        json.dump(VKreq.json_info_photos(), file, indent=4)  # Запаковываем JSON информацию в JSON файл
    yandex = YAuploader(yatoken, json_name)  # Передаём классу токен
    print(yandex.upload_files(VKreq.json_info_photos()))
