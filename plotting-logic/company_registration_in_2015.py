"""
Company Registrations Analysis (2015)

This script:
- Loads company registration data from CSV
- Uses a strict ZIP-to-district mapping file
- Counts registrations by district for the year 2015
- Plots a bar chart of top districts (only districts found in the ZIP mapping)
"""

import csv
import re
from collections import Counter
import matplotlib.pyplot as plt

# === Constants ===
REGISTRATION_DATE = 'CompanyRegistrationdate_date'
ADDRESS = 'Registered_Office_Address'
YEAR_OF_INTEREST = '2015'
TOP_N_DISTRICTS = 15

ZIPCODE_FILE = '../data/zipcode.csv'
COMPANIES_FILE = '../data/calculation.csv'


# === Core Calculation ===
def calculate(company_data, zipcode_data, year=YEAR_OF_INTEREST):
    """
    Count company registrations per district based on ZIP code.
    Only counts registrations if ZIP code is found in the mapping.
    """
    # Step 1: Map ZIP codes → Districts
    zip_to_district = {
        row["ZipCode"].replace(" ", ""): row["District"].strip()
        for row in zipcode_data
        if row.get("ZipCode") and row.get("District")
    }

    district_counts = Counter()

    for company in company_data:
        registration_date = company.get(REGISTRATION_DATE, "")
        address = company.get(ADDRESS, "")

        # Only consider companies registered in the given year
        if not registration_date.startswith(year):
            continue

        # Extract 6 or 7-digit ZIP codes anywhere in the address
        zip_codes = re.findall(r"\b\d{6,7}\b", address)

        for zip_code in zip_codes:
            zip_clean = zip_code.replace(" ", "")
            if zip_clean in zip_to_district:
                district_counts[zip_to_district[zip_clean]] += 1
                break  # Count only one ZIP per company

    return district_counts


# === Data Loading ===
def load_csv_as_dicts(csv_file):
    """Load CSV into a list of dictionaries using DictReader."""
    with open(csv_file, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


# === Plotting ===
def plot_registrations_by_district(district_counts, top_n=TOP_N_DISTRICTS):
    """
    Plot a horizontal bar chart of number of registrations by district.
    Shows only top N districts for readability.
    """
    if not district_counts:
        print("No registrations found for the given year and ZIPs.")
        return

    sorted_districts = sorted(
        district_counts.items(), key=lambda x: x[1], reverse=True
    )

    top_districts = dict(sorted_districts[:top_n])
    districts = list(top_districts.keys())
    counts = list(top_districts.values())

    plt.figure(figsize=(10, 6))
    bars = plt.barh(districts[::-1], counts[::-1],
                    color='#4C72B0', edgecolor='black')
    plt.xlabel('Number of Registrations')
    plt.ylabel('District')
    plt.title(f'Company Registrations in {YEAR_OF_INTEREST} by District (Top {top_n})')

    # Add numeric labels on bars
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.5, bar.get_y() + bar.get_height() / 2,
                 f'{int(width)}', va='center')

    plt.tight_layout()
    plt.savefig('../plotting-images/registrations-2015-by-district.png')
    plt.show()


# === Executor ===
def execute():
    """Main function to load data, calculate counts, and plot."""
    zipcode_data = load_csv_as_dicts(ZIPCODE_FILE)
    company_data = load_csv_as_dicts(COMPANIES_FILE)

    district_counts = calculate(company_data, zipcode_data, year=YEAR_OF_INTEREST)
    print("District counts:", district_counts)  # Debug print to confirm results
    plot_registrations_by_district(district_counts, top_n=TOP_N_DISTRICTS)


if __name__ == "__main__":
    execute()




