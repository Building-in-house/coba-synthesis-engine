import argparse
import os

def setup_cli_arguments():
    parser = argparse.ArgumentParser(prog='coba', description="CodeSynth Engine CLI")
    parser.add_argument('--use-clang', action='store_true', help='Use Clang parser for C++ analysis') # ADD --use-clang flag here at the top level
    subparsers = parser.add_subparsers(title='commands', dest='command')

    # `load_language` command
    load_language_parser = subparsers.add_parser('load_language', help='Specify the programming language')
    load_language_parser.add_argument('language', choices=['cpp', 'python', 'javascript'], help='Programming language (cpp, python, javascript)')

    # `load_project` command
    load_project_parser = subparsers.add_parser('load_project', help='Load a project from a given path and categorize files (does not analyze)')
    load_project_parser.add_argument('path', type=str, help='Path to the project directory')

    # `analyze` command (new command)
    analyze_parser = subparsers.add_parser('analyze', help='Parse and analyze the currently loaded project')
    # No need to add --use-clang to subparsers, it's a top-level argument

    # 'help' command
    help_parser = subparsers.add_parser('help', help='Show help messages for commands')

    # 'exit' or 'quit' command
    exit_parser = subparsers.add_parser('exit', help='Exit the interactive CLI')
    quit_parser = subparsers.add_parser('quit', help='Exit the interactive CLI')

    return parser

def parse_interactive_command(command_line_args):
    parser = setup_cli_arguments()

    print(f"DEBUG (cli.py): command_line_args: {command_line_args}") # Debug print

    if not command_line_args:
        return parser.parse_args([])

    try:
        args = parser.parse_args(command_line_args)
        print(f"DEBUG (cli.py): Parsed args: {args}") # Debug print of parsed args
        return args
    except SystemExit as e:
        if e.code == 0:
            return parser.parse_args(['help'])
        else:
            print(f"Error parsing command: {' '.join(command_line_args)}. Type 'help' for usage.")
            return argparse.Namespace(command=None)


if __name__ == '__main__':
    print("This is the cli module. Run 'main.py' to start the interactive CLI.")
