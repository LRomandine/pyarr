import contextlib
from datetime import datetime
import json
import random

import pytest
import responses

from pyarr.exceptions import (
    PyarrMissingArgument,
    PyarrRecordNotFound,
    PyarrResourceNotFound,
)
from pyarr.models.common import (
    PyarrBlocklistSortKey,
    PyarrDownloadClientSchema,
    PyarrHistorySortKey,
    PyarrImportListSchema,
    PyarrIndexerSchema,
    PyarrLogFilterKey,
    PyarrLogFilterValue,
    PyarrLogSortKey,
    PyarrNotificationSchema,
    PyarrSortDirection,
)
from pyarr.models.radarr import RadarrCommands, RadarrEventType, RadarrSortKeys
from pyarr.radarr import RadarrAPI
from pyarr.types import JsonArray, JsonObject

from tests import (
    RADARR_IMDB,
    RADARR_IMDB_LIST,
    RADARR_MOVIE_TERM,
    RADARR_TMDB,
    load_fixture,
)
from tests.conftest import radarr_client, radarr_mock_client


def test_add_root_folder(radarr_client: RadarrAPI):

    data = radarr_client.add_root_folder(directory="/defaults")
    assert isinstance(data, dict)


def test_get_root_folder(radarr_client: RadarrAPI):

    data = radarr_client.get_root_folder()
    assert isinstance(data, list)

    data = radarr_client.get_root_folder(data[0]["id"])
    assert isinstance(data, dict)


def test__movie_json(radarr_client: RadarrAPI):
    data = radarr_client._movie_json(
        id_=RADARR_IMDB,
        root_dir="/",
        quality_profile_id=1,
        monitored=False,
        search_for_movie=False,
    )
    assert isinstance(data, dict)
    assert data["rootFolderPath"] == "/"
    assert data["qualityProfileId"] == 1
    assert data["monitored"] == False

    with contextlib.suppress(DeprecationWarning):
        data = radarr_client._movie_json(
            id_=RADARR_IMDB, root_dir="/", quality_profile_id=1, tmdb=True
        )

    with contextlib.suppress(PyarrRecordNotFound):
        data = radarr_client._movie_json(
            id_="tt123d",
            root_dir="/",
            quality_profile_id=1,
            monitored=False,
            search_for_movie=False,
        )
        assert False


def test_get_command(radarr_client: RadarrAPI):
    """Check get_command()"""

    # No args
    data = radarr_client.get_command()
    assert isinstance(data, list)

    # When an ID is supplied
    data = radarr_client.get_command(data[0]["id"])
    assert isinstance(data, dict)

    # when an incorrect ID is supplied, not found response
    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_client.get_command(432111111)
        assert False


def test_post_command(radarr_client: RadarrAPI):

    data = radarr_client.post_command(name=RadarrCommands.RESCAN_MOVIE, movieid=1)
    assert isinstance(data, dict)
    data = radarr_client.post_command(name=RadarrCommands.REFRESH_MOVIE, seriesId=1)
    assert isinstance(data, dict)
    data = radarr_client.post_command(name=RadarrCommands.MISSING_MOVIES_SEARCH)
    assert isinstance(data, dict)
    data = radarr_client.post_command(name=RadarrCommands.DOWNLOADED_MOVIES_SCAN)
    assert isinstance(data, dict)
    data = radarr_client.post_command(name=RadarrCommands.RENAME_FILES, files=[1, 2, 3])
    assert isinstance(data, dict)
    data = radarr_client.post_command(name=RadarrCommands.RENAME_FILES)
    assert isinstance(data, dict)
    data = radarr_client.post_command(
        name=RadarrCommands.RENAME_MOVIE, seriesIds=[1, 2, 3]
    )
    assert isinstance(data, dict)
    data = radarr_client.post_command(name=RadarrCommands.BACKUP)
    assert isinstance(data, dict)


def test_add_quality_profile(radarr_client: RadarrAPI):

    data = radarr_client.get_quality_definition()
    assert isinstance(data, list)

    test_items = [data[0], data[3], data[5]]

    data = radarr_client.add_quality_profile(
        name="Testing", upgrades_allowed=True, cutoff=3, items=test_items
    )
    assert isinstance(data, dict)


