from bs4 import BeautifulSoup
import requests

# Read the URL from ana_link.txt
with open("ana_link.txt", "r", encoding="utf-8") as file:
    url = file.read().strip()  # Strip to remove any extra spaces or newline characters

# Send a GET request to fetch the HTML content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the div with the class "list-area"
list_area_div = soup.find("div", class_="list-area")

# If the div is found, proceed to extract the data
if list_area_div:
    # Find all elements with the required attributes (data-matchtype and get the text)
    matches = list_area_div.find_all(attrs={"data-matchtype": True})

    # Open mac_verileri.txt to write the extracted data
    with open("mac_verileri.txt", "w", encoding="utf-8") as output_file:
        for match in matches:
            # Extract the required data attributes
            matchtype = match.get("data-matchtype")
            txt = match.get_text(" ", strip=True).replace(",", "")  # Remove commas
            
            # Replace "-" with "vs"
            txt = txt.replace("-", "vs")

            # Write them into the text file
            output_file.write(f'MatchType: "{matchtype}"\n')
            output_file.write(f'Text: "{txt}"\n')
            output_file.write("\n")  # Add a space between matches

    print("Data has been extracted and saved to mac_verileri.txt")
else:
    print("The specified div <div class='list-area'> was not found.")
