import json

def output_json_report(data, filepath="analysis_report.json"):
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"\nJSON report saved to: {filepath}")
    except Exception as e:
        print(f"Error writing JSON report to {filepath}: {e}")

def print_function_calls_console(function_calls):
    if function_calls:
        print("\nExtracted Function Calls:")
        for call in function_calls:
            print(f"  - File: {call['file']}, Line: {call['line']}, Callee: {call['callee_function']}")
    else:
        print("\nNo function calls found.")
