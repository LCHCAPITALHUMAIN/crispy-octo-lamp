import pytest
from fastapi.testclient import TestClient

from resize_image.api import app


@pytest.fixture
def api_client() -> TestClient:
    """
    Return an API test client that can interact with a temporary database
    """
    return TestClient(app)
