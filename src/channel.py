import json
import os
from googleapiclient.discovery import build


class Channel:
    def __init__(self, channel_id: str):
        self.channel_id = channel_id
        self.api_key = os.getenv('YT_API_KEY')
        if not self.api_key:
            raise ValueError("API ключ не найден в переменных окружения.")

        # Инициализируем атрибуты данными из YouTube API
        self.channel_info = self.get_channel_info()

    def get_channel_info(self):
        youtube = self.get_service()

        response = youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()

        if 'items' in response:
            channel_data = response['items'][0]

            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            channel_info = {
                "id канала": self.channel_id,
                "Название канала": snippet['title'],
                "Описание канала": snippet['description'],
                "Ссылка на канал": f"https://www.youtube.com/channel/{self.channel_id}",
                "Количество подписчиков": statistics['subscriberCount'],
                "Количество видео": statistics['videoCount'],
                "Общее количество просмотров": statistics['viewCount']
            }
            return channel_info
        else:
            return None

    def print_info(self):
        if self.channel_info:
            print("Информация о канале:")
            print(f"id канала: {self.channel_info['id канала']}")
            print(f"Название канала: {self.channel_info['Название канала']}")
            print(f"Описание: {self.channel_info['Описание канала']}")
            print(f"Ссылка на канал: {self.channel_info['Ссылка на канал']}")
            print(f"Количество подписчиков: {self.channel_info['Количество подписчиков']}")
            print(f"Количество видео: {self.channel_info['Количество видео']}")
            print(f"Общее количество просмотров: {self.channel_info['Общее количество просмотров']}")
        else:
            print("Канал не найден или произошла ошибка при получении данных.")

    def to_json(self, filename: str):
        if self.channel_info:
            with open(filename, 'w', encoding='utf-8') as file:
                json.dump(self.channel_info, file, ensure_ascii=False, indent=2)
                print(f"Данные канала сохранены в файл {filename}")
        else:
            print("Невозможно сохранить данные, так как канал не найден или произошла ошибка при получении данных.")

    def __str__(self):
        return f"{self.channel_info['Название канала']} ({self.channel_info['Ссылка на канал']})"

    def __add__(self, other):
        if isinstance(other, Channel):
            return int(self.channel_info['Количество подписчиков']) + int(other.channel_info['Количество подписчиков'])
        else:
            raise TypeError("Unsupported operand type for +: 'Channel' and {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Channel):
            return int(self.channel_info['Количество подписчиков']) - int(other.channel_info['Количество подписчиков'])
        else:
            raise TypeError("Unsupported operand type for -: 'Channel' and {}".format(type(other)))

    def __lt__(self, other):
        if isinstance(other, Channel):
            return int(self.channel_info['Количество подписчиков']) < int(other.channel_info['Количество подписчиков'])
        else:
            raise TypeError("Unsupported operand type for <: 'Channel' and {}".format(type(other)))

    def __ge__(self, other):
        if isinstance(other, Channel):
            return int(self.channel_info['Количество подписчиков']) >= int(other.channel_info['Количество подписчиков'])
        else:
            raise TypeError("Unsupported operand type for >=: 'Channel' and {}".format(type(other)))

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        if not api_key:
            raise ValueError("API ключ не найден в переменных окружения.")
        return build('youtube', 'v3', developerKey=api_key)
