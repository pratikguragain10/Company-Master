± Company Master Project

± Project Overview

This repository contains Python scripts for analyzing and visualizing company registration data from the Ministry of Corporate Affairs (MCA) dataset.

± Key insights generated include:

- Total company registrations per year
- Registrations by district (e.g., in 2015)
- Histogram of authorized capital ranges
- Grouped bar plots of registrations by Principal Business Activity over the last 10 years

The scripts do not use heavy libraries like pandas or NumPy. Only Python’s built-in modules (`csv`, `collections`) and `matplotlib` for visualization.

All code is organized under `plotting-logic/`, raw data is in `data/`, and generated plots are saved in `plotting-images/`.


± Installation & Requirements

- Install Python 3.10+
- Install dependencies:

pip install -r requirements.txt


± How to Run

Run any script from the project root:

Example: run company registrations per year plot

python plotting-logic/registration_per_year.py
Replace registration_per_year.py with any other script in plotting-logic/.


± All scripts follow the same pattern:


load_...() – read & compute data directly from CSV

calculate_...() – optional, compute metrics (counts, aggregates)

plot_...() – generate visualization

execute() – orchestrates load/calculate + plot

Uses csv.DictReader for clean data handling

Descriptive variable names (no single-character names)

Minimal memory usage by performing computations directly in the CSV reading loop

Compatible with linters (flake8, pylint)


± Notes & Best Practices

.gitignore prevents tracking of large CSVs, generated plots, virtual environments, and IDE files

requirements.txt contains only the library actually used (matplotlib)

Code is ready for linting and follows best practices for readability and maintainability
