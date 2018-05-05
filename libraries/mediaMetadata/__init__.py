#
# /__init__.py
# Wills Media Server Media Metadata
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import json
import logging
import os
import subprocess

from wms import LIB_DIR


class Metadata:
    def __init__(self):
        self.logger = logging.getLogger('wms.media-metadata')
        self.logger.info("Initializing ffmpeg")
        self.ffmpegDir = ""
        self.logger.info("Attemting to use ffmpeg from path")
        try:
            data = subprocess.Popen(
                ["ffmpeg", "-version"], stdout=subprocess.PIPE)
            stdout, stderr = data.communicate()
            self.logger.debug(stdout.decode("utf-8"))
        except OSError as e:
            self.logger.debug("ffmpeg path error: {}".format(e))
            self.logger.info("Attempting to use ffmpeg from libraries")
            try:
                ffmpegDir = os.path.join(LIB_DIR, "ffmpeg", "bin")
                data = subprocess.Popen(
                    [os.path.join(ffmpegDir, "ffmpeg"), "-version"], stdout=subprocess.PIPE)
                stdout, stderr = data.communicate()
                self.logger.debug(stdout.decode("utf-8"))
                self.ffmpegDir = ffmpegDir
            except OSError as e:
                self.logger.debug("ffmpeg libraries error: {}".format(e))
                self.logger.warning(
                    "ffmpeg doesn't exist in the path or libraries folder, please install to gather media metadata!")
            except Exception as e:
                self.logger.warning(e)
        except Exception as e:
            self.logger.error(e)

    def metadata(self, path, tags=[]):
        metadata = subprocess.Popen([
            os.path.join(self.ffmpegDir, "ffprobe"),
            "-v",
            "quiet",
            "-print_format",
            "json",
            "-show_format",
            path
        ], stdout=subprocess.PIPE)
        stdout, stderr = metadata.communicate()
        jsonMetadata = json.loads(stdout)
        # self.logger.debug("STDERR: {}".format(stderr))
        # self.logger.debug("STDOUT: {}".format(json.dumps(jsonMetadata)))
        returnData = {}
        for tag in tags:
            try:
                returnData[tag] = jsonMetadata["format"]["tags"][tag]
            except:
                returnData[tag] = None
        return json.dumps(returnData)
