import csv
from tqdm import tqdm

Graph_Data = 'Project - VAST 2020/Data/CGCS-GraphData.csv'
output_file_path = 'Project - VAST 2020/Seed_Structure_data/SeedOne_2Levels_FilteredOn_FrequentEdges.csv'

def search_with_doc(sourceNodes, Graph_Data, output_file_path):
    for source in sourceNodes:

        print(f"Searching for {source}...")

        with open(Graph_Data, 'r') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter=',')
            with open(output_file_path, 'a', newline='') as outfile: 
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

                for bigRow in tqdm(reader, desc="Searching", unit="rows"):
                    # Convert bigRow['Source'] and bigRow['Target'] to integers for comparison
                    bigRow_source = int(bigRow['Source'])
                    bigRow_target = int(bigRow['Target'])
                    
                    if (bigRow_source == source and (bigRow_target in sourceNodes and bigRow_source in sourceNodes)):
                        writer.writerow(bigRow)

                    elif (bigRow_target == source and (bigRow_target in sourceNodes and bigRow_source in sourceNodes)):
                        writer.writerow(bigRow)


print("Finding level 1...")

sourceNodes = [600971, 554368, 612711, 604199, 523586, 622306, 584502, 506539, 587163, 564804, 522924]
test = [600971, 554368]

search_with_doc(sourceNodes, Graph_Data, output_file_path)

print(f"Matching rows have been written to {output_file_path}")
