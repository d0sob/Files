import json
import os
import requests

fileJson = "config.json"
file2write = 'random.txt'
download_directory = "thisIsTheGameFilesFolder"
with open(fileJson) as f:
    data = json.load(f)
def find_urls(obj):
    urls = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == 'url':
                urls.append(value)
            elif isinstance(value, (dict, list)):
                urls.extend(find_urls(value))
    elif isinstance(obj, list):
        for item in obj:
            urls.extend(find_urls(item))
    return urls
all_urls = find_urls(data)
with open(file2write, 'w') as outfile:
    for url in all_urls:
        outfile.write('https://venge.io/'+url + '\n')

link_to_move = "https://venge.io/__game-scripts.js\n"
with open(file2write, "r") as f:
    content = f.readlines()

content = [line for line in content if line != link_to_move]
content.append(link_to_move)

with open(file2write,"w") as f:
    f.writelines(content)

print("Game links updated Succesfully!")

if not os.path.exists(download_directory):
    os.makedirs(download_directory)

with open(file2write, "r") as f:
    urls = f.readlines()

for url in urls:
    url = url.strip()  
    if url:  
        try:
            url_path = url.split("://")[1] 
            path_parts = url_path.split("/")[1:]  
            
            file_name = path_parts[-1]
            directory_path = os.path.join(download_directory, *path_parts[:-1])
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
            file_path = os.path.join(directory_path, file_name)
            response = requests.get(url)
            response.raise_for_status()  
            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"Downloaded and saved: {file_path}")
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {url}: {e}")

print("All downloads completed!")
