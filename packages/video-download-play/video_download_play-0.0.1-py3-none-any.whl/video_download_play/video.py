from pytube import YouTube
import vlc
import time

def video_download(video_url):
    def video(func):
        def download_play(vname):
            yt = YouTube(video_url)
            yt.streams.filter(res="720p", progressive="True", type="video").first().download('.', vname)
            func(vname)
        return download_play
    return video

video_url = input("enter the youtube video url: ")

@video_download(video_url)
def video_play(video_name):
    media_player = vlc.MediaPlayer(video_name)
    media_player.play()
    time.sleep(240)

#video_play = (video_download(video_url))(video_play)
#video_play("video.mp4")