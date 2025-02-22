import clang.cindex
import os

def parse_cpp_file_clang(filepath):
    """Parses a C++ file using clang.cindex and returns the Translation Unit."""
    try:
        # Create Clang index
        index = clang.cindex.Index.create()

        # Parse the C++ file
        translation_unit = index.parse(filepath)  # TU = Translation Unit (root of AST)

        if translation_unit is None:
            print(f"Error: clang.cindex failed to parse C++ file: {filepath}")
            return None

        print(f"DEBUG (Clang): Successfully parsed C++ file: {filepath}")
        return translation_unit  # Return the Translation Unit (AST root)

    except Exception as e:
        print(f"Exception during clang.cindex parsing of {filepath}: {e}")
        return None


def extract_function_calls_clang(translation_unit, filepath):
    """Extracts function calls to user-defined functions from a Clang Translation Unit."""
    function_calls = []
    user_function_names = set() # Set to store names of user-defined functions

    # --- Step 1: Collect User-Defined Function Names ---
    def collect_user_functions(cursor):
        """Collects names of user-defined functions in the Translation Unit."""
        if cursor.kind in [clang.cindex.CursorKind.FUNCTION_DECL, clang.cindex.CursorKind.CXX_METHOD]:
            if cursor.is_definition(): # Only consider definitions, not just declarations
                if cursor.linkage == clang.cindex.LinkageKind.External: # Heuristic: consider external linkage as user-defined
                    user_function_names.add(cursor.spelling)

        for child in cursor.get_children():
            collect_user_functions(child)

    collect_user_functions(translation_unit.cursor) # Populate user_function_names set
    print(f"DEBUG (Clang): User-defined functions detected: {user_function_names}") # Debug print

    # --- Step 2: Extract Calls to User-Defined Functions ---
    def traverse_cursor(cursor):
        """Recursively traverses the Clang AST and extracts calls to user-defined functions."""
        if cursor.kind == clang.cindex.CursorKind.CALL_EXPR:  # Check for function call expressions
            callee_name = cursor.spelling  # Get the spelling of the cursor (function name at call site)
            line_number = cursor.location.line

            if callee_name in user_function_names: # Check if callee is in our set of user-defined functions
                function_calls.append({
                    'caller_function': "TODO: Determine caller function (Clang - User-Defined)", # Improve later
                    'callee_function': callee_name,
                    'file': filepath,
                    'line': line_number
                })
            # (Optionally) Could add filtering for member function calls (MEMBER_REF_EXPR) here if needed later

        # Recursively traverse child cursors
        for child in cursor.get_children():
            traverse_cursor(child)

    traverse_cursor(translation_unit.cursor)  # Start traversal from the root cursor
    return function_calls


# No initialize_clang_parser function needed for Clang (initialization is simpler)

if __name__ == '__main__':
    # Basic test of clang parsing and function call extraction (optional)
    test_file = "test_clang_input.cpp"  # You can create a simple test C++ file

    # Create a simple C++ test file (if it doesn't exist)
    if not os.path.exists(test_file):
        with open(test_file, "w") as f:
            f.write("""
            // test_clang_input.cpp
            #include "utils.h"
            #include <iostream>

            int main() {
                int result = add(5, 3); // Call to user-defined add function
                std::cout << "Result: " << result << std::endl; // Calls to std::cout, std::endl (should be filtered out)
                return 0;
            }
            """)

    tu = parse_cpp_file_clang(test_file)
    if tu:
        print(f"Clang Parsing Test: Successfully parsed {test_file} with Clang.")
        print(f"Root Node Kind (Clang): {tu.cursor.kind}")  # Print root node kind

        function_calls = extract_function_calls_clang(tu, test_file)
        if function_calls:
            print("\nExtracted Function Calls (Clang - User-Defined):")
            for call in function_calls:
                print(f"  - File: {call['file']}, Line: {call['line']}, Callee: {call['callee_function']}")
        else:
            print("\nNo function calls found (Clang - User-Defined).")

    else:
        print(f"Clang Parsing Test: Failed to parse {test_file} with Clang.")
