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

    list = []

    folder_path = "file/"

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        all_files = get_all_relative_files(folder_path)

        with open("output.csv", "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["File", "Labels"])  # Header row

            for file in all_files:

                if not file[-4:] == ".pdf":
                    continue

                # dicts = {
                #     "file_path": folder_path + file,
                #     "extracted_text": PDFExtractor().extract_text(folder_path + file)
                # }

                print(folder_path + file)
                text_extraction = PDFExtractor().extract_text(folder_path + file)

                labels = Form().extract_labels(text_extraction)

                writer.writerow([file, ", ".join(labels)])
                # print("File: "+ file)
                # print(Form().extract_labels(text_extraction))
                # # list.append(dicts)

            

        print(len(list))
        # for i in list:
        #     print(i)

    else:
        print("Invalid folder path.")
