import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tkinter as tk
from tkinter import simpledialog

# Function to get the page content and return BeautifulSoup object
def get_page(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for invalid status codes
    return BeautifulSoup(response.text, 'html.parser')

# Function to extract the image URL from a 'viewimage' page
def get_image_link(viewimage_url):
    soup = get_page(viewimage_url)
    # Look for the image URL from the <img> tag with the class 'pure-img'
    img_tag = soup.find('img', class_='pure-img')
    if img_tag:
        img_url = img_tag.get('src')  # Get the image URL
        if '/image/' in img_url:  # Ensure the image URL contains '/image/'
            return img_url
    return None

# Function to crawl the pages and gather the image links
def crawl_images(base_url):
    current_page = base_url
    while current_page:
        print(f"Crawling page: {current_page}")
        soup = get_page(current_page)
        
        # Find all 'viewimage' links on the page
        viewimage_links = soup.find_all('a', href=True)
        
        image_links = []

        for link in viewimage_links:
            href = link['href']
            if 'viewimage' in href:  # Check if the link is to a 'viewimage' page
                # Use urljoin to correctly join the base URL with the relative link
                viewimage_url = urljoin(base_url, href)
                print(f"Visiting: {viewimage_url}")
                image_url = get_image_link(viewimage_url)  # Extract the image URL
                if image_url:
                    image_links.append(image_url)

        # Write the image links to a text file
        if image_links:
            with open('links.txt', 'a') as f:
                for link in image_links:
                    f.write(link + '\n')
        
        # Find the "Next" button to go to the next page
        next_page = soup.find('a', string='Next »')
        if next_page:
            next_page_url = next_page.get('href')
            current_page = urljoin(base_url, next_page_url)  # Build the next page URL
        else:
            print("No more pages to crawl.")
            break

# Function to show the pop-up dialog to get the URL
def get_url_from_user():
    # Set up the tkinter root window (it won't be shown)
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Ask the user to enter the URL using a pop-up dialog
    url = simpledialog.askstring("Enter URL", 
                                 "Please enter the URL in the format:\n\nhttps://www.listal.com/albumname/pictures\n", 
                                 parent=root)

    # Check if the URL is valid
    if url:
        return url
    else:
        print("No URL entered. Exiting...")
        exit()

if __name__ == '__main__':
    # Prompt the user for the URL via the pop-up
    base_url = get_url_from_user()

    # Start the crawling process with the user-provided URL
    crawl_images(base_url)
