import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        request_to_data = youtube.channels().list(
            part="snippet,statistics",
            id=self.channel_id
        )
        response = request_to_data.execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))
