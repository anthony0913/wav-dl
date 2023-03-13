import yt_dlp
import os

class YoutubeDownloader:
    def get_playlist_videos(self, playlist_url):
        ydl_opts = {'ignoreerrors': True, 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_dict = ydl.extract_info(playlist_url, download=False)
            video_urls = []
            for video in playlist_dict['entries']:
                if 'id' in video.keys() and 'title' in video.keys():
                    video_info = {
                        'title': video['title'],
                        'id': video['id']
                    }
                    video_urls.append(video_info)
        return video_urls

    def download_video(self, video_id, title, output_dir):
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        ydl_opts = {'outtmpl': 'temp_video.webm', 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'ignoreerrors': True, 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except yt_dlp.utils.DownloadError:
            print(f'Error downloading video with ID {video_id}')
            os.remove('temp_video.webm.mp4')
            return False

        title = title.replace('/', '_')
        output_path = os.path.normpath(os.path.join(output_dir, f'{title}.wav'))
        os.makedirs(output_dir, exist_ok=True)
        os.system(f'ffmpeg -loglevel panic -y -i temp_video.webm.mp4 -acodec pcm_s16le -ar 44100 -ac 2 "{output_path}"')

        os.remove('temp_video.webm.mp4')
        return True

    def download_playlist(self, playlist_url, output_dir):
        video_urls = self.get_playlist_videos(playlist_url)
        self.counter = 1
        for video_info in video_urls:
            if self.download_video(video_info['id'], video_info['title'], output_dir):
                print('Downloaded video {} of {}'.format(self.counter, len(video_urls)))
                self.counter += 1
            else:
                print('Error downloading video with ID {}'.format(video_info['id']))
        print('Finished downloading playlist.')

def main():
    downloader = YoutubeDownloader()
    playlist_url = input('Enter YouTube playlist URL: ')
    output_dir = input('Enter output directory path: ')
    output_dir = os.path.normpath(os.path.expanduser(output_dir))
    downloader.download_playlist(playlist_url, output_dir)

main()
