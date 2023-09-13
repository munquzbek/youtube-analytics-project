import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')


class Channel:
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        data = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = data['items'][0]['snippet']['title']
        self.description = data['items'][0]['snippet']['description']
        self.url = data['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_count = data['items'][0]['statistics']['subscriberCount']
        self.video_count = data['items'][0]['statistics']['videoCount']
        self.view_count = data['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __ne__(self, other):
        return int(self.subscriber_count) != int(other.subscriber_count)

    @classmethod
    def get_service(cls):
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self, where_to_save):
        dictionary = {
            'title': self.title,
            'channel id': self.channel_id,
            'description': self.description,
            'url': self.url,
            'subsciber count': self.subscriber_count,
            'video count': self.video_count,
            'view count': self.view_count
        }

        with open(where_to_save, "w") as outfile:
            json.dump(dictionary, outfile, indent=4, ensure_ascii=False)
