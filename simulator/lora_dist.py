import json
import pickle

# Load civit_catalog.json
with open('cache/civit_catalog.json') as f:
    civit_catalog = json.load(f)

# Create a dictionary to store LORA id and its downloadCount and size
lora_freq = {}
for item in civit_catalog:
    if item['type'] == 'LORA':
        count = item['stats']['downloadCount']
        if len(item['modelVersions']) == 0:
            continue
        if len(item['modelVersions'][0]['files']) == 0:
            continue
        size = item['modelVersions'][0]['files'][0]['sizeKB']
        size_MB = size / 1024
        lora_freq[item['id']] = {'downloadCount': count, 'sizeMB': round(size_MB, 2)}

# Sort the dictionary by downloadCount
lora_freq = dict(sorted(lora_freq.items(), key=lambda item: item[1]['downloadCount'], reverse=True))

# Save the dictionary to lora_freq.json
with open('lora_freq.json', 'w') as f:
    json.dump(lora_freq, f, indent=4)

# Calculate the CDF
total_downloads = sum(item['downloadCount'] for item in lora_freq.values())
cdf_list = []
cumulative_probability = 0
for item_id, data in lora_freq.items():
    cumulative_probability += data['downloadCount'] / total_downloads
    cdf_list.append((cumulative_probability, item_id))

# Save the CDF model
with open('lora_dist_model.pkl', 'wb') as f:
    pickle.dump(cdf_list, f)


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