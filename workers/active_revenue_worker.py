
import requests
from requests.exceptions import HTTPError

def fetch_salesforce_data(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        exit(1)
    except Exception as err:
        print(f'An error occurred: {err}')
        exit(1)

def main():
    sf_instance_url = 'https://your-salesforce-instance.salesforce.com/services/data/v52.0'
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
        'Content-Type': 'application/json'
    }
    
    data = fetch_salesforce_data(sf_instance_url, headers)
    print(data)

if __name__ == "__main__":
    main()
exit(0)
