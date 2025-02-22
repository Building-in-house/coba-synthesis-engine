import os

def load_cpp_project(project_path):
    cpp_files = []
    header_files = []
    other_files = []

    for root, _, files in os.walk(project_path):
        for file in files:
            filepath = os.path.join(root, file)
            if file.endswith(('.cpp', '.cxx', '.c')):
                cpp_files.append(filepath)
            elif file.endswith(('.h', '.hpp', '.hxx', '.hh')):
                header_files.append(filepath)
            else:
                other_files.append(filepath)

    print(f"  Detected C++ Source Files: {len(cpp_files)}")
    print(f"  Detected C++ Header Files: {len(header_files)}")
    print(f"  Other Files: {len(other_files)}")

    return cpp_files, header_files, other_files

# You can add similar loader functions for other languages (Python, JavaScript) here later

def load_project(project_path, language):
    project_path = os.path.abspath(project_path)
    if not os.path.isdir(project_path):
        print(f"Error: '{project_path}' is not a valid directory.")
        return None, None, None  # Indicate error

    print(f"Loading project from: {project_path}")

    if language == 'cpp':
        return load_cpp_project(project_path)
    elif language == 'python':
        print("Python project loading not yet implemented.")
        return [], [], [] # Placeholder
    elif language == 'javascript':
        print("JavaScript project loading not yet implemented.")
        return [], [], [] # Placeholder
    else:
        print("No language specified or invalid language.")
        return [], [], [] # Placeholder
