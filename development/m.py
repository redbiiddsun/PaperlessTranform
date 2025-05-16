import csv
import re
from difflib import SequenceMatcher

# Function to calculate text accuracy
def word_accuracy(actual_text, extracted_text):
    actual_words = re.findall(r'\w+', actual_text.lower())
    extracted_words = re.findall(r'\w+', extracted_text.lower())
    matcher = SequenceMatcher(None, actual_words, extracted_words)
    accuracy = matcher.ratio() * 100
    return accuracy

# Read CSV and process each row
input_file = 'input.csv'  # Change to your CSV file path
output_file = 'output_with_accuracy.csv'

with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

    # Add accuracy column
    for row in rows:
        extracted_text = row['Extracted Text'] if row['Extracted Text'] else ''
        actual_text = row['Actual Text'] if row['Actual Text'] else ''

        if extracted_text and actual_text:
            row['Evaluation'] = f'{word_accuracy(actual_text, extracted_text):.2f}%'  # Calculate accuracy
        else:
            row['Evaluation'] = 'N/A'  # If missing data

# Write updated CSV
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = list(rows[0].keys())
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f'Results saved to {output_file}')
