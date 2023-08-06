from enum import Enum
from dataclasses import dataclass

from .subtypes import Adress, Company


class ApiCategories(Enum):
    todos = "todos"
    users = "users"
    posts = "posts"
    comments = "comments"
    albums = "albums"
    photos = "photos"


@dataclass
class Todo:
    user_d: int
    id: int
    title: str
    completed: bool


@dataclass
class User:
    id: int
    name: str
    username: str
    email: str
    adress: Adress
    phone: str
    website: str
    company: Company


@dataclass
class Photo:
    album_id: int
    id: int
    title: str
    url: str
    thumbnail_url: str


@dataclass
class Album:
    user_id: int
    id: int
    title: str


@dataclass
class Comment:
    post_id: int
    id: int
    name: str
    email: str
    body: str


@dataclass
class Post:
    user_id: int
    id: int
    title: str
    body: str
