""" Tests and Fixtures"""
from simple_coro import generateUpdateStatement


def test_update_post():
    # INPUT: Update value field of post with _id of 2
    input = { "posts": [{"_id": 2, "value": "too"}] }
    # OUTPUT: Update value field of post at index 0
    output = { "$update": {"posts.0.value": "too"} }
    result = generateUpdateStatement(mutation=input) 
    assert next(result) == output

def test_update_mention_with_id():
    # INPUT: Update text field in mention with _id of 5, for post with _id of 3
    input = { "posts": [{"_id": 3, "mentions": [ {"_id": 5, "text": "pear"}]}] }
    # OUTPUT: Update text field in mention at index 1, for post at index 0
    output = { "$update": {"posts.1.mentions.0.text": "pear"}}
    assert next(generateUpdateStatement(mutation=input)) == output

def test_add_post():
    #  INPUT: Add post; notice that there is no _id because the post doesn't exist yet
    input = {"posts": [{"value": "four"}] }
    # /OUTPUT: Add post
    output = {"$add": {"posts": [{"value": "four"}] }}
    assert next(generateUpdateStatement(mutation=input)) == output

def test_add_mention():
    # INPUT: Add mention to post with _id of 3
    input =  {"posts": [{"_id": 3, "mentions": [{"text": "banana"}]}]}
    # OUTPUT: Add mention for post at index 2
    output =  {"$add": {"posts.1.mentions": [{"text": "banana"}]}}
    assert next(generateUpdateStatement(mutation=input)) == output

def test_remove_post():
    # INPUT: Remove post with _id of 2
    input =  { "posts": [{"_id": 2, "_delete": True}] }
    # OUTPUT: Remove post at index 0
    output = { "$remove" : {"posts.0" : True} }
    assert next(generateUpdateStatement(mutation=input)) == output

def test_remove_mention():
    # INPUT: Remove mention with _id of 6, for post with _id of 3
    input =  { "posts": [{"_id": 3, "mentions": [{"_id": 6, "_delete": True}]}]}
    # OUTPUT: Remove mention at index 1, for post at index 1
    output = { "$remove" : {"posts.1.mentions.1": True}}
    assert next(generateUpdateStatement(mutation=input)) == output

def test_multiple_actions():
    input = {
    "posts": [
        {"_id": 2, "value": "too"},
        {"value": "four"},
        {"_id": 4, "_delete": True}
    ] }
    output = {
    "$update": {"posts.0.value": "too"},
    "$add": {"posts": [{"value": "four"}] },
    "$remove" : {"posts.2" : True}
    }
    assert next(generateUpdateStatement(mutation=input)) == output