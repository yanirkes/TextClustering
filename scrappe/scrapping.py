import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import os

# Get the current working directory
cur_dir = os.getcwd()


def remove_list_number_from_text(text):
    """
    Remove list numbers at the beginning of lines (e.g., '1. ', '12. ') in claim text.
    Useful for cleaning numbered lists in claims.
    """
    pattern = r'^\d+\.\s*'
    return re.sub(pattern, '', text, flags=re.MULTILINE)


def remove_claim_multi_referrals(text):
    """
    Replace multiple claim references such as 'claim 1 to 3' or 'claims 1, 2, or 3'
    with 'other claims'. This standardizes cross-references in claim texts.
    """
    patterns = [
        r'claims \d+\.? to \d+\.?',  # Matches ranges like 'claims 1 to 3'
        r'claims \d+\.? or \d+\.?',  # Matches alternatives like 'claims 1 or 2'
        r'claims \d+\.?, \d+\.? or \d+\.?',  # Matches lists like 'claims 1, 2, or 3'
        r'claim \d+\.? to \d+\.?',  # Matches single claim ranges like 'claim 1 to 3'
        r'claim \d+\.? or \d+\.?'  # Matches single claim alternatives like 'claim 1 or 2'
    ]

    for pattern in patterns:
        text = re.sub(pattern, 'other claims', text)
    return text


def remove_claim_referrals(text):
    """
    Replace individual claim references like 'claim 1' with a generic 'claim'.
    This removes specific claim numbers for generalization.
    """
    pattern = r'claim \d+\.?'
    return re.sub(pattern, 'claim', text)


def scrape_by_url(url_):
    """
    Scrape patent claims from the given URL and clean them.
    - Handles network errors and parsing issues.
    - Cleans each claim by removing list numbers and standardizing claim references.
    Returns a list of cleaned claims.
    """
    claims_lst = []

    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url_)
        response.raise_for_status()  # Raise an error for bad responses

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url_}: {e}")
        return claims_lst  # Return an empty list in case of errors

    # Parse the HTML response using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all divs with class 'claim'
    claim_divs = soup.find_all('div', class_='claim')

    if not claim_divs:
        print(f"No claims found for {url_}")
        return claims_lst

    # Loop through each 'claim' div and extract the text
    for claim in claim_divs:
        claim_text_div = claim.find('div', class_='claim-text')

        if claim_text_div:
            # Extract and clean the claim text
            claim_text = claim_text_div.get_text().strip()
            claim_text = remove_list_number_from_text(claim_text)
            claim_text = remove_claim_multi_referrals(claim_text)
            claim_text = remove_claim_referrals(claim_text)

            claims_lst.append(claim_text)
        else:
            print(f"Warning: 'claim-text' div not found in {url_}")

    return claims_lst


def save_claims_to_csv(claims, filename):
    """
    Save the scraped and cleaned claims into a CSV file.
    Creates the directory if it doesn't exist and handles any I/O errors.
    """
    group_data_path = os.path.join(cur_dir, 'Moveo', 'data', filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(group_data_path), exist_ok=True)

    # Convert the list of claims to a DataFrame and save it as a CSV file
    df = pd.DataFrame(claims, columns=['text'])

    try:
        df.to_csv(group_data_path, index=False)
        print(f"Claims saved to {group_data_path}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")


# List of patent URLs to scrape claims from
urls = [
    "https://patents.google.com/patent/GB2478972A/en?q=(phone)&oq=phone",
    "https://patents.google.com/patent/US9634864B2/en?oq=US9634864B2",
    "https://patents.google.com/patent/US9980046B2/en?oq=US9980046B2"
]

# Scrape claims from each URL and combine them into a single list
claims = []
for url in urls:
    claims += scrape_by_url(url)

# Save the scraped claims to a CSV file
filename = 'claims_text.csv'
save_claims_to_csv(claims, filename)
