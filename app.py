from models import Person, Post, Mention, PostsCommand
from typing import Callable, Dict, List, Union
from data import document
from orm import parse_queries_


def generateUpdateStatement(
    document: Dict = document, mutation: Union[Dict, None] = None
):  
    validated_doc = safe_call(lambda: Person(**document))
    commands_ = safe_call(
        lambda: [
            PostsCommand(**command) for command in mutation.get("posts", [])
        ]
    )
    return parse_queries_(commands_, validated_doc)

def safe_call(
    func: Callable, exception_: Callable = Exception, _msg: str = ""
) -> Union[None, Callable]:
    try:
        return func()
    except Exception as e:
        raise exception_(str(e)) from e