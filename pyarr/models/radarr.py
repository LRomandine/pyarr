from typing import Literal

RadarrCommands = Literal[
    "DownloadedMoviesScan",
    "MissingMoviesSearch",
    "RefreshMovie",
    "RenameMovie",
    "RenameFiles",
    "Backup",
]
"""
Radarr commands.

    Note:
        The parameters are supplied as `**kwargs` within the `post_command` method.

DownloadedMoviesScan:
    Scans for all clients for downloaded movies, or a single client by ID

    Args:
        clientid (int, optional): Download client ID

MissingMoviesSearch:
    Searches for any missing movies

RefreshMovies:
    Refreshes all of the movies, or specific by ID

    Args:
        movieid (int, Optional): ID of Movie

RenameMovie:
    Rename specific movie to correct format.

    Args:
        movieid (list[int]): ID of Movie or movies

RescanMovie:
    Rescans specific movie

    Args:
        movieid (int): ID of Movie

RenameFiles:
    Rename files to correct format

    Args:
        movieid (int): ID of Movie

Backup:
    Backup the server data
"""

#: Radarr sort keys
RadarrSortKey = Literal[
    "date",
    "downloadClient",
    "id",
    "indexer",
    "languages",
    "message",
    "modieId",
    "movies.sortTitle",
    "path",
    "progress",
    "protocol",
    "quality",
    "ratings",
    "title",
    "size",
    "sourcetitle",
    "status",
    "timeleft",
]


#: Radarr event types
RadarrEventType = Literal[
    "unknown",
    "grabbed",
    "downloadFolderImported",
    "downloadFailed",
    "movieFileDeleted",
    "movieFolderImported",
    "movieFileRenamed",
    "downloadIgnored",
]

#: Radarr movie availability types
RadarrMonitorType = Literal["movieOnly", "movieAndCollections", "none"]

#: Radarr movie availability types
RadarrAvailabilityType = Literal["announced", "inCinemas", "released"]
