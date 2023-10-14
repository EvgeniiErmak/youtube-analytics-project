import isodate
import datetime
from src.channel import BaseService

class PlayList(BaseService):
    def __init__(self, playlist_id):
        super().__init__()
        self.playlist_id = playlist_id
        self.title, self.url = self.get_playlist_info()


    def get_playlist_info(self):
        try:
            response = self.get_service().playlists().list(part='snippet', id=self.playlist_id).execute()
            items = response.get('items', [])

            if not items:
                raise ValueError("Плейлист не найден или пустой.")

            title = items[0]['snippet']['title']
            url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
            return title, url
        except Exception as e:
            raise ValueError(f"Ошибка при получении информации о плейлисте: {str(e)}")

    @property


    def total_duration(self):
        try:
            response = self.get_service().playlistItems().list(part='contentDetails', playlistId=self.playlist_id).execute()
            items = response.get('items', [])

            total_seconds = 0

            for item in items:
                video_id = item['contentDetails']['videoId']
                video_response = self.get_service().videos().list(part='contentDetails', id=video_id).execute()
                content_details = video_response['items'][0]['contentDetails']
                duration = content_details['duration']

                # Преобразование продолжительности видео в объект datetime.timedelta
                video_duration = self.parse_duration(duration)

                total_seconds += video_duration.total_seconds()

            return datetime.timedelta(seconds=total_seconds)
        except Exception as e:
            raise ValueError(f"Ошибка при вычислении общей длительности: {str(e)}")


    def parse_duration(self, duration):
        # Функция для преобразования строки продолжительности в объект datetime.timedelta
        time_elements = duration.split('T')[1]
        hours = 0
        minutes = 0
        seconds = 0

        if 'H' in time_elements:
            hours = int(time_elements.split('H')[0])
            time_elements = time_elements.split('H')[1]

        if 'M' in time_elements:
            minutes = int(time_elements.split('M')[0])
            time_elements = time_elements.split('M')[1]

        if 'S' in time_elements:
            seconds = int(time_elements.split('S')[0])

        return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)


    def show_best_video(self):
        try:
            response = self.get_service().playlistItems().list(part='snippet', playlistId=self.playlist_id).execute()
            items = response.get('items', [])

            best_video = None
            max_likes = 0

            for item in items:
                video_id = item['snippet']['resourceId']['videoId']
                video_response = self.get_service().videos().list(part='statistics', id=video_id).execute()
                statistics = video_response['items'][0]['statistics']

                likes = int(statistics.get('likeCount', 0))

                if likes > max_likes:
                    max_likes = likes
                    best_video = f"https://youtu.be/{video_id}"

            return best_video
        except Exception as e:
            raise ValueError(f"Ошибка при поиске самого популярного видео: {str(e)}")