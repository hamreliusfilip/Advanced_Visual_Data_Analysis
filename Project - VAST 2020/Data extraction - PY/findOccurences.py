import csv
from tqdm import tqdm

Graph_Data = 'Project - VAST 2020/Data/CGCS-GraphData.csv'
output_file_path = 'Project - VAST 2020/Seed_Structure_data/seedThreeBuyerTimeCONTROLTEST.csv'

def search_with_doc(sourceNodesSeedThree, Graph_Data, output_file_path, time_array):
    
    for target in TargetNodes:

        print(f"Searching for {target}...")

        with open(Graph_Data, 'r') as csvfile: 
            reader = csv.DictReader(csvfile, delimiter=',')
            with open(output_file_path, 'a', newline='') as outfile: 
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)

                for bigRow in tqdm(reader, desc="Searching", unit="rows"):
                 
                    bigRow_source = int(bigRow['Source'])
                    bigRow_target = int(bigRow['Target'])
                    bigRow_eType = int(bigRow['eType'])
                    bigRow_Time = int(bigRow['Time'])
                    
                    if ((bigRow_eType == 3) and (bigRow_target == target) and bigRow_Time in time_array):
                        writer.writerow(bigRow)


print("Finding level 1...")

# sourceNodes = [600971, 554368, 612711, 604199, 523586, 622306, 584502, 506539, 587163, 564804, 522924]
# test = [600971, 554368]
time = [25335385, 20252446, 6176935, 23266820, 11864168, 13742325, 19715214, 1581741, 22639500, 28359367, 29900754, 8729723, 24032911, 1991785, 6742286, 22839875, 812170, 4514441, 18318465, 24862946, 14695842, 5012296, 19360132, 7520632, 12216731, 9945315, 14696645, 21094222, 7393039, 28180334, 29900330, 29814652, 10568671, 18679619, 29203976, 15686347, 10892451, 12974449, 23039457, 30777789, 12963282, 1837105, 20910605, 30351616, 12115190, 20921572, 3740049, 26972005, 3921030, 1994798, 30247051]

TargetNodes = [516389, 657187, 593195]

search_with_doc(TargetNodes, Graph_Data, output_file_path, time)

print(f"Matching rows have been written to {output_file_path}")
