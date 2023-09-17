import json
from datetime import timedelta
import isodate

from src.channel import Channel


class PlayList(Channel):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_data = super().get_service().playlistItems().list(playlistId=playlist_id,
                                                                        part="contentDetails, snippet",
                                                                        maxResults=50,
                                                                        ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_data['items']]
        self.channel_id = self.playlist_data['items'][0]['snippet']['channelId']
        self.playlists = super().get_service().playlists().list(channelId=self.channel_id,
                                                                part='contentDetails,snippet',
                                                                maxResults=50,
                                                                ).execute()
        self.title = self.get_title_from_playlist()
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'

    def get_title_from_playlist(self):
        for playlist in self.playlists['items']:
            if playlist['id'] == self.playlist_id:
                return playlist['snippet']['title']

    @property
    def total_duration(self):
        duration_list = []
        for video_id in self.video_ids:
            video_data = super().get_service().videos().list(part='contentDetails',
                                                             id=video_id).execute()
            duration = isodate.parse_duration(video_data['items'][0]['contentDetails']['duration'])
            duration_list.append(duration)
        return timedelta(seconds=sum(td.total_seconds() for td in duration_list))

    def show_best_video(self):
        most_liked = 0
        video_url = str
        for video_id in self.video_ids:
            video_data = super().get_service().videos().list(part='statistics',
                                                             id=video_id).execute()
            if int(video_data['items'][0]['statistics']['likeCount']) > most_liked:
                most_liked = int(video_data['items'][0]['statistics']['likeCount'])
                video_url = video_data['items'][0]['id']
        return f'https://youtu.be/{video_url}'
