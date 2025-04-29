import requests


def api(licenseplate):
    # Define the API endpoint URL
    url = 'https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles'

    # API key
    api_key = ''

    # Define the headers
    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/json'
    }

    # Define the payload (data to be sent)
    payload = {
        'registrationNumber': str(licenseplate)
    }

    # Send a POST request to the API endpoint
    response = requests.post(url, headers=headers, json=payload)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Print the response content (the vehicle information)
        print(response.json())
        return response.json(), response.status_code
    else:
        # Print an error message if the request failed

        print('Error:', response.text)
        return response.text, response.status_code
api('LC73DYS')