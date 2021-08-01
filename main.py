import asyncio
from youtube import YoutubeVideoChecker


class MyYTChecker(YoutubeVideoChecker):
    async def on_video_upload(self, video):
        print(f'New Video Uploaded! {video}')

checker = MyYTChecker(google_api_key="AIzaSyC4mortgXXXXXXXXXXXXEmlwkCEX7kbi2ckI", channel_id="UCaj4XXXXXXXXXXXX81ow")
asyncio.run(checker.update())
