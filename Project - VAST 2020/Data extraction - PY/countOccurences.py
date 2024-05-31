import pandas as pd

def search_seeds(file_path_data, output_file_path):

    df = pd.read_csv(file_path_data)
 
    entity_counts = pd.concat([df['Source'], df['Target']]).value_counts()

    frequent_entities = entity_counts[entity_counts > 2].index.tolist()

    frequent_entities_df = pd.DataFrame(frequent_entities, columns=['Entity'])
    
    frequent_entities_df.to_csv(output_file_path, index=False)

file_path_data = 'Project - VAST 2020\Seed_Structure_data\Filtered_seedOne_014.csv'
output_file_path = 'Project - VAST 2020\Seed_Structure_data\Frequent_entities_of_seed_one.csv'

search_seeds(file_path_data, output_file_path)

print(f"Entities occurring more than 2 times have been written to {output_file_path}")
