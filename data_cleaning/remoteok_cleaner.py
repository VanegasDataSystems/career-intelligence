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
    
    
    for job in jobs_tuples[1:2]: # iterates through list of job tuples
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
    #desc = "\u003Cdiv\u003E\u003Cp style=\"text-align: justify;\"\u003E\u003Cstrong\u003EAbout Us\u003C/strong\u003E\u003Cbr\u003EWeâre Extenteam, a dynamic company revolutionizing the short term vacation rental industry. Our proven business model has generated consistent revenue, and we are now expanding from a professional services model to a scalable tech-based subscription-first model.\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003EAs a scaling stage startup, we aim to grow our Monthly Recurring Revenue (MRR) to double our revenue by January 2026 by providing an AI assisted SaaS platform that works for all short term rental businesses regardless of their size.\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003EExtenteam is on a mission to streamline and support vacation rental businesses by providing top-notch solutions, including guest communication and property management support.\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003EWe generate revenue through two primary streams:\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003E\u003Cstrong\u003EDedicated Team Members:\u003C/strong\u003E Providing trained overseas talent with a recurring premium model, replacing one-time recruitment fees.\u003Cbr\u003E\u003Cstrong\u003ETailwind \u003C/strong\u003E- SaaS Platform: A guest communication Software blended with our shared services team, supporting smaller operators typically with less than 50 units - helping Extenteam increase profitability while growing our product market fit and expanding TAM and service levels.\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003EExtenteam is a small but mighty team of 50 consisting of Sales, Partner Success, Marketing, HR &amp; Recruiting, Engineering, Product and Admin (IT, Data etc). We are spread out across the world but we have hubs in Miami, LA, Medellin, and actively expanding into Europe. Our 50 people core team is supported by 400+ DTMs (dedicated team members) that are servicing our customers.\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003E\u003Cstrong\u003EOur Values:\u003C/strong\u003E\u003C/p\u003E\n\u003Cp style=\"text-align: justify;\"\u003ECommitment to Excellence: Continuously raising the bar and setting new standards in guest communications and service delivery.&nbsp;\u003Cbr\u003EExceptional Collaboration: Thriving in a fast-paced, high-performance environment built on clea\u003Cbr/\u003E\u003Cbr/\u003EPlease mention the word **DOTINGLY** and tag RMzUuMjM1Ljk1LjEwOA== when applying to show you read the job post completely (#RMzUuMjM1Ljk1LjEwOA==). This is a beta feature to avoid spam applicants. Companies can search these words to find applicants that read this and see they're human."
    #cleaned_desc = desc_cleaner(desc)
    #new_tags = tag_extraction(cleaned_desc)
    #for tag in new_tags:
    #    print(tag[0])
