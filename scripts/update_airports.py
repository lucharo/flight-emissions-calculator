#!/usr/bin/env python3
import json
import csv
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass
import requests
import click
from loguru import logger
import pycountry

# Major international hubs - top 20 by passenger traffic (2021 data)
# Source: https://aci.aero/2022/07/25/final-data-released-top-20-busiest-airports-confirmed/
MAJOR_HUBS = {
    "ATL": 75_704_760,  # Atlanta
    "DFW": 62_465_756,  # Dallas/Fort Worth
    "DEN": 58_828_552,  # Denver
    "ORD": 54_020_399,  # Chicago O'Hare
    "LAX": 48_007_284,  # Los Angeles
    "CLT": 43_302_230,  # Charlotte
    "MCO": 40_351_068,  # Orlando
    "CAN": 40_259_401,  # Guangzhou
    "LAS": 39_754_366,  # Las Vegas
    "PHX": 38_834_677,  # Phoenix
    "MIA": 37_701_292,  # Miami
    "IST": 37_178_828,  # Istanbul
    "SZX": 36_510_807,  # Shenzhen
    "HND": 35_897_187,  # Tokyo Haneda
    "PVG": 32_910_447,  # Shanghai Pudong
    "IAH": 32_903_444,  # Houston
    "LHR": 32_820_865,  # London Heathrow
    "DEL": 37_140_000,  # Delhi
    "CDG": 32_362_306,  # Paris Charles de Gaulle
    "AMS": 31_588_031,  # Amsterdam
}

def calculate_airport_score(airport):
    """
    Calculate a popularity score for an airport based on various factors.
    Higher score = more popular/important
    """
    score = 0
    
    # Base score for having IATA code
    if airport.get('iata_code'):
        score += 10
        
        # Bonus for being a major hub
        if airport['iata_code'] in MAJOR_HUBS:
            score += 100 + (MAJOR_HUBS[airport['iata_code']] / 1_000_000)
    
    # Bonus for international airports
    if 'international' in airport.get('name', '').lower():
        score += 30
    
    # Bonus for capital cities
    try:
        country = pycountry.countries.get(alpha_2=airport.get('iso_country'))
        if country and airport['city'].lower() in country.name.lower():
            score += 20
    except:
        pass
    
    # Penalty for small/regional airports
    if any(term in airport.get('name', '').lower() for term in ['regional', 'municipal', 'general']):
        score -= 10
    
    return score

@dataclass
class Airport:
    name: str
    city: str
    country: str
    iata_code: str
    latitude: float
    longitude: float

    @classmethod
    def from_openflights(cls, fields: List[str]) -> 'Airport':
        return cls(
            name=fields[1],
            city=fields[2],
            country=fields[3],
            iata_code=fields[4],
            latitude=float(fields[6]),
            longitude=float(fields[7])
        )

    @classmethod
    def from_ourairports(cls, row: Dict[str, str]) -> 'Airport':
        return cls(
            name=row['name'],
            city=row.get('municipality', row['name'].split()[0]),
            country=pycountry.countries.get(alpha_2=row['iso_country']).name,
            iata_code=row['iata_code'],
            latitude=float(row['latitude_deg']),
            longitude=float(row['longitude_deg'])
        )

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "iata_code": self.iata_code,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

class AirportDataManager:
    URLS = {
        'openflights': 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat',
        'ourairports': 'https://raw.githubusercontent.com/davidmegginson/ourairports-data/main/airports.csv'
    }

    def __init__(self):
        self.airports: Dict[str, Airport] = {}

    def fetch_data(self, url: str) -> str:
        logger.info(f"Downloading data from {url}")
        return requests.get(url).text

    def process_openflights(self, data: str) -> None:
        count = 0
        for line in data.split('\n'):
            try:
                if not line: continue
                fields = [f.strip('"') for f in line.split(',')]
                if len(fields) < 7: continue
                iata = fields[4]
                if not iata or iata == '\\N' or len(iata) != 3: continue
                
                self.airports[iata] = Airport.from_openflights(fields)
                count += 1
            except Exception as e:
                logger.warning(f"Error parsing line: {line}. Error: {e}")
        logger.success(f"Processed {count} airports from OpenFlights")

    def process_ourairports(self, data: str) -> None:
        count = 0
        for row in csv.DictReader(data.splitlines()):
            try:
                if row.get('type') != 'large_airport': continue
                iata = row.get('iata_code', '')
                if not iata or len(iata) != 3: continue
                
                self.airports[iata] = Airport.from_ourairports(row)
                count += 1
            except Exception as e:
                logger.warning(f"Error parsing row: {row}. Error: {e}")
        logger.success(f"Processed {count} airports from OurAirports")

    def get_filtered_airports(self) -> List[Dict]:
        logger.info("Filtering and sorting airports")
        filtered = [
            airport.to_dict() for airport in self.airports.values()
            if 'international' in airport.name.lower() or 'airport' in airport.name.lower()
        ]
        for airport in filtered:
            airport['popularity_score'] = calculate_airport_score(airport)
        filtered.sort(key=lambda x: (-x['popularity_score'], x['city']))
        logger.success(f"Final airport count: {len(filtered)}")
        return filtered

    def process(self) -> List[Dict]:
        for source, url in self.URLS.items():
            data = self.fetch_data(url)
            if source == 'openflights':
                self.process_openflights(data)
            else:
                self.process_ourairports(data)
        return self.get_filtered_airports()

def setup_logger(verbose: bool):
    logger.remove()
    log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    logger.add(lambda msg: click.echo(msg, err=True), format=log_format, level="DEBUG" if verbose else "INFO", colorize=True)

def handle_output(airports: List[Dict], output: Path, dry_run: bool, preview_limit: int = 50):
    if dry_run:
        logger.info(f"\nDRY RUN - Would write {len(airports)} airports to {output}")
        preview = json.dumps(airports[:preview_limit], indent=2, ensure_ascii=False)
        click.echo(f"\nPreview of first {preview_limit} airports:\n{preview}")
        return

    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        backup = output.with_suffix('.backup.json')
        output.rename(backup)
        logger.info(f"Created backup at {backup}")

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(airports, f, indent=2, ensure_ascii=False)
    logger.success(f"Successfully wrote {len(airports)} airports to {output}")

@click.command()
@click.option('--dry-run', is_flag=True, help='Show what would be done without writing files')
@click.option('--output', '-o', default='public/data/airports.json', help='Output file path')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--preview-limit', '-l', default=50, help='Number of airports to preview in dry run')
def main(dry_run: bool, output: str, verbose: bool, preview_limit: int):
    """Update airport data from OpenFlights and OurAirports databases."""
    setup_logger(verbose)
    try:
        airports = AirportDataManager().process()
        handle_output(airports, Path(output), dry_run, preview_limit)
    except Exception as e:
        logger.error(f"Error updating airports: {e}")
        raise click.Abort()

if __name__ == '__main__':
    main()
