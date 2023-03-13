import yt_dlp
import os
import time
import subprocess

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

    def download_video(self, video_id):
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

        print(f'Converting video with ID {video_id} to WAV format')
        time.sleep(2)
        os.system('ffmpeg -i temp_video.webm.mp4 -acodec pcm_s16le -ar 44100 -ac 2 ~/Music/output{}.wav'.format(self.counter))
        os.remove('temp_video.webm.mp4')
        return True

    def download_playlist(self, playlist_url):
        video_urls = self.get_playlist_videos(playlist_url)
        self.counter = 1
        for video_info in video_urls:
            if self.download_video(video_info['id']):
                print('Downloaded video {} of {}'.format(self.counter, len(video_urls)))
                self.counter += 1
            else:
                print('Error downloading video with ID {}'.format(video_info['id']))
        print('Finished downloading playlist.')
        print('Saved to ~/Music')

def main():
    downloader = YoutubeDownloader()
    playlist_url = input('Enter YouTube playlist URL: ')
    downloader.download_playlist(playlist_url)
    print("Download complete.")

main()

#if __name__ == '__main__':
#    main()
