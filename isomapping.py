from bs4 import BeautifulSoup
import csv
import requests
import pandas as pd

url = 'https://www.cia.gov/the-world-factbook/references/country-data-codes/'

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')

# Now you can use BeautifulSoup to parse and extract data from the page HTML

table = soup.find('table', {'class':'content-table'})

rows = []
for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    rows.append([ele.text.strip() for ele in cols])

df = pd.DataFrame([[r[0], r[2]] for r in rows], columns=['name', 'alpha-2'])
df['alpha-2'] = df['alpha-2'].apply(lambda x: x.split('|')[0].strip())

df = df[df['alpha-2'] != '-']

df.to_csv('iso.csv', index=False)