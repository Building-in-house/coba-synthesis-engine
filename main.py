from cli import parse_interactive_command, setup_cli_arguments
from project_loader import load_project
from parser_cpp import parse_cpp_file, extract_function_calls  # Tree-sitter parser
from parser_clang import parse_cpp_file_clang, extract_function_calls_clang  # Clang parser
from output import output_json_report, print_function_calls_console

# Global variables to store loaded project information
GLOBAL_LANGUAGE = None
GLOBAL_PROJECT_PATH = None
GLOBAL_PROJECT_FILES = {
    'cpp_source': [],
    'cpp_header': [],
    'other': []
}
PROJECT_LOADED = False  # Flag to track if a project is loaded

def process_command(command_str, use_clang=False):  # Added use_clang parameter
    global GLOBAL_LANGUAGE, GLOBAL_PROJECT_PATH, GLOBAL_PROJECT_FILES, PROJECT_LOADED

    args = parse_interactive_command(command_str.split())

    if args.command == 'load_language':
        GLOBAL_LANGUAGE = args.language
        print(f"Language set to: {GLOBAL_LANGUAGE}")
        PROJECT_LOADED = False  # Reset project loaded flag when language changes

    elif args.command == 'load_project':
        project_path = args.path
        if GLOBAL_LANGUAGE is None:
            print("Error: Please specify a language using 'load_language <language>' before loading a project.")
            return True  # Continue loop
        if PROJECT_LOADED:
            print("Warning: A project is already loaded. Loading a new project will replace the current one.")

        if GLOBAL_LANGUAGE == 'cpp':
            cpp_source_files, cpp_header_files, other_project_files = load_project(project_path, GLOBAL_LANGUAGE)
            if cpp_source_files is None:  # Error in project loading
                return True  # Continue loop

            GLOBAL_PROJECT_PATH = project_path
            GLOBAL_PROJECT_FILES['cpp_source'] = cpp_source_files
            GLOBAL_PROJECT_FILES['cpp_header'] = cpp_header_files
            GLOBAL_PROJECT_FILES['other'] = other_project_files
            PROJECT_LOADED = True  # Set project loaded flag

            print("\nProject loaded and files categorized. Use 'analyze' command to parse and analyze.")
            print("C++ Project File Summary:")
            print(f"  Detected C++ Source Files: {len(GLOBAL_PROJECT_FILES['cpp_source'])}")
            print(f"  Detected C++ Header Files: {len(GLOBAL_PROJECT_FILES['cpp_header'])}")
            print(f"  Other Files: {len(GLOBAL_PROJECT_FILES['other'])}")

        elif GLOBAL_LANGUAGE in ['python', 'javascript']:
            print(f"{GLOBAL_LANGUAGE.capitalize()} project loading not yet implemented.")
        else:
            print(
                "Error: Invalid language set. Please use 'load_language cpp', 'load_language python', or 'load_language javascript'.")

    elif args.command == 'analyze':
        if not PROJECT_LOADED:
            print("Error: No project loaded. Please use 'load_project <path>' to load a project first.")
            return True  # Continue loop
        if GLOBAL_LANGUAGE == 'cpp':
            cpp_source_files = GLOBAL_PROJECT_FILES['cpp_source']
            if not cpp_source_files:
                print("No C++ source files found in the loaded project.")
                return True  # Continue loop

            all_function_calls = []
            for cpp_file in cpp_source_files:
                print(f"\nParsing and extracting calls from: {cpp_file}")
                tree_or_tu = None  # Variable to hold either Tree-sitter tree or Clang Translation Unit
                file_function_calls = []

                if use_clang:  # Use Clang parser if --use-clang flag is used
                    print("DEBUG: Using Clang parser")
                    tree_or_tu = parse_cpp_file_clang(cpp_file)  # Parse with Clang
                    if tree_or_tu:
                        file_function_calls = extract_function_calls_clang(tree_or_tu, cpp_file)  # Placeholder Clang extraction
                    else:
                        print("  Clang parsing failed.")
                else:  # Default to Tree-sitter parser
                    print("DEBUG: Using Tree-sitter parser")
                    tree_or_tu = parse_cpp_file(cpp_file)  # Parse with Tree-sitter
                    if tree_or_tu:
                        file_function_calls = extract_function_calls(tree_or_tu, cpp_file)  # Use Tree-sitter extraction
                    else:
                        print("  Tree-sitter parsing failed.")

                if tree_or_tu:  # Check if parsing (either parser) was successful
                    all_function_calls.extend(file_function_calls)
                    print(f"  Extracted {len(file_function_calls)} function calls (Placeholder).")  # Update message
                else:
                    print("  Parsing failed, skipping function call extraction.")

            if all_function_calls:
                output_data = {
                    "project_path": GLOBAL_PROJECT_PATH,
                    "language": GLOBAL_LANGUAGE,
                    "function_calls": all_function_calls,
                    "parser_used": "Clang" if use_clang else "Tree-sitter"  # Indicate parser used in output
                }
                output_json_report(output_data)
                print_function_calls_console(all_function_calls)
            else:
                print("\nNo function calls found in the loaded project.")

        elif GLOBAL_LANGUAGE in ['python', 'javascript']:
            print(f"{GLOBAL_LANGUAGE.capitalize()} analysis not yet implemented.")
        else:
            print("Error: Language not set or invalid. Analysis cannot proceed.")

    elif args.command is None:
        if command_str.strip():
            print("Invalid command. Type 'help' for available commands.")
        else:
            pass

    elif args.command == 'help':
        setup_cli_arguments().print_help()

    elif args.command in ['exit', 'quit']:
        print("Exiting CodeSynth Engine.")
        return False

    return True


if __name__ == "__main__":
    print("Welcome to CodeSynth Engine Interactive CLI (coba)")
    print("Type 'help' for available commands or 'exit' to quit.")

    running = True
    use_clang_parser = False  # Default to Tree-sitter parser

    # Modify CLI argument parsing in main() to handle --use-clang flag
    cli_parser = setup_cli_arguments()  # Get the argparse parser
   # cli_parser.add_argument('--use-clang', action='store_true', help='Use Clang parser for C++ analysis')  # Add --use-clang flag

    while running:
        command_input = input("coba> ")
        try:
            cli_args_main = cli_parser.parse_args(command_input.split())  # Parse args in main loop
            use_clang_parser = cli_args_main.use_clang  # Get --use-clang flag value
            running = process_command(command_input, use_clang=use_clang_parser)  # Pass use_clang flag to process_command
        except SystemExit:  # Handle help messages etc.
            pass  # Let help messages print, then continue loop

    print("CodeSynth Engine CLI session ended.")
