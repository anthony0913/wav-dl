import youtube_dl
import os

class YoutubeDownloader:
    def get_playlist_videos(self, playlist_url):
        ydl_opts = {'ignoreerrors': True, 'quiet': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            playlist_dict = ydl.extract_info(playlist_url, download=False)
            video_urls = []
            for video in playlist_dict['entries']:
                video_urls.append(video['url'])
        return video_urls

    def download_video(self, video_url):
        ydl_opts = {'outtmpl': 'temp_video.%(ext)s', 'ignoreerrors': True, 'quiet': True}
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except youtube_dl.DownloadError:
            os.remove('temp_video.mp4')
            return False

        os.system('ffmpeg -i temp_video.mp4 -acodec pcm_s16le -ar 44100 -ac 2 ~/Music/output{}.wav'.format(self.counter))
        os.remove('temp_video.mp4')
        self.counter += 1
        return True

    def download_playlist(self, playlist_url):
        video_urls = self.get_playlist_videos(playlist_url)
        self.counter = 1
        for url in video_urls:
            if self.download_video(url):
                print('Downloaded video {} of {}'.format(self.counter-1, len(video_urls)))
            else:
                print('Error downloading video at URL {}'.format(url))
        print('Finished downloading playlist.')

def main():
    downloader = YoutubeDownloader()
    playlist_url = input('Enter YouTube playlist URL: ')
    downloader.download_playlist(playlist_url)
    input('Download complete. Press Enter to exit.')

if __name__ == '__main__':
    main()