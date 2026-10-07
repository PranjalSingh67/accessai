"""Conftest for pytest fixtures."""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Provide test client for FastAPI app."""
    return TestClient(app)
