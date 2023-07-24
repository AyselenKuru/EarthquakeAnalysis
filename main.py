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


def transform_coordinates(gps_data, source_crs, target_crs):
    # Step 3: Coordinate Reference System (CRS) Transformation
    # Transform GPS coordinates to a common reference frame (CRS)
    transformer = pyproj.Transformer.from_crs(source_crs, target_crs, always_xy=True)
    gps_data['latitude'], gps_data['longitude'] = transformer.transform(gps_data['latitude'].values,
                                                                        gps_data['longitude'].values)


def filter_gps_data(gps_data):
    # Step 4: Data Filtering and Quality Control
    # Apply filters to remove noise and outliers from the GPS data
    #TODO
    filtered_data = gps_data.copy()  # Replace with actual filtering techniques

    return filtered_data


def calculate_baseline(gps_data, reference_time):
    # Step 5: Baseline Estimation
    # Calculate the baseline position for each GPS station
    baseline = gps_data[gps_data['timestamp'] == reference_time][['latitude', 'longitude']].values
    gps_data['rel_latitude'] = gps_data['latitude'] - baseline[0, 0]
    gps_data['rel_longitude'] = gps_data['longitude'] - baseline[0, 1]


def calculate_horizontal_displacements(gps_data):
    # Step 6: Time Series Analysis
    # Compute the time series of relative horizontal displacements for each GPS station
    # The result would be a DataFrame with 'station_id', 'timestamp', 'horizontal_displacement' columns
    # Replace this with actual calculations based on your GPS data format
    # TODO
    horizontal_displacements = gps_data.copy()

    return horizontal_displacements


# Main data processing pipeline
def process_gps_data(raw_gps_data):
    # Step 1: Data Collection (already available as 'raw_gps_data')

    # Step 2: Data Preprocessing
    preprocessed_data = (raw_gps_data)

    # Step 3: Coordinate Reference System (CRS) Transformation
    source_crs = 'EPSG:4326'  # Assuming GPS data is in WGS84
    target_crs = 'EPSG:xxxx'  # Replace 'xxxx' with the target CRS code (e.g., local CRS)
    transform_coordinates(preprocessed_data, source_crs, target_crs)

    # Step 4: Data Filtering and Quality Control
    filtered_data = filter_gps_data(preprocessed_data)

    # Step 5: Baseline Estimation
    reference_time = 'yyyy-mm-dd'  # Replace with the reference time for baseline calculation
    calculate_baseline(filtered_data, reference_time)

    # Step 6: Time Series Analysis
    horizontal_displacements = calculate_horizontal_displacements(filtered_data)

    return horizontal_displacements


if __name__ == "__main__":
    website_url = "http://www.koeri.boun.edu.tr/scripts/lasteq.asp"
    html_cont = access_website(website_url)
    extract_content_between_pre_tags(html_cont)

    process_gps_data()




