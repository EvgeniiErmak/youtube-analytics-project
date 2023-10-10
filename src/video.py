from src.channel import BaseService

class Video(BaseService):
    def __init__(self, video_id):
        self.video_id = video_id
        self._init_from_api()

    def _init_from_api(self):
        youtube = self.get_service()

        video = youtube.videos().list(id=self.video_id,
                                      part='snippet,statistics').execute()

        snippet = video['items'][0]['snippet']
        statistics = video['items'][0]['statistics']

        self.title = snippet['title']
        self.url = f'https://youtu.be/{self.video_id}'
        self.view_count = statistics['viewCount']
        self.like_count = statistics['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id