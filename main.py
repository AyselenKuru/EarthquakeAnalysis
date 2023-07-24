import requests
import re
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



website_url = "http://www.koeri.boun.edu.tr/scripts/lst6.asp"
html_cont =access_website(website_url)
extract_content_between_pre_tags(html_cont)


