from requests import get

from .apptypes import ApiCategories, Todo, User, Post, Photo, Comment, Album
from .subtypes import Adress, Geo, Company


def build_request_url(url: str, category: ApiCategories):
    return url + category.value


def get_todos(url: str, count: int):
    result: list[Todo] = []
    request_url = build_request_url(url, ApiCategories.todos)

    response = get(request_url).json()

    for i in range(0, count):
        result.append(Todo(
            user_id=response[i]['userId'],
            id=response[i]['id'],
            title=response[i]['title'],
            completed=response[i]['completed']
        ))

    return result


def get_users(url: str, count: int):
    result: list[User] = []
    request_url = build_request_url(url, ApiCategories.users)

    response = get(request_url).json()

    for i in range(0, count):
        result.append(User(
            id=response[i]['id'],
            name=response[i]['name'],
            username=response[i]['username'],
            email=response[i]['email'],
            adress=Adress(
                street=response[i]['address']['street'],
                suite=response[i]['address']['suite'],
                city=response[i]['address']['city'],
                zipcode=response[i]['address']['zipcode'],
                geo=Geo(
                    lat=response[i]['address']['geo']['lat'],
                    lng=response[i]['address']['geo']['lng']
                )
            ),
            phone=response[i]['phone'],
            website=response[i]['website'],
            company=Company(
                name=response[i]['company']['name'],
                catch_phrase=response[i]['company']['catchPhrase'],
                bs=response[i]['company']['bs']
            )
        ))

    return result


def get_posts(url: str, count: int):
    result: list[Post] = []
    request_url = build_request_url(url, ApiCategories.posts)

    response = get(request_url).json()

    for i in range(0, count):
        result.append(Post(
            user_id=response[i]['userId'],
            id=response[i]['id'],
            title=response[i]['title'],
            body=response[i]['body']
        ))

    return result


def get_comments(url: str, count: int):
    result: list[Comment] = []
    request_url = build_request_url(url, ApiCategories.comments)

    response = get(request_url).json()

    for i in range(0, count):
        result.append(Comment(
            post_id=response[i]['postId'],
            id=response[i]['id'],
            name=response[i]['name'],
            email=response[i]['email'],
            body=response[i]['body']
        ))

    return result


def get_albums(url: str, count: int):
    result: list[Album] = []
    request_url = build_request_url(url, ApiCategories.albums)

    response = get(request_url).json()

    for i in range(0, count):
        result.append(Album(
            user_id=response[i]['userId'],
            id=response[i]['id'],
            title=response[i]['title']
        ))

    return result


def get_photos(url: str, count: int):
    result: list[Photo] = []
    request_url = build_request_url(url, ApiCategories.photos)

    response = get(request_url).json()

    for i in range(0, count):
        result.append(Photo(
            album_id=response[i]['albumId'],
            id=response[i]['id'],
            title=response[i]['title'],
            url=response[i]['url'],
            thumbnail_url=response[i]['thumbnailUrl']
        ))

    return result
