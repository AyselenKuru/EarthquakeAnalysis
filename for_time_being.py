import requests
import re
import numpy as np
import pyproj
def access_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to access the website. Status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
def extract_content_between_pre_tags(html_content):
    # Use regular expression to find the content between <pre> and </pre> tags
    pattern = r"<pre>(.*?)</pre>"
    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        # Extract the content found inside the <pre> tags
        extracted_content = match.group(1)

        # Save the content to a file
        with open("extracted_content.txt", "w", encoding="utf-8") as file:
            file.write(extracted_content)

        print("Content between <pre> tags extracted and saved to 'extracted_content.txt'.")
    else:
        print("No content found between <pre> tags.")
area_coordinates = [
    (41.490555, 27.957669),
    (41.069493, 32.077542),
    (39.840681, 26.243802),
    (40.462076, 31.660061)
]
earthquakes=[]
station_cordinates=(41.060521, 29.063384)
# Function to check if a given latitude and longitude are within the area of choice
def is_within_area(lat, lon):
    for (lat_min, lon_min), (lat_max, lon_max) in zip(area_coordinates, area_coordinates[1:]):
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            return True
    return False
def process_gps_data_txt():
    with open(r"C:\Users\Ice\PycharmProjects\pythonProject\extracted_content.txt",'r') as file:
        for line in file:
            if(line.startswith("2023")):
                line_sep= line.split()
                latitude = float(line_sep[2])
                longitude = float(line_sep[3])
                if( is_within_area(latitude,longitude)):
                    earthquakes.append(line_sep)

    desired_elements = []

    # Iterate through the list of lists and extract the desired elements (index 2 and 6)
    for sublist in earthquakes:
        desired_element1 = sublist[8]
        desired_element2 = sublist[6]
        desired_elements.append((desired_element1, desired_element2))
    with open(r"C:\Users\Ice\PycharmProjects\pythonProject\quakes.txt", 'a') as file:
        file.write("Number Of Quakes\t"+str(earthquakes.__len__())+"\t"+desired_elements.__str__()+"\n")



if __name__ == "__main__":
    website_url = "http://www.koeri.boun.edu.tr/scripts/lasteq.asp"
    html_cont = access_website(website_url)
    extract_content_between_pre_tags(html_cont)
    process_gps_data_txt()





