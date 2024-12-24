#It takes a link and then downloads the source of that link, puts it in input.html then parses that. If for some reason this doesnt work, just directly go to link's html source and then copy the source in a file named input.html. Then run the code. 

import os
import requests
from bs4 import BeautifulSoup

# Prompt user for a link
link = input("Please provide the URL: ")

# Fetch the HTML content from the provided link
try:
    response = requests.get(link)
    response.raise_for_status()  # Raise an exception for HTTP errors
    html_content = response.text

    # Save the HTML content to a file
    with open("input.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML content saved to input.html")

except Exception as e:
    print(f"Error fetching the URL: {e}")
    exit(1)

# Directory to save images
output_dir = "art_photos"
os.makedirs(output_dir, exist_ok=True)

# Parse the saved HTML file
soup = BeautifulSoup(html_content, "html.parser")

# Find all the `article` tags with class `product-grid-item`
articles = soup.find_all("article", class_="product-grid-item")

# Loop through each article to get the image and title
for article in articles:
    try:
        # Extract image URL
        img_tag = article.find("img")
        img_url = img_tag["src"] if img_tag else None

        # Extract title
        title_tag = article.find("h3", class_="entry-title product-title")
        title = title_tag.text.strip() if title_tag else "untitled"

        if img_url:
            # Download the image
            img_data = requests.get(img_url).content
            img_ext = os.path.splitext(img_url)[-1]  # Get file extension (e.g., .jpg)

            # Sanitize title for filename
            filename = "".join(c if c.isalnum() or c in " ._-" else "_" for c in title) + img_ext

            # Save the image
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(img_data)
            print(f"Downloaded: {filename}")
        else:
            print(f"No image found for title: {title}")

    except Exception as e:
        print(f"Error processing article: {e}")

print("Download complete.")
