import os

MEDIA_DIRS = [r"E:\Music", r"C:\Users\wsnga\Music"]

supportedExt = [".mp3", ".wav", ".ogg"]
songs = []


for mediaDir in MEDIA_DIRS:
    for dir, subdir, files in os.walk(mediaDir):
        for file in files:
            for ext in supportedExt:
                if file.endswith(ext):
                    songs.append(os.path.join(dir,file))

# print(songs)
for song in songs:
    # print(song)
    print(os.path.basename(song).rsplit(".",1)[0])
