import os

filesToDelete = ["../../WMS-Core/database/main.db",
                 "../../WMS-Core/database/users.db",
                 "../../WMS-Core/database/libraries/music.db",
                 "../../WMS-Core/database/libraries/films.db",
                 "../../WMS-Core/database/libraries/tv.db",
                 "../../WMS-Core/logs/main.log",
                 "../../WMS-Core/config.ini"]

for f in filesToDelete:
    if os.path.isfile(f):
        os.remove(f)
        print("Deleted File: " + str(f))
