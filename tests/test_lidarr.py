import pytest

from pyarr.models.lidarr import LidarrArtistMonitor

from tests import load_fixture


@pytest.mark.usefixtures
def test_add_root_folder(responses, lidarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8686/api/v1/rootfolder",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/rootfolder.json"),
        status=201,
        match_querystring=True,
    )
    data = lidarr_client.add_root_folder(
        name="test", path="/path/to/folder", qualityProfile=1, metadataProfile=1
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_lookup(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/search?term=my+string",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.lookup(term="my string")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_artist(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/lookup?term=my+string",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.lookup_artist(term="my string")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_lookup_album(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/album/lookup?term=my+string",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.lookup_album(term="my string")
    assert isinstance(data, list)


@pytest.mark.usefixtures
def test_get_artist(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist_all.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_artist()
    assert isinstance(data, list)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_artist(id_=1)
    assert isinstance(data, dict)

    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist?mbId=123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.get_artist(id_="123456")
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test__artist_json(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/lookup?term=lidarr%3A123456-123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )

    data = lidarr_client._artist_json(
        id_="123456-123456",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        artist_monitor=LidarrArtistMonitor.FIRST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_add_artist(responses, lidarr_client):
    responses.add(
        responses.POST,
        "https://127.0.0.1:8686/api/v1/artist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=201,
        match_querystring=True,
    )
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/lookup?term=lidarr%3A123456",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/lookup.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.add_artist(
        id_="123456",
        root_dir="/",
        quality_profile_id=1,
        metadata_profile_id=1,
        monitored=False,
        artist_monitor=LidarrArtistMonitor.LATEST_ALBUM,
        artist_search_for_missing_albums=False,
    )
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_upd_artist(responses, lidarr_client):
    responses.add(
        responses.GET,
        "https://127.0.0.1:8686/api/v1/artist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=202,
        match_querystring=True,
    )
    artist = lidarr_client.get_artist(1)

    responses.add(
        responses.PUT,
        "https://127.0.0.1:8686/api/v1/artist",
        headers={"Content-Type": "application/json"},
        body=load_fixture("lidarr/artist.json"),
        status=202,
        match_querystring=True,
    )
    data = lidarr_client.upd_artist(data=artist)
    assert isinstance(data, dict)


@pytest.mark.usefixtures
def test_delete_artist(responses, lidarr_client):
    responses.add(
        responses.DELETE,
        "https://127.0.0.1:8686/api/v1/artist/1",
        headers={"Content-Type": "application/json"},
        body=load_fixture("common/delete.json"),
        status=200,
        match_querystring=True,
    )
    data = lidarr_client.delete_artist(1)
    assert isinstance(data, dict)
