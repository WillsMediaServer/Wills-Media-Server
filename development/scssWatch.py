# This requires the sass installed
from os.path import join, dirname, abspath, normpath
from os import system

BASE_DIR = normpath(join(dirname(abspath(__file__)), ".."))
inputDir = join(BASE_DIR, "wms", "static", "scss")
outputDir = join(BASE_DIR, "wms", "static", "css")

system("sass --watch '" + join(inputDir, "main.scss") + "':'" + join(outputDir, "main-dev.css") + "' --style compressed")
