from http import HTTPStatus
from pathlib import Path
from fastapi.testclient import TestClient
from resize_image.api import app
import os


def test_upload_remove_bg():

    pkg_dir = os.path.abspath(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
    )

    _test_upload_image = os.path.join(pkg_dir, "files/image.jpg")
    _test_upload_file = Path(_test_upload_image)
    _files = {"image": _test_upload_file.open("rb")}
    with TestClient(app) as client:
        response = client.post("/image/remove_bg", files=_files)
        assert response.status_code == HTTPStatus.OK


# remove the test file from the config directory
# _copied_file = Path('/usr/src/app/config', 'new-index.json')
# _copied_file.unlink()
