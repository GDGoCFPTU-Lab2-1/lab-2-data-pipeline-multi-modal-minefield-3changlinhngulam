import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # Use the 'ast' module to find docstrings for functions
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        print(f"Error parsing code: {e}")
        return {}
    
    # Extract module-level docstring
    module_docstring = ast.get_docstring(tree)
    
    # Extract function docstrings
    function_docs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_name = node.name
            func_docstring = ast.get_docstring(node)
            if func_docstring:
                function_docs.append(f"Function '{func_name}': {func_docstring}")
    
    # Extract business rules from comments using regex
    business_rules = re.findall(r'# Business Logic Rule \d+:.*', source_code)
    
    # Combine all extracted information
    content_parts = []
    
    if module_docstring:
        content_parts.append(f"Module Documentation: {module_docstring}")
    
    if function_docs:
        content_parts.append("Function Documentation: " + " | ".join(function_docs))
    
    if business_rules:
        content_parts.append("Business Rules: " + " | ".join(business_rules))
    
    content = " ".join(content_parts)
    
    # Return a dictionary for the UnifiedDocument schema
    return {
        "document_id": "code-legacy-001",
        "content": content,
        "source_type": "Code",
        "author": "Senior Dev (retired)",
        "timestamp": None,
        "tags": ["legacy", "business-logic", "documentation"],
        "source_metadata": {
            "original_file": "legacy_pipeline.py",
            "module_docstring": module_docstring,
            "function_count": len(function_docs),
            "business_rules_count": len(business_rules)
        }
    }

