
import requests
from requests.exceptions import RequestException

def fetch_salesforce_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Request failed: {e}")
        exit(1)

def main():
    url = "https://your-salesforce-b2b-cloud-endpoint.com/api/data"
    data = fetch_salesforce_data(url)
    # Process the fetched data here
    print("Data fetched successfully")
    exit(0)

if __name__ == "__main__":
    main()
