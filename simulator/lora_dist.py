import json
import pickle
from datetime import datetime

# Load civit_catalog.json
with open('cache/civit_catalog.json') as f:
    civit_catalog = json.load(f)

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")

# Create a dictionary to store LORA id and its downloadCount and size
lora_freq = {}
# end date is 2024-03-22
end_date = datetime.strptime("2024-03-30", "%Y-%m-%d")

for item in civit_catalog:
    if item['type'] == 'LORA':
        count = item['stats']['downloadCount']
        # Find the last item in the list of modelVersions
        if len(item['modelVersions']) == 0:
            continue
        oldest_version = item['modelVersions'][-1]
        published_date_str = oldest_version['publishedAt']
        if published_date_str is None:
            continue
        published_date = parse_date(published_date_str)
        time_diff = end_date - published_date
        freq = count / time_diff.days

        if len(item['modelVersions'][0]['files']) == 0:
            continue
        size = item['modelVersions'][0]['files'][0]['sizeKB']
        size_MB = size / 1024

        baseModel = item['modelVersions'][0]['baseModel']
        
        lora_freq[item['id']] = {'download_freq': freq, 'sizeMB': round(size_MB, 2), 'baseModel': baseModel}

# Sort the dictionary by downloadCount
lora_freq = dict(sorted(lora_freq.items(), key=lambda item: item[1]['download_freq'], reverse=True))

# Save the dictionary to lora_freq.json
with open('lora_freq.json', 'w') as f:
    json.dump(lora_freq, f, indent=4)

# Calculate the CDF
total_downloads = sum(item['download_freq'] for item in lora_freq.values())
cdf_list = []
cumulative_probability = 0
for item_id, data in lora_freq.items():
    cumulative_probability += data['download_freq'] / total_downloads
    cdf_list.append((cumulative_probability, (item_id, data['baseModel'])))

# with open('lora_cdf.json', 'w') as f:
#     json.dump(cdf_list, f, indent=4)

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