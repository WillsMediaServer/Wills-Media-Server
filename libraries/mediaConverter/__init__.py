#
# /__init__.py
# Wills Media Server Media Converter
# Version: 0.0.1.0 Alpha
# Created By William Neild
#

import json
import logging
import os
import subprocess

from wms import LIB_DIR, STATIC_DIR


class Converter:
    def __init__(self):
        self.logger = logging.getLogger('wms.media-converter')
        self.logger.info("Initializing ffmpeg")
        self.ffmpegDir = ""
        self.logger.info("Attemting to use ffmpeg from path")
        try:
            data = subprocess.Popen(
                ["ffmpeg", "-version"], stdout=subprocess.PIPE)
            stdout, stderr = data.communicate()
            self.logger.debug(stderr)
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

    def conv(self, path, format, songId):
        AUDIO_DIR = os.path.join(STATIC_DIR, "music", format)
        if not os.path.exists(AUDIO_DIR):
            os.makedirs(AUDIO_DIR)
        if not os.path.isfile(os.path.join(AUDIO_DIR, "{}.{}".format(songId, format))):
            data = subprocess.Popen([
                os.path.join(self.ffmpegDir, "ffmpeg"),
                "-i",
                str(path),
                "-f",
                str(format),
                os.path.join(STATIC_DIR, "music", format,
                             "{}.{}".format(songId, format))
            ])
            data.wait()
        return os.path.join(AUDIO_DIR, "{}.{}".format(songId, format))
