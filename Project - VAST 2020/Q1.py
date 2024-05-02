import networkx as nx
import matplotlib.pyplot as plt
import csv
import matplotlib.patches as mpatches

G = nx.DiGraph()

file_path = 'Data/CGCS-Template.csv'

with open(file_path, 'r') as csvfile:
    
    reader = csv.DictReader(csvfile, delimiter=',')
    column_names = reader.fieldnames
    next(reader)
    
    for row in reader:
        source = row['Source']
        target = row['Target']
        edge_type = row['eType']
        G.add_edge(source, target, type=edge_type)

edge_colors = {
    '0': 'red',
    '1': 'blue',
    '2': 'green',
    '3': 'yellow',
    '4': 'orange',
    # '5': 'purple', -> This channel creates many edges that do not represent person-to-person connections 
    # in the same way as the other channels. 
    '6': 'brown',
}

# pos = nx.spring_layout(G)
pos = nx.circular_layout(G)


nx.draw_networkx_nodes(G, pos, node_color='blue', node_size=50)

edge_labels = {edge_type: f'Type {edge_type}' for edge_type in edge_colors}

legend_handles = []

for edge_type, color in edge_colors.items():
    edges_of_type = [(u, v) for u, v, d in G.edges(data=True) if d['type'] == edge_type]
    nx.draw_networkx_edges(G, pos, edgelist=edges_of_type, edge_color=color)
    legend_handles.append(mpatches.Patch(color=color, label=edge_labels[edge_type]))

nx.draw_networkx_labels(G, pos)

plt.title('CGCS-Template')
plt.legend(handles=legend_handles, title='Edge Types', loc='upper left')
plt.show()
