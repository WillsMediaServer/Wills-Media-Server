import subprocess, json, os, logging

from os.path import join, dirname, abspath, normpath
LIB_DIR = normpath(join(dirname(abspath(__file__)), ".."))

class Wrapper:
    def __init__(self):
        try:
            logging.info("Attempting to use ffmpeg from path")
            data = subprocess.Popen(["ffmpeg", "-version"], stdout=subprocess.PIPE)
            stdout, stderr = data.communicate()
            logging.info(stdout.decode("utf-8"))
            self.ffmpegdir = ""
        except Exception:
            try:
                logging.info("Attempting to use ffmpeg from libs directory")
                data = subprocess.Popen([join(LIB_DIR, "ffmpeg", "bin", "ffmpeg"), "-version"], stdout=subprocess.PIPE)
                stdout, stderr = data.communicate()
                logging.info(stdout.decode("utf-8"))
                self.ffmpegdir = join(LIB_DIR, "ffmpeg", "bin")
            except Exception:
                logging.error("Please add ffmpeg to your path or to the WMS libs directory")

    def metadata(self, filename, tags):
        metadata = subprocess.Popen([join(self.ffmpegdir, "ffprobe"), "-v", "quiet", "-print_format", "json" ,"-show_format", filename], stdout=subprocess.PIPE)
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
        return json.dumps(returnData)
