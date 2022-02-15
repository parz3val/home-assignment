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
    mentions: Union[List[Mention], None] = None


@dataclass
class Person:
    _id: int
    name: str
    posts: Union[List[Post], None] = None


@dataclass
class MentionCommand:
    _id: Union[int, None] = None
    text: Union[str, None] = None
    _delete: bool = False

    @property
    def query(self):
        raise NotImplementedError


@dataclass
class PostsCommand:
    value: Union[str, None] = None
    mentions: Union[List[MentionCommand], None] = None
    _delete: bool = False
    _id: Union[Optional[int], None] = None
