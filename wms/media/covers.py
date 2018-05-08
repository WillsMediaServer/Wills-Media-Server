import base64
import io
import logging

from flask import Blueprint, send_file

from wms import STATIC_DIR
from wms.database import AudioImages


class Covers:
    def __init__(self, database):
        self.logger = logging.getLogger('wms.media.covers')
        self.covers = Blueprint("covers", __name__, url_prefix='/media/covers')
        self.main(self.covers, database)

    def main(self, covers, database):
        @covers.route('/<int:id>')
        def getCover(id):
            cover = AudioImages.query.filter_by(id=id).first()
            if cover == None:
                filename = os.path.join(STATIC_DIR, "img", "blankAudio.png")
                return send_file(filename, mimetype="image/png")
            else:
                image = base64.b64decode(cover.image)
                return send_file(io.BytesIO(image), mimetype="image/png")
