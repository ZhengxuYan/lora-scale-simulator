import json
import pickle
from datetime import datetime

# Load civit_catalog.json
with open('cache/civit_catalog.json') as f:
    civit_catalog = json.load(f)

lora_image_count = {}

for item in civit_catalog:
    if item['type'] == 'LORA':
        if len(item['modelVersions']) == 0:
            continue
        most_recent_version = item['modelVersions'][0]
        # print(most_recent_version.keys())
        # Check if the images key exists
        if 'images' not in most_recent_version.keys():
            continue
        most_recent_image_count = len(most_recent_version['images'])
        # Add the image counts for all versions
        sum_image_count = 0
        for version in item['modelVersions']:
            version_image_count = len(version['images'])
            sum_image_count += version_image_count
        lora_image_count[item['id']] = {'most_recent_image_count': most_recent_image_count, 'sum_image_count': sum_image_count}

# Sort the dictionary by most_recent_image_count
lora_image_count = dict(sorted(lora_image_count.items(), key=lambda item: item[1]['sum_image_count'], reverse=True))

# Save the dictionary to lora_image_count.json
with open('lora_image_count.json', 'w') as f:
    json.dump(lora_image_count, f, indent=4)

# Save the sum_image_count list to lora_image_count.pkl
sum_image_count = [item[1]['sum_image_count'] for item in lora_image_count.items()]

with open('lora_image_count.pkl', 'wb') as f:
    pickle.dump(sum_image_count, f)