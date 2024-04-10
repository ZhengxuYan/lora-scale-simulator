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
lora_count = {}
# end date is 2024-03-22
end_date = datetime.strptime("2024-03-30", "%Y-%m-%d")

for item in civit_catalog:
    if item['type'] == 'LORA':
        count = item['stats']['downloadCount']
        # Find the last item in the list of modelVersions
        if len(item['modelVersions']) == 0:
            continue
        # oldest_version = item['modelVersions'][-1]
        # published_date_str = oldest_version['publishedAt']
        # if published_date_str is None:
        #     continue
        # published_date = parse_date(published_date_str)
        # time_diff = end_date - published_date

        if len(item['modelVersions'][0]['files']) == 0:
            continue
        size = item['modelVersions'][0]['files'][0]['sizeKB']
        size_MB = size / 1024

        baseModel = item['modelVersions'][0]['baseModel']
        
        lora_count[item['id']] = {'download_count': count, 'sizeMB': round(size_MB, 2), 'baseModel': baseModel}

# Sort the dictionary by downloadCount
lora_count = dict(sorted(lora_count.items(), key=lambda item: item[1]['download_count'], reverse=True))

# # Save the dictionary to lora_freq.json
# with open('lora_count.json', 'w') as f:
#     json.dump(lora_count, f, indent=4)

download_count = [item['download_count'] for item in lora_count.values()]
# Save the download count to lora_download_count.pdl
with open('lora_download_count.pkl', 'wb') as f:
    pickle.dump(download_count, f)

# Calculate the CDF
total_downloads = sum(item['download_count'] for item in lora_count.values())
cdf_list = []
cumulative_probability = 0
for item_id, data in lora_count.items():
    cumulative_probability += data['download_count'] / total_downloads
    cdf_list.append((cumulative_probability, (item_id, data['baseModel'])))

# Calculate the PDF
pdf_list = []
for item_id, data in lora_count.items():
    pdf_list.append((data['download_count'] / total_downloads, (item_id, data['baseModel'])))

# # Save the PDF model
# with open('lora_pdf_model.pkl', 'wb') as f:
#     pickle.dump(pdf_list, f)

# Save the CDF model
with open('lora_cdf_model.pkl', 'wb') as f:
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