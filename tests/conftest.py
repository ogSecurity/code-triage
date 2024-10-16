import csv


def read_csv_as_dict(filepath):
    """Helper function to read a CSV file and return it as a list of dicts."""
    with open(filepath, 'r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

