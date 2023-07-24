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



"""
import matplotlib.pyplot as plt
import geopandas as gpd
import cartopy.crs as ccrs

# Sample coordinates (latitude and longitude) of points in Turkey
turkey_coordinates = [
    (39.9334, 32.8597),  # Ankara
    (41.0082, 28.9784),  # Istanbul
    (38.4192, 27.1287),  # Izmir
]

# Load the world countries shapefile using Geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Filter the data to get only Turkey
turkey = world[world['name'] == 'Turkey']

# Get the bounding box of Turkey
turkey_bbox = turkey.total_bounds

# Create a Cartopy PlateCarree projection centered around Turkey
projection = ccrs.PlateCarree(central_longitude=(turkey_bbox[0] + turkey_bbox[2]) / 2)

# Create a figure and axis for the map
fig, ax = plt.subplots(subplot_kw={'projection': projection}, figsize=(10, 6))

# Add country borders to the map
ax.add_geometries(turkey['geometry'], crs=ccrs.PlateCarree(), edgecolor='black', facecolor='none', alpha=0.5)

# Plot each point in Turkey on the map
for lat, lon in turkey_coordinates:
    ax.plot(lon, lat, 'bo', markersize=8, transform=ccrs.PlateCarree())

# Add labels for each point (optional)
for i, (lat, lon) in enumerate(turkey_coordinates):
    plt.text(lon + 0.05, lat + 0.05, f'Point {i + 1}', transform=ccrs.PlateCarree())

# Set the title for the map
ax.set_title('Points in Turkey')

# Set the map extent to zoom in on Turkey
ax.set_extent([turkey_bbox[0], turkey_bbox[2], turkey_bbox[1], turkey_bbox[3]], crs=ccrs.PlateCarree())

# Show the map
plt.show()
"""





