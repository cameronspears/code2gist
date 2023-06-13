import requests
import json
import os

def create_gist(description, files):
    url = "https://api.github.com/gists"
    headers = {
        "Authorization": "token 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",
        "Accept": "application/vnd.github.v3+json",
    }
    data = {
        "public": False,
        "description": description,
        "files": files
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_files_in_directory(directory):
    files = {}
    for root, dirnames, filenames in os.walk(directory):
        # Skip directories starting with .
        dirnames[:] = [d for d in dirnames if not d[0] == '.']
        
        for filename in filenames:
            # Skip files starting with . and files not ending with .py
            if filename.startswith('.') or not filename.endswith('.py'):
                continue

            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, directory)  # get relative path
            
            with open(path, 'r') as file:
                try:
                    files[rel_path] = {"content": file.read()}  # use relative path as key
                except UnicodeDecodeError:
                    print(f"Could not read file: {path}")
    return files

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    description = os.path.basename(directory)
    files = get_files_in_directory(directory)
    response = create_gist(description, files)
    print("\nFiles in Gist:")
    for filename, file_info in response['files'].items():
        print(f"\n- File: {filename}")
        print(f"  URL: {file_info['raw_url']}")
