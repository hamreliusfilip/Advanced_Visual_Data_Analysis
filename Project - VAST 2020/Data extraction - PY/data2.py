import csv
from tqdm import tqdm  # Import tqdm

# ------------------------ Seed one ------------------------:
print("Extracting seed...")
seed_data_one = []

with open('Data/Q2-Seed1.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_one.append(row)

# ------------------------ Seed two ------------------------

seed_data_two = []

with open('Data/Q2-Seed2.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_two.append(row)

# ------------------------ Seed three ------------------------

seed_data_three = []

with open('Data/Q2-Seed3.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_three.append(row)

# ------------------------ Search for seed ------------------------

# file_path_data = 'Data/test.csv'
file_path_data = 'Data/CGCS-GraphData.csv'

def match_seed(row, seed):
    for key, value in seed.items():
        if row[key] != value:
            return False
    return True

def search_seeds(file_path, seeds):
    found_seeds = {f"Seed {i+1}": [] for i in range(len(seeds))}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        progress_bar = tqdm(reader, total=123000000)
        for idx, row in enumerate(progress_bar, start=2):
            for i, seed in enumerate(seeds):
                if match_seed(row, seed):
                    found_seeds[f"Seed {i+1}"].append((idx, row))
                    progress_bar.close()  
                    return found_seeds 
    return found_seeds


print("Finding seed...")
found_seeds = search_seeds(file_path_data, seed_data_one)

for seed, data in found_seeds.items():
    print(seed)
    for idx, row in data:
        print(f"Row {idx}: {row}")
        
        
# ------------------------ Find connecting nodes to seed ------------------------

# file_path_data = 'Data/test.csv'
file_path_data = 'Data/CGCS-GraphData.csv'

def match_Node(row, seed):
    return row['Source'] == seed['Target'] or row['Target'] == seed['Source']

def search_Nodes(file_path, seeds):
    found_nodes = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(tqdm(reader, total=123000000), start=2):
            for seed in seeds:
                if match_Node(row, seed):
                    found_nodes.append((idx, row))
                    break  
    return found_nodes

print("Finding structure...")
found_nodes = search_Nodes(file_path_data, seed_data_one)

def save_all_found_structure(found_seeds, found_nodes, output_file):
    header = [
        "Source", "eType", "Target", "Time", "Weight",
        "SourceLocation", "TargetLocation", "SourceLatitude",
        "SourceLongitude", "TargetLatitude", "TargetLongitude"
    ]

    all_nodes = []

    for seed, data in found_seeds.items():
        all_nodes.extend(data)
    
    all_nodes.extend(found_nodes)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for idx, row in all_nodes:
            writer.writerow(list(row.values()))

print("Saving all nodes...")
output_file = 'Seed_Structure_data/testtesttest.csv'
save_all_found_structure(found_seeds, found_nodes, output_file)
