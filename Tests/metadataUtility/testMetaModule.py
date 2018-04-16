from wmsMeta.meta import meta, tagsList
import mutagen

# MP3 Format Test

print("="*25)
print("MP3 Test".center(25, " "))

mp3Files = [r"E:\Music\A Head Full of Dreams\A Head Full of Dreams.mp3",
            r"E:\Music\Human\Skin.mp3",
            r"E:\Music\Now! That's What I Call Music- 30 Years Disc 3\Gangnam Style.mp3"]
for file in mp3Files:
    print("="*25)
    print("File: " + file)
    for option in tagsList["audio/mp3"]:
        print(option + ": " + str(meta(file, option)))

# M4A Format Test - MPEG-4

print("="*25)
print("M4A Test".center(25, " "))
m4aFiles = [r"C:\Users\wsnga\Downloads\testFile.m4a"]
for file in m4aFiles:
    print("="*25)
    print("File: " + file)
    for option in tagsList["audio/mp4"]:
        print(option + ": " + str(meta(file, option)))

# OGG Format Test

print("="*25)
print("OGG Test".center(25, " "))

oggFiles = [r"C:\Users\wsnga\Downloads\music.ogg"]
for file in oggFiles:
    print("="*25)
    print("File: " + file)
    for option in tagsList["audio/vorbis"]:
        print(option + ": " + str(meta(file, option)))
