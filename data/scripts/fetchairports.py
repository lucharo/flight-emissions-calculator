import pandas as pd
import json

def fetch_and_filter_airports(url, output_file):
    # Fetch the airport data from the provided URL
    airports_df = pd.read_csv(url)
    
    # Filter for only medium and large airports and create a copy
    filtered_airports_df = airports_df[airports_df['type'].isin(['large_airport', 'medium_airport'])].copy()
    
    # Use country name directly from the dataset
    filtered_airports_df['country'] = filtered_airports_df['iso_country']
    
    # Columns to keep
    columns_to_keep = ['name', 'latitude_deg', 'longitude_deg', 'country', 'municipality', 'iata_code']
    filtered_airports_df = filtered_airports_df[columns_to_keep]
    
    # Save the filtered data to the specified output CSV file
    filtered_airports_df.to_csv(output_file, index=False)
    print(f"Filtered data saved to {output_file}")


# URL for the airport data
url = "https://davidmegginson.github.io/ourairports-data/airports.csv"
output_file = "filtered_airports.csv"

# Call the function with the desired output file name
fetch_and_filter_airports(url, output_file)

def csv_to_json(filepath):
    # Read the CSV file
    df = pd.read_csv(filepath)
    
    # Extract necessary columns and rename them to match desired format
    df_extracted = df[['name', 'municipality', 'country', 'latitude_deg', 'longitude_deg', 'iata_code']].rename(
        columns={
            'municipality': 'city',
            'latitude_deg': 'latitude',
            'longitude_deg': 'longitude'
        }
    )
    
    # Drop rows with missing coordinates or IATA codes
    df_extracted = df_extracted.dropna(subset=['latitude', 'longitude', 'iata_code'])
    
    # Convert the DataFrame to the desired JSON format
    json_data = df_extracted.to_dict(orient='records')
    
    # Save directly to public/data directory
    import os
    os.makedirs('../../public/data', exist_ok=True)
    
    output_filepath = '../../public/data/airportlookup.json'
    # Save the JSON data to a local file
    with open(output_filepath, 'w') as json_file:
        json.dump(json_data, json_file, indent=2)
    
    print(f"JSON data saved to {output_filepath}")

# Convert the CSV to JSON
csv_to_json('filtered_airports.csv')
