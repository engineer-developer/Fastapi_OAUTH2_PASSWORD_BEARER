import pytest


@pytest.fixture
async def new_user():
    return {"name": "Dart Weider"}


@pytest.fixture
async def new_tweet():
    return {"tweet_data": "New message", "tweet_media_ids": [1, 2]}
