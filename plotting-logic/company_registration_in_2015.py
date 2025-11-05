"""
Optimized script to calculate and plot company registrations in 2015 by district.
Shows top districts and combines smaller ones into 'Other'.
"""

import csv
import matplotlib.pyplot as plt

REGISTRATION_DATE = 'CompanyRegistrationdate_date'
ADDRESS = 'Registered_Office_Address'
YEAR_OF_INTEREST = 2015
TOP_N_DISTRICTS = 15  

def count_registrations_by_district(companies_file):
    """Count number of companies registered in 2015 per district extracted from address."""
    district_counts = {}

    with open(companies_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for company in reader:
            try:
                year = int(company[REGISTRATION_DATE].split('-')[0])
            except (ValueError, KeyError):
                continue

            if year != YEAR_OF_INTEREST:
                continue

            address = company[ADDRESS].strip()
            parts = address.replace(',', ' ').split()
            if not parts:
                district = 'Unknown'
            else:
                district = parts[-2] if parts[-1].isdigit() and len(parts[-1]) == 6 else parts[-1]

            district_counts[district] = district_counts.get(district, 0) + 1

    return district_counts

def plot_registrations_by_district(district_counts):
    """Plot a horizontal bar chart of number of registrations by district, top N only."""
    # Sort districts by count
    sorted_districts = sorted(district_counts.items(), key=lambda x: x[1], reverse=True)
    top_districts = dict(sorted_districts[:TOP_N_DISTRICTS])
    other_count = sum(count for _, count in sorted_districts[TOP_N_DISTRICTS:])
    if other_count > 0:
        top_districts['Other'] = other_count

    districts = list(top_districts.keys())
    counts = list(top_districts.values())

    plt.figure(figsize=(12, 8))
    plt.barh(districts[::-1], counts[::-1], color='purple', edgecolor='black')  # reverse for descending
    plt.xlabel('Number of Companies')
    plt.ylabel('District')
    plt.title(f'Company Registrations in {YEAR_OF_INTEREST} by District (Top {TOP_N_DISTRICTS})')
    plt.tight_layout()
    plt.savefig('../plotting-images/registrations-2015-by-district.png')
    plt.show()

def execute(companies_file):
    district_counts = count_registrations_by_district(companies_file)
    plot_registrations_by_district(district_counts)

if __name__ == "__main__":
    COMPANIES_PATH = '../data/calculation.csv'
    execute(COMPANIES_PATH)

