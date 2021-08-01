import datetime
import aiohttp
from datetime import datetime as dt

class YoutubeVideoChecker:
    def __init__(self, google_api_key:str, channel_id:str):
        self.last_check = 0
        self.channel_id = channel_id
        self.playlist_id = f"UU{self.channel_id[-2:]}"
        self.google_api_key = google_api_key

    @staticmethod
    async def _get_req(url):
        async with aiohttp.request("GET", url) as r:
            return await r.json()

    async def get_channel_uploads(self):
        j = await self._get_req(f"https://www.googleapis.com/youtube/v3/channels?part=snippet,contentDetails,statistics&id={self.channel_id}&key={self.google_api_key}")
        return j.get("items")[0].get("contentDetails").get("uploads")

    async def get_recent_videos(self):
        j = await self._get_req(f"https://www.googleapis.com/youtube/v3/playlistItems?key={self.google_api_key}&playlistId={self.playlist_id}&part=snippet,id&order=date&maxResults=5")
        videos = list()
        for i in j.get("items"):
            vid = {
                "title": i.get("snippet").get("title"),
                "videoId": i.get("snippet").get("resourceId").get("videoId"),
                "postedAt": int(dt.strptime(i.get("snippet").get("publishedAt"), "%Y-%m-%dT%H:%M:%SZ").timestamp())
            }
            videos.append(vid)
        return videos

    async def on_video_upload(self, video):
        pass

    async def update(self):
        vids = await self.get_recent_videos()
        for v in vids:
            if v.get("postedAt") > self.last_check:
                await self.on_video_upload(v)
        self.last_check = dt.now(tz=datetime.timezone.utc)
