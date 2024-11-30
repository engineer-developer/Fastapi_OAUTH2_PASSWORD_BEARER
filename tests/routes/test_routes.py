from typing import Optional

import pytest
from httpx import AsyncClient
from sqlalchemy import select

from dao.models import User
from tests.conftest import (
    async_client,
    async_session,
)


@pytest.mark.parametrize(
    "route",
    [
        "/api/",
    ],
)
async def test_route_status_200(
    async_client: AsyncClient,
    route: str,
):
    """Test all routes which return status code = 200"""

    response = await async_client.get(route)
    assert response.status_code == 200, f"Url {route} not reachable"


# class TestUsers:
#     """Tests for all users endpoints"""
#
#     @classmethod
#     async def fetch_users_count(cls, session):
#         stmt = select(User)
#         result = await session.execute(stmt)
#         users: list = result.scalars().all()
#         return len(users)
#
#     @classmethod
#     async def test_can_add_new_user_to_db(
#         cls,
#         async_client: AsyncClient,
#         new_user,
#     ):
#         """Test client can add new user to database"""
#
#         async with async_session() as session:
#             user_count_before = await cls.fetch_users_count(session)
#             print(f"{user_count_before=}")
#             url = "/api/users"
#             response = await async_client.post(url, json=new_user)
#             assert response.status_code == 201
#             assert response.json()["id"] == 5
#             user_count_after = await cls.fetch_users_count(session)
#             print(f"{user_count_after=}")
#             assert user_count_after - user_count_before == 1
#
#     @classmethod
#     async def test_can_delete_user_from_db(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can delete user from database"""
#
#         async with async_session() as session:
#             user_count_before = await cls.fetch_users_count(session)
#             print(f"{user_count_before=}")
#             user_id = 5
#             url = f"/api/users/{user_id}"
#             response = await async_client.delete(url, headers=headers)
#             assert response.status_code == 200
#             assert response.json()["result"] is True
#             user_count_after = await cls.fetch_users_count(session)
#             print(f"{user_count_after=}")
#             assert user_count_before - user_count_after == 1
#
#     @classmethod
#     async def fetch_user_by_id(cls, session, user_id):
#         stmt = select(User).where(User.id == user_id)
#         result = await session.execute(stmt)
#         user: Optional[User] = result.scalar_one_or_none()
#         return user
#
#     @classmethod
#     async def fetch_user_by_api(cls, session, api_key):
#         stmt = select(User).join(ApiKey).where(ApiKey.api_key == api_key)
#         result = await session.execute(stmt)
#         user: Optional[User] = result.scalar_one_or_none()
#         return user
#
#     @classmethod
#     async def test_can_follow_another_user(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can follow another user"""
#
#         user_to_follow_id = 2
#         url = f"/api/users/{user_to_follow_id}/follow"
#         response = await async_client.post(url, headers=headers)
#         assert response.status_code == 200
#         assert response.json()["result"] is True
#
#         async with async_session() as session:
#             api_key = headers.get("api-key")
#             user = await cls.fetch_user_by_api(session, api_key)
#             user_to_follow = await cls.fetch_user_by_id(session, user_to_follow_id)
#             assert user_to_follow in user.following
#
#     @classmethod
#     async def test_can_unfollow_another_user(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can follow another user"""
#
#         user_to_follow_id = 2
#         url = f"/api/users/{user_to_follow_id}/follow"
#         response = await async_client.delete(url, headers=headers)
#         assert response.status_code == 200
#         assert response.json()["result"] is True
#
#         async with async_session() as session:
#             api_key = headers.get("api-key")
#             user = await cls.fetch_user_by_api(session, api_key)
#             user_to_follow = await cls.fetch_user_by_id(
#                 session,
#                 user_to_follow_id,
#             )
#             assert user_to_follow not in user.following
#
#
# class TestTweets:
#     """Tests for all tweets endpoints"""
#
#     @classmethod
#     async def fetch_all_tweets(cls, session):
#         """Fetch all tweets from database"""
#         stmt = select(Tweet)
#         result = await session.execute(stmt)
#         return result.scalars().all()
#
#     @classmethod
#     async def test_can_create_new_tweet(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#         new_tweet,
#     ):
#         """Test client can create new tweet"""
#
#         url = "/api/tweets"
#         response = await async_client.post(url, json=new_tweet, headers=headers)
#         assert response.status_code == 201
#         assert response.json()["result"] is True
#         assert response.json()["tweet_id"] == 1
#         async with async_session() as session:
#             tweets = await cls.fetch_all_tweets(session)
#         assert len(tweets) == 1
#
#     @classmethod
#     async def test_can_get_all_tweets(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can get all tweets from database"""
#
#         url = "/api/tweets"
#         response = await async_client.get(url, headers=headers)
#         assert response.status_code == 200
#         tweets_count = response.json().keys()
#         assert len(tweets_count) > 0
#
#     @classmethod
#     async def test_can_mark_like_on_tweet(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can mark like on tweet"""
#
#         tweet_id = 1
#         url = f"/api/tweets/{tweet_id}/likes"
#         response = await async_client.post(url, headers=headers)
#         assert response.status_code == 201
#         assert response.json()["result"] is True
#
#     @classmethod
#     async def test_can_unmark_like_from_tweet(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can unmark like from tweet"""
#
#         tweet_id = 1
#         url = f"/api/tweets/{tweet_id}/likes"
#         response = await async_client.delete(url, headers=headers)
#         assert response.status_code == 200
#         assert response.json()["result"] is True
#
#     @classmethod
#     async def test_can_delete_tweet_by_id(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#     ):
#         """Test client can delete tweet from database"""
#
#         async with async_session() as session:
#             tweets_before = await cls.fetch_all_tweets(session)
#             tweet_id = 1
#             url = f"/api/tweets/{tweet_id}"
#             response = await async_client.delete(url, headers=headers)
#             assert response.status_code == 200
#             assert response.json()["result"] is True
#             tweets_after = await cls.fetch_all_tweets(session)
#             assert len(tweets_before) - len(tweets_after) == 1
#
#
# class TestMedias:
#     """Tests for all medias endpoints"""
#
#     @classmethod
#     @pytest.mark.parametrize(
#         "extension",
#         {"png", "jpg", "jpeg", "gif"},
#     )
#     async def test_can_upload_image(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#         tmp_path,
#         extension,
#     ):
#         """Test client can upload image"""
#
#         image_file = tmp_path / "image_file.{}".format(extension)
#         image_file.write_bytes(b"1")
#         upload_file = {"file": open(image_file, "rb")}
#
#         url = "/api/medias"
#         headers["Content-Type"] = "multipart/form-data; boundary=image"
#         response = await async_client.post(
#             url=url,
#             files=upload_file,
#             headers=headers,
#         )
#         assert response.status_code == 201
#         assert response.json()["result"] is True
#         assert response.json()["media_id"] > 0
#
#     @classmethod
#     @pytest.mark.parametrize(
#         "extension",
#         {"sh", "js", "src", "css", "py", "perl", "pdf", "txt"},
#     )
#     async def test_can_not_upload_not_image_file(
#         cls,
#         async_client: AsyncClient,
#         headers: dict[str, str],
#         tmp_path,
#         extension,
#     ):
#         """Test client can not upload not image files"""
#
#         image_file = tmp_path / "image_file.{}".format(extension)
#         image_file.write_bytes(b"1")
#         upload_file = {"file": open(image_file, "rb")}
#
#         url = "/api/medias"
#         headers["Content-Type"] = "multipart/form-data; boundary=image"
#         response = await async_client.post(
#             url=url,
#             files=upload_file,
#             headers=headers,
#         )
#         assert response.status_code == 403
#         assert response.json()["result"] is False
