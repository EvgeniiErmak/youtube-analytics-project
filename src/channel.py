import json
import os
from googleapiclient.discovery import build

class BaseService:
    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        if not api_key:
            raise ValueError("API ключ не найден в переменных окружения.")
        return build('youtube', 'v3', developerKey=api_key)

class Channel(BaseService):
    def __init__(self, channel_id: str) -> None:
        self.__channel_id = channel_id
        self._init_from_api()

    def _init_from_api(self) -> None:
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()

        if 'items' in channel:
            channel_data = channel['items'][0]['snippet']
            statistics = channel['items'][0]['statistics']

            self.title = channel_data['title']
            self.description = channel_data['description']
            self.url = f'https://www.youtube.com/channel/{channel["items"][0]["id"]}'
            self.subscriber_count = statistics['subscriberCount']
            self.video_count = statistics['videoCount']
            self.view_count = statistics['viewCount']
        else:
            raise ValueError(f"Канал с id {self.__channel_id} не найден или произошла ошибка при получении данных.")

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print("Информация о канале:")
        print(f"id канала: {self.__channel_id}")
        print(f"Название канала: {self.title}")
        print(f"Описание: {self.description}")
        print(f"Ссылка на канал: {self.url}")
        print(f"Количество подписчиков: {self.subscriber_count}")
        print(f"Количество видео: {self.video_count}")
        print(f"Общее количество просмотров: {self.view_count}")

    def to_json(self, filename: str) -> None:
        """Сохраняет данные экземпляра класса в файл."""
        dict_to_write = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(filename, 'w') as fp:
            json.dump(dict_to_write, fp)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriber_count) + int(other.subscriber_count)
        else:
            raise TypeError("Unsupported operand type for +: 'Channel' and {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriber_count) - int(other.subscriber_count)
        else:
            raise TypeError("Unsupported operand type for -: 'Channel' and {}".format(type(other)))

    def __lt__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriber_count) < int(other.subscriber_count)
        else:
            raise TypeError("Unsupported operand type for <: 'Channel' and {}".format(type(other)))

    def __ge__(self, other):
        if isinstance(other, Channel):
            return int(self.subscriber_count) >= int(other.subscriber_count)
        else:
            raise TypeError("Unsupported operand type for >=: 'Channel' and {}".format(type(other)))
