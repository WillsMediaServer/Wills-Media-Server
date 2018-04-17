# this file is to store the code that adds an:
# Artist, Genre, Album and a Song

### THIS CODE WILL NOT RUN
### YOU NEED TO RUN IT INSIDE A FLASK VIEW BLUEPRINT

from wms.db import db, Artists, Genres, Albums, Songs
import datetime

newArtist = Artists(name="An Artist", description="An Artists Description")
newGenre  = Genres(name="A Genre", description="A Genre's Description")
newAlbum  = Albums(artist=1, name="An Album", releaseDate=datetime.datetime(year=1, month=1, day=1), genre=1, picture="/path/to/image/file")
newSong   = Songs(name="A Song", album=1, artist=1, length=datetime.time(hour=1, minute=1, second=1), location="/path/to/audio/file")
db.session.add(newArtist)
db.session.add(newGenre)
db.session.add(newAlbum)
db.session.add(newSong)
db.session.commit()
