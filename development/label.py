import csv
import os

from form import Form
from text_extraction.PDF import PDFExtractor

def get_all_relative_files(folder_path):
    file_list = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, folder_path)
            file_list.append(relative_path)
    
    return file_list

# Example usage
if __name__ == "__main__":

    folder_path = "file/"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        all_files = get_all_relative_files(folder_path)

        with open("output2.csv", "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["File", "Extracted Label", "Actual Label", "Accuracy(%)"])  # Header row

            for file in all_files:
                if not file.lower().endswith(".pdf"):
                    continue

                print(folder_path + file)
                text_extraction = PDFExtractor().extract_text(folder_path + file)
                no_newline_text_extraction = "\n".join([line for line in text_extraction.splitlines() if line.strip()])

                labels = Form().extract_labels(text_extraction)
                formatted_labels = "\n".join(labels)  # Format labels to be readable

                writer.writerow([file, formatted_labels, "", ""])

        print("Process completed.")

    else:
        print("Invalid folder path.")
