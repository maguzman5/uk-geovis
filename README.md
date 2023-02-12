# Data Analysis about UK Electricity Consumption

This repo contains an analysis of UK Open Data about Electricity Consumption per year, and also analized by location using the Post code information from

- [UK Open Data](https://www.data.gov.uk/dataset/e7d4c1cf-45a0-4070-878f-24ad9641f655/domestic-electricity-and-gas-estimates-by-postcode-in-great-britain)

## Scraping

The scraping of the UK Open Data is done using the following libraries

- *requests*
- *BeautifulSoup4*
- *Pandas*

To execute the scraping use the code `execute_scraper.py` (this requires to have a folder named `data` in the main directory)

## Data Processing

Using the data extracted, the objectives are:

- Load the data and extract the coordinates for the postal codes
- Using GeoJSON from UK districts, assign to each district the mean of kwh consumption
- Analyze the data obtained

Then, from this point, it will be developed a map visualization

The code for the processing is in `notebooks/data_processing.ipynb`

## Visualization

TODO

## Sources

- [UK Open Data](https://www.data.gov.uk/dataset/e7d4c1cf-45a0-4070-878f-24ad9641f655/domestic-electricity-and-gas-estimates-by-postcode-in-great-britain)
- [UK GeoJSON](https://martinjc.github.io/UK-GeoJSON/)
- [UK Postcodes API](https://postcodes.io/)

