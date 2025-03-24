import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

BASE_URL = "http://35.200.185.69:8000/v1/autocomplete"
DELAY = 0.5  

extracted_names = set()
api_call_count = 0  

def query_api(query, retries=3):
    global api_call_count
    url = f"{BASE_URL}?query={query}" 
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            api_call_count += 1 

            if response.status_code == 200:
                data = response.json()
                logging.info(f"Response for query '{query}': {data}")
                return data
            elif response.status_code in {429, 503}:
                logging.warning(f"Rate limited or unavailable (status: {response.status_code}). Sleeping...")
                time.sleep(DELAY * (attempt + 1))
            else:
                logging.error(f"Unexpected status code {response.status_code} for query: {query}")
                break
        except requests.RequestException as e:
            logging.error(f"Request error for query '{query}': {e}")
            time.sleep(DELAY * (attempt + 1))
    
    return None

def dfs(query_prefix, depth=0, max_depth=10):
    if depth > max_depth:
        return

    logging.info(f"Querying with prefix: '{query_prefix}'")
    response_data = query_api(query_prefix)
    if response_data is None:
        logging.warning(f"No response data for prefix: '{query_prefix}'")
        return

    names = response_data.get("results", [])
    logging.info(f"Received {len(names)} results for prefix '{query_prefix}': {names}")

    for name in names:
        if name.lower().startswith(query_prefix.lower()):
            if name not in extracted_names:
                extracted_names.add(name)
                logging.info(f"Found name: {name} (prefix: '{query_prefix}')")
    
    if response_data.get("count", 0) == 10:
        for char in "abcdefghijklmnopqrstuvwxyz0123456789#&+-.":
            new_prefix = query_prefix + char
            dfs(new_prefix, depth=depth+1, max_depth=max_depth)
            time.sleep(DELAY)

def main():
    for char in "abcdefghijklmnopqrstuvwxyz":
        dfs(char, depth=1, max_depth=10)
    
    logging.info(f"Total unique names extracted: {len(extracted_names)}")
    logging.info(f"Total API calls made: {api_call_count}")  

    with open("extracted_names_new_v1_last.txt", "w") as f:
        for name in sorted(extracted_names):
            f.write(name + "\n")

if __name__ == "__main__":
    main()
