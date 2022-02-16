"""
Simple Parser for nested generic documents
document = {
    **fields,
    nodes: [
        **{
            **fields,
            nodes: [
                **{
                }
        }
    ***
    ***
    ***
    ]
    ***

}
"""

from typing import Dict

def generateUpdateStatement(document, mutation):
    """Generic statement parser"""
    nodes, nodes_name = children_nodes(document, mutation)
    queries: Dict = {}
    [
        queries.update(get_statement(nodes, command, nodes_name))
        for command in mutation.get(nodes_name)
    ]
    yield queries


def get_statement(nodes, command, nodes_name):
    # check if the child exist in the node
    exists, index = child_status(nodes, command)
    if exists:
        return get_update_statement(nodes[index], command, index, nodes_name)
    else:
        return {"$add": {f"{nodes_name}": [command]}}


def get_update_statement(node, command, index, nodes_name):
    """Get update statement"""
    if command.get("_delete") == True:
        return {"$remove": {f"{nodes_name}.{index}": True}}
    # elif check if the childrens exist in the node
    elif children_nodes(node, command):
        nodes, children_name = children_nodes(node, command)
        return get_statement(
            nodes,
            command.get(children_name)[0],
            f"{nodes_name}.{index}.{children_name}",
        )
    else:
        # get the text and field from the command
        for keys in command.keys():
            if keys not in ["_id", "_delete"]:
                return {
                    "$update": {
                        f"{nodes_name}.{index}.{keys}": command.get(keys)
                    }
                }


def child_status(nodes, command):
    return next(
        (
            (True, nodes.index(node))
            for node in nodes
            if node.get("_id") == command.get("_id")
        ),
        (False, 0),
    )


def children_nodes(document, command):
    """Match child in document"""
    keys = list(command.keys())
    for key in keys:
        if key in document and isinstance(document[key], list):
            return document[key], key
