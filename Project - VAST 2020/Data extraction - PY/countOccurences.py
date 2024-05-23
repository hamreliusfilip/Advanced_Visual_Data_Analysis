import pandas as pd

def search_seeds(file_path_data, output_file_path):
    # Read the CSV file
    df = pd.read_csv(file_path_data)
    
    # Combine Source and Target columns to count occurrences of each entity
    entity_counts = pd.concat([df['Source'], df['Target']]).value_counts()
    
    # Filter entities that occur more than 2 times
    frequent_entities = entity_counts[entity_counts > 2].index.tolist()
    
    # Create a new DataFrame with these entities
    frequent_entities_df = pd.DataFrame(frequent_entities, columns=['Entity'])
    
    # Write the DataFrame to a new CSV file
    frequent_entities_df.to_csv(output_file_path, index=False)

# Define the file paths
file_path_data = 'Project - VAST 2020\Seed_Structure_data\Filtered_seedOne_014.csv'
output_file_path = 'Project - VAST 2020\Seed_Structure_data\Frequent_entities_of_seed_one.csv'

# Search for seeds and write them to a new CSV file
search_seeds(file_path_data, output_file_path)

print(f"Entities occurring more than 2 times have been written to {output_file_path}")
