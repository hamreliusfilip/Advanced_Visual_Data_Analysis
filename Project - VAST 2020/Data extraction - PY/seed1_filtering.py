import csv
from tqdm import tqdm

file_path_data = 'Project - VAST 2020/Seed_Structure_data/output_total_seedOne.csv'
Graph_Data = 'Project - VAST 2020\Data\CGCS-GraphData.csv'
output_file_path = 'Project - VAST 2020/Seed_Structure_data/seed1_filtering.csv'


print("Extracting seed...")
seed_data_one = []

with open('Project - VAST 2020/Data/Q2-Seed1.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    for row in reader:
        seed_data_one.append(row)

def level1_doc(file_path, output_file_path):
    doc_total = []

    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        with open(output_file_path, 'w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerow(seed_data_one[0])

            for row in tqdm(reader, desc="Searching", unit="rows"):
                if row['eType'] == '4':  
                    doc_total.append(row)
                    writer.writerow(row)

    return doc_total


def search_with_doc(doc_total, Graph_Data, output_file_path):
    for row in doc_total:
        target = row['Target']
        print(f"Searching for {target}...")

        with open(Graph_Data, 'r') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter=',')
            with open(output_file_path, 'a', newline='') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

                for bigRow in tqdm(reader, desc="Searching", unit="rows"):
                    if bigRow['Target'] == target:
                        writer.writerow(bigRow)


print("Finding level 1...")

doc_total = level1_doc(file_path_data, output_file_path)

search_with_doc(doc_total, Graph_Data, output_file_path)

print(f"Matching rows have been written to {output_file_path}")