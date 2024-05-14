
import csv

# ------------------------ Seed one ------------------------: 
print("Extracting seed...")
seed_data_one = []

with open('Project - VAST 2020/Data/Q2-Seed1.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_one.append(row)

# ------------------------ Seed two ------------------------

seed_data_two = []

with open('Project - VAST 2020/Data/Q2-Seed2.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_two.append(row)

# ------------------------ Seed three ------------------------

seed_data_three = []

with open('Project - VAST 2020/Data/Q2-Seed3.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_three.append(row)

# ------------------------ Search for seed ------------------------

file_path_data = 'Project - VAST 2020/Data/test.csv'

def match_seed(row, seed):
    for key, value in seed.items():
        if row[key] != value:
            return False
    return True

def search_seeds(file_path, seeds):
    found_seeds = {f"Seed {i+1}": [] for i in range(len(seeds))}
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader, start=2):
            for i, seed in enumerate(seeds):
                if match_seed(row, seed):
                    found_seeds[f"Seed {i+1}"].append((idx, row))
                    break  
    return found_seeds

print("Finding seed...")
found_seeds = search_seeds(file_path_data, seed_data_one)

# for seed, data in found_seeds.items():
#     print(seed)
#     for idx, row in data:
#         print(f"Row {idx}: {row}")
        
        
# ------------------------ Find connecting nodes to seed ------------------------

# file_path_data = 'Project - VAST 2020/Data/test.csv'
file_path_data = 'Project - VAST 2020/Data/CGCS-GraphData.csv'

def find_connected_nodes(seed, all_nodes):
    connected_nodes = set()
    for node in all_nodes:
        if node['Source'] == seed['Target']:
            connected_nodes.add(node['Target'])
        elif node['Target'] == seed['Source']:
            connected_nodes.add(node['Source'])
    return connected_nodes

def search_connected_nodes(seed, all_nodes, levels=2):
    connected_nodes = find_connected_nodes(seed, all_nodes)
    if levels == 1:
        return connected_nodes
    else:
        further_connected_nodes = set()
        for connected_node in connected_nodes:
            further_connected_nodes.update(search_connected_nodes({'Source': connected_node, 'Target': None}, all_nodes, levels - 1))
        return further_connected_nodes.union(connected_nodes)

def search_Nodes(file_path, seeds):
    found_nodes = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        all_nodes = [row for row in reader]
        for seed in seeds:
            connected_nodes = search_connected_nodes(seed, all_nodes)
            for node in all_nodes:
                if node['Source'] in connected_nodes or node['Target'] in connected_nodes:
                    found_nodes.append((idx, row))
    return found_nodes

print("Finding structure...")
found_nodes = search_Nodes(file_path_data, seed_data_one)

# for idx, row in found_nodes:
#     print(f"Row {idx}: {row}")

        
# ------------------------ Save seed to CSV ------------------------

def save_found_structure(found_seeds, found_nodes, output_file):
    header = [
        "Source", "eType", "Target", "Time", "Weight",
        "SourceLocation", "TargetLocation", "SourceLatitude",
        "SourceLongitude", "TargetLatitude", "TargetLongitude"
    ]
    
    unique_nodes = {}
    
    for seed, data in found_seeds.items():
        for idx, row in data:
            node_id = row['Source'] if row['Source'] else row['Target']
            if node_id not in unique_nodes or int(row['Time']) < int(unique_nodes[node_id]['Time']):
                unique_nodes[node_id] = row
    
    for idx, row in found_nodes:
        node_id = row['Source'] if row['Source'] else row['Target']
        if node_id not in unique_nodes or int(row['Time']) < int(unique_nodes[node_id]['Time']):
            unique_nodes[node_id] = row
    
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for node in unique_nodes.values():
            writer.writerow(list(node.values()))

print("Saving structure...")
output_file = 'output_structure_seed_one_two_levels_deep.csv'
save_found_structure(found_seeds, found_nodes, output_file)
