import json
import os
from googleapiclient.discovery import build

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.getenv('YT_API_KEY')
        if not self.api_key:
            raise ValueError("API ключ не найден в переменных окружения.")

    def get_channel_info(self) -> dict:
        """Получает информацию о канале с помощью YouTube API и возвращает ее в виде словаря."""
        youtube = build('youtube', 'v3', developerKey=self.api_key)

        response = youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        ).execute()

        if 'items' in response:
            channel_data = response['items'][0]

            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            channel_info = {
                "Название канала": snippet['title'],
                "Описание": snippet['description'],
                "Подписчики": statistics['subscriberCount'],
                "Просмотры": statistics['viewCount'],
                "Количество видео": statistics['videoCount']
            }
            return channel_info
        else:
            return None

    def print_info(self) -> None:
        """Выводит информацию о канале в консоль без лишних скобок и кавычек."""
        channel_info = self.get_channel_info()

        if channel_info:
            print("Информация о канале:")
            print(f"Название канала: {channel_info['Название канала']}")
            print(f"Описание: {channel_info['Описание']}")
            print(f"Подписчики: {channel_info['Подписчики']}")
            print(f"Просмотры: {channel_info['Просмотры']}")
            print(f"Количество видео: {channel_info['Количество видео']}")
        else:
            print("Канал не найден или произошла ошибка при получении данных.")


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
