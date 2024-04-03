import json
import powerlaw
import numpy as np

file_path = 'simulator\lora_freq.json'

with open(file_path, 'r') as file:
    data = json.load(file)

download_counts = [details['downloadCount'] for details in data.values()]


download_counts = np.array(download_counts) 

results = powerlaw.Fit(download_counts) # fit a power law distribution


alpha = results.power_law.alpha ## get alpha (the parameter)
print(f"Alpha for powerlaw: {alpha}")


R, p = results.distribution_compare('power_law', 'exponential')
print(f"Loglikelihood ratio (R) comparing power law and exponential distributions: {R}, p-value: {p}")