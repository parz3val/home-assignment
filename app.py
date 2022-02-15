from models import Person, Post, Mention, PostsCommand
from typing import Callable, Dict, List, Union
from data import document


def generateUpdateStatement(
    document: Dict = document, mutation: Union[Dict, None] = None
):  
    validated_doc = safe_call(lambda: Person(**document))
    import pdb
    pdb.set_trace()
    commands_ = safe_call(
        lambda: [
            PostsCommand(**command) for command in mutation.get("posts", [])
        ]
    )

def safe_call(
    func: Callable, exception_: Callable = Exception, _msg: str = ""
) -> Union[None, Callable]:
    try:
        return func()
    except Exception as e:
        raise exception_(str(e)) from e