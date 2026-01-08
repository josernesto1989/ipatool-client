# print(exec("ipatool search --limit 1 instagram"))
#./ipatool download -i 310633997
#./ipatool download -i 'com.burbn.instagram'
#./ipatool purchase -b 'com.burbn.instagram'
import subprocess
import re
import json

ANSI_ESCAPE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
IPATOOL_PATH = "./ipatool"

def clean_ansi(text):
    """Removes ANSI escape sequences from a string."""
    return ANSI_ESCAPE.sub('', text)

def find_app_by_name(name):
    
    # Define the command to execute
    command = [IPATOOL_PATH, "search", "--limit", "10", name]

    # Execute the command and capture the output
    # capture_output=True, text=True are correct.
    result = subprocess.run(command, capture_output=True, text=True, check=False) 

    stdout_output = result.stdout
    stderr_output = result.stderr

    # --- Robust JSON Extraction ---



    data = stdout_output.split('=')[1] if len(stdout_output.split('=')) > 1 else None
    data = clean_ansi(data) if data else None
    data = data[:-5] if len(data)>5 else data  # Remove last 5 characters if data is long enough

    print("--- Initial Extraction Attempt ---")
    print("JSON Data (Initial Attempt):", data)

    start_index = data.find('[')
    end_index = data.rfind(']')
    print(f"Start index: {start_index}, End index: {end_index}")

    print(f"Data before slicing: {(data)}")
    # Check if both start and end delimiters were found
    if start_index != -1 and end_index != -1 and start_index < end_index:
        # Slice the string to include the JSON array, from '[' to ']' inclusive
        data = data[start_index : end_index + 1].strip()
    else:
        data = None
    # ------------------------------

    print("--- Extracted Data Attempt ---")
    print("JSON Data (Slice Attempt):", data)
    json_data = None
    if data:
        try:
            json_data = json.loads(data)
            print("\n--- Successful JSON Decode ---")
            print(json.dumps(json_data, indent=4))  # Pretty-print the JSON data
        except json.JSONDecodeError as e:
            print("\n--- JSON Decode FAILED ---")
            print(f"Error: {e}")
            # Print the problematic data to see what the decoder received
            print("Problematic string:", repr(data))
    else:
        print("\n--- JSON Decode FAILED ---")
        print("Could not find start/end brackets for JSON extraction.")


    print("\n--- Full Output ---")
    print("Standard Output:")
    print(stdout_output.strip()) # strip for cleaner display
    print("\nStandard Error:")
    print(stderr_output.strip())
    return json_data

# find_app_by_name( "instagram")

def download_app_by_id(app_id,callback=None):
    command = [IPATOOL_PATH, "purchase", "-b", str(app_id)]  
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    stdout_output = result.stdout
    stderr_output = result.stderr
    print("\n--- Download Output ---")
    print("Standard Output:")
    print(stdout_output.strip())
    print("\nStandard Error:")
    print(stderr_output.strip())
    command = [IPATOOL_PATH, "download", "-b", str(app_id)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)

    stdout_output = result.stdout
    stderr_output = result.stderr

    print("\n--- Download Output ---")
    output = stdout_output.strip().split('\n')[-1]
    error = stderr_output.strip().split('\n')[-1]
    print("Standard Output:")
    print(output)
    print("\nStandard Error:")
    print(error)
    return [output,error]

def authenticate_user(username, password):
    command = [IPATOOL_PATH, "auth", "login", "-e", username, "-p", password]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    stdout_output = result.stdout
    stderr_output = result.stderr
    return stdout_output, stderr_output