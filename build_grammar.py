import subprocess
import os

def build_cpp_grammar():
    grammar_dir = os.path.abspath('tree-sitter-cpp')
    grammar_js_path = os.path.join(grammar_dir, 'grammar.js')
    output_lib = './my-languages.so'

    if not os.path.exists(grammar_dir):
        print(f"Error: Grammar directory '{grammar_dir}' not found. Make sure you cloned 'tree-sitter-cpp'.")
        return False
    if not os.path.exists(grammar_js_path):
        print(f"Error: Grammar file '{grammar_js_path}' not found. Something is wrong with tree-sitter-cpp clone.")
        return False


    try:
        # Use tree-sitter generate command (command-line interface)
        subprocess.run(
            ['tree-sitter', 'generate', '--abi', '135', grammar_js_path], # Pass grammar_js_path directly
            check=True,
            cwd='.' # Run in the current directory
        )

        # Compile the generated parser (parser.c and potentially scanner.c)
        parser_c_path = os.path.join(grammar_dir, 'src', 'parser.c')
        scanner_c_path = os.path.join(grammar_dir, 'src', 'scanner.c') # Scanner is optional

        compile_commands = [
            'gcc',
            '-shared',
            '-o', output_lib,
            '-fPIC',  # Required for shared libraries on Linux/macOS
            parser_c_path,
        ]
        if os.path.exists(scanner_c_path): # Add scanner if it exists
            compile_commands.append(scanner_c_path)

        subprocess.run(
            compile_commands,
            check=True,
            cwd='.'
        )

        print(f"C++ grammar library built successfully: {output_lib}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error building grammar library:")
        print(e)
        return False


if __name__ == "__main__":
    build_cpp_grammar()
