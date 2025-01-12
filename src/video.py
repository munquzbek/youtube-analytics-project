from src.channel import Channel


class Video(Channel):
    def __init__(self, video_id):
        self.video_id = video_id
        try:
            video_response = super().get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video_id).execute()
            if not video_response['items']:
                self.title = None
                self.url = None
                self.view_count = None
                self.like_count = None
                raise VideoNotFound
            else:
                self.title = video_response['items'][0]['snippet']['title']
                self.url = video_response['items'][0]['snippet']['thumbnails']['default']['url']
                self.view_count = video_response['items'][0]['statistics']['viewCount']
                self.like_count = video_response['items'][0]['statistics']['likeCount']
        except VideoNotFound:
            raise VideoNotFound('Video id is wrong')

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
        video_response = super().get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                             id=video_id).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.url = video_response['items'][0]['snippet']['thumbnails']['default']['url']
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


class VideoNotFound(Exception):
    def __init__(self, *args):
        self.message = args
