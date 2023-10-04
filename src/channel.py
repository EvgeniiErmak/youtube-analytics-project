import requests

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = 'AIzaSyAqyYxiqs3S2UnchCBECOAFigXA_PJqAwY'  # Замените на свой ключ YouTube API

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        url = f'https://www.googleapis.com/youtube/v3/channels'
        params = {
            'part': 'snippet,statistics',
            'id': self.channel_id,
            'key': self.api_key,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if 'items' in data:
            channel_data = data['items'][0]

            snippet = channel_data['snippet']
            statistics = channel_data['statistics']

            print(f"Название канала: {snippet['title']}")
            print(f"Описание: {snippet['description']}")
            print(f"Подписчики: {statistics['subscriberCount']}")
            print(f"Просмотры: {statistics['viewCount']}")
            print(f"Количество видео: {statistics['videoCount']}")
        else:
            print("Канал не найден или произошла ошибка при получении данных.")
