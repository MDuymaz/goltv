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

# Find the div with the class "channel-area"
channel_area_div = soup.find("div", class_="channel-area")

# Open m3u_link.txt to write the extracted data
with open("m3u_link.txt", "w", encoding="utf-8") as output_file:
    
    # Function to extract and write data-seolink URLs
    def extract_and_write(div):
        if div:
            seolinks = div.find_all(attrs={"data-seolink": True})
            if seolinks:
                for link in seolinks:
                    seolink = link.get("data-seolink")
                    full_url = f"{base_url}{seolink}"
                    output_file.write(f"{full_url}\n")
            else:
                output_file.write("LINK BULUNAMADI\n")
        else:
            output_file.write("LINK BULUNAMADI\n")

    # Extract data from both divs
    extract_and_write(list_area_div)
    extract_and_write(channel_area_div)

print("Data has been extracted and saved to m3u_link.txt")
