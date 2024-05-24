import csv
from tqdm import tqdm

# Function to load seed data from a file
def load_seed_data(file_path):
    seed_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            seed_data.append(row)
    return seed_data

# Function to match nodes with the eType check
def match_node(row, seed):
    if row['eType'] not in {'0', '1', '4'}:
        return False
    return row['Target'] == seed['Source']

# Function to search nodes efficiently
def search_nodes(file_path, seeds, depth=2):
    found_nodes = []
    next_seeds = seeds

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        progress_bar = tqdm(reader, total=123000000)
        for idx, row in enumerate(progress_bar, start=2):
            for seed in next_seeds:
                if match_node(row, seed):
                    found_nodes.append((idx, row))
                    break

    return found_nodes

# Function to save all found structure to a file
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

    # Remove duplicates while preserving order
    unique_nodes = list(dict.fromkeys(all_nodes))

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for idx, row in unique_nodes:
            writer.writerow(list(row.values()))

# Main script
if __name__ == "__main__":
    # Load seed data
    print("Extracting seeds...")
    seed_data_one = load_seed_data('Project - VAST 2020/Data/Q2-Seed1.csv')

    # Define the file path for the main data
    file_path_data = 'Project - VAST 2020/Data/CGCS-GraphData.csv'

    # Find seeds in the main data
    print("Finding seed...")
    found_seeds = {"Seed 1": search_nodes(file_path_data, seed_data_one, depth=1)}

    # Find nodes connected to the found seeds (two levels deep)
    print("Finding structure...")
    found_nodes_level_1 = search_nodes(file_path_data, seed_data_one, depth=1)
    found_nodes_level_2 = search_nodes(file_path_data, [row for _, row in found_nodes_level_1], depth=1)

    # Combine all found nodes
    all_found_nodes = found_nodes_level_1 + found_nodes_level_2

    # Save all found structure
    print("Saving all nodes...")
    output_file = 'Project - VAST 2020/Seed_Structure_data/seed_one_multiple_levels_filtered.csv'
    save_all_found_structure(found_seeds, all_found_nodes, output_file)
