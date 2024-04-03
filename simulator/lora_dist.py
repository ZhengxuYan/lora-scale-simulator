import json

# Load civit_catalog.json
with open('cache/civit_catalog.json') as f:
    civit_catalog = json.load(f)

# Create a dictionary to store LORA id and its downloadCount and size
lora_dist = {}
for item in civit_catalog:
    if item['type'] == 'LORA':
        count = item['stats']['downloadCount']
        if len(item['modelVersions']) == 0:
            continue
        if len(item['modelVersions'][0]['files']) == 0:
            continue
        size = item['modelVersions'][0]['files'][0]['sizeKB']
        size_MB = size / 1024
        lora_dist[item['id']] = {'downloadCount': count, 'sizeMB': round(size_MB, 2)}

# Sort the dictionary by downloadCount
lora_dist = dict(sorted(lora_dist.items(), key=lambda item: item[1]['downloadCount'], reverse=True))

# Save the dictionary to lora_dist.json
with open('lora_dist.json', 'w') as f:
    json.dump(lora_dist, f, indent=4)


# # lora_info dictionary
# lora_info = {}
# for item in civit_catalog:
#     if item['type'] == 'LORA':
#         lora_info[item['id']] = item

# # Sort the dictionary by downloadCount
# lora_info = dict(sorted(lora_info.items(), key=lambda item: item[1]['stats']['downloadCount'], reverse=True))

# # Save the dictionary to lora_info.json
# with open('lora_info.json', 'w') as f:
#     json.dump(lora_info, f, indent=4)