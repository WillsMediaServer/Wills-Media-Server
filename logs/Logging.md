Log Files
=========

Once you start Wills Media Server, Log files will be written here. They will contain the steps
taken to launch the server and every request to the server.

Example Format:

```
[2018-05-04 17:48:18,920] [wms.server] [INFO] 192.168.61.1 GET 200 OK "application/json" /api/v1/music/songs/
```

Now, lets explain each section:

| Section | Description |
|---------|-------------|
| ` [2018-05-04 17:48:18,920] ` | This is the date in the format YYYY-MM-DD HH:MM:SS,MS |
| ` [wms.server] ` | This is the section that the log came from |
| ` [INFO] ` | This is the Level of the log. The levels are DEBUG, INFO, WARNING, ERROR, CRITICAL in ascending severity. |
| **Request Specific:** | |
| ` 192.168.61.1 ` | This is the IP Address that the request came from. 192.168.x.x usually means that it came from a local device on your network |
| ` GET ` | This is the HTTP Method used for the request |
| ` 200 OK ` | This is the HTTP Response Code. 2xx means OK, 3xx means a redirect took place, 4xx means a client error and 5xx means a server error. |
| ` "application/json" ` | This is the format that the server responded with. |
| ` /api/v1/music/songs/ ` | Finally, this is the URL that the client requested from the server. |
