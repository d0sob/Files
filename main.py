import json

with open('config.json') as f:
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
with open('links.txt', 'w') as outfile:
    for url in all_urls:
        outfile.write('https://venge.io/'+url + '\n')
