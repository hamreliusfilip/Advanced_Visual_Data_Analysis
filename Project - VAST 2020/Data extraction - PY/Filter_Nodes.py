import csv
from tqdm import tqdm

def load_seed_data(file_path):
    seed_data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            seed_data.append(row)
    return seed_data

def match_node(row, seed):
    if row['eType'] not in {'0', '1', '4'}:
        return False
    return row['Target'] == seed['Source']

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

    unique_nodes = list(dict.fromkeys(all_nodes))

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for idx, row in unique_nodes:
            writer.writerow(list(row.values()))


if __name__ == "__main__":

    print("Extracting seeds...")
    seed_data_one = load_seed_data('Project - VAST 2020/Data/Q2-Seed1.csv')


    file_path_data = 'Project - VAST 2020/Data/CGCS-GraphData.csv'


    print("Finding seed...")
    found_seeds = {"Seed 1": search_nodes(file_path_data, seed_data_one, depth=1)}

)
    print("Finding structure...")
    found_nodes_level_1 = search_nodes(file_path_data, seed_data_one, depth=1)
    found_nodes_level_2 = search_nodes(file_path_data, [row for _, row in found_nodes_level_1], depth=1)


    all_found_nodes = found_nodes_level_1 + found_nodes_level_2


    print("Saving all nodes...")
    output_file = 'Project - VAST 2020/Seed_Structure_data/seed_one_multiple_levels_filtered.csv'
    save_all_found_structure(found_seeds, all_found_nodes, output_file)