def test_get_quality_profile(radarr_client: RadarrAPI):

    data = radarr_client.get_quality_profile()
    assert isinstance(data, list)

    data = radarr_client.get_quality_profile(data[0]["id"])
    assert isinstance(data, dict)


def test_upd_quality_profile(radarr_client: RadarrAPI):

    quality_profiles = radarr_client.get_quality_profile()

    for profile in quality_profiles:
        if profile["name"] == "Testing":
            data = radarr_client.upd_quality_profile(id_=profile["id"], data=profile)
            assert isinstance(data, dict)


def test_lookup_movie(radarr_client: RadarrAPI):
    data = radarr_client.lookup_movie(term=f"imdb:{RADARR_IMDB}")
    assert isinstance(data, list)

    data = radarr_client.lookup_movie(term=f"tmdb:{RADARR_TMDB}")
    assert isinstance(data, list)

    data = radarr_client.lookup_movie(term=RADARR_MOVIE_TERM)
    assert isinstance(data, list)


def test_lookup_movie_by_tmdb_id(radarr_client: RadarrAPI):

    data = radarr_client.lookup_movie_by_tmdb_id(id_=RADARR_TMDB)
    assert isinstance(data, list)


def test_lookup_movie_by_imdb_id(radarr_client: RadarrAPI):

    data = radarr_client.lookup_movie_by_imdb_id(id_=RADARR_IMDB)
    assert isinstance(data, list)


def test_add_movie(radarr_client: RadarrAPI):

    data = radarr_client.add_movie(
        id_=RADARR_IMDB,
        root_dir="/",
        quality_profile_id=1,
        monitored=False,
        search_for_movie=False,
    )
    data = radarr_client.add_movie(
        id_=RADARR_IMDB_LIST[0],
        root_dir="/",
        quality_profile_id=1,
        monitored=False,
        search_for_movie=False,
    )
    assert isinstance(data, dict)
    data = radarr_client.add_movie(
        id_=RADARR_IMDB_LIST[1],
        root_dir="/",
        quality_profile_id=1,
        monitored=False,
        search_for_movie=False,
    )
    assert isinstance(data, dict)
    assert isinstance(data, dict)
    with contextlib.suppress(DeprecationWarning):
        data = radarr_client.add_movie(
            id_=RADARR_TMDB, root_dir="/", quality_profile_id=1, tmdb=True
        )

    with contextlib.suppress(PyarrRecordNotFound):
        data = radarr_client.add_movie(
            id_="tt123d",
            root_dir="/",
            quality_profile_id=1,
            monitored=False,
            search_for_movie=False,
        )
        assert False


def test_get_movie(radarr_client: RadarrAPI):
    data = radarr_client.get_movie()
    assert isinstance(data, list)

    data = radarr_client.get_movie(id_=data[0]["id"])
    assert isinstance(data, dict)

    data = radarr_client.get_movie(id_=RADARR_TMDB, tmdb=True)
    assert isinstance(data, list)


def test_get_movie_by_movie_id(radarr_client: RadarrAPI):

    movie = radarr_client.get_movie()
    data = radarr_client.get_movie_by_movie_id(movie[0]["id"])
    assert isinstance(data, dict)

    with pytest.deprecated_call():
        radarr_client.get_movie_by_movie_id(movie[0]["id"])

    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_client.get_movie_by_movie_id(999)
        assert False


def test_upd_movie(radarr_client: RadarrAPI):

    movie = radarr_client.get_movie()

    data = radarr_client.upd_movie(data=movie[0])
    assert isinstance(data, dict)

    data = radarr_client.upd_movie(data=movie[0], move_files=True)
    assert isinstance(data, dict)


def test_upd_movies(radarr_client: RadarrAPI):
    movie = radarr_client.get_movie()
    quality_profile = radarr_client.get_quality_profile()
    update_data = {
        "movieIds": [movie[0]["id"]],
        "rootFolderPath": "/defaults/",
        "monitored": True,
        "qualityProfileId": quality_profile[0]["id"],
        "minimumAvailability": "inCinemas",
    }
    data = radarr_client.upd_movies(data=update_data)
    assert isinstance(data, list)

    movie = radarr_client.get_movie()
    update_data = {
        "movieIds": [movie[0]["id"]],
        "monitored": False,
    }
    data = radarr_client.upd_movies(data=update_data)
    assert isinstance(data, list)


