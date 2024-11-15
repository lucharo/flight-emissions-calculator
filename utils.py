import json

def get_suggestions(query):
    with open('airportlookup.json', 'r') as file:
        data = json.load(file)

    matching_entries = []
    query = query.lower()

    for entry in data:
        name = str(entry.get("name", "")).lower()
        city = str(entry.get("city", "")).lower()
        country = str(entry.get("country", "")).lower()

        if query in name or query in city or query in country:
            matching_entries.append(entry)

    return matching_entries[:5]  # Return top 5 matches
