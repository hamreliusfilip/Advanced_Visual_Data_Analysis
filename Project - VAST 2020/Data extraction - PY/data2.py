import csv
import networkx as nx
from tqdm import tqdm
from networkx.algorithms.similarity import graph_edit_distance

# Load seed data
def load_seed_data(file_path):
    seed_graph = nx.Graph()
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            source = row['Source']
            target = row['Target']
            weight = float(row['Weight']) if 'Weight' in row else 1.0
            seed_graph.add_edge(source, target, weight=weight)
    return seed_graph

# Load template graph
def load_template_graph(file_path):
    template_graph = nx.Graph()
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            source = row['Source']
            target = row['Target']
            weight = float(row['Weight']) if 'Weight' in row else 1.0
            template_graph.add_edge(source, target, weight=weight)
    return template_graph

# Function to match seed node
def match_seed_node(row, seed_nodes):
    source = row['Source']
    target = row['Target']
    return source in seed_nodes or target in seed_nodes

# Search for seed nodes in large dataset and expand to find subgraphs
def search_and_expand(file_path, seed_nodes, neighborhood_size):
    potential_subgraphs = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        graph = nx.Graph()
        for row in tqdm(reader):
            source = row['Source']
            target = row['Target']
            weight = float(row['Weight']) if 'Weight' in row else 1.0
            graph.add_edge(source, target, weight=weight)
            if source in seed_nodes or target in seed_nodes:
                neighbors = nx.single_source_shortest_path_length(graph, source, cutoff=neighborhood_size)
                subgraph_nodes = list(neighbors.keys())
                subgraph = graph.subgraph(subgraph_nodes)
                potential_subgraphs.append(subgraph)
    return potential_subgraphs

# Compare subgraphs to template graph
def find_best_match(potential_subgraphs, template_graph):
    best_match = None
    best_distance = float('inf')
    for subgraph in potential_subgraphs:
        distance = graph_edit_distance(subgraph, template_graph)
        if distance < best_distance:
            best_distance = distance
            best_match = subgraph
    return best_match

# Save the best matching subgraph
def save_best_match(subgraph, output_file):
    header = [
        "Source", "eType", "Target", "Time", "Weight",
        "SourceLocation", "TargetLocation", "SourceLatitude",
        "SourceLongitude", "TargetLatitude", "TargetLongitude"
    ]
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for u, v, data in subgraph.edges(data=True):
            row = [u, '', v, '', data['weight'], '', '', '', '', '', '']
            writer.writerow(row)

# Main function to load data, find matches, and save the best match
def main():
    seed_graph = load_seed_data('Data/Q2-Seed1.csv')
    seed_nodes = set(seed_graph.nodes())
    template_graph = load_template_graph('Data/CGCS-Template.csv')
    potential_subgraphs = search_and_expand('Data/CGCS-GraphData.csv', seed_nodes, neighborhood_size=2)
    best_match = find_best_match(potential_subgraphs, template_graph)
    if best_match:
        save_best_match(best_match, 'Seed_Structure_data/testtesttest.csv')
    else:
        print("No matching subgraph found")

if __name__ == "__main__":
    main()
