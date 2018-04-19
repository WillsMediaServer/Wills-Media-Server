import subprocess
import json

from os.path import join, dirname, abspath, normpath
LIB_DIR = normpath(join(dirname(abspath(__file__)), ".."))

class Wrapper:
    def __init__(self):
        pass

    def metadata(self, filename, tags):
        metadata = subprocess.Popen([join(LIB_DIR, "ffmpeg", "bin", "ffprobe"), "-v", "quiet", "-print_format", "json" ,"-show_format", filename], stdout=subprocess.PIPE)
        stdout, stderr = metadata.communicate()
        jsonMetadata = json.loads(stdout)
        # print(json.dumps(jsonMetadata))
        neededMetadata = jsonMetadata["format"]
        returnData = {}
        for tag in tags:
            try:
                returnData[tag] = neededMetadata["tags"][tag]
            except:
                returnData[tag] = None
        print(json.dumps(returnData))
