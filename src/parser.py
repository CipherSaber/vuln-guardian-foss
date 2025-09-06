# In src/parser.py

from tree_sitter_languages import get_language, get_parser

# Initialize the C language parser
language = get_language('c')
parser = get_parser('c')

def parse_c_functions(file_content_bytes):
    """
    Parses the byte content of a C file and extracts all function definitions.

    Args:
        file_content_bytes (bytes): The content of the C file as bytes.

    Returns:
        list: A list of dictionaries, where each dictionary represents a function
              and contains its name, code, and starting line number.
    """
    try:
        tree = parser.parse(file_content_bytes)
        root_node = tree.root_node
        
        functions = []
        # A tree-sitter query to find all nodes of type 'function_definition'
        query = language.query("""
        (function_definition) @function
        """)
        captures = query.captures(root_node)
        
        for node, _ in captures:
            try:
                # This logic robustly finds the function name within the declarator
                declarator_node = node.child_by_field_name('declarator')
                if declarator_node:
                    identifier_node = declarator_node.child_by_field_name('declarator')
                    if not identifier_node: # Handles simple cases like "void func()"
                        identifier_node = declarator_node
                    
                    # Handles more complex cases with pointers etc.
                    while 'declarator' in [child.type for child in identifier_node.children]:
                        identifier_node = identifier_node.child_by_field_name('declarator')

                    function_name = identifier_node.text.decode('utf8')
                    function_code = node.text.decode('utf8')
                    # Get the starting line number (tree-sitter is 0-indexed, we want 1-indexed for humans)
                    start_line = node.start_point[0] + 1
                    
                    functions.append({
                        "name": function_name,
                        "code": function_code,
                        "line": start_line
                    })
            except Exception:
                # If a specific function node is malformed, skip it and continue
                continue
                
        return functions
    except Exception:
        # If the entire file is unparseable, return an empty list
        return []
