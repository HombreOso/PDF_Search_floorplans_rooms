import os
import PyPDF2
import re

# Define the folder path where the PDF files are located
folder_path = "./Grundrisse/"

# Define the regular expression pattern
search_pattern_list = [r"WTE-2\D+", r"WTE-1\D+"]

# search_pattern = r"example \d+"

for search_pattern in search_pattern_list:

    # Compile the regular expression object
    regex = re.compile(search_pattern)

    # Loop through all the files in the folder
    for filename in os.listdir(folder_path):
        # Check if the file is a PDF file
        if filename.endswith(".pdf"):
            # Open the PDF file in read-binary mode
            with open(os.path.join(folder_path, filename), "rb") as f:
                # Create a PDF reader object
                reader = PyPDF2.PdfReader(f)

                # Loop through all the pages in the PDF file
                for page_num, page in enumerate(reader.pages):
                    # Extract the text from the page
                    text = page.extract_text()

                    # Search for matches using the regular expression object
                    matches = regex.findall(text)

                    # Check if any matches were found
                    if matches:
                        # Print the filename, page number, and matches where the search term was found
                        print(f"Found {len(matches)} matches in file '{filename}' on page {page_num + 1}:")
                        for match in matches:
                            print(f"  - {match}")
