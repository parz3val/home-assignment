from dataclasses import dataclass
from typing import List, Optional, Union

@dataclass
class PostType:
    name: str =  "posts"

@dataclass
class MentionType:
    name: str = "mentions"

@dataclass
class Mention:
    _id: int
    text: str


@dataclass
class Post:
    _id: int
    value: str
    mentions: List[Mention] = None


@dataclass
class Person:
    _id: int
    name: str
    posts: List[Post] = None

