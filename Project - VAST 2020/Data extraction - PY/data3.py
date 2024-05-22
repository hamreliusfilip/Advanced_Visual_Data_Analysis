import csv
from tqdm import tqdm

print("Extracting seed...")
seed_data_one = []

# Step 1: Read the seed data from Q2-Seed1.csv
with open('Project - VAST 2020/Data/Q2-Seed3.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_one.append(row)

# Ensure seed_source_id is a string for comparison
seed_source_id = str(seed_data_one[0]['Source'])

print("Seed Source ID:", seed_source_id)

file_path_data = 'Project - VAST 2020/Data/CGCS-GraphData.csv'
output_file_path = 'Project - VAST 2020/Seed_Structure_data/output_total_seedThree.csv'

def search_with_seed(file_path, seed, output_file_path):
    with open(file_path, 'r') as csvfile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        # Use tqdm for the progress bar
        for row in tqdm(reader, desc="Searching", unit="rows"):
            if ((row['Source'] == seed or row['Target'] == seed)):
                writer.writerow(row)

print("Finding seed...")

# Step 2: Search for all rows with the matching seed and write them directly to the output file
search_with_seed(file_path_data, seed_source_id, output_file_path)

print(f"Matching rows have been written to {output_file_path}")