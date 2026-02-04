import csv
import duckdb
from bs4 import BeautifulSoup
import yake


def main():
    """
    Contains main logic, establishes connection with DuckDB database, retrieves and organizes relevant data,
    cleaning as necessary, then writes to csv file
    
    For reference, DuckDB job tuple indices mapped to fieldname:  
    
    last_updated [0], legal [1], dlt_load_id [2], dlt_id [3], slug [4], id [5], epoch [6],
    date [7], company [8], company_logo [9], position [10], description [11], location [12],
    apply_url [13], salary_min [14], salary_max [15], logo [16], url [17], original [18],
    verified [19]

    DuckDB tags tuple indices mapped to fieldname:
    value [0], _dlt_parent_id [1], _dlt_list_idx [2], _dlt_id[3]
    """
    filename = 'remoteok_cleaned_data.csv'
    cleaned_data = [['job_id', 'company', 'position', 'location', 'url', 'description', 'tags']]    
    con = duckdb.connect('fv/remoteok_loader.duckdb')
    con.sql("use job_listings")
    jobs_tuples = con.execute("SELECT * FROM remoteok_jobs").fetchall() # fetches job
    tags_tuples = con.execute("SELECT value, _dlt_parent_id FROM remoteok_jobs__tags").fetchall() # fetches tags
    
    
    for job in jobs_tuples[1:]: # iterates through list of job tuples
        cleaned_data_row = [job[5], job[8], job[10], job[12], job[17]]  # id, company, position, location, url added to data row first
        
        desc = job[11]
        if desc is not None: # cleans and adds description to data row
            cleaned_desc = desc_cleaner(desc)
            cleaned_data_row.append(cleaned_desc) # adds cleaned description to data row
        
        dlt_id = job[3]
        tags = []
        if dlt_id is not None: # retrieves current tags from database
            for tag in tags_tuples: # iterates through tags tuples
                if tag[1] == dlt_id: # appends tags that match the current job's dlt ID
                    tags.append(tag[0])
        tags = tags + (tag_extractor(cleaned_desc)) # combines current tags with extracted tags
        cleaned_data_row.append(tags) # appends tags list to cleaned data row
        cleaned_data.append(cleaned_data_row) # appends new row to cleaned data list
    with open(filename, 'w', newline='', encoding='utf-8') as cleaned_data_csv: # writes cleaned data into truncated csv file
        writer = csv.writer(cleaned_data_csv)
        writer.writerows(cleaned_data)


def desc_cleaner(html_desc):
    """
    Takes description with HTML, unknown chars, incorrect spacing etc., parses and cleans, and returns cleaned text description
    """
    boilerplate_text = " Please mention the word **"
    soup = BeautifulSoup(html_desc, 'html.parser')
    clean_desc = (soup
                  .get_text(separator=" ", strip=True) # parses and removes HTML tags
                  .replace('â', "'") 
                  .split(boilerplate_text)[0]) # removes boilerplate text
    return clean_desc


def tag_extractor(cleaned_desc):
    """
    
    """
    keyword_extractor = yake.KeywordExtractor(
        lan="en",
        n=3,
        dedupLim=0.9,
        top=10,
        features=None
    )
    keywords = keyword_extractor.extract_keywords(cleaned_desc)
    return [keyword[0] for keyword in keywords]


if __name__ == "__main__":
    main()
