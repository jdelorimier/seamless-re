from sec_edgar_downloader import Downloader
import glob
from bs4 import BeautifulSoup
import re

def text_extract_13D(path):
    """
    This function strips Item 2. from SEC schedule 13D. This section reports on the Identity and Background of individuals with 
    controlling shares of a given organization.

    Inputs:
    - path: the path to a downloaded filing

    Output:
    - text (str): The extracted text from this section of the filing
    """
    with open(path, 'r') as infile:
        text = infile.read()
    soup = BeautifulSoup(text, features="lxml")
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    pattern = r"(?<=Identity and Background)(?s:.)*(?=Source and Amount of Funds)"
    match = re.search(pattern, text)
    output = match[0] if match else ""
    return output

def get_id_and_background(ticker, amount=1, filing_type="SC 13D",download_path="/tmp"):
    """
    input: 
    - ticker (str): The ticker code of a company (e.g. APPL)
    - amount (int): Amount of recent filings 
    - filing: MUST BE 13D FOR NOW
    - download_path: Storage of SEC Download (this does not have error handling)

    output:
    text_blobs (list): A list of text blobs of the given amount of filings. Some of these may be empty
    file_paths (list): paths to files
    """
    print("Collecting Data...")
    dl = Downloader(download_path)
    dl.get(filing_type, ticker, amount = amount)
    htmls = glob.glob(f"/tmp/sec-edgar-filings/{ticker}/{filing_type}/*/*.html")
    text_blobs = []
    for html in htmls:
        text_blobs.append(text_extract_13D(html))
    print("Data collection complete.")
    return text_blobs, htmls