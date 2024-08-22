import ast

import astor


class PythonContextManager:
    def __init__(self, filename):
        self.filename = filename
        self.tree = None

    def __enter__(self):
        # Read the existing content of the file
        with open(self.filename, "r") as file:
            file_content = file.read()

        # Parse the file content into an AST
        self.tree = ast.parse(file_content)

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # Convert the modified AST back to source code
        new_file_content = astor.to_source(self.tree)

        # Write the modified content back to the file
        with open(self.filename, "w") as file:
            file.write(new_file_content)

        # Propagate any exceptions
        return False

    def _find_assign_node(self, id):
        assign_node = None
        # Traverse the node tree
        for node in ast.walk(self.tree):
            # If a node is an assignment target
            if isinstance(node, ast.Assign):
                # If this targets id matches what we are looking for
                if any(isinstance(target, ast.Name) and target.id == id for target in node.targets):
                    assign_node = node
                    break

        # Throw if no node with the specified id is found
        if assign_node is None:
            raise ValueError(f'Could not find identifier "{id}" in the file.')

        return assign_node

    def modify_array(self, array_id, values, extend=False):
        # Find the node with the given id
        array_node = self._find_assign_node(array_id)

        # Throw if the node found is not a list
        if not isinstance(array_node.value, ast.List):
            raise ValueError(f'Identifier "{array_id}" is not an array.')

        # Parse new values into AST nodes
        new_values_nodes = [ast.parse(value).body[0].value for value in values]
        new_values = ast.List(elts=new_values_nodes, ctx=ast.Load())

        # Replace or extend the existing list
        if extend:
            array_node.value.elts.extend(new_values.elts)
        else:
            array_node.value = new_values

    def add_code(self, code, end=True):
        # Parse code lines into AST nodes
        new_code_lines_nodes = [ast.parse(line).body for line in code]
        new_code_nodes = [node for line_nodes in new_code_lines_nodes for node in line_nodes]

        # Add these nodes into the tree body at the top or bottom
        self.tree.body = self.tree.body + new_code_nodes if end else new_code_nodes + self.tree.body
