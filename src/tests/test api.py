import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup

def find_power(reg):
    # URL of the website
    url = f"https://www.carcheck.co.uk/vauxhall/{reg}"

    # Define headers to mimic a typical web browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    try:
        # Initialize a session object with retries
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Send an HTTP GET request to the URL with headers
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Get the HTML content of the page
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all table rows
        table_rows = soup.find_all('tr')

        # Initialize dictionaries to store the extracted information
        info = {}

        # Loop through each table row and extract the data
        for row in table_rows:
            # Extract the table headers and table data
            header = row.find('th')
            data = row.find('td')
            if header and data:
                # Store the data in the dictionary
                info[header.text.strip()] = data.text.strip()

        # Extract specific details
        power = info.get('Power', 'Not found')
        max_torque = info.get('Max. torque', 'Not found')
        engine_capacity = info.get('Engine capacity', 'Not found')
        cylinders = info.get('Cylinders', 'Not found')
        fuel_type = info.get('Fuel type', 'Not found')

        # Print the extracted information
        print("Power:", power)
        print("Max. torque:", max_torque)
        print("Engine capacity:", engine_capacity)
        print("Cylinders:", cylinders)
        print("Fuel type:", fuel_type)

    except requests.RequestException as e:
        print("Error occurred during request:", e)

    except Exception as e:
        print("Error occurred:", e)

# Example usage
find_power("DL18JLO")