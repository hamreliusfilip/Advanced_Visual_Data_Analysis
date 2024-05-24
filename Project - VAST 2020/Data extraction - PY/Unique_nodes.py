import csv
from tqdm import tqdm


file_path_data = 'Project - VAST 2020/Seed_Structure_data/output_total_seedOne.csv'
output_file_path = 'Project - VAST 2020/Seed_Structure_data/Filtered_seedOne_014.csv'

def search_with_seed(file_path, output_file_path):
    with open(file_path, 'r') as csvfile, open(output_file_path, 'w', newline='') as outfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()


        unique_nodes = []

        def unique_node(source, target):
            for node in unique_nodes:
                if row['Source'] == node['Source'] and row['Target'] == node['Target']:
                    return False
            return True
        
        # Use tqdm for the progress bar
        for row in tqdm(reader, desc="Searching", unit="rows"):
            if (row['eType'] == '0' or row['eType'] == '1' or row['eType'] == '4'):

                source = row['Source']
                target = row['Target']

                if (unique_node(source, target)):
                    writer.writerow(row)
                    unique_nodes.append(row)
                    # writer.writerow(row)

                unique_nodes.append(row)
                # writer.writerow(row)

print("Finding seed...")

# Step 2: Search for all rows with the matching seed and write them directly to the output file
search_with_seed(file_path_data, output_file_path)

print(f"Matching rows have been written to {output_file_path}")