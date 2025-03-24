# API Data Extraction Report

## Overview
This project is designed to extract names from the API endpoint `http://35.200.185.69:8000/v1/autocomplete` using a recursive depth-first search (DFS) approach. The script explores possible prefixes to maximize the number of extracted names while handling API rate limits efficiently.

## Approach
1. **Recursive DFS Search:**
   - The script starts with single-character queries (a-z) and recursively appends characters (`abcdefghijklmnopqrstuvwxyz0123456789#&+-.`) to find all possible names.
   - If a query returns the maximum allowed results (10), it assumes more names exist and explores deeper.
   
2. **Rate Limit Handling:**
   - The script detects `429 (Too Many Requests)` and `503 (Service Unavailable)` responses and applies an exponential backoff strategy.
   - It retries the request with incremental delays.

3. **Tracking API Calls and Extracted Data:**
   - The script maintains a counter for API calls.
   - Extracted names are stored in a set to ensure uniqueness.
   - The final list of names is written to a file.


## Findings
- Total API calls for v1 were significantly more than v2 and v3.
- The pattern observed was that v1 did not had any numbers in the unique names and the max number of unique names obtained through a query was 10.
- For v1 and v2, the max number of unique names obtained through a query was 12.
- Querying deeper levels with non-alphabetic characters helped discover more names.
- API rate limits were encountered frequently, requiring retries with increasing delays.

## Metrics
- **Total API calls made for v1:** `520`
- **Total API calls made for v2:** `26`
- **Total API calls made for v3:** `26`

- **Total unique names extracted:** `18631`
- **Total unique names extracted:** `312`
- **Total unique names extracted:** `390`

## Usage
1. Activate a python virtual environment and install requests.
2. Run the script using:
   ```sh
   python script.py
   ```
3. The extracted names will be saved in `extracted_names_v1.txt`.


