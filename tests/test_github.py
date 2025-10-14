from unittest.mock import MagicMock, patch

import pytest
import requests

from githubstats.github import GitHubClient
from githubstats import __version__


@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    mock.json.return_value = {
        "full_name": "test/repo",
        "stargazers_count": 100,
        "forks_count": 50,
        "open_issues_count": 10,
        "subscribers_count": 25,
        "created_at": "2022-01-01T00:00:00Z",
        "updated_at": "2022-02-01T00:00:00Z",
        "language": "Python",
    }
    return mock


def test_get_repo_stats(mock_response):
    with patch("requests.get", return_value=mock_response) as mock_get:
        client = GitHubClient()
        stats = client.get_repo_stats("test", "repo")

        mock_get.assert_called_once()
        _, kwargs = mock_get.call_args
        assert kwargs["timeout"] == 10
        assert kwargs["headers"]["User-Agent"] == f"githubstats/{__version__}"
        assert kwargs["headers"]["Accept"] == "application/vnd.github+json"
        assert stats["name"] == "test/repo"
        assert stats["stars"] == 100
        assert stats["forks"] == 50


def test_github_client_with_token():
    client = GitHubClient("test_token")
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == "token test_token"


def test_github_client_without_token():
    client = GitHubClient()
    assert "Authorization" not in client.headers
    assert client.headers["User-Agent"] == f"githubstats/{__version__}"


def test_get_repo_stats_http_error(mock_response):
    error_response = MagicMock()
    error_response.status_code = 404
    error_response.reason = "Not Found"
    error_response.json.return_value = {"message": "Repository not found"}
    http_error = requests.HTTPError(response=error_response)

    mock_response.raise_for_status.side_effect = http_error

    with patch("requests.get", return_value=mock_response):
        client = GitHubClient()
        with pytest.raises(RuntimeError) as exc:
            client.get_repo_stats("test", "missing")

    assert "404 Not Found" in str(exc.value)
    assert "Repository not found" in str(exc.value)


def test_get_repo_stats_invalid_json(mock_response):
    mock_response.json.side_effect = ValueError("no json")

    with patch("requests.get", return_value=mock_response):
        client = GitHubClient()
        with pytest.raises(RuntimeError) as exc:
            client.get_repo_stats("test", "repo")

    assert "invalid JSON" in str(exc.value)
