from secedgar import FilingType, CompanyFilings
import datetime

def cik_lookup(search: str):
    return search

def filing_lookup(cik, filing_type = FilingType.FILING_SC13D, user_agent = "dat.pull@protonmail.com", count = 10):
    # https://sec-edgar.github.io/sec-edgar/filings.html#filing
    filings = CompanyFilings(cik_lookup,
        filing_type=filing_type,
        user_agent=user_agent, 
        start_date=None, 
        end_date=datetime.date(2022, 1, 2), 
        client=None, 
        count=count, 
        ownership='include', 
        match_format='ALL', **kwargs)
        
    return filings

def get_urls(filings):
    safe_urls = filings.get_urls_safely()
    return safe_urls

def save_filings(filings, dir = "/tmp"):
    filings.save(
        dir_pattern = "cik_{cik}/{type}",
        file_pattern = "{accession_number}"
    )
    return None



    

    

