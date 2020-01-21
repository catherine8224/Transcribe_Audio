import sys
import requests
import os 
import codecs

#youtube_ids = open("ids.txt", "r")
youtube_id = input("Please tell me the youtube id: "  )
lyrics_dir_path = "/Users/catherineng/Desktop/Python_Projects/huntercodefest/app/music/lyrics/"
#"data/lyrics/"
sounds_dir_path = "app/music/sounds/"
#"data/sound/"
#counter = 0

is_downloaded = True
#for line in youtube_ids.readlines():
    #yt_id = line.rstrip("\n")

sound_path = sounds_dir_path + 'SOUND' #str(counter).zfill(4)
lyrics_path = lyrics_dir_path + 'LYRICS.txt' #str(counter).zfill(4) + ".txt"
#counter += 1
#if youtube_id == "DONE":
#    is_downloaded = False
#    continue
#if is_downloaded:
#    continue
video_url = "https://www.youtube.com/watch?v=" + youtube_id
os.system('youtube-dl --extract-audio --audio-format mp3 --prefer-ffmpeg -o /Users/catherineng/Desktop/Python_Projects/huntercodefest/' + sound_path + ".m4a " + video_url)

Lyrics_URL = "http://video.google.com/timedtext?type=list&v=" + youtube_id #hSnB7zGW15M

lyrics_url = "http://video.google.com/timedtext?lang=en&v=" + youtube_id
lyrics = requests.get(lyrics_url)
lyrics_file = codecs.open(lyrics_path, mode='w+', encoding='utf-8')
lyrics_file.write(lyrics.text)