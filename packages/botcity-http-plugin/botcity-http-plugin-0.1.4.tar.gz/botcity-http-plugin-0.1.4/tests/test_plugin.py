import shutil

import pytest
import hashlib
import tempfile
import os
from typing import Dict

from botcity.plugins.http import BotHttpPlugin


@pytest.fixture(autouse=True, scope="session")
def tmp_folder() -> str:
    folder = tempfile.mkdtemp()
    yield folder
    shutil.rmtree(folder)


def test_get():
    assert BotHttpPlugin("https://httpbin.org/get?test=The test of BotHttpPlugin work!").get().json()["args"]["test"]  == "The test of BotHttpPlugin work!"


def test_post():
    assert BotHttpPlugin("https://httpbin.org/post?test=The test of BotHttpPlugin work!").post().json()["args"]["test"]  == "The test of BotHttpPlugin work!"


def test_get_bytes():
    # Expected values
    url = "https://files.pythonhosted.org/packages/b7/86/c9ea9877ed8f9abc4e7f55fc910c40fbbf88778b65e006a917970ac5524f/botcity-framework-web-0.2.0.tar.gz"
    expected_sha = "3637f54e8d9e24f4d346a5e511b545e059e938144beedcfa9323d00aaf18154b"

    content = BotHttpPlugin(url).get_bytes()
    assert hashlib.sha256(content).hexdigest() == expected_sha


def test_get_file(tmp_folder: str):
    # Expected values
    url = "https://files.pythonhosted.org/packages/b7/86/c9ea9877ed8f9abc4e7f55fc910c40fbbf88778b65e006a917970ac5524f/botcity-framework-web-0.2.0.tar.gz"
    expected_sha = "3637f54e8d9e24f4d346a5e511b545e059e938144beedcfa9323d00aaf18154b"

    # Downloads the file with a get request
    name = BotHttpPlugin(url).get_as_file(f"{tmp_folder}/get_file_test")

    # Verifies if the file was properly downloaded
    with open(os.path.join(os.getcwd(), name), 'rb') as file:
        data = file.read()
    assert hashlib.sha256(data).hexdigest() == expected_sha


def test_set_url():
    bot = BotHttpPlugin(url="")
    assert bot.url == ""
    url = "https://httpbin.org/get?test=The test of BotHttpPlugin work!"
    response = bot.set_url(url=url)
    assert isinstance(response, BotHttpPlugin)
    assert bot.url == url


def test_set_params():
    bot = BotHttpPlugin(url="")
    params = {"test": True}
    bot.set_params(params=params)
    assert bot.params == params


def test_add_params():
    bot = BotHttpPlugin(url="")
    params = {"test": True}
    bot.set_params(params=params)
    assert bot.params == params
    response = bot.add_param(key="test_two", value=True)
    assert isinstance(response, BotHttpPlugin)
    assert bot.params.get("test_two")


def test_get_as_json():
    bot = BotHttpPlugin("https://httpbin.org/get?test=The test of BotHttpPlugin work!")
    response = bot.get_as_json()
    assert isinstance(response, Dict)
    assert response.get("args").get("test") == "The test of BotHttpPlugin work!"


def test_post_as_json():
    bot = BotHttpPlugin("https://httpbin.org/post?test=The test of BotHttpPlugin work!")
    response = bot.post_as_json()
    assert isinstance(response, Dict)
    assert response.get("args").get("test") == "The test of BotHttpPlugin work!"
