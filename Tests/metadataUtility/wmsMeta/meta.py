import mutagen, re

tagsList = {
    "audio/mp3" : {
        "title" : "TIT2",
        "artist" : "TPE1",
        "album": "TALB",
        "genre": "TCON",
        "track": "TRCK",
        "release" : "TDRC"
    },
    "audio/mp4" : {
        "title" : "\xa9nam",
        "artist" : "\xa9ART",
        "album": "\xa9alb",
        "genre": "\xa9gen",
        "track": "trkn",
        "release" : "\xa9day"
    },
    "audio/vorbis" : {
        "title" : "title",
        "artist" : "artist",
        "album": None,
        "genre": None,
        "track": None,
        "release" : "date"
    }
}

# Add duplicate mime types

# MP3 - ID3 Tags
tagsList["audio/x-mp3"] = tagsList["audio/mp3"]
tagsList["audio/mpeg"] = tagsList["audio/mp3"]
tagsList["audio/mpg"] = tagsList["audio/mp3"]

# MP4
tagsList["audio/x-m4a"] = tagsList["audio/mp4"]
tagsList["audio/mpeg4"] = tagsList["audio/mp4"]

# OGG
tagsList["audio/x-vorbis"] = tagsList["audio/vorbis"]
tagsList["application/ogg"] = tagsList["audio/vorbis"]
tagsList["application/x-ogg"] = tagsList["audio/vorbis"]

# print(sorted(tagsList))

def meta(filename, option):
    audioFile = mutagen.File(filename)
    #print(audioFile.tags)

    if audioFile == None:
        return None

    audioFileMime = audioFile.mime[0]
    if audioFileMime in tagsList:
        formatSpecificName = tagsList[audioFileMime][option]
        if formatSpecificName == None:
            return None
        else:
            try:
                metadata = audioFile.tags.get(formatSpecificName)
                if isinstance(metadata, (list, tuple,)):
                    metadata = metadata[0]
                if (option == "release"):
                    metadata = re.findall("\d{4}", str(metadata))[0]

                return metadata
            except Exception as e:
                print(e)
                return None
