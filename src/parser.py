# Create this file if it doesn't exist
from tree_sitter_languages import get_language, get_parser

language = get_language('c')
parser = get_parser('c')

def parse_c_functions(file_content_bytes):
    tree = parser.parse(file_content_bytes)
    root_node = tree.root_node
    
    functions = []
    query = language.query("""
    (function_definition) @function
    """)
    captures = query.captures(root_node)
    
    for node, _ in captures:
        try:
            # This logic tries to find the function name robustly
            declarator_node = node.child_by_field_name('declarator')
            if declarator_node:
                # Handle simple declarators and pointer declarators
                identifier_node = declarator_node.child_by_field_name('declarator')
                if not identifier_node: # Case for simple function like "void func()"
                    identifier_node = declarator_node
                
                # Further nesting for complex declarators
                while 'declarator' in [child.type for child in identifier_node.children]:
                    identifier_node = identifier_node.child_by_field_name('declarator')

                function_name = identifier_node.text.decode('utf8')
                function_code = node.text.decode('utf8')
                
                functions.append({
                    "name": function_name,
                    "code": function_code,
                })
        except Exception:
            # Ignore functions we can't parse correctly
            continue
            
    return functions