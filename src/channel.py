import os
import json
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        data = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        for d in data["items"]:
            self.title = d['snippet']['title']
            self.description = d['snippet']['description']
            self.url = d['snippet']['thumbnails']['default']['url']
            self.subscriber_count = d['statistics']['subscriberCount']
            self.video_count = d['statistics']['videoCount']
            self.view_count = d['statistics']['viewCount']

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
            json.dump(dictionary, outfile, indent=4)


