import ast

import astor


def modify_py_array(filename, array_id, values, extend=False):
    # Read the existing content of the file
    with open(filename, "r") as file:
        file_content = file.read()

    # Parse the file content into an AST
    tree = ast.parse(file_content)

    # Find the node with the given id
    array_node = None
    # Traverse the node tree
    for node in ast.walk(tree):
        # If a node is an assignment target
        if isinstance(node, ast.Assign):
            # If this targets id matches what we are looking for
            if any(isinstance(target, ast.Name) and target.id == array_id for target in node.targets):
                array_node = node
                break

    # Throw if no node with the specified id is found
    if array_node is None:
        raise ValueError(f'Could not find identifier "{array_id}" in the file.')

    # Throw if the node found is not a list
    if not isinstance(node.value, ast.List):
        raise ValueError(f'Identifier "{array_id}" is not an array.')

    # Parse new values into AST nodes
    new_values_nodes = [ast.parse(value).body[0].value for value in values]
    new_values = ast.List(elts=new_values_nodes, ctx=ast.Load())

    # Replace or extend the existing list
    if extend:
        array_node.value.elts.extend(new_values.elts)
    else:
        array_node.value = new_values

    # Convert the modified AST back to source code
    new_file_content = astor.to_source(tree)

    # Write the modified content back to the file
    with open(filename, "w") as file:
        file.write(new_file_content)
