""" Simple Query Builder to build queries for commands
"""
from models import MentionCommand, MentionType, Person, PostType, PostsCommand
from typing import List, Dict, Literal, Union


class QueryBuilder:
    def __init__(cls, command: PostsCommand, document: Person):
        cls.post = command
        cls.mentions = command.mentions
        cls.document = document
        cls.index = document.posts.index(cls.get_post(document, command)) if command._id else None
    
    def get_post(cls, document, command):
        return next(
            (
                post
                for post in document.posts
                if post.get('_id') == command._id
            ),
            None,
        )
    
    def get_mention(cls, document, command):
        return next(
            (
                mention
                for mention in document.posts[cls.index].get('mentions')
                if mention.get("_id") == command.get('_id')
            ),
            None,
        )
    def get_mention_idx(cls, command_):
        if cls.document.posts[cls.index].get('mentions') and cls.get_mention(cls.document, command_):
            return cls.document.posts[cls.index].get('mentions').index(cls.get_mention(cls.document, command_))
    
    def post_query(cls, type:PostType, command_: PostsCommand):
        if command_._delete:
            # find the index of command._id in document.posts
            return {"$remove": {f"posts.{cls.index}": True}}
        elif cls.index==0 or cls.index:
            return {"$update": {f"posts.{cls.index}.value": command_.value}}
        else:
            idx_ = 0 if cls.index is None else cls.index
            return {"$add": {'posts': [{'value': command_.value}]}}


    def mention_query(cls, type:MentionType, command_: MentionCommand):
        if command_.get('_delete'):
            return {"$remove": {f"posts.{cls.index}.mentions.{cls.get_mention_idx(command_)}": True}}
        elif cls.get_mention_idx(command_) == 0 or cls.get_mention_idx(command_):
            return {
                "$update": {f"posts.{cls.index}.mentions.{cls.get_mention_idx(command_)}.text": command_.get("text")}
            }
        else:
            return {
                "$add": {
                    f"posts.{cls.index}.mentions": [{"text": command_.get("text")}]
                }
            }




def parse_query(command: PostsCommand, document: Person) -> Dict:
    orm_conn = QueryBuilder(command, document)
    if orm_conn.post._id is None or orm_conn.post._delete:
        return orm_conn.post_query(type=PostType(), command_=orm_conn.post)
    elif orm_conn.mentions not in [[], None]:
        return orm_conn.mention_query(type=MentionType(), command_=orm_conn.mentions[0])
    else:
        return orm_conn.post_query(type=PostType(), command_=orm_conn.post)



def parse_queries_(
    commands_: List[PostsCommand], document: Person
) -> Dict:
    """
    Map posts command into into statement
    """
    queries:Dict = {}
    [queries.update(parse_query(command, document)) for command in commands_]
    return queries
