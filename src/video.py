from src.channel import BaseService
from googleapiclient.errors import HttpError


class Video(BaseService):
    def __init__(self, video_id):
        """
        Инициализируйте экземпляр Video с предоставленным video_id.

        Args:
            video_id (str): Идентификатор видео.

        Атрибуты:
            video_id (str): Идентификатор видео.
            title (str): Название видео, или None, если видео не найдено.
            url (str): URL видео, или None, если видео не найдено.
            view_count (int): Количество просмотров видео, или None, если видео не найдено.
            like_count (int): Количество лайков видео, или None, если видео не найдено.
        """
        self.video_id = video_id
        self._init_from_api()

    def _init_from_api(self):
        youtube = self.get_service()

        try:
            video = youtube.videos().list(id=self.video_id,
                                          part='snippet,statistics').execute()

            if 'items' in video and video['items']:
                snippet = video['items'][0]['snippet']
                statistics = video['items'][0]['statistics']

                self.title = snippet['title']
                self.url = f'https://youtu.be/{self.video_id}'
                self.view_count = statistics['viewCount']
                self.like_count = statistics['likeCount']
            else:
                # Если 'items' отсутствует в ответе или список пуст, установите свойства в None.
                self.title = None
                self.url = None
                self.view_count = None
                self.like_count = None

        except HttpError:
            # Если возникла ошибка HttpError, это означает, что видео с предоставленным ID не существует.
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
