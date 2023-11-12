# Celebrity Deaths Scraper

## Overview

This Python script, `celebrity_deaths_scraper.py`, automates the process of scraping and compiling a list of celebrity deaths from USA Today's website. It fetches data for each year from 2018 to the current year and outputs the results into a CSV file named `celebrity_deaths.csv`.

This data can then be used to test the knowledge of LLMs.

## Installation

To run this script, you will need Python 3 and the following packages:

- `requests`
- `beautifulsoup4`
- `pandas`

You can install these packages using pip:

```bash
pip install requests beautifulsoup4 pandas
```

## Usage

Run the script using Python from the command line:

```bash
python celebrity_deaths_scraper.py
```

After successful execution, the script will create a `celebrity_deaths.csv` file in the same directory, containing the names, birthdates, and death dates of celebrities.

## Contributing

Contributions to this project are welcome! If you have a suggestion for improving the script or have found a bug, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

## Disclaimer

This script is intended for educational purposes only. Please ensure you have permission to scrape data from websites and adhere to the terms of service of the website.
