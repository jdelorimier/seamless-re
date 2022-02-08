from secedgar import FilingType, CompanyFilings, filings
import datetime

def cik_lookup(search):
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
        # match_format='ALL',
        )
        
    return filings.get_urls_safely()

def get_urls(filings):
    safe_urls = filings.get_urls_safely()
    return safe_urls

def save_filings(filings, dir = "/tmp"):
    filings.save(
        dir_pattern = "cik_{cik}/{type}",
        file_pattern = "{accession_number}"
    )
    return None

if __name__=="__main__":
    my_filings = filings(cik_lookup="tkc",
                     filing_type=FilingType.FILING_SC13D,
                     user_agent="dat.pull@protonmail.com")
    my_filings.save(
        dir_pattern = "/tmp/cik_{cik}/{type}",
        file_pattern = "{accession_number}"
    )



    

    

