## Restaurant Data Scraper
This repository contains two Python scripts, `scrapper2.py` and `dynamic_scrapper.py`, for scraping restaurant data from Google search results. Both scripts use Selenium and BeautifulSoup for extracting information, but they differ in terms of file-saving behavior.

### Features
- Scrapes restaurant names, ratings, number of reviews, addresses, and expense levels.
- Handles pagination for multi-page results.
- Dynamically removes unwanted special characters from addresses while retaining valid information.

### 1. scrapper2.py
#### Overview
`scrapper2.py` allows you to specify the output file where the scraped data will be saved. It dynamically fetches data from Google search results based on the specified region.

#### Usage
```bash
python scrapper2.py --region "Region Name" --output "output_file.csv"
```
Parameters:
- **Region**: Specify the location for which you want to scrape restaurant data.
- **Output File**: Provide the name of the file to save the results (e.g., `restaurants.csv`).

#### Key Features
- **Custom File Save**: Allows the user to specify the name of the output file.
- **Expense Level Parsing**: Determines expense levels (e.g., $, $$, etc.) from Google results.
- **Special Character Removal**: Cleans up addresses only if they contain unwanted characters like ·, numbers, or –.

#### Example
To scrape data for New York City and save it in `restaurants.csv`:
```bash
python scrapper2.py --region "New York City" --output "restaurants.csv"
```

#### File Output
The script saves the results in a user-specified CSV file with the following columns:
- **Name**: Name of the restaurant.
- **Rating**: Restaurant's rating (e.g., 4.5).
- **Reviews**: Number of reviews (e.g., 200).
- **Address**: Cleaned address of the restaurant.
- **Expense Level**: Cost level (e.g., Moderate Cost).

### 2. dynamic_scrapper.py
#### Overview
`dynamic_scrapper.py` simplifies the file-saving process by automatically creating a default output file. The user only needs to specify the region for scraping, and the data is saved in a pre-defined file.

#### Usage
```bash
python dynamic_scrapper.py --region "Region Name"
```
Parameters:
- **Region**: Specify the location for which you want to scrape restaurant data.

#### Key Features
- **Default File Save**: Automatically saves the results to a file named based on the region (e.g., `restaurants_Los_Angeles.csv`), eliminating the need for the user to specify an output file.
- **Expense Level Parsing**: Determines expense levels (e.g., $, $$, etc.) from Google results.
- **Special Character Removal**: Cleans up addresses only if they contain unwanted characters like ·, numbers, or –.

#### Example
To scrape data for Los Angeles:
```bash
python dynamic_scrapper.py --region "Los Angeles"
```

#### File Output
The script saves the results in a default CSV file with the following columns:
- **Name**: Name of the restaurant.
- **Rating**: Restaurant's rating (e.g., 4.5).
- **Reviews**: Number of reviews (e.g., 200).
- **Address**: Cleaned address of the restaurant.
- **Expense Level**: Cost level (e.g., Moderate Cost).