def test_get_history(radarr_client: RadarrAPI):

    data = radarr_client.get_history()
    assert isinstance(data, dict)

    data = radarr_client.get_history(
        page=1,
        page_size=10,
        sort_key=PyarrHistorySortKey.TIME,
        sort_dir=PyarrSortDirection.DEFAULT,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_history(sort_key=PyarrHistorySortKey.TIME)
        assert False

    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_history(sort_dir=PyarrSortDirection.DESC)
        assert False


def test_get_calendar(radarr_client: RadarrAPI):

    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = radarr_client.get_calendar(start_date=start, end_date=end)
    assert isinstance(data, list)

    start = datetime.strptime("Nov 30 2020  1:33PM", "%b %d %Y %I:%M%p")
    end = datetime.strptime("Dec 1 2020  1:33PM", "%b %d %Y %I:%M%p")
    data = radarr_client.get_calendar(start_date=start, end_date=end, unmonitored=False)
    assert isinstance(data, list)


def test_get_system_status(radarr_client: RadarrAPI):

    data = radarr_client.get_system_status()
    assert isinstance(data, dict)


def test_get_health(radarr_client: RadarrAPI):

    data = radarr_client.get_health()
    assert isinstance(data, list)


def test_get_metadata(radarr_client: RadarrAPI):

    data = radarr_client.get_metadata()
    assert isinstance(data, list)

    data = radarr_client.get_metadata(data[0]["id"])
    assert isinstance(data, dict)


def test_get_update(radarr_client: RadarrAPI):

    data = radarr_client.get_update()
    assert isinstance(data, list)


def test_get_disk_space(radarr_client: RadarrAPI):

    data = radarr_client.get_disk_space()
    assert isinstance(data, list)


def test_get_backup(radarr_client: RadarrAPI):

    data = radarr_client.get_backup()
    assert isinstance(data, list)


def test_get_log(radarr_client: RadarrAPI):

    data = radarr_client.get_log()
    assert isinstance(data, dict)

    data = radarr_client.get_log(
        page=10,
        page_size=10,
        sort_key=PyarrLogSortKey.ID,
        sort_dir=PyarrSortDirection.DESC,
        filter_key=PyarrLogFilterKey.LEVEL,
        filter_value=PyarrLogFilterValue.ALL,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_log(sort_key=PyarrLogSortKey.ID)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_log(sort_dir=PyarrSortDirection.DESC)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_log(filter_key=PyarrLogFilterKey.LEVEL)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_client.get_log(filter_value=PyarrLogFilterValue.ALL)
        assert False


def test_get_task(radarr_client: RadarrAPI):

    data = radarr_client.get_task()
    assert isinstance(data, list)

    data = radarr_client.get_task(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_get_config_ui(radarr_client: RadarrAPI):

    data = radarr_client.get_config_ui()
    assert isinstance(data, dict)


def test_upd_config_ui(radarr_client: RadarrAPI):

    payload = radarr_client.get_config_ui()
    payload["enableColorImpairedMode"] = True
    data = radarr_client.upd_config_ui(payload)
    assert isinstance(data, dict)
    assert data["enableColorImpairedMode"] == True


def test_get_config_host(radarr_client: RadarrAPI):

    data = radarr_client.get_config_host()
    assert isinstance(data, dict)


def test_upd_config_host(radarr_client: RadarrAPI):

    payload = radarr_client.get_config_host()
    payload["backupRetention"] = 29
    data = radarr_client.upd_config_host(payload)

    assert isinstance(data, dict)
    assert data["backupRetention"] == 29


def test_get_config_naming(radarr_client: RadarrAPI):

    data = radarr_client.get_config_naming()
    assert isinstance(data, dict)


def test_upd_config_naming(radarr_client: RadarrAPI):

    payload = radarr_client.get_config_naming()
    if (
        payload["standardMovieFormat"]
        == "{Movie Title} ({Release Year}) {Quality Full}"
    ):
        payload["standardMovieFormat"] = "{Movie Title} {Quality Full} ({Release Year})"
    else:
        payload["standardMovieFormat"] = "{Movie Title} ({Release Year}) {Quality Full}"

    data = radarr_client.upd_config_naming(payload)

    assert isinstance(data, dict)
    if (
        payload["standardMovieFormat"]
        == "{Movie Title} ({Release Year}) {Quality Full}"
    ):
        assert (
            data["standardMovieFormat"]
            == "{Movie Title} ({Release Year}) {Quality Full}"
        )
    else:
        assert (
            data["standardMovieFormat"]
            == "{Movie Title} {Quality Full} ({Release Year})"
        )


def test_get_media_management(radarr_client: RadarrAPI):

    data = radarr_client.get_media_management()
    assert isinstance(data, dict)


def test_upd_media_management(radarr_client: RadarrAPI):

    payload = radarr_client.get_media_management()
    payload["recycleBinCleanupDays"] = 6
    data = radarr_client.upd_media_management(payload)

    assert isinstance(data, dict)
    assert data["recycleBinCleanupDays"] == 6


def test_get_notification_schema(radarr_client: RadarrAPI):

    data = radarr_client.get_notification_schema()
    assert isinstance(data, list)

    data = radarr_client.get_notification_schema(
        implementation=PyarrNotificationSchema.BOXCAR
    )
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = radarr_client.get_notification_schema(implementation="polarbear")
        assert False


def test_create_tag(radarr_client: RadarrAPI):

    data = radarr_client.create_tag(label="string")
    assert isinstance(data, dict)


def test_get_tag(radarr_client: RadarrAPI):

    data = radarr_client.get_tag()
    assert isinstance(data, list)

    data = radarr_client.get_tag(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_get_tag_detail(radarr_client: RadarrAPI):

    data = radarr_client.get_tag_detail()
    assert isinstance(data, list)

    data = radarr_client.get_tag_detail(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_tag(radarr_client: RadarrAPI):
    tags = radarr_client.get_tag()

    data = radarr_client.upd_tag(id_=tags[0]["id"], label="newstring")
    assert isinstance(data, dict)
    assert data["label"] == "newstring"


def test_get_download_client_schema(radarr_client: RadarrAPI):

    data = radarr_client.get_download_client_schema()
    assert isinstance(data, list)

    data = radarr_client.get_download_client_schema(
        implementation=PyarrDownloadClientSchema.ARIA2
    )
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = radarr_client.get_download_client_schema(implementation="polarbear")
        assert False


def test_get_import_list_schema(radarr_client: RadarrAPI):

    data = radarr_client.get_import_list_schema()
    assert isinstance(data, list)

    data = radarr_client.get_import_list_schema(
        implementation=PyarrImportListSchema.PLEX
    )
    assert isinstance(data, list)

    with contextlib.suppress(PyarrRecordNotFound):
        data = radarr_client.get_import_list_schema(implementation="polarbear")
        assert False


def test_get_import_list(radarr_client: RadarrAPI):
    data = radarr_client.get_import_list()
    assert isinstance(data, list)


def test_get_config_download_client(radarr_client: RadarrAPI):
    data = radarr_client.get_config_download_client()
    assert isinstance(data, dict)


def test_upd_config_download_client(radarr_client: RadarrAPI):
    dc_config = radarr_client.get_config_download_client()
    dc_config["autoRedownloadFailed"] = False
    data = radarr_client.upd_config_download_client(data=dc_config)
    assert isinstance(data, dict)
    assert data["autoRedownloadFailed"] == False


def test_add_download_client():
    return NotImplemented


def test_upd_download_client():
    return NotImplemented


def test_get_download_client(radarr_client: RadarrAPI):
    data = radarr_client.get_download_client()
    assert isinstance(data, list)
    # TODO: Get download client by ID (required add_download_client first)


def test_get_quality_definition(radarr_client: RadarrAPI):

    data = radarr_client.get_quality_definition()
    assert isinstance(data, list)

    data = radarr_client.get_quality_definition(id_=data[0]["id"])
    assert isinstance(data, dict)


def test_upd_quality_definition(radarr_client: RadarrAPI):
    rand_float = round(random.uniform(100.0, 199.9))

    quality_definitions = radarr_client.get_quality_definition()
    quality_definition = radarr_client.get_quality_definition(
        id_=quality_definitions[0]["id"]
    )
    quality_definition["maxSize"] = rand_float
    data = radarr_client.upd_quality_definition(
        quality_definition["id"], quality_definition
    )
    assert isinstance(data, dict)
    assert data["maxSize"] == rand_float


def test_get_queue_status(radarr_client: RadarrAPI):

    data = radarr_client.get_queue_status()
    assert isinstance(data, dict)


def test_get_custom_filter(radarr_client: RadarrAPI):

    data = radarr_client.get_custom_filter()
    assert isinstance(data, list)


def test_get_indexer_schema(radarr_client: RadarrAPI):
    data = radarr_client.get_indexer_schema()
    assert isinstance(data, list)
    data = radarr_client.get_indexer_schema(
        implementation=PyarrIndexerSchema.IP_TORRENTS
    )
    assert isinstance(data, list)
    assert data[0]["implementation"] == PyarrIndexerSchema.IP_TORRENTS

    with contextlib.suppress(PyarrRecordNotFound):
        data = radarr_client.get_indexer_schema(implementation="polarbear")
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_indexer(radarr_mock_client: RadarrAPI):

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/indexer",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer_all.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_indexer()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_indexer(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_upd_indexer(radarr_mock_client: RadarrAPI):

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_indexer(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:7878/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/indexer.json"),
        status=202,
        match_querystring=True,
    )
    data = radarr_mock_client.upd_indexer(1, data)
    assert isinstance(data, dict)


# def test_add_notification(radarr_client: RadarrAPI):
#    schema = radarr_client.get_notification_schema(implementation=PyarrNotificationSchema.EMAIL)
#
#    schema["name"] = "Testing123"
#    for schema_config in schema["fields"]:
#        if schema_config["name"] == "server":
#            schema_config["value"] == "smtp.testing.com"
#
#
#
#    data = radarr_client.add_notification(data=)


def test_get_notification(radarr_client: RadarrAPI):
    data = radarr_client.get_notification()
    assert isinstance(data, list)
    # TODO: Get notification by ID (required add_notification first)


def test_get_movie_history(radarr_client: RadarrAPI):
    movie = radarr_client.get_movie()
    data = radarr_client.get_movie_history(id_=movie[0]["id"])
    assert isinstance(data, list)

    data = radarr_client.get_movie_history(
        id_=movie[0]["id"], event_type=RadarrEventType.UNKNOWN
    )
    assert isinstance(data, list)


def test_get_remote_path_mapping(radarr_client: RadarrAPI):
    data = radarr_client.get_remote_path_mapping()
    assert isinstance(data, list)


@pytest.mark.usefixtures
@responses.activate
def test_get_blocklist_by_movie_id(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/blocklist/movie?movieId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_blocklist.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_blocklist_by_movie_id(id_=1)
    assert isinstance(data, list)


@pytest.mark.usefixtures
@responses.activate
def test_get_blocklist(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/blocklist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blocklist.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_blocklist()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/blocklist?page=1&pageSize=10&sortKey=date&sortDirection=ascending",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blocklist.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_blocklist(
        page=1,
        page_size=10,
        sort_key=PyarrBlocklistSortKey.DATE,
        sort_dir=PyarrSortDirection.ASC,
    )
    assert isinstance(data, dict)
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_mock_client.get_blocklist(sort_key=PyarrBlocklistSortKey.DATE)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_mock_client.get_blocklist(sort_dir=PyarrSortDirection.ASC)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_queue(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_queue()
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue?page=1&pageSize=20&sortKey=timeleft&sortDirection=default&includeUnknownMovieItems=False",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_queue(
        page=1,
        page_size=20,
        sort_key=RadarrSortKeys.TIMELEFT,
        sort_dir=PyarrSortDirection.DEFAULT,
        include_unknown_movie_items=False,
    )
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_mock_client.get_queue(sort_key=RadarrSortKeys.TIMELEFT)
        assert False
    with contextlib.suppress(PyarrMissingArgument):
        data = radarr_mock_client.get_queue(sort_dir=PyarrSortDirection.DEFAULT)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_get_queue_details(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue/details",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue_details.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_queue_details()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/queue/details?movieId=1&includeMovie=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/queue_details.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_queue_details(id_=1, include_movie=True)
    assert isinstance(data, list)


@pytest.mark.usefixtures
@responses.activate
def test_import_movies(radarr_mock_client: RadarrAPI):

    responses.add(
        responses.POST,
        "https://127.0.0.1:7878/api/v3/movie/import",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/movie_import.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.import_movies(
        data=json.loads(load_fixture("radarr/movie_import.json"))
    )
    assert isinstance(data, list)


@pytest.mark.usefixtures
@responses.activate
def test_get_movie_files_by_movie_id(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/moviefile?movieId=1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/moviefiles.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_movie_files_by_movie_id(id_=1)
    assert isinstance(data, list)


@pytest.mark.usefixtures
@responses.activate
def test_get_movie_file(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/moviefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/moviefile.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_movie_file(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:7878/api/v3/moviefile?movieFileIds=1&movieFileIds=2&movieFileIds=3&movieFileIds=4",
        headers={"Content-Type": "application/json"},
        body=load_fixture("radarr/moviefiles.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.get_movie_file(id_=[1, 2, 3, 4])
    assert isinstance(data, list)


def test_get_indexer(radarr_client: RadarrAPI):
    data = radarr_client.get_indexer()
    assert isinstance(data, list)


#### DELETES MUST BE LAST


def test_del_download_client():
    return NotImplemented


def test_del_tag(radarr_client: RadarrAPI):
    tags = radarr_client.get_tag()
    data = radarr_client.del_tag(tags[0]["id"])
    assert data.status_code == 200


def test_del_movie(radarr_client: RadarrAPI):

    movie = radarr_client.get_movie()

    data = radarr_client.del_movie(
        movie[0]["id"], delete_files=True, add_exclusion=True
    )
    assert data.status_code == 200

    movies = radarr_client.get_movie()
    movie_ids = [movie["id"] for movie in movies]
    print(movie_ids)
    data = radarr_client.del_movie(id_=movie_ids, delete_files=True, add_exclusion=True)
    assert isinstance(data, dict)

    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_client.del_movie(999)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_del_movies(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/movie/editor",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    del_data = {"movieIds": [0], "deleteFIles": True, "addImportExclusion": True}
    data = radarr_mock_client.del_movies(data=del_data)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_blocklist(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/blocklist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.del_blocklist(id_=1)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_blocklist_bulk(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/blocklist/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.del_blocklist_bulk(ids=[1, 2, 3])
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_movie_file(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/moviefile/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.del_movie_file(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/moviefile/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_mock_client.del_movie_file(id_=999)
        assert False

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/moviefile/bulk",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
    )
    data = radarr_mock_client.del_movie_file(id_=[1, 2, 3])
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_queue_bulk(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/queue/bulk?removeFromClient=True&blocklist=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )

    data = radarr_mock_client.del_queue_bulk(
        id_=[1, 2, 3], remove_from_client=True, blocklist=True
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_queue(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/queue/1?removeFromClient=True&blocklist=True",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )

    data = radarr_mock_client.del_queue(id_=1, remove_from_client=True, blocklist=True)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
@responses.activate
def test_del_indexer(radarr_mock_client: RadarrAPI):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/indexer/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = radarr_mock_client.del_indexer(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.DELETE,
        "https://127.0.0.1:7878/api/v3/indexer/999",
        headers={"Content-Type": "application/json"},
        status=404,
    )
    with contextlib.suppress(PyarrResourceNotFound):
        data = radarr_mock_client.del_indexer(id_=999)
        assert False


@pytest.mark.usefixtures
@responses.activate
def test_force_grab_queue_item(radarr_mock_client: RadarrAPI):
    # TODO: get filled out fixture
    responses.add(
        responses.POST,
        "https://127.0.0.1:7878/api/v3/queue/grab/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/blank_dict.json"),
        status=201,
        match_querystring=True,
    )
    data = radarr_mock_client.force_grab_queue_item(id_=1)
    assert isinstance(data, dict)


def test_del_root_folder(radarr_client: RadarrAPI):

    root_folders = radarr_client.get_root_folder()

    # Check folder can be deleted
    data = radarr_client.del_root_folder(root_folders[0]["id"])
    assert data.status_code == 200

    # Check that none existant root folder doesnt throw error
    data = radarr_client.del_root_folder(999)
    assert data.status_code == 200


def test_del_quality_profile(radarr_client: RadarrAPI):

    quality_profiles = radarr_client.get_quality_profile()

    for profile in quality_profiles:
        if profile["name"] == "Testing":

            # Check folder can be deleted
            data = radarr_client.del_quality_profile(profile["id"])
            assert data.status_code == 200

    # Check that none existant root folder doesnt throw error
    data = radarr_client.del_quality_profile(999)
    assert data.status_code == 200
