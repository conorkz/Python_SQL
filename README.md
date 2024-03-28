# Data Extractor and Database Loader

## Overview

This Python script extracts structured data from text files and stores the information into a PostgreSQL database. It leverages **BeautifulSoup** (or an alternative HTML/XML parsing library) for web scraping capabilities, enabling the extraction of critical data from websites.

## Features

- Processes a directory of `.txt` files, extracting specific fields (*Link, Title, Author*, etc.).
- Parses summary text using flexible keywords.
- Creates a PostgreSQL table (if it doesn't exist).
- Inserts extracted data into the database using **psycopg2**.

## Prerequisites

- Python 3.x
- PostgreSQL database installed and running
- `psycopg2` library (`pip install psycopg2`)
- **BeautifulSoup** or another HTML/XML parsing library (`pip install beautifulsoup4`)

## How to Use

1. **Configure Database Settings:** In the `db_params` dictionary, provide your PostgreSQL database name, username, password, host, and port.

2. **Set Input Directory:** Modify the `input_directory` variable to the path where your `.txt` files are located.

3. **Run the Script:** Execute the script from the command line:

    ```bash
    python data_extractor.py
    ```

## Data Format

The script assumes your `.txt` files contain data in a key-value format separated by a colon (e.g., "Title: The Hitchhiker's Guide to the Galaxy"). Keywords are used to identify the start of the summary text section.

## Customization

- Adjust the `keys_to_extract` list to modify which fields are extracted.
- Change the summary section keywords for different text file structures.
- Explore using **BeautifulSoup** or another HTML/XML parser if you need to extract data from web sources.

## Dependencies

- `psycopg2`
- **BeautifulSoup** (or other suitable HTML/XML parsing library)
