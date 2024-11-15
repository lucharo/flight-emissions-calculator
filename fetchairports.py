import pandas as pd
import json

def fetch_and_filter_airports(url, output_file):
    # Fetch the airport data from the provided URL
    airports_df = pd.read_csv(url)
    
    # Load the ISO Country code to country name mapping from the provided file
    iso_country_df = pd.read_csv('iso.csv')
    iso_country_mapping = dict(zip(iso_country_df['alpha-2'], iso_country_df['name']))
    
    # Filter for only medium and large airports and create a copy
    filtered_airports_df = airports_df[airports_df['type'].isin(['large_airport', 'medium_airport'])].copy()

    
    # Map the 'iso_country' values in the filtered airport data to country names
    filtered_airports_df.loc[:, 'country'] = filtered_airports_df['iso_country'].map(iso_country_mapping)
    
    # Columns to keep
    columns_to_keep = ['ident', 'type', 'name', 'latitude_deg', 'longitude_deg', 'iso_country', 'country', 'municipality', 'iata_code']
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
    df_extracted = df[['name', 'municipality', 'country']].rename(columns={'municipality': 'city'})
    
    # Convert the DataFrame to the desired JSON format
    json_data = df_extracted.to_dict(orient='records')
    
    output_filepath = 'airportlookup.json'
    # Save the JSON data to a local file
    with open(output_filepath, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
    
    print(f"JSON data saved to {output_filepath}")

csv_to_json(output_file)

