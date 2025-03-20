from bs4 import BeautifulSoup
import requests

# Read the URL from ana_link.txt
with open("ana_link.txt", "r", encoding="utf-8") as file:
    base_url = file.read().strip()  # Read and strip any extra spaces or newlines

# Send a GET request to fetch the HTML content
response = requests.get(base_url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the div with the class "list-area"
list_area_div = soup.find("div", class_="list-area")

# If the div is found, proceed to extract the data
if list_area_div:
    # Find all elements with the "data-seolink" attribute
    seolinks = list_area_div.find_all(attrs={"data-seolink": True})

    # Open m3u_link.txt to write the extracted data
    with open("m3u_link.txt", "w", encoding="utf-8") as output_file:
        # Now write the full URL for each seolink data
        for link in seolinks:
            # Extract the "data-seolink" attribute value
            seolink = link.get("data-seolink")

            # Create the full URL by concatenating the base URL with the seolink
            full_url = f"{base_url}{seolink}"

            # Write the full URL into the text file
            output_file.write(f"{full_url}\n")

    print("Data has been extracted and saved to m3u_link.txt")
else:
    print("The specified div <div class='list-area'> was not found.")
