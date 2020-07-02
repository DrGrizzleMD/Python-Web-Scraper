'''
Sample Web Scraper in Python3

This program will look at the top 1000 rated movies on IMDB and
we will take the top 50 of them.

'''

import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as numpy

# Ensures that the movie titles scraped are in English Language
headers = {"Accept-Language": "en-US, en;q=0.5"}

# URL we are looking at
url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"

# Method to grab the contents of the URL
results = requests.get(url, headers=headers)

# Variable created to assign method BeatifulSoup to.
# This allows Python to read the components of the page rather than treating it as one long string.
soup = BeautifulSoup(results.text, "html.parser")


# Variables to store info we want
titles = []
years = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

# Find_all method extracts all div containers that have a class attribute of "lister-item mode-advanced"
# from what we have stored in variable "soup"
movie_div = soup.find_all('div', class_ = 'lister-item mode-advanced')

# Iterates through every div container we stored in move_div
for container in movie_div:

    # Name
    name = container.h3.a.text
    titles.append(name)

    #Year
    year = container.h3.find('span', class_ = 'lister-item-year').text
    years.append(year)

    #Time
    runtime = container.find('span', class_ = 'runtime').text if container.p.find('span', class_ = 'runtime') else '-'
    time.append(runtime)

    # IMDB rating
    imdb = float(container.strong.text)
    imdb_ratings.append(imdb)

    # Metascore
    m_score = container.find('span', class_ = 'metascore').text if container.find('span', class_ = 'metascore') else '-'
    metascores.append(m_score)

    # Two nv containers, grabbing both as they hold votes and grosses
    nv = container.find_all('span', attrs = {'name': 'nv'})

    # Filter nv for votes
    vote = nv[0].text
    votes.append(vote)

    # Filter nv for gross
    grosses = nv[1].text if len(nv) > 1 else '-'
    us_gross.append(grosses)


movies_df = pd.DataFrame({
    'movie': titles,
    'year': years,
    'timeMin': time,
    'imdb': imdb_ratings,
    'metascore': metascores,
    'votes': votes,
    'us_grossMillions': us_gross,})



#########################
### Cleaning our data ###
#########################

# Extract all digits in the string and convert to int
movies_df['year'] = movies_df['year'].str.extract('(\d+)').astype(int)

# Extract all digits in the string and convert to int
movies_df['timeMin'] = movies_df['timeMin'].str.extract('(\d+)').astype(int)

# Convert to int
movies_df['metascore'] = movies_df['metascore'].astype(int)

# Replaces commas with nothing and convert to int
movies_df['votes'] = movies_df['votes'].str.replace(',', '').astype(int)

# Removes the '$' and 'M' characters. Also converts to float
movies_df['us_grossMillions'] = movies_df['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies_df['us_grossMillions'] = pd.to_numeric(movies_df['us_grossMillions'], errors = 'coerce')

print(movies_df)
print(movies_df.dtypes)