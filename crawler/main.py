from playwright.sync_api import sync_playwright
from datetime import datetime
from db.db import insert_job


url = "https://remoteok.com/?search=software%20engineer"

def load_data(page):
    # load remoteok to the page
    page.goto(url, timeout = 100000)
    
    # wait for at least 1 result exist through data-id attribute
    page.wait_for_selector("tr.job[data-id]")

    # load the entire res
    return page.query_selector_all("tr.job[data-id]")


def extract_text(el, sel):
    # find the element
    found = el.query_selector(sel)

    if found is None:
        return None
    
    text = found.inner_text()
    text = text.strip()

    return text

def load_single_page(s_page, s_url):
    # open page
    s_page.goto(s_url, timeout = 100000)

    # wait for the div.description to load in full
    s_page.wait_for_selector("div.description")

    # for some url, good info is under div.markdown
    # for some url, there is no markdown, all info is under div.description
    # so the script here has some fallback: look for markdown first, then description, then the entire html
    parent_container = s_page.query_selector("div.description")
    if parent_container is None:
        return None

    # try if mark down available
    markdown = parent_container.query_selector("div.markdown")

    if markdown is not None:
        return markdown.inner_text().strip()
    
    # mark down is not available, so grab div.description
    not_markdown = parent_container.query_selector("div.html")
    if not_markdown is not None:
        return not_markdown.inner_text().strip()
    
    return parent_container.inner_text().strip()

def main():
    with sync_playwright() as c:
        # first, open a chromium browser
        browser = c.chromium.launch(headless = True)

        # then, open a new tab
        page = browser.new_page()
        s_page = browser.new_page()

        # get results 
        res = load_data(page)

        print("jobs count: ", len(res))
        count = 0 # only load 10 

        for r in res:
            job_id = r.get_attribute("data-id")
            href = r.get_attribute("data-url")

            if job_id is None or href is None:
                continue

            job_url = "https://remoteok.com" + href

            # this info can be gathered from search result page
            job_title = extract_text(r, "h2[itemprop='title']")
            job_firm = extract_text(r, "h3[itemprop='name']")
            job_location = extract_text(r, "div.location")
            job_salary = extract_text(r, "div.salary")

            # then load single url to get the long description
            job_detail = load_single_page(s_page, job_url)

            print("id" ,job_id)
            print("title", job_title)
            print("company", job_firm)
            print("loc", job_location)
            print("pay", job_salary)
            print("URL", job_url)
            print("short desc")
            if job_detail:
                print(job_detail[:800])
            else:
                print(None)

            job = {
                "job_id": job_id,
                "job_url": job_url,
                "title": job_title,
                "company": job_firm,
                "location": job_location,
                "salary": job_salary,
                "description": job_detail,
                "ts": datetime.now(),
            }

            insert_job(job)  # push to db

            count += 1
            print("pushing", count, job_id)
            if count >= 10:
                break

        browser.close()

if __name__ == "__main__":
    main()
